"""
파일명: real_time_collector.py
목적: 거래소 API 또는 WebSocket을 통해 실시간 거래 데이터를 수집
주요 기능:
1. WebSocket 및 REST API를 통한 실시간 데이터 스트리밍
2. 실시간 데이터의 빠른 처리 및 저장
3. 연결 끊김 또는 API 제한 시 자동 복구
4. 수집된 데이터를 신호 생성 및 UI로 전달
5. 실시간 데이터 수집 실패 시 재시도 및 예외 처리
"""

import websocket
import json
import threading
from datetime import datetime
from typing import Optional, Dict, Callable, Any
import time
import ccxt
from queue import Queue

from .logger import trading_logger
from .data_storage import DataStorage

class RealTimeCollector:
    """
    실시간 데이터 수집을 담당하는 클래스
    """
    
    def __init__(
        self,
        exchange_id: str = 'binance',
        symbols: list = None,
        storage: Optional[DataStorage] = None
    ):
        """
        실시간 데이터 수집기 초기화
        
        Args:
            exchange_id (str): 거래소 ID
            symbols (list): 수집할 심볼 목록
            storage (DataStorage, optional): 데이터 저장소 인스턴스
        """
        self.exchange_id = exchange_id
        self.symbols = symbols or ['BTC/USDT']
        self.storage = storage or DataStorage()
        self.logger = trading_logger
        
        self.ws = None
        self.ws_url = self._get_websocket_url()
        self.running = False
        self.reconnect_count = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 5
        
        # 데이터 큐
        self.data_queue = Queue()
        self.processor_thread = None
        
    def _get_websocket_url(self) -> str:
        """
        거래소별 WebSocket URL을 반환합니다.
        """
        if self.exchange_id == 'binance':
            return "wss://stream.binance.com:9443/ws"
        else:
            raise ValueError(f"Unsupported exchange: {self.exchange_id}")
            
    def _on_message(self, ws: websocket.WebSocketApp, message: str) -> None:
        """
        WebSocket 메시지 수신 핸들러
        
        Args:
            ws: WebSocket 인스턴스
            message: 수신된 메시지
        """
        try:
            data = json.loads(message)
            self.data_queue.put(data)
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse message: {str(e)}")
            
    def _on_error(self, ws: websocket.WebSocketApp, error: Exception) -> None:
        """
        WebSocket 에러 핸들러
        """
        self.logger.error(f"WebSocket error: {str(error)}")
        
    def _on_close(self, ws: websocket.WebSocketApp, close_status_code: int, close_msg: str) -> None:
        """
        WebSocket 연결 종료 핸들러
        """
        self.logger.warning("WebSocket connection closed")
        if self.running:
            self._reconnect()
            
    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        """
        WebSocket 연결 수립 핸들러
        """
        self.logger.info("WebSocket connection established")
        self.reconnect_count = 0
        
        # 구독 메시지 전송
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": [f"{symbol.lower()}@trade" for symbol in self.symbols],
            "id": 1
        }
        ws.send(json.dumps(subscribe_message))
        
    def _reconnect(self) -> None:
        """
        WebSocket 재연결을 시도합니다.
        """
        if self.reconnect_count < self.max_reconnect_attempts:
            self.reconnect_count += 1
            self.logger.warning(
                f"Attempting to reconnect ({self.reconnect_count}/{self.max_reconnect_attempts})"
            )
            time.sleep(self.reconnect_delay)
            self.start()
        else:
            self.logger.error("Max reconnection attempts reached")
            self.stop()
            
    def _process_data(self) -> None:
        """
        수신된 데이터를 처리하는 스레드 함수
        """
        while self.running:
            try:
                data = self.data_queue.get(timeout=1)
                
                # 데이터 처리 및 저장
                if 'e' in data and data['e'] == 'trade':
                    trade_data = {
                        'timestamp': datetime.fromtimestamp(data['T'] / 1000),
                        'symbol': data['s'],
                        'price': float(data['p']),
                        'quantity': float(data['q']),
                        'is_buyer_maker': data['m']
                    }
                    
                    # 데이터베이스 저장
                    self.storage.store_trade_data(trade_data)
                    
            except Exception as e:
                if self.running:  # 정상 종료가 아닌 경우에만 에러 로깅
                    self.logger.error(f"Error processing data: {str(e)}")
                    
    def start(self) -> None:
        """
        실시간 데이터 수집을 시작합니다.
        """
        if self.running:
            return
            
        self.running = True
        
        # WebSocket 연결 설정
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        
        # WebSocket 스레드 시작
        ws_thread = threading.Thread(target=self.ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()
        
        # 데이터 처리 스레드 시작
        self.processor_thread = threading.Thread(target=self._process_data)
        self.processor_thread.daemon = True
        self.processor_thread.start()
        
        self.logger.info(f"Started real-time data collection for {', '.join(self.symbols)}")
        
    def stop(self) -> None:
        """
        실시간 데이터 수집을 중지합니다.
        """
        self.running = False
        if self.ws:
            self.ws.close()
        self.logger.info("Stopped real-time data collection")

# 사용 예시
if __name__ == "__main__":
    collector = RealTimeCollector(symbols=['BTC/USDT', 'ETH/USDT'])
    try:
        collector.start()
        # 테스트를 위해 60초 동안 실행
        time.sleep(60)
    finally:
        collector.stop()