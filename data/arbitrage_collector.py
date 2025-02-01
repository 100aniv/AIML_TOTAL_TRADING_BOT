# arbitrage_collector.py
# Description and functionality placeholder.

"""
파일명: arbitrage_collector.py
목적: 여러 거래소의 가격 차이를 실시간으로 모니터링하여 차익거래 기회를 포착
주요 기능:
1. 다중 거래소 실시간 가격 데이터 수집
2. 거래소 간 가격 차이 계산
3. 차익거래 기회 감지 및 알림
4. 수수료 및 전송 비용 고려
5. 실시간 모니터링 및 자동 재연결
"""

import ccxt
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import time
from datetime import datetime
import threading
from queue import Queue

from .logger import trading_logger
from .data_storage import DataStorage

class ArbitrageCollector:
    """
    차익거래 기회 탐지를 위한 데이터 수집기
    """
    
    def __init__(
        self,
        exchanges: List[str] = None,
        symbols: List[str] = None,
        min_profit_percent: float = 0.5,
        storage: Optional[DataStorage] = None
    ):
        """
        차익거래 수집기 초기화
        
        Args:
            exchanges (List[str]): 모니터링할 거래소 목록
            symbols (List[str]): 모니터링할 심볼 목록
            min_profit_percent (float): 최소 수익률 (%)
            storage (DataStorage, optional): 데이터 저장소 인스턴스
        """
        self.exchanges = exchanges or ['binance', 'upbit']
        self.symbols = symbols or ['BTC/USDT', 'ETH/USDT']
        self.min_profit_percent = min_profit_percent
        self.storage = storage or DataStorage()
        self.logger = trading_logger
        
        self.exchange_apis = {}
        self.running = False
        self.price_data = {}
        self.opportunities = Queue()
        
        self._initialize_exchanges()
        
    def _initialize_exchanges(self) -> None:
        """
        거래소 API 초기화
        """
        for exchange_id in self.exchanges:
            try:
                exchange_class = getattr(ccxt, exchange_id)
                self.exchange_apis[exchange_id] = exchange_class({
                    'enableRateLimit': True,
                })
                self.logger.info(f"Initialized {exchange_id} exchange")
            except Exception as e:
                self.logger.error(f"Failed to initialize {exchange_id}: {str(e)}")
                
    def fetch_ticker(self, exchange_id: str, symbol: str) -> Optional[Dict]:
        """
        특정 거래소의 티커 정보를 조회합니다.
        
        Args:
            exchange_id (str): 거래소 ID
            symbol (str): 심볼
            
        Returns:
            Optional[Dict]: 티커 정보
        """
        try:
            ticker = self.exchange_apis[exchange_id].fetch_ticker(symbol)
            return {
                'exchange': exchange_id,
                'symbol': symbol,
                'bid': float(ticker['bid']),
                'ask': float(ticker['ask']),
                'timestamp': datetime.fromtimestamp(ticker['timestamp'] / 1000)
            }
        except Exception as e:
            self.logger.error(f"Error fetching {symbol} ticker from {exchange_id}: {str(e)}")
            return None
            
    def calculate_arbitrage(
        self,
        ticker1: Dict,
        ticker2: Dict,
        fees: Dict[str, float] = None
    ) -> Optional[Dict]:
        """
        두 거래소 간의 차익거래 기회를 계산합니다.
        
        Args:
            ticker1 (Dict): 첫 번째 거래소 티커
            ticker2 (Dict): 두 번째 거래소 티커
            fees (Dict[str, float]): 거래소별 수수료
            
        Returns:
            Optional[Dict]: 차익거래 기회 정보
        """
        if not (ticker1 and ticker2):
            return None
            
        fees = fees or {
            ticker1['exchange']: 0.1,  # 0.1%
            ticker2['exchange']: 0.1   # 0.1%
        }
        
        # 매수-매도 가격 차이 계산
        buy_price = ticker1['ask']  # 첫 번째 거래소에서 매수
        sell_price = ticker2['bid']  # 두 번째 거래소에서 매도
        
        # 수수료 고려
        total_fee_percent = fees[ticker1['exchange']] + fees[ticker2['exchange']]
        profit_percent = ((sell_price / buy_price) - 1) * 100 - total_fee_percent
        
        if profit_percent > self.min_profit_percent:
            return {
                'timestamp': datetime.now(),
                'symbol': ticker1['symbol'],
                'buy_exchange': ticker1['exchange'],
                'sell_exchange': ticker2['exchange'],
                'buy_price': buy_price,
                'sell_price': sell_price,
                'profit_percent': profit_percent,
                'total_fee_percent': total_fee_percent
            }
        return None
        
    def monitor_opportunities(self) -> None:
        """
        차익거래 기회를 지속적으로 모니터링합니다.
        """
        while self.running:
            try:
                for symbol in self.symbols:
                    tickers = []
                    for exchange_id in self.exchanges:
                        ticker = self.fetch_ticker(exchange_id, symbol)
                        if ticker:
                            tickers.append(ticker)
                    
                    # 모든 거래소 조합에 대해 차익거래 기회 계산
                    for i in range(len(tickers)):
                        for j in range(i + 1, len(tickers)):
                            # 양방향 차익거래 확인
                            opp1 = self.calculate_arbitrage(tickers[i], tickers[j])
                            opp2 = self.calculate_arbitrage(tickers[j], tickers[i])
                            
                            for opp in [opp1, opp2]:
                                if opp:
                                    self.opportunities.put(opp)
                                    self.logger.info(
                                        f"Found arbitrage opportunity: "
                                        f"{opp['buy_exchange']} -> {opp['sell_exchange']}, "
                                        f"Profit: {opp['profit_percent']:.2f}%"
                                    )
                                    # 데이터베이스 저장
                                    self.storage.store_arbitrage_opportunity(opp)
                    
                time.sleep(1)  # API 레이트 리밋 고려
                
            except Exception as e:
                self.logger.error(f"Error in monitoring opportunities: {str(e)}")
                time.sleep(5)  # 오류 발생 시 잠시 대기
                
    def start(self) -> None:
        """
        차익거래 모니터링을 시작합니다.
        """
        if self.running:
            return
            
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_opportunities)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        self.logger.info(
            f"Started arbitrage monitoring for {', '.join(self.symbols)} "
            f"across {', '.join(self.exchanges)}"
        )
        
    def stop(self) -> None:
        """
        차익거래 모니터링을 중지합니다.
        """
        self.running = False
        self.logger.info("Stopped arbitrage monitoring")

# 사용 예시
if __name__ == "__main__":
    collector = ArbitrageCollector(
        exchanges=['binance', 'upbit'],
        symbols=['BTC/USDT', 'ETH/USDT'],
        min_profit_percent=0.5
    )
    try:
        collector.start()
        # 테스트를 위해 60초 동안 실행
        time.sleep(60)
    finally:
        collector.stop()
