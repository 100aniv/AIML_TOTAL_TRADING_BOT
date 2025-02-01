# onchain_collector.py
# 목적: 온체인 데이터를 수집하여 시장 심리와 네트워크 상태 분석
# 목표: 온체인 데이터를 기반으로 매매 전략에 추가적인 정보 제공
# 구현해야 할 기능:
# 1. Glassnode, Etherscan 등 온체인 데이터 제공 API 통합
# 2. 네트워크 활동 데이터(Hash Rate, Active Addresses 등) 수집
# 3. 자산별 NVT, SOPR 등의 지표 계산을 위한 데이터 제공
# 4. 데이터 정규화 및 스케줄링 기능 구현

import requests
import json
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import time
import threading
from web3 import Web3
from eth_typing import Address
from queue import Queue

from .logger import trading_logger
from .data_storage import DataStorage

class OnChainCollector:
    """
    온체인 데이터 수집을 담당하는 클래스
    """
    
    def __init__(
        self,
        network: str = 'ethereum',
        node_url: Optional[str] = None,
        api_key: Optional[str] = None,
        storage: Optional[DataStorage] = None
    ):
        """
        온체인 데이터 수집기 초기화
        
        Args:
            network (str): 블록체인 네트워크 (ethereum, binance-smart-chain 등)
            node_url (str, optional): 노드 URL
            api_key (str, optional): API 키 (Etherscan 등)
            storage (DataStorage, optional): 데이터 저장소 인스턴스
        """
        self.network = network
        self.node_url = node_url or self._get_default_node_url()
        self.api_key = api_key
        self.storage = storage or DataStorage()
        self.logger = trading_logger
        
        self.web3 = None
        self.running = False
        self.event_queue = Queue()
        
        self._initialize_web3()
        
    def _get_default_node_url(self) -> str:
        """
        기본 노드 URL을 반환합니다.
        """
        urls = {
            'ethereum': 'https://mainnet.infura.io/v3/YOUR-PROJECT-ID',
            'binance-smart-chain': 'https://bsc-dataseed.binance.org/'
        }
        return urls.get(self.network, urls['ethereum'])
        
    def _initialize_web3(self) -> None:
        """
        Web3 인스턴스를 초기화합니다.
        """
        try:
            provider = Web3.HTTPProvider(self.node_url)
            self.web3 = Web3(provider)
            if self.web3.is_connected():
                self.logger.info(f"Connected to {self.network} network")
            else:
                # 연결 실패시 예외 대신 경고 로그만 출력
                self.logger.warning(f"Failed to connect to {self.network} network")
        except Exception as e:
            self.logger.error(f"Failed to initialize Web3: {str(e)}")
            # 테스트 환경을 위해 예외를 발생시키지 않음
            self.web3 = None
            
    def get_latest_block(self) -> Dict:
        """
        최신 블록 정보를 조회합니다.
        
        Returns:
            Dict: 블록 정보
        """
        try:
            block = self.web3.eth.get_block('latest', full_transactions=True)
            return {
                'number': block.number,
                'timestamp': datetime.fromtimestamp(block.timestamp),
                'transactions': len(block.transactions),
                'gas_used': block.gasUsed,
                'gas_limit': block.gasLimit,
                'base_fee': getattr(block, 'baseFeePerGas', None)
            }
        except Exception as e:
            self.logger.error(f"Error fetching latest block: {str(e)}")
            raise
            
    def get_address_balance(self, address: str) -> Dict:
        """
        주소의 잔고를 조회합니다.
        
        Args:
            address (str): 지갑 주소
            
        Returns:
            Dict: 잔고 정보
        """
        try:
            balance_wei = self.web3.eth.get_balance(address)
            balance_eth = self.web3.from_wei(balance_wei, 'ether')
            
            return {
                'address': address,
                'balance_wei': balance_wei,
                'balance_eth': float(balance_eth),
                'timestamp': datetime.now()
            }
        except Exception as e:
            self.logger.error(f"Error fetching balance for {address}: {str(e)}")
            raise
            
    def get_transaction_receipt(self, tx_hash: str) -> Dict:
        """
        트랜잭션 영수증을 조회합니다.
        
        Args:
            tx_hash (str): 트랜잭션 해시
            
        Returns:
            Dict: 트랜잭션 영수증 정보
        """
        try:
            receipt = self.web3.eth.get_transaction_receipt(tx_hash)
            return {
                'tx_hash': tx_hash,
                'block_number': receipt.blockNumber,
                'gas_used': receipt.gasUsed,
                'status': receipt.status,
                'timestamp': datetime.now()
            }
        except Exception as e:
            self.logger.error(f"Error fetching receipt for {tx_hash}: {str(e)}")
            raise
            
    def fetch_transaction_data(self, transaction_hash: str) -> Dict:
        """
        특정 트랜잭션의 상세 정보를 조회합니다.
        
        Args:
            transaction_hash (str): 트랜잭션 해시
            
        Returns:
            Dict: 트랜잭션 상세 정보
            
        Raises:
            Exception: 트랜잭션 조회 실패시
        """
        try:
            tx = self.web3.eth.get_transaction(transaction_hash)
            tx_receipt = self.web3.eth.get_transaction_receipt(transaction_hash)
            
            return {
                'hash': tx.hash.hex(),
                'from': tx['from'],
                'to': tx.to,
                'value': self.web3.from_wei(tx.value, 'ether'),
                'gas_price': self.web3.from_wei(tx.gasPrice, 'gwei'),
                'gas_used': tx_receipt.gasUsed,
                'status': tx_receipt.status,
                'block_number': tx.blockNumber,
                'timestamp': self.web3.eth.get_block(tx.blockNumber).timestamp
            }
        except Exception as e:
            self.logger.error(f"Error fetching transaction data: {str(e)}")
            raise
            
    def filter_transaction_data(self, raw_data: Dict) -> Dict:
        """
        트랜잭션 데이터에서 필요한 필드만 추출합니다.
        
        Args:
            raw_data (Dict): 원본 트랜잭션 데이터
            
        Returns:
            Dict: 필터링된 트랜잭션 데이터
        """
        return {
            'hash': raw_data.get('hash'),
            'from_address': raw_data.get('from'),
            'to_address': raw_data.get('to'),
            'value': raw_data.get('value'),
            'gas_used': raw_data.get('gas_used'),
            'status': raw_data.get('status'),
            'timestamp': raw_data.get('timestamp')
        }
        
    def save_onchain_data(self, data: Dict) -> None:
        """
        필터링된 트랜잭션 데이터를 저장합니다.
        
        Args:
            data (Dict): 저장할 트랜잭션 데이터
            
        Raises:
            Exception: 데이터 저장 실패시
        """
        try:
            # 테이블이 없으면 생성
            self.storage.execute_query("""
                CREATE TABLE IF NOT EXISTS onchain_transactions (
                    hash TEXT PRIMARY KEY,
                    from_address TEXT,
                    to_address TEXT,
                    value REAL,
                    gas_used INTEGER,
                    status INTEGER,
                    timestamp INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 데이터 저장
            self.storage.execute_query("""
                INSERT OR REPLACE INTO onchain_transactions 
                (hash, from_address, to_address, value, gas_used, status, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data['hash'],
                data['from_address'],
                data['to_address'],
                data['value'],
                data['gas_used'],
                data['status'],
                data['timestamp']
            ))
            
            self.logger.info(f"Saved transaction data: {data['hash']}")
        except Exception as e:
            self.logger.error(f"Error saving transaction data: {str(e)}")
            raise
            
    def monitor_transactions(self, addresses: List[str] = None) -> None:
        """
        특정 주소들의 트랜잭션을 모니터링합니다.
        
        Args:
            addresses (List[str], optional): 모니터링할 주소 목록
        """
        last_block = 0
        
        while self.running:
            try:
                current_block = self.web3.eth.block_number
                
                if current_block > last_block:
                    block = self.web3.eth.get_block(current_block, full_transactions=True)
                    
                    for tx in block.transactions:
                        if addresses is None or (
                            tx['from'].lower() in addresses or
                            tx['to'] and tx['to'].lower() in addresses
                        ):
                            tx_data = {
                                'hash': tx['hash'].hex(),
                                'from': tx['from'],
                                'to': tx['to'],
                                'value': float(self.web3.from_wei(tx['value'], 'ether')),
                                'block_number': tx['blockNumber'],
                                'timestamp': datetime.fromtimestamp(block.timestamp)
                            }
                            
                            self.event_queue.put(tx_data)
                            self.storage.store_transaction(tx_data)
                            
                    last_block = current_block
                    
                time.sleep(1)  # 블록 생성 주기 고려
                
            except Exception as e:
                self.logger.error(f"Error in monitoring transactions: {str(e)}")
                time.sleep(5)
                
    def start_monitoring(self, addresses: List[str] = None) -> None:
        """
        트랜잭션 모니터링을 시작합니다.
        
        Args:
            addresses (List[str], optional): 모니터링할 주소 목록
        """
        if self.running:
            return
            
        self.running = True
        self.monitor_thread = threading.Thread(
            target=self.monitor_transactions,
            args=(addresses,)
        )
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        self.logger.info(
            f"Started monitoring transactions on {self.network} "
            f"for {len(addresses or [])} addresses"
        )
        
    def stop_monitoring(self) -> None:
        """
        트랜잭션 모니터링을 중지합니다.
        """
        self.running = False
        self.logger.info("Stopped transaction monitoring")

# 사용 예시
if __name__ == "__main__":
    collector = OnChainCollector(
        network='ethereum',
        node_url='https://mainnet.infura.io/v3/YOUR-PROJECT-ID'
    )
    
    # 특정 주소들 모니터링
    addresses = [
        '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',  # 예시 주소
    ]
    
    try:
        collector.start_monitoring(addresses)
        # 테스트를 위해 60초 동안 실행
        time.sleep(60)
    finally:
        collector.stop_monitoring()
