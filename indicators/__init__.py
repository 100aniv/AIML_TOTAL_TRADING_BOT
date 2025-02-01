# __init__.py
# Description and functionality placeholder.

"""
1. indicators 모듈 초기화

2. 정의
이 모듈은 다양한 기술적 지표를 계산하는 함수들을 제공합니다.
총 7개의 카테고리로 구분된 96개의 지표를 포함합니다.

3. Categories:
3.1. Trend Indicators (추세 지표) - 11개
- sma: 단순 이동평균선
- ema: 지수 이동평균선
- wma: 가중 이동평균선
- tema: 삼중 지수 이동평균선
- macd: 이동평균수렴확산지수
- ichimoku: 일목균형표
- parabolic_sar: 포물선 추세 반전 시스템
- vi: 복합 추세 지표
- adx: 평균 방향성 지수
- hma: 헐 이동평균선
- dema: 이중 지수 이동평균선

3.2. Momentum Indicators (모멘텀 지표) - 12개
- rsi: 상대강도지수
- rsi_divergence: 상대강도지수 다이버전스
- williams_r: 윌리엄스 %R
- cci: 상품채널지수
- money_flow_index: 자금흐름지수
- tsi: 진실강도지수
- cmf: 차이킨 자금흐름
- dmi: 방향성 이동지수
- stochastic: 스토캐스틱
- roc: 변화율
- ppo: 가격변동율 오실레이터
- kst: Know Sure Thing

3.3. Volume Indicators (거래량 지표) - 22개
- money_flow_index: 자금흐름지수
- volume_price_trend: 거래량 가격 추세
- negative_volume_index: 음수 거래량 지수
- accumulation_distribution_index: 축적/분배 지수
- ease_of_movement: 이동 용이성
- volume_rsi: 거래량 RSI
- demand_index: 수요 지수
- up_down_volume_ratio: 상승/하락 거래량 비율
- chaikin_volatility: 차이킨 변동성
- obv: 온밸런스 볼륨
- vwap: 거래량 가중 평균 가격
- pvi: 양수 거래량 지수
- vwma: 거래량 가중 이동평균
- ad_line: 축적/분배선
- vzo: 거래량 영역 오실레이터
- kvo: 클링거 거래량 오실레이터
- emv: 이동 용이성 값
- vrsi: 거래량 RSI
- vmi: 거래량 모멘텀 지수
- trin: 거래 지수
- uvdr: 상승/하락 거래량 비율
- cv: 차이킨 변동성

3.4. Volatility Indicators (변동성 지표) - 8개
- atr: 평균 실제 범위
- standard_deviation: 표준 편차
- ci: 횡보성 지수
- historical_volatility: 역사적 변동성
- ulcer_index: 얼서 지수
- donchian_channel: 돈치안 채널
- keltner_channel: 켈트너 채널
- bollinger_bands: 볼린저 밴드

3.5. Sentiment Indicators (감성 지표) - 11개
- fear_greed_index: 공포탐욕지수
- social_sentiment: 소셜 감성 지수
- news_sentiment: 뉴스 감성 지수
- crypto_fear_greed: 암호화폐 공포탐욕지수
- whale_sentiment: 대형 투자자 심리 지수
- funding_sentiment: 펀딩 심리 지수
- options_sentiment: 옵션 시장 심리 지수
- long_short_ratio: 롱숏 비율
- liquidation_sentiment: 청산 심리 지수
- exchange_flow_sentiment: 거래소 자금 흐름 심리
- social_engagement: 소셜 참여도

3.6. Onchain Indicators (온체인 지표) - 20개
- nvt_ratio: 네트워크 가치 대비 거래량 비율
- mvrv_ratio: 시장가치 대비 실현가치 비율
- sopr_ratio: 사용된 출력 수익 비율
- active_addresses: 활성 주소 수
- transaction_volume: 거래량
- exchange_flow: 거래소 자금 흐름
- hodl_waves: 보유 기간 분포
- mining_difficulty: 채굴 난이도
- hash_rate: 해시레이트
- realized_cap: 실현 시가총액
- stock_to_flow: 저량 대비 유량 비율
- utxo_age_distribution: UTXO 연령 분포
- miners_rolling_inventory: 채굴자 재고 지수
- coin_days_destroyed: 코인일 소멸량
- thermocap: 열역학적 시가총액
- rhodl_ratio: 실현 HODL 비율
- puell_multiple: 푸엘 멀티플
- difficulty_ribbon: 난이도 리본
- reserve_risk: 보유 리스크
- relative_unrealized_pnl: 상대적 미실현 손익

3.7. Composite Indicators (복합 지표) - 13개
- kst: Know Sure Thing
- supertrend: 수퍼트렌드
- detrended_price_oscillator: 추세제거 가격 진동자
- aroon: 아룬 지표
- elder_ray: 엘더레이 지표
- ultimate_oscillator: 궁극 진동자
- mass_index: 매스 지수
- zigzag: 지그재그
- fractal_indicator: 프랙탈 지표
- pivot_points: 피봇 포인트
- schaff_trend_cycle: 샤프 추세 사이클
- alma: 아노말리 제거 이동평균
- connors_rsi: 코너스 RSI

4. 참고 사항
• 모든 지표는 Pandas DataFrame/Series 형태로 반환
• 실시간 계산 지원
• 벡터화된 연산으로 성능 최적화
• 자동 캐싱으로 재계산 최소화

5. 사용 예시
from indicators import TrendIndicator, FeatureGenerator
from indicators import sma, macd, rsi_divergence

# 개별 지표 사용
result = sma(data['close'], period=20)

# 클래스 기반 사용
trend = TrendIndicator(data)
features = trend.calculate_all()

# 특징 생성기 사용
generator = FeatureGenerator(data)
all_features = generator.generate_all_features()
"""

from typing import List, Optional, Union, Tuple
import pandas as pd
import numpy as np

# 클래스 임포트
from .trend_indicator import TrendIndicator
from .momentum_indicator import MomentumIndicator
from .volume_indicator import VolumeIndicator
from .volatility_indicator import VolatilityIndicator
from .sentiment_indicator import SentimentIndicator
from .composite_indicator import CompositeIndicator
from .onchain_indicator import OnchainIndicator
from .feature_generator import FeatureGenerator

# 유틸리티 함수 임포트
from .utils import validate_data, get_available_indicators

# 추세 지표
from .trend_indicator import (
    sma, ema, wma, tema, macd, ichimoku, parabolic_sar, vi, adx,
    hma, dema
)

# 모멘텀 지표
from .momentum_indicator import (
    rsi, rsi_divergence, williams_r, cci, money_flow_index, tsi, cmf, dmi,
    stochastic, roc, ppo, kst
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
    atr, standard_deviation, ci, historical_volatility,
    ulcer_index, donchian_channel, keltner_channel, bollinger_bands
)

# 감성 지표
from .sentiment_indicator import (
    fear_greed_index, social_sentiment, news_sentiment,
    crypto_fear_greed, whale_sentiment, funding_sentiment,
    options_sentiment, long_short_ratio, liquidation_sentiment,
    exchange_flow_sentiment, social_engagement
)

# 온체인 지표
from .onchain_indicator import (
    nvt_ratio, mvrv_ratio, sopr_ratio, active_addresses,
    transaction_volume, exchange_flow, hodl_waves, mining_difficulty,
    hash_rate, realized_cap, stock_to_flow, utxo_age_distribution,
    miners_rolling_inventory, coin_days_destroyed, thermocap,
    rhodl_ratio, puell_multiple, difficulty_ribbon,
    reserve_risk, relative_unrealized_pnl
)

# 복합 지표
from .composite_indicator import (
    kst, supertrend, detrended_price_oscillator, aroon,
    elder_ray, ultimate_oscillator, mass_index, zigzag,
    fractal_indicator, pivot_points, schaff_trend_cycle,
    alma, connors_rsi
)

# 기본 설정값
DEFAULT_PERIOD = 14
DEFAULT_FAST_PERIOD = 12
DEFAULT_SLOW_PERIOD = 26
DEFAULT_SIGNAL_PERIOD = 9

# 버전 정보
__version__ = '1.0.0'
__author__ = 'Your Name'
__email__ = 'your.email@example.com'

# 모든 public 심볼 정의
__all__ = [
    # Indicator Classes
    'TrendIndicator', 'MomentumIndicator', 'VolumeIndicator',
    'VolatilityIndicator', 'SentimentIndicator', 'CompositeIndicator',
    'OnchainIndicator', 'FeatureGenerator',
    
    # Utility Functions
    'validate_data', 'get_available_indicators',
    
    # Constants
    'DEFAULT_PERIOD', 'DEFAULT_FAST_PERIOD', 'DEFAULT_SLOW_PERIOD',
    'DEFAULT_SIGNAL_PERIOD',
    
    # 추세 지표
    'sma', 'ema', 'wma', 'tema', 'macd', 'ichimoku', 'parabolic_sar',
    'vi', 'adx', 'hma', 'dema',
    
    # 모멘텀 지표
    'rsi', 'rsi_divergence', 'williams_r', 'cci', 'money_flow_index', 'tsi',
    'cmf', 'dmi', 'stochastic', 'roc', 'ppo', 'kst',
    
    # 거래량 지표
    'money_flow_index', 'volume_price_trend', 'negative_volume_index',
    'accumulation_distribution_index', 'ease_of_movement', 'volume_rsi',
    'demand_index', 'up_down_volume_ratio', 'chaikin_volatility',
    'obv', 'vwap', 'pvi', 'vwma', 'ad_line', 'vzo', 'kvo', 'emv',
    'vrsi', 'vmi', 'trin', 'uvdr', 'cv',
    
    # 변동성 지표
    'atr', 'standard_deviation', 'ci', 'historical_volatility',
    'ulcer_index', 'donchian_channel', 'keltner_channel', 'bollinger_bands',
    
    # 감성 지표
    'fear_greed_index', 'social_sentiment', 'news_sentiment',
    'crypto_fear_greed', 'whale_sentiment', 'funding_sentiment',
    'options_sentiment', 'long_short_ratio', 'liquidation_sentiment',
    'exchange_flow_sentiment', 'social_engagement',
    
    # 온체인 지표
    'nvt_ratio', 'mvrv_ratio', 'sopr_ratio', 'active_addresses',
    'transaction_volume', 'exchange_flow', 'hodl_waves', 'mining_difficulty',
    'hash_rate', 'realized_cap', 'stock_to_flow', 'utxo_age_distribution',
    'miners_rolling_inventory', 'coin_days_destroyed', 'thermocap',
    'rhodl_ratio', 'puell_multiple', 'difficulty_ribbon',
    'reserve_risk', 'relative_unrealized_pnl',
    
    # 복합 지표
    'kst', 'supertrend', 'detrended_price_oscillator', 'aroon',
    'elder_ray', 'ultimate_oscillator', 'mass_index', 'zigzag',
    'fractal_indicator', 'pivot_points', 'schaff_trend_cycle',
    'alma', 'connors_rsi'
]

def get_indicator_info(indicator_name: str) -> dict:
    """특정 지표에 대한 상세 정보를 반환합니다.
    
    Args:
        indicator_name: 지표 이름
        
    Returns:
        dict: 지표 정보 (이름, 설명, 파라미터)
        
    Note:
        - 존재하지 않는 지표인 경우 None 반환
        - 파라미터 정보는 함수 시그니처에서 추출
    """
    indicator_func = globals().get(indicator_name)
    if indicator_func:
        return {
            'name': indicator_name,
            'description': indicator_func.__doc__,
            'parameters': indicator_func.__code__.co_varnames[:indicator_func.__code__.co_argcount]
        }
    return None

def get_available_indicators() -> List[str]:
    """사용 가능한 모든 지표 목록을 반환합니다.
    
    Returns:
        List[str]: 지표 이름 목록
        
    Note:
        - 카테고리별로 정렬된 목록 반환
        - 클래스와 함수 모두 포함
    """
    return sorted([name for name in __all__ if not name.startswith('_')])

# utils 함수들을 내부에 직접 구현
def validate_data(data: pd.DataFrame) -> bool:
    """데이터 유효성 검증"""
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    return all(col in data.columns for col in required_columns)
