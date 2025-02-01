"""
파일명: collector.py
목적: 거래소 API를 통해 과거 데이터를 수집하여 데이터 분석과 모델 학습에 사용할 데이터셋을 준비
주요 기능:
1. 다양한 거래소 API(CCXT 등)와의 통합
2. OHLCV 데이터 수집
3. 특정 타임프레임 데이터 수집
4. 데이터 유효성 검증
5. 재시도 및 예외 처리
"""

import ccxt
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import time
from pathlib import Path

from .logger import trading_logger

class DataCollector:
    """
    거래소 데이터 수집을 담당하는 클래스
    """
    
    def __init__(self, exchange_id: str = 'binance'):
        """
        데이터 수집기 초기화
        
        Args:
            exchange_id (str): 거래소 ID (예: 'binance', 'upbit')
        """
        self.exchange_id = exchange_id
        self.exchange = getattr(ccxt, exchange_id)()
        self.logger = trading_logger
        self.setup_exchange()
        
    def setup_exchange(self) -> None:
        """
        거래소 설정을 초기화합니다.
        """
        self.exchange.load_markets()
        self.logger.info(f"Connected to {self.exchange_id} exchange")
        
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = '1d',
        since: Optional[int] = None,
        limit: Optional[int] = None,
        retry_count: int = 3,
        retry_delay: int = 5
    ) -> pd.DataFrame:
        """
        OHLCV 데이터를 수집합니다.
        
        Args:
            symbol (str): 거래 쌍 (예: 'BTC/USDT')
            timeframe (str): 시간 프레임 (예: '1m', '1h', '1d')
            since (int, optional): 데이터 시작 시점 (timestamp)
            limit (int, optional): 조회할 데이터 개수
            retry_count (int): 재시도 횟수
            retry_delay (int): 재시도 간격 (초)
            
        Returns:
            pd.DataFrame: OHLCV 데이터프레임
            
        Raises:
            ccxt.NetworkError: 네트워크 오류 발생 시
            ccxt.ExchangeError: 거래소 관련 오류 발생 시
        """
        for attempt in range(retry_count):
            try:
                # OHLCV 데이터 조회
                ohlcv = self.exchange.fetch_ohlcv(
                    symbol=symbol,
                    timeframe=timeframe,
                    since=since,
                    limit=limit
                )
                
                # 데이터프레임 변환
                df = pd.DataFrame(
                    ohlcv,
                    columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
                )
                
                # 타임스탬프 변환
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
                
                self.logger.info(
                    f"Successfully fetched {len(df)} {timeframe} candles for {symbol}",
                    notify=False
                )
                return df
                
            except (ccxt.NetworkError, ccxt.ExchangeError) as e:
                if attempt == retry_count - 1:
                    self.logger.error(
                        f"Failed to fetch data after {retry_count} attempts: {str(e)}",
                        notify=True
                    )
                    raise
                    
                self.logger.warning(
                    f"Attempt {attempt + 1}/{retry_count} failed: {str(e)}. "
                    f"Retrying in {retry_delay} seconds..."
                )
                time.sleep(retry_delay)

    def fetch_historical_data(
        self,
        symbol: str,
        timeframe: str = '1d',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        특정 기간의 과거 데이터를 수집합니다.
        
        Args:
            symbol (str): 거래 쌍 (예: 'BTC/USDT')
            timeframe (str): 시간 프레임 (예: '1m', '1h', '1d')
            start_date (str, optional): 시작 날짜 ('YYYY-MM-DD')
            end_date (str, optional): 종료 날짜 ('YYYY-MM-DD')
            
        Returns:
            pd.DataFrame: 수집된 과거 데이터
        """
        # 날짜 처리
        if start_date:
            since = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
        else:
            since = None
            
        if end_date:
            until = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp() * 1000)
        else:
            until = int(datetime.now().timestamp() * 1000)
            
        # 데이터 수집
        data = []
        current_since = since
        
        while True:
            chunk = self.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                since=current_since,
                limit=1000  # CCXT 기본 제한
            )
            
            if chunk.empty:
                break
                
            data.append(chunk)
            
            # 다음 조회 시작점 설정
            current_since = int(chunk.index[-1].timestamp() * 1000)
            
            if current_since >= until:
                break
                
            # API 레이트 리밋 고려
            time.sleep(self.exchange.rateLimit / 1000)
            
        if not data:
            return pd.DataFrame()
            
        # 데이터 병합
        result = pd.concat(data)
        result = result[~result.index.duplicated(keep='first')]
        result = result[result.index <= pd.to_datetime(until, unit='ms')]
        
        self.logger.info(
            f"Collected {len(result)} historical {timeframe} candles for {symbol} "
            f"from {result.index[0]} to {result.index[-1]}"
        )
        
        return result

    def get_available_symbols(self) -> List[str]:
        """
        거래 가능한 심볼 목록을 반환합니다.
        
        Returns:
            List[str]: 거래 가능한 심볼 목록
        """
        return [symbol for symbol in self.exchange.symbols if self.exchange.markets[symbol]['active']]

    def get_exchange_status(self) -> Dict:
        """
        거래소 상태 정보를 반환합니다.
        
        Returns:
            Dict: 거래소 상태 정보
        """
        return {
            'exchange_id': self.exchange_id,
            'rate_limit': self.exchange.rateLimit,
            'has_fetch_ohlcv': self.exchange.has.get('fetchOHLCV', False),
            'timeframes': list(self.exchange.timeframes.keys()) if hasattr(self.exchange, 'timeframes') else [],
            'symbols_count': len(self.get_available_symbols())
        }

# 사용 예시
if __name__ == "__main__":
    collector = DataCollector(exchange_id='binance')
    status = collector.get_exchange_status()
    print(f"Exchange Status: {status}")