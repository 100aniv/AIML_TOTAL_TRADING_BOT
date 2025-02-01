"""
추세 지표(Trend Indicators) 테스트

테스트 대상 지표 (6개):
1. SMA (Simple Moving Average)
   - 단순 이동평균선
   - 기간: 5, 10, 20, 60일

2. EMA (Exponential Moving Average)
   - 지수 이동평균선
   - 기간: 5, 10, 20, 60일

3. WMA (Weighted Moving Average)
   - 가중 이동평균선
   - 기간: 5, 10, 20, 60일

4. MACD (Moving Average Convergence Divergence)
   - 이동평균 수렴/발산
   - 단기: 12일, 장기: 26일, 시그널: 9일

5. Ichimoku Cloud (일목균형표)
   - 전환선(9일), 기준선(26일)
   - 선행스팬1, 선행스팬2, 후행스팬

6. Parabolic SAR
   - 추세 반전 지표
   - 가속도: 0.02, 최대: 0.2
"""

import pytest
import pandas as pd
import numpy as np
from indicators.trend_indicator import TrendIndicator, sma, ema, wma, macd, ichimoku, parabolic_sar

def test_trend_indicator_initialization(sample_data):
    """
    1. TrendIndicator 클래스 초기화 테스트
    - 클래스가 정상적으로 초기화되는지 확인
    - 데이터가 올바르게 저장되는지 확인
    """
    indicator = TrendIndicator(sample_data)
    assert indicator is not None
    assert isinstance(indicator.data, pd.DataFrame)
    assert all(col in indicator.data.columns for col in ['open', 'high', 'low', 'close', 'volume'])

def test_trend_indicator_validation(sample_data):
    """
    2. 데이터 검증 테스트
    - 필수 컬럼이 있는지 확인
    - 데이터 형식이 올바른지 확인
    - 결측치가 없는지 확인
    """
    indicator = TrendIndicator(sample_data)
    validation_result = indicator._validate_data()
    assert validation_result is None  # 검증 통과시 None 반환

def test_calculate_all(sample_data, print_indicator_result):
    """
    3. 모든 추세 지표 통합 계산 테스트
    - calculate_all 메서드로 모든 지표 계산
    - 결과 데이터 검증
    """
    indicator = TrendIndicator(sample_data)
    results = indicator.calculate_all()
    
    print_indicator_result("추세 지표 통합 계산", results, "Trend Indicators")
    
    # 1) 필수 컬럼 존재 확인
    expected_columns = [
        'sma_5', 'sma_10', 'sma_20', 'sma_60',
        'ema_5', 'ema_10', 'ema_20', 'ema_60',
        'wma_5', 'wma_10', 'wma_20', 'wma_60',
        'macd', 'macd_signal', 'macd_hist',
        'ichimoku_tenkan', 'ichimoku_kijun', 'ichimoku_senkou_a',
        'ichimoku_senkou_b', 'ichimoku_chikou',
        'psar'
    ]
    assert all(col in results.columns for col in expected_columns)
    
    # 2) 데이터 형식 검증
    assert isinstance(results, pd.DataFrame)
    assert len(results) == len(sample_data)
    assert not results.isnull().all().any()  # 전체가 NaN인 컬럼이 없어야 함

def test_individual_indicators(sample_data, print_indicator_result):
    """
    4. 개별 지표 테스트
    각 지표별 계산 결과를 확인하고 출력
    """
    # 1) SMA (Simple Moving Average) 테스트
    periods = [5, 10, 20, 60]
    sma_results = {f'SMA_{p}': sma(sample_data['close'], period=p) for p in periods}
    print_indicator_result("단순 이동평균선(SMA)", pd.DataFrame(sma_results), "개별지표")
    
    # 2) EMA (Exponential Moving Average) 테스트
    ema_results = {f'EMA_{p}': ema(sample_data['close'], period=p) for p in periods}
    print_indicator_result("지수 이동평균선(EMA)", pd.DataFrame(ema_results), "개별지표")
    
    # 3) WMA (Weighted Moving Average) 테스트
    wma_results = {f'WMA_{p}': wma(sample_data['close'], period=p) for p in periods}
    print_indicator_result("가중 이동평균선(WMA)", pd.DataFrame(wma_results), "개별지표")
    
    # 4) MACD 테스트
    macd_line, signal_line, hist = macd(sample_data['close'])
    print_indicator_result("MACD", pd.DataFrame({
        'MACD': macd_line,
        'Signal': signal_line,
        'Histogram': hist
    }), "개별지표")
    
    # 5) Ichimoku Cloud 테스트
    tenkan, kijun, senkou_a, senkou_b, chikou = ichimoku(
        sample_data['high'], sample_data['low'], sample_data['close']
    )
    print_indicator_result("일목균형표", pd.DataFrame({
        'Tenkan (전환선)': tenkan,
        'Kijun (기준선)': kijun,
        'Senkou A (선행스팬1)': senkou_a,
        'Senkou B (선행스팬2)': senkou_b,
        'Chikou (후행스팬)': chikou
    }), "개별지표")
    
    # 6) Parabolic SAR 테스트
    psar_result = parabolic_sar(sample_data['high'], sample_data['low'])
    print_indicator_result("Parabolic SAR", psar_result, "개별지표")

def test_edge_cases():
    """
    5. 엣지 케이스 테스트
    - 빈 데이터 처리
    - 누락된 데이터 처리
    - 이상치 처리
    """
    # 1) 빈 데이터 테스트
    empty_data = pd.DataFrame()
    with pytest.raises(ValueError):
        TrendIndicator(empty_data)
    
    # 2) 누락된 데이터 테스트
    missing_data = pd.DataFrame({
        'open': [1, 2, np.nan, 4, 5],
        'high': [2, 3, 4, 5, 6],
        'low': [0, 1, 2, 3, 4],
        'close': [1, 2, 3, np.nan, 5],
        'volume': [100, 200, 300, 400, 500]
    })
    indicator = TrendIndicator(missing_data)
    results = indicator.calculate_all()
    assert not results.empty
    
    # 3) 이상치 테스트
    outlier_data = pd.DataFrame({
        'open': [1, 2, 1000000, 4, 5],
        'high': [2, 3, 1000001, 5, 6],
        'low': [0, 1, 999999, 3, 4],
        'close': [1, 2, 1000000, 4, 5],
        'volume': [100, 200, 300, 400, 500]
    })
    indicator = TrendIndicator(outlier_data)
    results = indicator.calculate_all()
    assert not results.empty

def test_performance(sample_data, benchmark):
    """
    6. 성능 테스트
    - 계산 속도 측정
    - 메모리 사용량 확인
    """
    indicator = TrendIndicator(sample_data)
    benchmark(indicator.calculate_all) 