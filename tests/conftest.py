import os
import sys
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

@pytest.fixture
def sample_data():
    """
    테스트용 OHLCV 데이터 생성
    
    Returns:
        DataFrame: 다음 컬럼들을 포함하는 100일치 샘플 데이터
        - date: 날짜
        - open: 시가
        - high: 고가
        - low: 저가
        - close: 종가
        - volume: 거래량
    """
    # 날짜 생성
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    
    # 기본 가격 시나리오 생성 (추세 + 변동성)
    base_price = 1000
    trend = np.linspace(0, 100, 100)  # 상승추세
    noise = np.random.normal(0, 20, 100)  # 변동성
    
    # OHLCV 데이터 생성
    data = {
        'open': base_price + trend + noise,
        'high': base_price + trend + noise + abs(np.random.normal(0, 10, 100)),
        'low': base_price + trend + noise - abs(np.random.normal(0, 10, 100)),
        'close': base_price + trend + noise + np.random.normal(0, 5, 100),
        'volume': np.random.randint(1000, 10000, 100)
    }
    
    df = pd.DataFrame(data, index=dates)
    
    # 데이터 무결성 보장
    df['high'] = df[['high', 'open', 'close']].max(axis=1)
    df['low'] = df[['low', 'open', 'close']].min(axis=1)
    
    return df

@pytest.fixture
def sample_onchain_data(sample_data):
    """
    테스트용 온체인 데이터 생성
    
    Returns:
        DataFrame: 기본 OHLCV에 온체인 지표 관련 컬럼이 추가된 데이터
    """
    df = sample_data.copy()
    
    # 온체인 데이터 추가
    df['active_addresses'] = np.random.randint(1000, 5000, len(df))
    df['transaction_count'] = np.random.randint(5000, 15000, len(df))
    df['hash_rate'] = np.random.randint(100000, 200000, len(df))
    df['difficulty'] = np.random.randint(50000, 100000, len(df))
    
    return df

@pytest.fixture
def sample_sentiment_data(sample_data):
    """
    테스트용 감성 데이터 생성
    
    Returns:
        DataFrame: 기본 OHLCV에 감성 지표 관련 컬럼이 추가된 데이터
    """
    df = sample_data.copy()
    
    # 감성 데이터 추가
    df['social_score'] = np.random.uniform(-1, 1, len(df))
    df['news_score'] = np.random.uniform(-1, 1, len(df))
    df['fear_greed'] = np.random.randint(0, 100, len(df))
    
    return df

@pytest.fixture
def print_indicator_result():
    """
    지표 계산 결과를 보기 좋게 출력하는 헬퍼 함수
    
    Usage:
        def test_something(print_indicator_result):
            result = calculate_something()
            print_indicator_result("지표명", result)
    """
    def _print_result(indicator_name, result, category=""):
        print("\n" + "="*50)
        print(f"[{category}] {indicator_name} 지표 테스트 결과")
        print("-"*50)
        
        if isinstance(result, pd.DataFrame):
            print("\n데이터 미리보기 (앞부분 3행):")
            print(result.head(3))
            print("\n데이터 미리보기 (뒷부분 3행):")
            print(result.tail(3))
            print("\n기초 통계량:")
            print(result.describe())
        else:
            print("\n계산 결과:")
            print(result)
            
        print("="*50 + "\n")
    
    return _print_result 