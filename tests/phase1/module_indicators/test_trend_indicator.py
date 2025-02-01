"""
추세 지표(Trend Indicators) 테스트

테스트 대상:
1. 단순 이동평균선 (SMA)
2. 지수 이동평균선 (EMA)
3. 가중 이동평균선 (WMA)
4. MACD
5. Ichimoku Cloud
6. Parabolic SAR
7. VI (Volatility Index)
8. ADX (Average Directional Index)
9. HMA (Hull Moving Average)
10. DEMA (Double Exponential Moving Average)
11. TEMA (Triple Exponential Moving Average)
"""

import pytest
import pandas as pd
import numpy as np
from indicators.trend_indicator import TrendIndicator

class TestTrendIndicator:
    @pytest.fixture(scope="class")
    def sample_data(self):
        """테스트용 샘플 데이터 생성"""
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        return pd.DataFrame({
            'open': np.random.randn(len(dates)) * 10 + 100,
            'high': np.random.randn(len(dates)) * 10 + 105,
            'low': np.random.randn(len(dates)) * 10 + 95,
            'close': np.random.randn(len(dates)) * 10 + 100,
            'volume': np.random.randint(1000, 10000, len(dates))
        }, index=dates)

    @pytest.fixture(scope="class")
    def indicator(self, sample_data):
        """TrendIndicator 인스턴스 생성"""
        return TrendIndicator(sample_data)

    def test_initialization(self, indicator, sample_data):
        """초기화 테스트"""
        assert isinstance(indicator, TrendIndicator)
        assert indicator.data.equals(sample_data)
        assert all(col in indicator.data.columns 
                  for col in ['open', 'high', 'low', 'close', 'volume'])

    def test_sma_calculation(self, indicator):
        """SMA 계산 테스트"""
        periods = [5, 10, 20, 60]
        for period in periods:
            sma = indicator.calculate_sma(period=period)
            assert isinstance(sma, pd.Series)
            assert len(sma) == len(indicator.data)
            assert not sma.isnull().all()
            # 첫 (period-1)개 데이터는 NaN이어야 함
            assert sma.iloc[:period-1].isnull().all()

    def test_ema_calculation(self, indicator):
        """EMA 계산 테스트"""
        periods = [5, 10, 20, 60]
        for period in periods:
            ema = indicator.calculate_ema(period=period)
            assert isinstance(ema, pd.Series)
            assert len(ema) == len(indicator.data)
            assert not ema.isnull().all()

    def test_macd_calculation(self, indicator):
        """MACD 계산 테스트"""
        macd_line, signal_line, histogram = indicator.calculate_macd()
        assert all(isinstance(x, pd.Series) for x in [macd_line, signal_line, histogram])
        assert len(macd_line) == len(indicator.data)
        assert len(signal_line) == len(indicator.data)
        assert len(histogram) == len(indicator.data)

    def test_trend_detection(self, indicator):
        """추세 감지 테스트"""
        trend = indicator.detect_trend()
        assert trend in ['uptrend', 'downtrend', 'sideways']

    def test_crossover_detection(self, indicator):
        """이동평균 교차 감지 테스트"""
        crossovers = indicator.detect_ma_crossover()
        assert isinstance(crossovers, pd.Series)
        assert all(x in [1, -1, 0] for x in crossovers.dropna())

    def test_performance(self, indicator):
        """성능 테스트"""
        import time
        
        start_time = time.time()
        indicator.calculate_all()
        elapsed = time.time() - start_time
        
        assert elapsed < 0.5  # 500ms 이내 수행

    def test_error_handling(self, indicator):
        """에러 처리 테스트"""
        with pytest.raises(ValueError):
            indicator.calculate_sma(period=0)
        
        with pytest.raises(ValueError):
            indicator.calculate_sma(period=-1)

    def test_edge_cases(self, indicator):
        """엣지 케이스 테스트"""
        # 데이터가 모두 같은 값일 때
        same_data = pd.DataFrame({
            'close': [100] * len(indicator.data),
            'volume': [1000] * len(indicator.data)
        })
        result = TrendIndicator(same_data).calculate_sma(period=5)
        assert all(result.dropna() == 100)

if __name__ == '__main__':
    pytest.main([__file__]) 