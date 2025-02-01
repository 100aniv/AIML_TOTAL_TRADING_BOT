import unittest
import pandas as pd
from data import collector
from indicators import FeatureGenerator
from signals import generator

class TestIndicatorsIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 실제 데이터 수집
        cls.collector = collector.DataCollector()
        cls.data = cls.collector.get_historical_data('BTC/USD', '1d', limit=100)
        
    def test_end_to_end_flow(self):
        """전체 데이터 흐름 테스트"""
        # 1. Feature 생성
        feature_gen = FeatureGenerator(self.data)
        features = feature_gen.generate_all_features()
        
        # 2. 신호 생성
        signal_gen = generator.SignalGenerator(features)
        signals = signal_gen.generate_signals()
        
        # 검증
        self.assertIsInstance(features, pd.DataFrame)
        self.assertIsInstance(signals, pd.DataFrame)
        self.assertTrue(len(signals) > 0)
        
    def test_real_time_processing(self):
        """실시간 처리 테스트"""
        import time
        
        # 실시간 데이터 시뮬레이션
        feature_gen = FeatureGenerator(self.data)
        
        start_time = time.time()
        features = feature_gen.generate_features_realtime(self.data.iloc[-1])
        elapsed = time.time() - start_time
        
        self.assertLess(elapsed, 0.1)  # 100ms 이내 수행

if __name__ == '__main__':
    unittest.main() 