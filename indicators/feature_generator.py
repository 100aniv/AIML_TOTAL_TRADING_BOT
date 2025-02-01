import pandas as pd
import numpy as np
from .trend_indicator import *
from .momentum_indicator import *
from .volume_indicator import *
from .volatility_indicator import *
from .sentiment_indicator import *
from .composite_indicator import *
from .onchain_indicator import *
from typing import List, Dict

'''
9. ML 특징 생성기 (ML Feature Generator)

정의
기술적 지표와 시장 데이터를 기반으로 머신러닝에 적합한 특징들을 생성하는 도구입니다.

목적
• 기술적 지표 기반 특징 생성
• 통계적 특징 추출
• 시장 구조 특징 분석
• 특징 전처리 및 정규화
• 차원 축소 및 특징 선택

특징 목록 (15개)
1. Technical Features: 기술적 지표 기반 특징 (이동평균, 오실레이터, 기술적 지표 조합)
2. Price Features: 가격 데이터 기반 특징 (가격 패턴, 가격 모멘텀, 가격 변동성)
3. Volume Features: 거래량 기반 특징 (거래량 프로필, 거래량 패턴, 거래량 가중 지표)
4. Volatility Features: 변동성 기반 특징 (ATR, 볼린저밴드, 변동성 지표)
5. Momentum Features: 모멘텀 지표 기반 특징 (RSI, MACD, 스토캐스틱)
6. Trend Features: 추세 지표 기반 특징 (이동평균, 추세선, 방향성 지표)
7. Pattern Features: 차트 패턴 기반 특징 (캔들스틱, 차트 패턴, 가격 형태)
8. Sentiment Features: 감성 지표 기반 특징 (시장 심리, 투자자 심리, 뉴스 감성)
9. Onchain Features: 온체인 데이터 기반 특징 (네트워크 지표, 온체인 활동)
10. Market Structure Features: 시장 구조 특징 (유동성, 호가창, 주문흐름)
11. Statistical Features: 통계적 특징 (시계열 특성, 분포, 상관관계)
12. Time Features: 시간 기반 특징 (계절성, 주기성, 시간 패턴)
13. Correlation Features: 상관관계 특징 (자산간 상관관계, 섹터 상관관계)
14. ML-Specific Features: ML 전용 특징 (파생 특징, 교차 특징, 시계열 특징)
15. Composite Features: 복합 지표 기반 특징 (다중 지표 조합, 복합 신호)

특징 목록 상세
1. Technical Features
   - 이동평균 (SMA, EMA, WMA)
   - 오실레이터 (RSI, Stochastic, CCI)
   - 기술적 지표 조합 (MACD, Bollinger Bands)

2. Price Features
   - 가격 패턴 (캔들스틱, 가격대별 거래량)
   - 가격 모멘텀 (ROC, Price Momentum)
   - 가격 변동성 (ATR, True Range)

3. Volume Features
   - 거래량 프로필 (Volume Profile, VWAP)
   - 거래량 패턴 (Volume Trend, Volume Breakouts)
   - 거래량 가중 지표 (Volume RSI, Volume Force)

4. Volatility Features
   - 변동성 지표 (ATR, Historical Volatility)
   - 변동성 밴드 (Bollinger Bands, Keltner Channel)
   - 변동성 패턴 (Volatility Breakouts)

5. Momentum Features
   - 기본 모멘텀 (RSI, Stochastic)
   - 추세 모멘텀 (MACD, ADX)
   - 가격 모멘텀 (ROC, Momentum)

6. Trend Features
   - 이동평균 (SMA, EMA, DEMA)
   - 추세선 (Linear Regression, ADX)
   - 방향성 지표 (DI+/-, Aroon)

7. Pattern Features
   - 캔들스틱 패턴 (Doji, Hammer)
   - 차트 패턴 (Head & Shoulders, Triangles)
   - 가격 형태 (Price Patterns, Formations)

8. Sentiment Features
   - 시장 심리 (Fear & Greed Index)
   - 투자자 심리 (Put/Call Ratio)
   - 뉴스 감성 (News Sentiment Score)

9. Onchain Features
   - 네트워크 지표 (NVT, MVRV)
   - 온체인 활동 (Active Addresses)
   - 채굴자 행동 (Hash Rate, Difficulty)

10. Market Structure Features
    - 유동성 지표 (Bid-Ask Spread)
    - 호가창 분석 (Order Book Depth)
    - 주문흐름 (Order Flow Imbalance)

11. Statistical Features
    - 시계열 특성 (Autocorrelation)
    - 분포 특성 (Skewness, Kurtosis)
    - 통계적 모멘트 (Statistical Moments)

12. Time Features
    - 계절성 (Seasonality)
    - 주기성 (Cyclical Patterns)
    - 시간대 효과 (Time of Day Effects)

13. Correlation Features
    - 자산간 상관관계 (Asset Correlations)
    - 섹터 상관관계 (Sector Correlations)
    - 크로스 마켓 (Cross-Market Relations)

14. ML-Specific Features
    - 파생 특징 (Feature Derivatives)
    - 교차 특징 (Feature Interactions)
    - 시계열 특징 (Lagged Features)

15. Composite Features
    - 다중 지표 조합 (Multi-Indicator)
    - 복합 신호 (Signal Combinations)
    - 앙상블 특징 (Ensemble Features)

참고 사항
• 실시간 특징 생성 지원
• 특징 정규화 필수
• 차원 축소 고려
• 특징 선택 로직 포함

[2024.03.XX] 함수명 패턴 표준화
기존 함수명 -> 변경된 함수명:
- calculate_technical_features -> technical_features
- calculate_price_features -> price_features
- calculate_volume_features -> volume_features
- calculate_statistical -> statistical_features
- calculate_market_structure -> market_features
- calculate_ml_specific -> ml_features
'''

#1. Technical Features: 기술적 지표 기반 특징
def technical_features(df: pd.DataFrame, periods: List[int] = [5, 10, 20]) -> pd.DataFrame:
    """기술적 지표 기반 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        periods: 계산 기간 리스트 (기본값: [5, 10, 20])
        
    Returns:
        기술적 지표 특징들 (DataFrame)
        
    Note:
        - 이동평균 지표
        - 오실레이터 지표
        - 기술적 지표 조합
    """
    features = pd.DataFrame(index=df.index)
    
    # 이동평균 (SMA, EMA, WMA)
    for period in periods:
        features[f'sma_{period}'] = sma(df['close'], period)
        features[f'ema_{period}'] = ema(df['close'], period)
        features[f'wma_{period}'] = wma(df['close'], period)
    
    # 오실레이터 (RSI, Stochastic, CCI)
    for period in periods:
        features[f'rsi_{period}'] = rsi(df['close'], period)
        features[f'stoch_{period}'] = stochastic(df['high'], df['low'], df['close'], period)
        features[f'cci_{period}'] = cci(df['high'], df['low'], df['close'], period)
    
    # 기술적 지표 조합 (MACD, Bollinger Bands)
    features['macd'], features['macd_signal'], features['macd_hist'] = macd(df['close'])
    features['bb_upper'], features['bb_middle'], features['bb_lower'] = bollinger_bands(df['close'])
    
    return features

#2. Price Features: 가격 데이터 기반 특징
def price_features(df: pd.DataFrame, periods: List[int] = [5, 10, 20]) -> pd.DataFrame:
    """가격 데이터 기반 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        periods: 계산 기간 리스트 (기본값: [5, 10, 20])
        
    Returns:
        가격 기반 특징들 (DataFrame)
        
    Note:
        - 가격 패턴
        - 가격 모멘텀
        - 가격 변동성
    """
    features = pd.DataFrame(index=df.index)
    
    # 가격 패턴
    features['body_size'] = abs(df['close'] - df['open'])
    features['upper_shadow'] = df['high'] - df[['open', 'close']].max(axis=1)
    features['lower_shadow'] = df[['open', 'close']].min(axis=1) - df['low']
    
    # 가격 모멘텀
    for period in periods:
        features[f'roc_{period}'] = (df['close'] / df['close'].shift(period) - 1) * 100
        features[f'momentum_{period}'] = df['close'] - df['close'].shift(period)
    
    # 가격 변동성
    features['atr'] = atr(df['high'], df['low'], df['close'])
    features['true_range'] = true_range(df['high'], df['low'], df['close'])
    
    return features

#3. Volume Features: 거래량 기반 특징
def volume_features(df: pd.DataFrame, periods: List[int] = [5, 10, 20]) -> pd.DataFrame:
    """거래량 기반 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        periods: 계산 기간 리스트 (기본값: [5, 10, 20])
        
    Returns:
        거래량 기반 특징들 (DataFrame)
        
    Note:
        - 거래량 프로필
        - 거래량 패턴
        - 거래량 가중 지표
    """
    features = pd.DataFrame(index=df.index)
    
    # 거래량 프로필
    for period in periods:
        features[f'vwap_{period}'] = vwap(df['close'], df['volume'], period)
        features[f'volume_profile_{period}'] = volume_profile(df['close'], df['volume'], period)
    
    # 거래량 패턴
    features['volume_trend'] = volume_trend(df['volume'])
    features['volume_breakout'] = volume_breakout(df['volume'], df['close'])
    
    # 거래량 가중 지표
    features['volume_rsi'] = volume_rsi(df['volume'])
    features['volume_force'] = volume_force(df['close'], df['volume'])
    
    return features

#4. Volatility Features: 변동성 기반 특징
def volatility_features(df: pd.DataFrame, periods: List[int] = [5, 10, 20]) -> pd.DataFrame:
    """변동성 기반 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        periods: 계산 기간 리스트 (기본값: [5, 10, 20])
        
    Returns:
        변동성 기반 특징들 (DataFrame)
        
    Note:
        - 변동성 지표
        - 변동성 밴드
        - 변동성 패턴
    """
    features = pd.DataFrame(index=df.index)
    
    # 변동성 지표
    for period in periods:
        features[f'atr_{period}'] = atr(df['high'], df['low'], df['close'], period)
        features[f'historical_vol_{period}'] = historical_volatility(df['close'], period)
    
    # 변동성 밴드
    features['bb_upper'], features['bb_middle'], features['bb_lower'] = bollinger_bands(df['close'])
    features['kc_upper'], features['kc_middle'], features['kc_lower'] = keltner_channel(df['high'], df['low'], df['close'])
    
    # 변동성 패턴
    features['volatility_breakout'] = volatility_breakout(df['close'], df['high'], df['low'])
    features['bb_width'] = bollinger_bandwidth(df['close'])
    
    return features

#5. Momentum Features: 모멘텀 지표 기반 특징
def momentum_features(df: pd.DataFrame, periods: List[int] = [5, 10, 20]) -> pd.DataFrame:
    """모멘텀 지표 기반 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        periods: 계산 기간 리스트 (기본값: [5, 10, 20])
        
    Returns:
        모멘텀 기반 특징들 (DataFrame)
        
    Note:
        - 기본 모멘텀 (RSI, Stochastic)
        - 추세 모멘텀 (MACD, ADX)
        - 가격 모멘텀 (ROC, Momentum)
    """
    features = pd.DataFrame(index=df.index)
    
    # 기본 모멘텀
    features['rsi'] = rsi(df['close'])
    features['stoch_k'], features['stoch_d'] = stochastic(df['high'], df['low'], df['close'])
    
    # 추세 모멘텀
    features['macd'], features['macd_signal'], features['macd_hist'] = macd(df['close'])
    features['adx'] = adx(df['high'], df['low'], df['close'])
    
    # 가격 모멘텀
    for period in periods:
        features[f'roc_{period}'] = roc(df['close'], period)
        features[f'momentum_{period}'] = momentum(df['close'], period)
    
    return features

#6. Trend Features: 추세 지표 기반 특징
def trend_features(df: pd.DataFrame, periods: List[int] = [5, 10, 20]) -> pd.DataFrame:
    """추세 지표 기반 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        periods: 계산 기간 리스트 (기본값: [5, 10, 20])
        
    Returns:
        추세 기반 특징들 (DataFrame)
        
    Note:
        - 이동평균 (SMA, EMA, DEMA)
        - 추세선 (Linear Regression, ADX)
        - 방향성 지표 (DI+/-, Aroon)
    """
    features = pd.DataFrame(index=df.index)
    
    # 이동평균
    for period in periods:
        features[f'sma_{period}'] = sma(df['close'], period)
        features[f'ema_{period}'] = ema(df['close'], period)
        features[f'dema_{period}'] = dema(df['close'], period)
    
    # 추세선
    features['linear_reg'] = linear_regression(df['close'])
    features['adx'] = adx(df['high'], df['low'], df['close'])
    
    # 방향성 지표
    features['di_plus'], features['di_minus'] = directional_index(df['high'], df['low'], df['close'])
    features['aroon_up'], features['aroon_down'] = aroon(df['high'], df['low'])
    
    return features

#7. Pattern Features: 차트 패턴 기반 특징
def pattern_features(df: pd.DataFrame) -> pd.DataFrame:
    """차트 패턴 기반 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        
    Returns:
        패턴 기반 특징들 (DataFrame)
        
    Note:
        - 캔들스틱 패턴 (Doji, Hammer)
        - 차트 패턴 (Head & Shoulders, Triangles)
        - 가격 형태 (Price Patterns, Formations)
    """
    features = pd.DataFrame(index=df.index)
    
    # 캔들스틱 패턴
    features['doji'] = detect_doji(df['open'], df['high'], df['low'], df['close'])
    features['hammer'] = detect_hammer(df['open'], df['high'], df['low'], df['close'])
    features['shooting_star'] = detect_shooting_star(df['open'], df['high'], df['low'], df['close'])
    
    # 차트 패턴
    features['head_shoulders'] = detect_head_shoulders(df['close'])
    features['double_top'] = detect_double_top(df['close'])
    features['triangle'] = detect_triangle(df['high'], df['low'])
    
    # 가격 형태
    features['support_resistance'] = detect_support_resistance(df['close'])
    features['trend_channels'] = detect_trend_channels(df['high'], df['low'])
    
    return features

#8. Sentiment Features: 감성 지표 기반 특징
def sentiment_features(df: pd.DataFrame, sentiment_data: Dict) -> pd.DataFrame:
    """감성 지표 기반 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        sentiment_data: 감성 분석 데이터 (Dict)
        
    Returns:
        감성 기반 특징들 (DataFrame)
        
    Note:
        - 시장 심리 (Fear & Greed Index)
        - 투자자 심리 (Put/Call Ratio)
        - 뉴스 감성 (News Sentiment Score)
    """
    features = pd.DataFrame(index=df.index)
    
    # 시장 심리
    features['fear_greed'] = fear_greed_index(
        sentiment_data['volatility'],
        sentiment_data['momentum'],
        sentiment_data['volume'],
        sentiment_data['market_cap'],
        sentiment_data['social_data']
    )
    
    # 투자자 심리
    features['put_call_ratio'] = put_call_ratio(
        sentiment_data['put_volume'],
        sentiment_data['call_volume']
    )
    features['bullish_percent'] = bullish_percent_index(
        sentiment_data['bullish_count'],
        sentiment_data['total_count']
    )
    
    # 뉴스 감성
    features['social_sentiment'] = social_sentiment(sentiment_data['social_texts'])
    features['news_sentiment'] = news_sentiment(
        sentiment_data['headlines'],
        sentiment_data['contents']
    )
    
    return features

#9. Onchain Features: 온체인 데이터 기반 특징
def onchain_features(df: pd.DataFrame, onchain_data: Dict) -> pd.DataFrame:
    """온체인 데이터 기반 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        onchain_data: 온체인 데이터 (Dict)
        
    Returns:
        온체인 기반 특징들 (DataFrame)
        
    Note:
        - 네트워크 지표 (NVT, MVRV)
        - 온체인 활동 (Active Addresses)
        - 채굴자 행동 (Hash Rate, Difficulty)
    """
    features = pd.DataFrame(index=df.index)
    
    # 네트워크 지표
    features['nvt_ratio'] = nvt_ratio(
        onchain_data['market_cap'],
        onchain_data['transaction_volume']
    )
    features['mvrv_ratio'] = mvrv_ratio(
        onchain_data['market_value'],
        onchain_data['realized_value']
    )
    
    # 온체인 활동
    features['active_addresses'] = active_addresses(
        onchain_data['address_data']
    )
    features['transaction_volume'] = transaction_volume(
        onchain_data['transaction_data']
    )
    
    # 채굴자 행동
    features['mining_difficulty'] = mining_difficulty(
        onchain_data['difficulty_data']
    )
    features['hash_rate'] = hash_rate(
        onchain_data['hash_data']
    )
    
    return features

#10. Market Structure Features: 시장 구조 특징
def market_features(df: pd.DataFrame) -> pd.DataFrame:
    """시장 구조 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        
    Returns:
        시장 구조 특징들 (DataFrame)
        
    Note:
        - 유동성 지표 (Bid-Ask Spread)
        - 호가창 분석 (Order Book Depth)
        - 주문흐름 (Order Flow Imbalance)
    """
    features = pd.DataFrame(index=df.index)
    
    # 유동성 지표
    features['bid_ask_spread'] = df['ask'] - df['bid']
    features['relative_spread'] = features['bid_ask_spread'] / df['close']
    features['effective_spread'] = calculate_effective_spread(df)
    
    # 호가창 분석
    features['book_depth'] = calculate_book_depth(df)
    features['book_imbalance'] = calculate_book_imbalance(df)
    features['book_pressure'] = calculate_book_pressure(df)
    
    # 주문흐름 분석
    features['order_flow'] = calculate_order_flow(df)
    features['trade_flow'] = calculate_trade_flow(df)
    features['flow_imbalance'] = calculate_flow_imbalance(df)
    
    return features

#11. Statistical Features: 통계적 특징
def statistical_features(df: pd.DataFrame) -> pd.DataFrame:
    """통계적 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        
    Returns:
        통계적 특징들 (DataFrame)
        
    Note:
        - 시계열 특성 (Autocorrelation)
        - 분포 특성 (Skewness, Kurtosis)
        - 통계적 모멘트 (Statistical Moments)
    """
    features = pd.DataFrame(index=df.index)
    
    # 시계열 특성
    features['autocorr'] = calculate_autocorrelation(df['close'])
    features['partial_autocorr'] = calculate_partial_autocorr(df['close'])
    features['adf_stat'] = calculate_adf_statistic(df['close'])
    
    # 분포 특성
    features['skewness'] = calculate_skewness(df['close'])
    features['kurtosis'] = calculate_kurtosis(df['close'])
    features['normality'] = calculate_normality_test(df['close'])
    
    # 통계적 모멘트
    features['first_moment'] = calculate_first_moment(df['close'])
    features['second_moment'] = calculate_second_moment(df['close'])
    features['third_moment'] = calculate_third_moment(df['close'])
    
    return features

#12. Time Features: 시간 기반 특징
def time_features(df: pd.DataFrame) -> pd.DataFrame:
    """시간 기반 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        
    Returns:
        시간 기반 특징들 (DataFrame)
        
    Note:
        - 계절성 (Seasonality)
        - 주기성 (Cyclical Patterns)
        - 시간대 효과 (Time of Day Effects)
    """
    features = pd.DataFrame(index=df.index)
    
    # 계절성 분석
    features['month'] = df.index.month
    features['quarter'] = df.index.quarter
    features['year_progress'] = df.index.dayofyear / 365.25
    
    # 주기성 분석
    features['day_of_week'] = df.index.dayofweek
    features['week_of_year'] = df.index.isocalendar().week
    features['is_month_end'] = df.index.is_month_end.astype(int)
    
    # 시간대 효과
    features['hour_of_day'] = df.index.hour
    features['is_trading_hour'] = (df.index.hour >= 9) & (df.index.hour <= 16)
    features['session_progress'] = (df.index.hour * 60 + df.index.minute) / (24 * 60)
    
    return features

#13. Correlation Features: 상관관계 특징
def correlation_features(df: pd.DataFrame) -> pd.DataFrame:
    """상관관계 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        
    Returns:
        상관관계 기반 특징들 (DataFrame)
        
    Note:
        - 자산간 상관관계 (Asset Correlations)
        - 섹터 상관관계 (Sector Correlations)
        - 크로스 마켓 (Cross-Market Relations)
    """
    features = pd.DataFrame(index=df.columns)
    
    # 자산간 상관관계
    features['asset_correlation'] = calculate_asset_correlation(df)
    features['rolling_correlation'] = calculate_rolling_correlation(df)
    
    # 섹터 상관관계
    features['sector_correlation'] = calculate_sector_correlation(df)
    features['sector_beta'] = calculate_sector_beta(df)
    
    # 크로스 마켓
    features['market_correlation'] = calculate_market_correlation(df)
    features['cross_asset_flow'] = calculate_cross_asset_flow(df)
    
    return features

#14. ML-Specific Features: ML 전용 특징
def ml_features(df: pd.DataFrame) -> pd.DataFrame:
    """ML 전용 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        
    Returns:
        ML 전용 특징들 (DataFrame)
        
    Note:
        - 파생 특징 (Feature Derivatives)
        - 교차 특징 (Feature Interactions)
        - 시계열 특징 (Lagged Features)
    """
    features = pd.DataFrame(index=df.index)
    
    # 파생 특징
    features['price_derivative'] = calculate_price_derivative(df['close'])
    features['volume_derivative'] = calculate_volume_derivative(df['volume'])
    features['momentum_derivative'] = calculate_momentum_derivative(df)
    
    # 교차 특징
    features['price_volume_interaction'] = calculate_price_volume_interaction(df)
    features['trend_momentum_interaction'] = calculate_trend_momentum_interaction(df)
    features['volatility_volume_interaction'] = calculate_volatility_volume_interaction(df)
    
    # 시계열 특징
    features['lagged_returns'] = calculate_lagged_returns(df['close'])
    features['lagged_volume'] = calculate_lagged_volume(df['volume'])
    features['lagged_volatility'] = calculate_lagged_volatility(df)
    
    return features

#15. Composite Features: 복합 지표 기반 특징
def composite_features(df: pd.DataFrame, feature_sets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """복합 지표 기반 특징 생성
    
    Args:
        df: OHLCV 데이터프레임
        feature_sets: 각 특징 세트들의 딕셔너리
        
    Returns:
        복합 지표 기반 특징들 (DataFrame)
        
    Note:
        - 다중 지표 조합 (Multi-Indicator)
        - 복합 신호 (Signal Combinations)
        - 앙상블 특징 (Ensemble Features)
    """
    features = pd.DataFrame(index=df.index)
    
    # 다중 지표 조합
    features['multi_indicator'] = calculate_multi_indicator_combination(feature_sets)
    features['weighted_signals'] = calculate_weighted_signals(feature_sets)
    
    # 복합 신호
    features['signal_consensus'] = calculate_signal_consensus(feature_sets)
    features['signal_strength'] = calculate_signal_strength(feature_sets)
    
    # 앙상블 특징
    features['ensemble_score'] = calculate_ensemble_score(feature_sets)
    features['feature_importance'] = calculate_feature_importance(feature_sets)
    
    # 전처리 및 품질 관리
    features = preprocess_features(features)
    features = validate_feature_quality(features)
    
    return features

class FeatureGenerator:
    """ML 특징 생성기 클래스
    
    Args:
        data: OHLCV 데이터프레임 (선택사항)
        
    Note:
        - 15개의 특징 카테고리 생성
        - 자동 전처리 및 품질 관리
        - 실시간 특징 생성 지원
    """
    
    def __init__(self, data=None):
        """특징 생성기 클래스 초기화
        
        Args:
            data: OHLCV 데이터프레임 (선택사항)
            
        Note:
            - 필수 컬럼: open, high, low, close, volume
            - 선택 컬럼: sentiment_score, blockchain_data, related_assets
        """
        self.data = data
        if data is not None:
            self._validate_data()

    def _validate_data(self):
        """데이터 유효성 검증
        
        Raises:
            ValueError: 필수 컬럼이 누락된 경우
        """
        required = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Required columns missing: {required}")

    def generate_all(self):
        """모든 특징 생성"""
        results = pd.DataFrame(index=self.data.index)
        
        # 기술적 특징 생성
        results = pd.concat([results, technical_features(self.data)], axis=1)
        
        # 가격 특징 생성
        results = pd.concat([results, price_features(self.data)], axis=1)
        
        # 거래량 특징 생성
        results = pd.concat([results, volume_features(self.data)], axis=1)
        
        # 변동성 특징 생성
        results = pd.concat([results, volatility_features(self.data)], axis=1)
        
        # 모멘텀 특징 생성
        results = pd.concat([results, momentum_features(self.data)], axis=1)
        
        # 추세 특징 생성
        results = pd.concat([results, trend_features(self.data)], axis=1)
        
        # 패턴 특징 생성
        results = pd.concat([results, pattern_features(self.data)], axis=1)
        
        # 감성 특징 생성
        if 'sentiment_score' in self.data.columns:
            results = pd.concat([results, sentiment_features(self.data)], axis=1)
        
        # 온체인 특징 생성
        if 'blockchain_data' in self.data.columns:
            results = pd.concat([results, onchain_features(self.data)], axis=1)
        
        # 시간 특징 생성
        results = pd.concat([results, time_features(self.data)], axis=1)
        
        # 상관관계 특징 생성
        if 'related_assets' in self.data.columns:
            results = pd.concat([results, correlation_features(self.data)], axis=1)
        
        # 복합 특징 생성
        results = pd.concat([results, composite_features(results, {
            'technical': technical_features(self.data),
            'volume': volume_features(self.data),
            'volatility': volatility_features(self.data),
            'sentiment': sentiment_features(self.data, {}),
            'onchain': onchain_features(self.data, {}),
            'time': time_features(self.data),
            'pattern': pattern_features(self.data),
            'correlation': correlation_features(self.data)
        })], axis=1)
        
        return results
