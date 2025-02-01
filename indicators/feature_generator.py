'''
Feature Generator (특징 생성기)

정의
indicators 모듈의 각종 지표들을 활용하여 종합적인 특징을 생성하는 모듈입니다.

목적
• 각 카테고리별 지표들의 통합 관리
• 일관된 인터페이스를 통한 특징 생성
• ML/AI 모델을 위한 특징 데이터셋 생성
• 실시간 특징 업데이트 지원

지표 목록 (7개)
1. TrendFeatures: 이동평균, MACD, 추세선 등 추세 관련 지표
2. MomentumFeatures: RSI, CCI, 스토캐스틱 등 모멘텀 관련 지표
3. VolumeFeatures: OBV, MFI, 거래량 프로필 등 거래량 관련 지표
4. VolatilityFeatures: 볼린저밴드, ATR 등 변동성 관련 지표
5. SentimentFeatures: 공포탐욕지수, 시장심리 등 감성 관련 지표
6. OnchainFeatures: 네트워크 지표, 온체인 활동 등 온체인 관련 지표
7. CompositeFeatures: KST, Supertrend 등 복합 지표

[2024-01] 함수명 패턴 표준화
- calculate_features -> generate_features
- get_indicators -> generate_[category]_features
'''

from typing import Dict, List, Optional, Union, Tuple
import pandas as pd
import numpy as np

# 추세 지표
from .trend_indicator import (
    sma, ema, wma, tema, macd, ichimoku, parabolic_sar, vi, adx,
    hma, dema  # 추가
)

# 모멘텀 지표
from .momentum_indicator import (
    rsi_divergence, williams_r, cci, money_flow_index, tsi, cmf, dmi,
    stochastic, roc, ppo, kst  # 추가
)

# 거래량 지표
from .volume_indicator import (
    money_flow_index, volume_price_trend, negative_volume_index,
    accumulation_distribution_index, ease_of_movement, volume_rsi,
    demand_index, up_down_volume_ratio, chaikin_volatility,
    obv, vwap, pvi, vwma, ad_line, vzo, kvo, emv,
    vrsi, vmi, trin, uvdr, cv
)

# 변동성 지표
from .volatility_indicator import (
    standard_deviation, ci, ulcer_index, dc, kc, bb,
    atr, sd, hv  # 추가
)

# 감성 지표
from .sentiment_indicator import (
    fear_greed_index, social_sentiment, news_sentiment,
    crypto_fear_greed, whale_sentiment, funding_sentiment,
    options_sentiment, long_short_ratio, liquidation_sentiment,
    exchange_flow_sentiment, social_engagement
)

# 복합 지표
from .composite_indicator import (
    kst, supertrend, detrended_price_oscillator, aroon,
    elder_ray, ultimate_oscillator, mass_index
)

# 온체인 지표
from .onchain_indicator import (
    active_addresses, coin_age_distribution, mining_difficulty,
    stock_to_flow, utxo_age_distribution, thermocap,
    nvt_ratio, mvrv_ratio, sopr_ratio, exchange_flow,  # 추가
    hodl_waves, hash_rate, realized_cap,  # 추가
    miners_rolling_inventory, coin_days_destroyed,  # 추가
    rhodl_ratio, puell_multiple, difficulty_ribbon,  # 추가
    reserve_risk, relative_unrealized_pnl  # 추가
)

class FeatureGenerator:
    """특징 생성을 담당하는 클래스"""
    
    #1. 초기화
    def __init__(self, data: Optional[pd.DataFrame] = None):
        """초기화 함수
        
        Args:
            data: OHLCV 데이터를 포함한 DataFrame (옵션)
            
        Note:
            데이터가 제공되면 자동으로 검증 수행
        """
        if data is not None:
            self.set_data(data)

    #2. 데이터 검증
    def _validate_data(self) -> None:
        """데이터 검증
        
        필수 컬럼 존재 여부를 검증합니다.
        
        Raises:
            ValueError: 필수 컬럼이 없는 경우
            
        Note:
            필수 컬럼: open, high, low, close, volume
        """
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in self.data.columns for col in required_columns):
            raise ValueError(f"데이터에 필수 컬럼이 없습니다: {required_columns}")

    #3. 데이터 설정
    def set_data(self, data: pd.DataFrame) -> None:
        """데이터 설정
        
        Args:
            data: OHLCV 데이터를 포함한 DataFrame
            
        Note:
            데이터 복사본을 생성하여 원본 데이터 보호
        """
        self.data = data.copy()
        self._validate_data()

    #4. 추세 특징 생성
    def generate_trend_features(self, params: Optional[Dict] = None) -> pd.DataFrame:
        """추세 관련 특징 생성"""
        features = pd.DataFrame(index=self.data.index)
        
        # 기본 이동평균
        features['sma'] = sma(self.data['close'])
        features['ema'] = ema(self.data['close'])
        features['wma'] = wma(self.data['close'])
        features['tema'] = tema(self.data['close'])
        
        # 추가된 이동평균
        features['hma'] = hma(self.data['close'])
        features['dema'] = dema(self.data['close'])
        
        # MACD
        macd_line, signal_line, histogram = macd(self.data['close'])
        features['macd'] = macd_line
        features['macd_signal'] = signal_line
        features['macd_hist'] = histogram
        
        # 일목균형표
        tenkan, kijun, senkou_a, senkou_b, chikou = ichimoku(
            self.data['high'], self.data['low'], self.data['close']
        )
        features['ichimoku_tenkan'] = tenkan
        features['ichimoku_kijun'] = kijun
        features['ichimoku_senkou_a'] = senkou_a
        features['ichimoku_senkou_b'] = senkou_b
        features['ichimoku_chikou'] = chikou
        
        # 기타 추세 지표
        features['psar'] = parabolic_sar(self.data['high'], self.data['low'])
        features['vi_plus'], features['vi_minus'] = vi(
            self.data['high'], self.data['low'], self.data['close']
        )
        features['adx'] = adx(self.data['high'], self.data['low'], self.data['close'])
        
        return features

    #5. 모멘텀 특징 생성
    def generate_momentum_features(self, params: Optional[Dict] = None) -> pd.DataFrame:
        """모멘텀 관련 특징 생성"""
        features = pd.DataFrame(index=self.data.index)
        
        # 기본 모멘텀 지표
        features['rsi'] = rsi_divergence(self.data['close'])
        features['williams_r'] = williams_r(self.data['high'], self.data['low'], self.data['close'])
        features['cci'] = cci(self.data['high'], self.data['low'], self.data['close'])
        
        # 추가된 지표들
        k_line, d_line = stochastic(self.data['high'], self.data['low'], self.data['close'])
        features['stoch_k'] = k_line
        features['stoch_d'] = d_line
        features['roc'] = roc(self.data['close'])
        features['ppo'] = ppo(self.data['close'])
        features['kst'] = kst(self.data['close'])
        
        return features

    #6. 거래량 특징 생성
    def generate_volume_features(self, params: Optional[Dict] = None) -> pd.DataFrame:
        """거래량 관련 특징 생성"""
        features = pd.DataFrame(index=self.data.index)
        
        # 기본 거래량 지표
        features['obv'] = obv(self.data['close'], self.data['volume'])
        features['vwap'] = vwap(self.data['close'], self.data['volume'])
        features['mfi'] = money_flow_index(self.data['high'], self.data['low'], 
                                         self.data['close'], self.data['volume'])
        
        # 추가된 지표들
        features['pvi'] = pvi(self.data['close'], self.data['volume'])
        features['vwma'] = vwma(self.data['close'], self.data['volume'])
        features['ad_line'] = ad_line(self.data['high'], self.data['low'], 
                                     self.data['close'], self.data['volume'])
        features['vzo'] = vzo(self.data['close'], self.data['volume'])
        features['kvo'] = kvo(self.data['high'], self.data['low'], 
                             self.data['close'], self.data['volume'])
        features['emv'] = emv(self.data['high'], self.data['low'], self.data['volume'])
        features['vrsi'] = vrsi(self.data['volume'])
        features['vmi'] = vmi(self.data['volume'])
        features['trin'] = trin(self.data['advances'], self.data['declines'],
                               self.data['advance_volume'], self.data['decline_volume'])
        features['uvdr'] = uvdr(self.data['close'], self.data['volume'])
        features['cv'] = cv(self.data['high'], self.data['low'])
        
        return features

    #7. 변동성 특징 생성
    def generate_volatility_features(self, params: Optional[Dict] = None) -> pd.DataFrame:
        """변동성 관련 특징 생성"""
        features = pd.DataFrame(index=self.data.index)
        
        # 기본 변동성 지표
        features['std'] = standard_deviation(self.data['close'])
        features['ci'] = ci(self.data['high'], self.data['low'])
        features['ulcer'] = ulcer_index(self.data['close'])
        
        # 추가된 지표들
        features['atr'] = atr(self.data['high'], self.data['low'], self.data['close'])
        features['sd'] = sd(self.data['close'])
        features['hv'] = hv(self.data['close'])
        
        # 채널 지표들
        dc_upper, dc_middle, dc_lower = dc(self.data['high'], self.data['low'])
        features['dc_upper'] = dc_upper
        features['dc_middle'] = dc_middle
        features['dc_lower'] = dc_lower
        
        kc_upper, kc_middle, kc_lower = kc(self.data['high'], self.data['low'], self.data['close'])
        features['kc_upper'] = kc_upper
        features['kc_middle'] = kc_middle
        features['kc_lower'] = kc_lower
        
        bb_upper, bb_middle, bb_lower = bb(self.data['close'])
        features['bb_upper'] = bb_upper
        features['bb_middle'] = bb_middle
        features['bb_lower'] = bb_lower
        
        return features

    #8. 감성 특징 생성
    def generate_sentiment_features(self, params: Optional[Dict] = None) -> pd.DataFrame:
        """감성 관련 특징 생성"""
        features = pd.DataFrame(index=self.data.index)
        
        # 기본 감성 지표
        features['fear_greed'] = fear_greed_index(self.data)
        features['social_sentiment'] = social_sentiment(self.data)
        features['news_sentiment'] = news_sentiment(self.data)
        
        # 추가된 지표들
        features['crypto_fear'] = crypto_fear_greed(self.data)
        features['whale_sentiment'] = whale_sentiment(self.data)
        features['funding_sentiment'] = funding_sentiment(self.data)
        features['options_sentiment'] = options_sentiment(self.data)
        features['long_short'] = long_short_ratio(self.data)
        features['liquidation'] = liquidation_sentiment(self.data)
        features['exchange_flow'] = exchange_flow_sentiment(self.data)
        features['social_engagement'] = social_engagement(self.data)
        
        return features

    #9. 온체인 특징 생성
    def generate_onchain_features(self, params: Optional[Dict] = None) -> pd.DataFrame:
        """온체인 관련 특징 생성"""
        features = pd.DataFrame(index=self.data.index)
        
        # 기본 온체인 지표
        features['active_addr'] = active_addresses(self.data)
        features['coin_age'] = coin_age_distribution(self.data)
        features['mining_diff'] = mining_difficulty(self.data)
        
        # 추가된 지표들
        features['nvt'] = nvt_ratio(self.data)
        features['mvrv'] = mvrv_ratio(self.data)
        features['sopr'] = sopr_ratio(self.data)
        features['exchange_flow'] = exchange_flow(self.data)
        features['hodl_waves'] = hodl_waves(self.data)
        features['hash_rate'] = hash_rate(self.data)
        features['realized_cap'] = realized_cap(self.data)
        features['miners_inventory'] = miners_rolling_inventory(self.data)
        features['coin_days'] = coin_days_destroyed(self.data)
        features['rhodl'] = rhodl_ratio(self.data)
        features['puell'] = puell_multiple(self.data)
        features['diff_ribbon'] = difficulty_ribbon(self.data)
        features['reserve_risk'] = reserve_risk(self.data)
        features['unrealized_pnl'] = relative_unrealized_pnl(self.data)
        
        return features

    #10. 복합 특징 생성
    def generate_composite_features(self, params: Optional[Dict] = None) -> pd.DataFrame:
        """복합 지표 관련 특징 생성
        
        Args:
            params: 지표별 파라미터 (옵션)
            
        Returns:
            pd.DataFrame: 복합 지표 관련 특징이 포함된 DataFrame
            
        Note:
            - KST를 통한 장기 추세 분석
            - Supertrend를 통한 추세 전환점 포착
            - 여러 지표의 조합을 통한 복합 신호 생성
        """
        features = pd.DataFrame(index=self.data.index)
        
        features['kst'] = kst(self.data['close'])
        features['supertrend'] = supertrend(
            self.data['high'],
            self.data['low'],
            self.data['close']
        )
        features['dpo'] = detrended_price_oscillator(self.data['close'])
        
        aroon_result = aroon(self.data['high'], self.data['low'])
        features['aroon_up'] = aroon_result[0]
        features['aroon_down'] = aroon_result[1]
        
        features['elder_ray'] = elder_ray(self.data['close'])
        features['uo'] = ultimate_oscillator(
            self.data['high'],
            self.data['low'],
            self.data['close']
        )
        
        return features

    #11. 전체 특징 생성
    def generate_all_features(self, params: Optional[Dict] = None) -> pd.DataFrame:
        """모든 카테고리의 특징 생성
        
        Args:
            params: 지표별 파라미터 딕셔너리
            
        Returns:
            pd.DataFrame: 모든 특징이 포함된 DataFrame
            
        Note:
            - 모든 카테고리의 특징을 통합 생성
            - 카테고리별 파라미터 개별 설정 가능
            - 결과는 단일 DataFrame으로 통합
        """
        all_features = pd.concat([
            self.generate_trend_features(params),
            self.generate_momentum_features(params),
            self.generate_volume_features(params),
            self.generate_volatility_features(params),
            self.generate_sentiment_features(params),
            self.generate_onchain_features(params),
            self.generate_composite_features(params)
        ], axis=1)
        
        return all_features
