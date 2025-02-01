"""
Data 모듈 통합 테스트
목적: Phase 1 data 모듈의 전체 데이터 흐름 테스트
"""

import os
import pytest
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

from data.logger import trading_logger
from data.collector import DataCollector
from data.data_storage import DataStorage
from data.preprocessor import DataPreprocessor

class TestDataPipeline:
    """데이터 파이프라인 통합 테스트"""
    
    @pytest.fixture(autouse=True)
    def setup_test_env(self):
        """테스트 환경 설정"""
        # 테스트 디렉토리 생성
        Path("logs").mkdir(exist_ok=True)
        Path("test_data").mkdir(exist_ok=True)
        yield
        # 테스트 후 정리
        if os.path.exists("test_trading_bot.db"):
            os.remove("test_trading_bot.db")
    
    @pytest.fixture
    def setup_pipeline(self):
        """파이프라인 컴포넌트 설정"""
        collector = DataCollector()
        storage = DataStorage("test_trading_bot.db")
        preprocessor = DataPreprocessor()
        return collector, storage, preprocessor

    def test_data_collection_to_preprocessing(self, setup_pipeline):
        """데이터 수집부터 전처리까지 전체 흐름 테스트"""
        collector, storage, preprocessor = setup_pipeline
        symbol = "BTC/USDT"
        timeframe = "1h"
        exchange = "binance"
        
        try:
            # 1. 데이터 수집
            trading_logger.info(f"데이터 수집 시작: {symbol}")
            raw_data = collector.fetch_ohlcv(symbol, timeframe, limit=100)
            assert len(raw_data) > 0
            assert all(col in raw_data.columns for col in ['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            trading_logger.info(f"데이터 수집 완료: {len(raw_data)} 레코드")

            # 2. 데이터 저장
            trading_logger.info("데이터베이스 저장 시작")
            storage.store_ohlcv_data(raw_data, symbol, timeframe, exchange)
            trading_logger.info("데이터베이스 저장 완료")

            # 3. 저장된 데이터 조회
            trading_logger.info("저장된 데이터 조회")
            stored_data = storage.get_ohlcv_data(
                symbol=symbol,
                timeframe=timeframe,
                exchange=exchange
            )
            assert len(stored_data) == len(raw_data)
            trading_logger.info("데이터 조회 완료")

            # 4. 데이터 전처리
            trading_logger.info("데이터 전처리 시작")
            # 4.1 이상치 제거
            cleaned_data = preprocessor.remove_outliers(stored_data, 'close')
            assert len(cleaned_data) > 0
            trading_logger.info(f"이상치 제거 완료: {len(raw_data) - len(cleaned_data)}개 제거됨")

            # 4.2 데이터 정규화
            normalized_data = preprocessor.normalize_data(cleaned_data, 'close')
            assert normalized_data['close'].min() >= 0
            assert normalized_data['close'].max() <= 1
            trading_logger.info("데이터 정규화 완료")

            # 5. 전체 파이프라인 검증
            assert not normalized_data.empty
            assert 'close' in normalized_data.columns
            trading_logger.info("데이터 파이프라인 검증 완료")

        except Exception as e:
            trading_logger.error(f"파이프라인 실행 중 오류 발생: {str(e)}")
            raise

    def test_error_handling(self, setup_pipeline):
        """오류 처리 및 복구 테스트"""
        collector, storage, preprocessor = setup_pipeline
        
        try:
            # 1. 잘못된 심볼로 데이터 수집 시도
            with pytest.raises(Exception):
                collector.fetch_ohlcv("INVALID/PAIR", "1h", limit=10)
                trading_logger.info("잘못된 심볼 테스트 완료")

            # 2. 빈 데이터프레임 저장 시도
            empty_df = pd.DataFrame()
            storage.store_ohlcv_data(empty_df, "BTC/USDT", "1h", "binance")
            trading_logger.info("빈 데이터프레임 처리 테스트 완료")

            # 3. 잘못된 컬럼으로 전처리 시도
            invalid_df = pd.DataFrame({'invalid_col': [1, 2, 3]})
            with pytest.raises(Exception):
                preprocessor.normalize_data(invalid_df, 'close')
                trading_logger.info("잘못된 컬럼 테스트 완료")

        except Exception as e:
            trading_logger.error(f"오류 처리 테스트 중 예상치 못한 오류 발생: {str(e)}")
            raise

if __name__ == "__main__":
    pytest.main(["-v", __file__])
