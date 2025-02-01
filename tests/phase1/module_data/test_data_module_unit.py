"""
Data 모듈 단위 테스트
목적: Phase 1 data 모듈의 각 컴포넌트 독립적 테스트
"""

import os
import pytest
import pandas as pd
from datetime import datetime
from pathlib import Path

from data.logger import trading_logger
from data.collector import DataCollector
from data.data_storage import DataStorage
from data.preprocessor import DataPreprocessor

# 테스트 데이터 디렉토리 생성
@pytest.fixture(autouse=True)
def setup_test_env():
    """테스트 환경 설정"""
    # logs 디렉토리 생성
    Path("logs").mkdir(exist_ok=True)
    # test_data 디렉토리 생성
    Path("test_data").mkdir(exist_ok=True)
    yield
    # 테스트 후 정리
    if os.path.exists("test_trading_bot.db"):
        os.remove("test_trading_bot.db")

@pytest.fixture
def sample_ohlcv_data():
    """테스트용 OHLCV 데이터"""
    return pd.DataFrame({
        'timestamp': [datetime.now()],
        'open': [50000.0],
        'high': [51000.0],
        'low': [49000.0],
        'close': [50500.0],
        'volume': [100.0]
    })

class TestLogger:
    """로깅 기능 테스트"""
    def test_log_creation(self):
        """로그 파일 생성 테스트"""
        trading_logger.info("테스트 메시지")
        log_file = f"logs/trading_bot_{datetime.now().strftime('%Y%m%d')}.log"
        assert os.path.exists(log_file)

    def test_log_levels(self):
        """로그 레벨별 기록 테스트"""
        test_msg = "테스트 메시지"
        trading_logger.debug(f"DEBUG: {test_msg}")
        trading_logger.info(f"INFO: {test_msg}")
        trading_logger.warning(f"WARNING: {test_msg}")
        trading_logger.error(f"ERROR: {test_msg}")

        log_file = f"logs/trading_bot_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "INFO: 테스트 메시지" in content
            assert "WARNING: 테스트 메시지" in content
            assert "ERROR: 테스트 메시지" in content

class TestDataCollector:
    """데이터 수집 테스트"""
    @pytest.fixture
    def collector(self):
        return DataCollector()

    def test_collector_initialization(self, collector):
        """수집기 초기화 테스트"""
        assert isinstance(collector, DataCollector)

    def test_fetch_ohlcv(self, collector):
        """OHLCV 데이터 수집 테스트"""
        data = collector.fetch_ohlcv("BTC/USDT", "1h", limit=5)
        
        # 데이터 구조 검증
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 5
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        assert all(col in data.columns for col in required_columns)
        
        # 데이터 타입 검증
        assert pd.api.types.is_datetime64_any_dtype(data['timestamp'])
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        assert all(pd.api.types.is_numeric_dtype(data[col]) for col in numeric_columns)

class TestDataStorage:
    """데이터 저장소 테스트"""
    @pytest.fixture
    def storage(self):
        return DataStorage("test_trading_bot.db")

    def test_db_initialization(self, storage):
        """DB 초기화 테스트"""
        assert os.path.exists("test_trading_bot.db")

    def test_store_and_get_ohlcv(self, storage, sample_ohlcv_data):
        """데이터 저장 및 조회 테스트"""
        symbol = "BTC/USDT"
        timeframe = "1m"
        exchange = "binance"
        
        # 데이터 저장
        storage.store_ohlcv_data(sample_ohlcv_data, symbol, timeframe, exchange)
        
        # 데이터 조회 (get_ohlcv_data -> get_ohlcv_data로 수정)
        retrieved_data = storage.get_ohlcv_data(
            symbol=symbol,
            timeframe=timeframe,
            exchange=exchange,
            start_date=None,  # 옵션 파라미터 추가
            end_date=None     # 옵션 파라미터 추가
        )
        
        # 데이터 검증
        assert not retrieved_data.empty
        assert len(retrieved_data) == len(sample_ohlcv_data)
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        assert all(col in retrieved_data.columns for col in required_columns)

class TestPreprocessor:
    """데이터 전처리 테스트"""
    @pytest.fixture
    def preprocessor(self):
        return DataPreprocessor()

    def test_preprocessor_initialization(self, preprocessor):
        """전처리기 초기화 테스트"""
        assert isinstance(preprocessor, DataPreprocessor)

    def test_remove_outliers(self, preprocessor):
        """이상치 제거 테스트"""
        data = pd.DataFrame({
            'close': [100.0, 101.0, 102.0, 1000.0, 103.0, 104.0, 105.0]
        })
        cleaned = preprocessor.remove_outliers(data, 'close', threshold=2.0)
        assert len(cleaned) < len(data)
        assert 1000.0 not in cleaned['close'].values

    def test_normalize_data(self, preprocessor):
        """데이터 정규화 테스트"""
        data = pd.DataFrame({
            'close': [100.0, 200.0, 300.0, 400.0, 500.0]
        })
        normalized = preprocessor.normalize_data(data, 'close')
        assert normalized['close'].min() >= 0
        assert normalized['close'].max() <= 1

if __name__ == "__main__":
    pytest.main(["-v", __file__])
