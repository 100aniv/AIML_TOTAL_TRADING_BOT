import unittest
import pandas as pd
import numpy as np
from indicators import (
    TrendIndicator, MomentumIndicator, VolumeIndicator,
    VolatilityIndicator, SentimentIndicator, OnchainIndicator,
    CompositeIndicator
)

class TestIndicators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 테스트용 데이터 생성
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        cls.test_data = pd.DataFrame({
            'open': np.random.randn(len(dates)) * 10 + 100,
            'high': np.random.randn(len(dates)) * 10 + 105,
            'low': np.random.randn(len(dates)) * 10 + 95,
            'close': np.random.randn(len(dates)) * 10 + 100,
            'volume': np.random.randint(1000, 10000, len(dates))
        }, index=dates)

    def test_trend_indicators(self):
        """추세 지표 테스트"""
        trend = TrendIndicator(self.test_data)
        
        # SMA 테스트
        sma = trend.calculate_sma(period=20)
        self.assertIsInstance(sma, pd.Series)
        self.assertEqual(len(sma), len(self.test_data))
        
        # MACD 테스트
        macd = trend.calculate_macd()
        self.assertIsInstance(macd, tuple)
        self.assertEqual(len(macd[0]), len(self.test_data))

    def test_momentum_indicators(self):
        """모멘텀 지표 테스트"""
        momentum = MomentumIndicator(self.test_data)
        
        # RSI 테스트
        rsi = momentum.calculate_rsi()
        self.assertIsInstance(rsi, pd.Series)
        self.assertTrue(all(0 <= x <= 100 for x in rsi.dropna()))

    def test_volume_indicators(self):
        """거래량 지표 테스트"""
        volume = VolumeIndicator(self.test_data)
        
        # OBV 테스트
        obv = volume.calculate_obv()
        self.assertIsInstance(obv, pd.Series)
        self.assertEqual(len(obv), len(self.test_data))

    def test_volatility_indicators(self):
        """변동성 지표 테스트"""
        volatility = VolatilityIndicator(self.test_data)
        
        # Bollinger Bands 테스트
        bb = volatility.calculate_bollinger_bands()
        self.assertIsInstance(bb, tuple)
        self.assertEqual(len(bb), 3)  # upper, middle, lower

    def test_performance(self):
        """성능 테스트"""
        import time
        
        trend = TrendIndicator(self.test_data)
        start_time = time.time()
        trend.calculate_all()
        elapsed = time.time() - start_time
        
        self.assertLess(elapsed, 0.5)  # 500ms 이내 수행

    def test_error_handling(self):
        """에러 처리 테스트"""
        # 잘못된 데이터로 테스트
        invalid_data = self.test_data.copy()
        invalid_data.loc[invalid_data.index[0], 'close'] = np.nan
        
        trend = TrendIndicator(invalid_data)
        sma = trend.calculate_sma(period=20)
        self.assertTrue(pd.isna(sma[0]))

if __name__ == '__main__':
    unittest.main() 