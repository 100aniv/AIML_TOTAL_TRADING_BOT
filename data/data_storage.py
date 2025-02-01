# data_storage.py
# 목적: 데이터 수집 및 저장 기능 구현
# 목표: 실시간 데이터 수집 및 저장 기능 제공
# 구현해야 할 기능:
# 1. 데이터 수집 기능 구현
# 2. 데이터 저장 기능 구현
# 3. 데이터 정규화 및 스케일링 기능 구현
# 4. 데이터 백업 및 복구 기능 구현
# 5. 데이터 시각화 기능 구현
# 6. 데이터 보안 기능 구현
# 7. 데이터 활용 기능 구현 

"""
파일명: data_storage.py
목적: 수집된 데이터를 효율적으로 저장하고 관리하는 모듈
주요 기능:
1. SQLite 데이터베이스 초기화 및 관리
2. 데이터 저장 및 조회
3. 데이터 백업 및 복구
4. 중복 데이터 처리
5. 데이터 정리 및 최적화
"""

import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional, Union, List
import json
import shutil

from .logger import trading_logger

class DataStorage:
    """
    데이터 저장 및 관리를 담당하는 클래스
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        데이터 저장소 초기화
        
        Args:
            db_path (str, optional): 데이터베이스 파일 경로
        """
        if db_path is None:
            db_path = str(Path(__file__).parent.parent / 'data' / 'trading_bot.db')
            
        self.db_path = db_path
        self.logger = trading_logger
        self.conn = None  # Initialize connection as None
        self.initialize_database()
        
    def initialize_database(self):
        """
        데이터베이스 및 필요한 테이블을 초기화합니다.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)  # Store connection as instance variable
            cursor = self.conn.cursor()
            
            # OHLCV 데이터 테이블 생성
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ohlcv (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    volume REAL NOT NULL,
                    timeframe TEXT NOT NULL,
                    exchange TEXT NOT NULL,
                    UNIQUE(timestamp, symbol, timeframe, exchange)
                )
            """)
            
            # 메타데이터 테이블 생성
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL UNIQUE,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            self.conn.commit()
            self.logger.info("Database initialized successfully")
            
        except sqlite3.Error as e:
            self.logger.error(f"Failed to initialize database: {str(e)}")
            raise
            
    def store_ohlcv(
        self,
        data: pd.DataFrame,
        symbol: str,
        exchange: str
    ) -> None:
        """
        OHLCV 데이터를 데이터베이스에 저장합니다.

        Args:
            data (pd.DataFrame): OHLCV 데이터프레임
            symbol (str): 거래 쌍
            exchange (str): 거래소 이름
        """
        return self.store_ohlcv_data(data, symbol, '1m', exchange)  # Call original method with default timeframe
        
    def store_ohlcv_data(
        self,
        data: pd.DataFrame,
        symbol: str,
        timeframe: str,
        exchange: str
    ) -> None:
        """
        OHLCV 데이터를 데이터베이스에 저장합니다.
        
        Args:
            data (pd.DataFrame): OHLCV 데이터프레임
            symbol (str): 거래 쌍
            timeframe (str): 시간 프레임
            exchange (str): 거래소 이름
        """
        if data.empty:
            self.logger.warning(f"No data to store for {symbol}")
            return
            
        try:
            # 기존 데이터 복사
            df = data.copy()
            
            # 메타데이터 추가
            df['symbol'] = symbol
            df['timeframe'] = timeframe
            df['exchange'] = exchange
            
            # timestamp 처리
            if isinstance(df.index, pd.DatetimeIndex):
                df = df.reset_index()
            df['timestamp'] = df['timestamp'].astype(str)
            
            # 컬럼 순서 지정 (기존 컬럼 유지하면서 순서만 조정)
            required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'symbol', 'timeframe', 'exchange']
            existing_columns = [col for col in required_columns if col in df.columns]
            df = df[existing_columns]
            
            # 데이터베이스 저장 (기존 성능 최적화 유지)
            df.to_sql('ohlcv', self.conn, if_exists='append', index=False,
                     method='multi', chunksize=1000)
            self.conn.commit()
            
            self.logger.info(f"Stored {len(df)} records for {symbol} ({timeframe}) from {exchange}")
            
        except sqlite3.Error as e:
            self.logger.error(f"Failed to store data: {str(e)}")
            raise
            
    def get_ohlcv(self, symbol: str, exchange: str) -> pd.DataFrame:
        """저장된 OHLCV 데이터 조회"""
        query = """
            SELECT timestamp, open, high, low, close, volume 
            FROM ohlcv 
            WHERE symbol=? AND exchange=?
            ORDER BY timestamp
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (symbol, exchange))
        rows = cursor.fetchall()
        
        if not rows:
            return pd.DataFrame()
        
        return pd.DataFrame(rows, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
    def create_backup(self, backup_path: Optional[str] = None) -> str:
        """
        데이터베이스 백업을 생성합니다.
        
        Args:
            backup_path (str, optional): 백업 파일 경로
            
        Returns:
            str: 생성된 백업 파일 경로
        """
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = str(Path(self.db_path).parent / f'backup_{timestamp}.db')
            
        try:
            shutil.copy2(self.db_path, backup_path)
            self.logger.info(f"Database backup created at: {backup_path}")
            return backup_path
            
        except IOError as e:
            self.logger.error(f"Failed to create backup: {str(e)}")
            raise
            
    def restore_from_backup(self, backup_path: str) -> None:
        """
        백업에서 데이터베이스를 복구합니다.
        
        Args:
            backup_path (str): 백업 파일 경로
        """
        try:
            # 현재 데이터베이스 백업
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_backup = str(Path(self.db_path).parent / f'temp_backup_{timestamp}.db')
            shutil.copy2(self.db_path, temp_backup)
            
            # 백업에서 복구
            shutil.copy2(backup_path, self.db_path)
            self.logger.info(f"Database restored from: {backup_path}")
            
        except IOError as e:
            self.logger.error(f"Failed to restore from backup: {str(e)}")
            if Path(temp_backup).exists():
                shutil.copy2(temp_backup, self.db_path)
            raise
            
        finally:
            if Path(temp_backup).exists():
                Path(temp_backup).unlink()
                
    def optimize_database(self) -> None:
        """
        데이터베이스를 최적화합니다.
        """
        try:
            self.conn.execute("VACUUM")
            self.conn.execute("ANALYZE")
            self.logger.info("Database optimization completed")
            
        except sqlite3.Error as e:
            self.logger.error(f"Failed to optimize database: {str(e)}")
            raise

    def get_ohlcv_data(
        self,
        symbol: str,
        timeframe: str,
        exchange: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        저장된 OHLCV 데이터를 조회합니다.
        
        Args:
            symbol (str): 거래 쌍
            timeframe (str): 시간 프레임
            exchange (str): 거래소 이름
            start_date (str, optional): 시작 날짜 ('YYYY-MM-DD')
            end_date (str, optional): 종료 날짜 ('YYYY-MM-DD')
            
        Returns:
            pd.DataFrame: 조회된 OHLCV 데이터
        """
        query = """
            SELECT timestamp, open, high, low, close, volume 
            FROM ohlcv 
            WHERE symbol = ? AND timeframe = ? AND exchange = ?
        """
        params = [symbol, timeframe, exchange]
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        
        query += " ORDER BY timestamp"
        
        try:
            df = pd.read_sql_query(query, self.conn, params=params)
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            return df
            
        except sqlite3.Error as e:
            self.logger.error(f"Failed to fetch data: {str(e)}")
            raise

# 사용 예시
if __name__ == "__main__":
    storage = DataStorage()
    print(f"Database path: {storage.db_path}") 