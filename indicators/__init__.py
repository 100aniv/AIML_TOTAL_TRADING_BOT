# __init__.py
# Description and functionality placeholder.

'''
indicators 모듈 초기화

이 모듈은 다양한 기술적 지표를 계산하는 함수들을 제공합니다.
총 9개의 카테고리로 구분된 89개의 지표를 포함합니다.

Categories:
1. Volume Indicators (거래량 지표) - 9개
- obv, vwap, ad_line, chaikin_money_flow, ease_of_movement
- volume_price_trend, negative_volume_index, positive_volume_index
- percentage_volume_oscillator

2. Momentum Indicators (모멘텀 지표) - 14개
- rsi, stochastic_oscillator, williams_r, cci, roc, mfi
- ultimate_oscillator, rvi, tsi, advance_decline_line
- mcclellan_oscillator, mcclellan_summation_index
- kst_oscillator, market_breadth

3. Trend Indicators (추세 지표) - 6개
- sma, ema, wma, macd, ichimoku, parabolic_sar

4. Volatility Indicators (변동성 지표) - 9개
- atr, std_deviation, choppiness_index, historical_volatility
- bollinger_bandwidth, ulcer_index, chaikin_volatility
- donchian_channel, keltner_channel

5. Sentiment Indicators (심리 지표) - 11개
- fear_greed_index, social_sentiment, news_sentiment
- trading_activity_index, put_call_ratio, margin_debt_ratio
- technical_sentiment, volatility_sentiment, bullish_percent_index
- high_low_index, market_sentiment

6. On-Chain Indicators (온체인 지표) - 10개
- nvt_ratio, mvrv_ratio, stock_to_flow_ratio, active_addresses
- transaction_volume, exchange_flow, hodl_waves, mining_difficulty
- hash_rate, realized_cap

7. Composite Indicators (복합 지표) - 13개
- zigzag, fractal_indicator, pivot_points, schaff_trend_cycle
- alma, connors_rsi, triple_screen, elder_ray, demark_indicators
- hybrid_rsi, trend_strength_index, volume_price_confirmation
- multi_factor_ranking

8. Feature Generator (특징 생성기) - 9개
- generate_technical_features, generate_volume_features
- generate_volatility_features, generate_sentiment_features
- generate_onchain_features, generate_time_features
- generate_pattern_features, generate_correlation_features
- combine_features

9. Arbitrage Features (차익거래 특징) - 8개
- generate_price_spread_features, generate_volume_spread_features
- generate_orderbook_features, generate_execution_cost_features
- generate_liquidity_features, generate_market_impact_features
- generate_risk_features, generate_opportunity_score
'''

# Technical Indicators
from .trend_indicator import (
    TrendIndicator,
    sma, ema, wma, macd, ichimoku, parabolic_sar
)

from .momentum_indicator import (
    MomentumIndicator,
    rsi, stochastic_oscillator, williams_r, cci, roc, mfi,
    ultimate_oscillator, rvi, tsi, advance_decline_line,
    mcclellan_oscillator, mcclellan_summation_index,
    kst_oscillator, market_breadth
)

from .volume_indicator import (
    VolumeIndicator,
    obv, vwap, ad_line, chaikin_money_flow, ease_of_movement,
    volume_price_trend, negative_volume_index, positive_volume_index,
    percentage_volume_oscillator
)

from .volatility_indicator import (
    VolatilityIndicator,
    atr, std_deviation, choppiness_index, historical_volatility,
    bollinger_bandwidth, ulcer_index, chaikin_volatility,
    donchian_channel, keltner_channel
)

from .sentiment_indicator import (
    SentimentIndicator,
    fear_greed_index, social_sentiment, news_sentiment,
    trading_activity_index, put_call_ratio, margin_debt_ratio,
    technical_sentiment, volatility_sentiment, bullish_percent_index,
    high_low_index, market_sentiment
)

from .onchain_indicator import (
    OnchainIndicator,
    nvt_ratio, mvrv_ratio, stock_to_flow_ratio, active_addresses,
    transaction_volume, exchange_flow, hodl_waves, mining_difficulty,
    hash_rate, realized_cap
)

from .composite_indicator import (
    CompositeIndicator,
    zigzag, fractal_indicator, pivot_points, schaff_trend_cycle,
    alma, connors_rsi, triple_screen, elder_ray, demark_indicators,
    hybrid_rsi, trend_strength_index, volume_price_confirmation,
    multi_factor_ranking
)

# ML/AI Features
from .arbitrage_feature import (
    ArbitrageFeature,
    generate_price_spread_features, generate_volume_spread_features,
    generate_orderbook_features, generate_execution_cost_features,
    generate_liquidity_features, generate_market_impact_features,
    generate_risk_features, generate_opportunity_score
)

from .feature_generator import (
    FeatureGenerator,
    generate_technical_features, generate_volume_features,
    generate_volatility_features, generate_sentiment_features,
    generate_onchain_features, generate_time_features,
    generate_pattern_features, generate_correlation_features,
    combine_features
)

# 유틸리티 함수들
from .utils import validate_data, get_available_indicators

# 설정 및 상수
DEFAULT_PERIOD = 14
DEFAULT_FAST_PERIOD = 12
DEFAULT_SLOW_PERIOD = 26
DEFAULT_SIGNAL_PERIOD = 9

__version__ = '1.0.0'

# 모든 public 심볼 정의
__all__ = [
    # Indicator Classes
    'TrendIndicator', 'MomentumIndicator', 'VolumeIndicator',
    'VolatilityIndicator', 'SentimentIndicator', 'CompositeIndicator',
    'OnchainIndicator', 'ArbitrageFeature', 'FeatureGenerator',
    
    # Utility Functions
    'validate_data', 'get_available_indicators',
    
    # Constants
    'DEFAULT_PERIOD', 'DEFAULT_FAST_PERIOD', 'DEFAULT_SLOW_PERIOD',
    'DEFAULT_SIGNAL_PERIOD',
    
    # Individual Functions
    'sma', 'ema', 'wma', 'macd', 'ichimoku', 'parabolic_sar',
    'rsi', 'stochastic_oscillator', 'williams_r', 'cci', 'roc', 'mfi',
    'ultimate_oscillator', 'rvi', 'tsi', 'advance_decline_line',
    'mcclellan_oscillator', 'mcclellan_summation_index', 'kst_oscillator',
    'market_breadth', 'obv', 'vwap', 'ad_line', 'chaikin_money_flow',
    'ease_of_movement', 'volume_price_trend', 'negative_volume_index',
    'positive_volume_index', 'percentage_volume_oscillator', 'atr',
    'std_deviation', 'choppiness_index', 'historical_volatility',
    'bollinger_bandwidth', 'ulcer_index', 'chaikin_volatility',
    'donchian_channel', 'keltner_channel', 'fear_greed_index',
    'social_sentiment', 'news_sentiment', 'trading_activity_index',
    'put_call_ratio', 'margin_debt_ratio', 'technical_sentiment',
    'volatility_sentiment', 'bullish_percent_index', 'high_low_index',
    'market_sentiment', 'nvt_ratio', 'mvrv_ratio', 'stock_to_flow_ratio',
    'active_addresses', 'transaction_volume', 'exchange_flow', 'hodl_waves',
    'mining_difficulty', 'hash_rate', 'realized_cap', 'zigzag',
    'fractal_indicator', 'pivot_points', 'schaff_trend_cycle', 'alma',
    'connors_rsi', 'triple_screen', 'elder_ray', 'demark_indicators',
    'hybrid_rsi', 'trend_strength_index', 'volume_price_confirmation',
    'multi_factor_ranking', 'generate_price_spread_features',
    'generate_volume_spread_features', 'generate_orderbook_features',
    'generate_execution_cost_features', 'generate_liquidity_features',
    'generate_market_impact_features', 'generate_risk_features',
    'generate_opportunity_score', 'generate_technical_features',
    'generate_volume_features', 'generate_volatility_features',
    'generate_sentiment_features', 'generate_onchain_features',
    'generate_time_features', 'generate_pattern_features',
    'generate_correlation_features', 'combine_features'
]

def get_indicator_info(indicator_name):
    """특정 지표에 대한 상세 정보를 반환합니다."""
    indicator_func = globals().get(indicator_name)
    if indicator_func:
        return {
            'name': indicator_name,
            'description': indicator_func.__doc__,
            'parameters': indicator_func.__code__.co_varnames[:indicator_func.__code__.co_argcount]
        }
    return None
