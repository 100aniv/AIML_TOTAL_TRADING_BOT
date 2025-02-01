"""
7. 감성 지표 (Sentiment Indicators)

정의
시장 참여자들의 심리와 행동을 분석하여 시장의 전반적인 감성을 측정하는 지표들입니다.

목적
• 시장 심리 상태 파악
• 과매수/과매도 구간 식별
• 투자자 행동 패턴 분석
• 시장 전환점 예측
• 리스크 관리

지표 목록 (12개)
1. Fear & Greed Index: 시장의 공포와 탐욕 수준을 종합적으로 측정하는 지표
2. Social Media Sentiment: 소셜 미디어 데이터 기반의 시장 감성 분석 지표
3. News Sentiment: 뉴스 데이터의 감성 분석을 통한 시장 심리 측정 지표
4. Google Trends: 검색 트렌드 데이터 기반의 관심도 분석 지표
5. Crypto Fear & Greed: 암호화폐 시장 전용 공포/탐욕 지수
6. Whale Transaction: 대형 거래자들의 행동 패턴 분석 지표
7. Options Sentiment: 옵션 시장 데이터 기반의 투자자 심리 지표
8. Funding Rate: 선물 시장의 펀딩비를 통한 시장 심리 분석 지표
9. Long/Short Ratio: 롱/숏 포지션 비율을 통한 시장 참여자 심리 지표
10. Liquidation Data: 청산 데이터 기반의 시장 스트레스 측정 지표
11. Exchange Flow Sentiment: 거래소 자금 흐름 기반의 투자자 심리 지표
12. Social Engagement: 소셜 미디어 참여도 기반의 관심도 측정 지표

참고 사항
• 여러 데이터 소스의 통합 분석 필요
• 실시간 데이터 업데이트 중요
• 시장별 특성 고려 필요
• 다른 기술적 지표와 결합하여 사용

[2024.03.XX] 함수명 패턴 표준화
기존 함수명 -> 변경된 함수명:
- calculate_fear_greed -> fear_greed
- calculate_social_sentiment -> social_sentiment
- calculate_news_sentiment -> news_sentiment
- calculate_google_trends -> google_trends
- calculate_crypto_fear -> crypto_fear_greed
- calculate_whale_sentiment -> whale_sentiment
- calculate_options_sentiment -> options_sentiment
- calculate_funding_sentiment -> funding_sentiment
- calculate_long_short -> long_short_ratio
- calculate_liquidation -> liquidation_sentiment
- calculate_exchange_flow -> exchange_flow_sentiment
- calculate_social_engagement -> social_engagement
"""
import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from typing import List, Optional

#1. Fear & Greed Index: 시장의 공포와 탐욕 수준을 종합적으로 측정하는 지표
def calculate_fear_greed_index(volatility, momentum, volume, dominance, social_data):
    """
    Fear & Greed Index 계산
    :param volatility: 변동성 데이터 (Pandas Series)
    :param momentum: 모멘텀 데이터 (Pandas Series)
    :param volume: 거래량 데이터 (Pandas Series)
    :param dominance: 시장 지배력 데이터 (Pandas Series)
    :param social_data: 소셜 데이터 (Pandas Series)
    :return: Fear & Greed Index 값 (Pandas Series)
    """
    # 각 지표별 가중치 설정
    weights = {
        'volatility': 0.25,
        'momentum': 0.25,
        'volume': 0.15,
        'dominance': 0.15,
        'social': 0.20
    }
    
    # 각 지표 정규화 (0-100)
    normalized_data = {
        'volatility': (volatility - volatility.min()) / (volatility.max() - volatility.min()) * 100,
        'momentum': (momentum - momentum.min()) / (momentum.max() - momentum.min()) * 100,
        'volume': (volume - volume.min()) / (volume.max() - volume.min()) * 100,
        'dominance': (dominance - dominance.min()) / (dominance.max() - dominance.min()) * 100,
        'social': (social_data - social_data.min()) / (social_data.max() - social_data.min()) * 100
    }
    
    # 가중 평균 계산
    fear_greed = sum(normalized_data[k] * weights[k] for k in weights.keys())
    return fear_greed

# 기존 함수 유지
def fear_greed(volatility, momentum, volume, dominance, social_data):
    return calculate_fear_greed_index(volatility, momentum, volume, dominance, social_data)

#2. Social Media Sentiment: 소셜 미디어 데이터 기반의 시장 감성 분석 지표.
def calculate_social_sentiment_score(texts, weights=None):
    """
    소셜 미디어 감성 분석
    :param texts: 분석할 텍스트 리스트 (List of str)
    :param weights: 텍스트별 가중치 (기본값: None, 동일 가중치)
    :return: 감성 점수 (-1 to 1)
    """
    if weights is None:
        weights = [1/len(texts)] * len(texts)
    
    sentiments = []
    for text in texts:
        # 텍스트 전처리
        clean_text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        # 감성 분석
        blob = TextBlob(clean_text)
        sentiments.append(blob.sentiment.polarity)
    
    # 가중 평균 계산
    weighted_sentiment = np.average(sentiments, weights=weights)
    return weighted_sentiment

# 기존 함수 유지
def social_sentiment(texts, weights=None):
    return calculate_social_sentiment_score(texts, weights)

#3. News Sentiment: 뉴스 데이터의 감성 분석을 통한 시장 심리 측정 지표.
def calculate_news_sentiment_score(headlines, contents, weights={'headline': 0.4, 'content': 0.6}):
    """
    뉴스 기사 감성 분석
    :param headlines: 헤드라인 리스트 (List of str)
    :param contents: 본문 리스트 (List of str)
    :param weights: 헤드라인과 본문의 가중치
    :return: 감성 점수 (-1 to 1)
    """
    headline_sentiments = []
    content_sentiments = []
    
    for headline, content in zip(headlines, contents):
        # 헤드라인 분석
        headline_blob = TextBlob(headline)
        headline_sentiments.append(headline_blob.sentiment.polarity)
        
        # 본문 분석
        content_blob = TextBlob(content)
        content_sentiments.append(content_blob.sentiment.polarity)
    
    # 가중 평균 계산
    final_sentiment = (np.mean(headline_sentiments) * weights['headline'] + 
                      np.mean(content_sentiments) * weights['content'])
    return final_sentiment

# 기존 함수 유지
def news_sentiment(headlines, contents, weights={'headline': 0.4, 'content': 0.6}):
    return calculate_news_sentiment_score(headlines, contents, weights)

#4. Google Trends: 검색 트렌드 데이터 기반의 관심도 분석 지표.
def calculate_google_trends_analysis(search_data, period=14):
    """
    Google Trends 분석
    :param search_data: 검색량 데이터 (Pandas Series)
    :param period: 분석 기간 (기본값: 14일)
    :return: 트렌드 점수 (0-100)
    """
    normalized = (search_data - search_data.min()) / (search_data.max() - search_data.min()) * 100
    return normalized.rolling(window=period).mean()

# 기존 함수 유지
def google_trends(search_data, period=14):
    return calculate_google_trends_analysis(search_data, period)

#5. Crypto Fear & Greed: 암호화폐 시장 전용 공포/탐욕 지수
def calculate_crypto_fear_greed(volatility, period=30):
    """Crypto Fear & Greed 지수 계산
    
    Args:
        volatility: 변동성 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 30일)
        
    Returns:
        공포/탐욕 지수 (Pandas Series)
        
    Note:
        - 0-25: 극도의 공포
        - 26-45: 공포
        - 46-54: 중립
        - 55-75: 탐욕
        - 76-100: 극도의 탐욕
    """
    normalized = (volatility - volatility.rolling(period).min()) / \
                (volatility.rolling(period).max() - volatility.rolling(period).min()) * 100
    return 100 - normalized  # 변동성이 높을수록 공포 지수가 높아짐

# 기존 함수 유지
def crypto_fear_greed(volatility, period=30):
    return calculate_crypto_fear_greed(volatility, period)

#6. Whale Transaction: 대형 거래자들의 행동 패턴 분석
def calculate_whale_sentiment(volume, price_change, period=14):
    """Whale Sentiment 계산
    
    Args:
        volume: 거래량 데이터 (Pandas Series)
        price_change: 가격 변화율 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14일)
        
    Returns:
        대형 거래자 심리 지수 (Pandas Series)
        
    Note:
        - 양수: 대형 매수 우세
        - 음수: 대형 매도 우세
        - 극단값: 강한 시장 신호
    """
    whale_impact = volume * price_change
    return whale_impact.rolling(window=period).mean()

# 기존 함수 유지
def whale_sentiment(volume, price_change, period=14):
    return calculate_whale_sentiment(volume, price_change, period)

#7. Options Sentiment: 옵션 시장 데이터 기반의 투자자 심리 지표
def calculate_options_sentiment(put_volume, call_volume, period=14):
    """Options Sentiment 계산
    
    Args:
        put_volume: 풋 옵션 거래량 데이터 (Pandas Series)
        call_volume: 콜 옵션 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14일)
        
    Returns:
        옵션 시장 감성 점수 (-1 to 1)
        
    Note:
        - 1에 가까울수록: 강한 매수 심리
        - -1에 가까울수록: 강한 매도 심리
        - 0 근처: 중립적 심리
    """
    put_call_ratio = (put_volume / call_volume).rolling(window=period).mean()
    return 1 - (2 / (1 + np.exp(-put_call_ratio)))

# 기존 함수 유지
def options_sentiment(put_volume, call_volume, period=14):
    return calculate_options_sentiment(put_volume, call_volume, period)

#8. Funding Rate: 선물 시장의 펀딩비를 통한 시장 심리 분석 지표.
def calculate_funding_sentiment(funding_rate, period=14):
    """Funding Sentiment 계산
    
    Args:
        funding_rate: 펀딩비 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14일)
        
    Returns:
        펀딩비 심리 지수 (Pandas Series)
        
    Note:
        - 양수: 롱 포지션 우세
        - 음수: 숏 포지션 우세
        - 극단값: 레버리지 과다
    """
    return funding_rate.rolling(window=period).mean()

# 기존 함수 유지
def funding_sentiment(funding_rate, period=14):
    return calculate_funding_sentiment(funding_rate, period)

#9. Long/Short Ratio: 롱/숏 포지션 비율을 통한 시장 참여자 심리 지표.
def calculate_long_short_ratio(long_volume, short_volume, period=14):
    """Long/Short Ratio 계산
    
    Args:
        long_volume: 롱 포지션 거래량 데이터 (Pandas Series)
        short_volume: 숏 포지션 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14일)
        
    Returns:
        롱/숏 비율 지수 (Pandas Series)
        
    Note:
        - 1 초과: 롱 포지션 우세
        - 1 미만: 숏 포지션 우세
        - 1: 중립적 상태
    """
    ratio = long_volume / short_volume
    return ratio.rolling(window=period).mean()

# 기존 함수 유지
def long_short_ratio(long_volume, short_volume, period=14):
    return calculate_long_short_ratio(long_volume, short_volume, period)

#10. Liquidation Data: 청산 데이터 기반의 시장 스트레스 측정 지표
def calculate_liquidation_sentiment(liquidation_data, period=14):
    """Liquidation Sentiment 계산
    
    Args:
        liquidation_data: 청산 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14일)
        
    Returns:
        청산 심리 지수 (Pandas Series)
        
    Note:
        - 급증: 시장 스트레스 증가
        - 저점: 안정적 시장 상태
        - 추세: 시장 방향성 예측
    """
    return liquidation_data.rolling(window=period).mean()

# 기존 함수 유지
def liquidation_sentiment(liquidation_data, period=14):
    return calculate_liquidation_sentiment(liquidation_data, period)

#11. Exchange Flow Sentiment: 거래소 자금 흐름 기반의 투자자 심리 지표
def calculate_exchange_flow_sentiment(volume, price_change, period=14):
    """Exchange Flow Sentiment 계산
    
    Args:
        volume: 거래량 데이터 (Pandas Series)
        price_change: 가격 변화율 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14일)
        
    Returns:
        거래소 자금 흐름 지수 (Pandas Series)
        
    Note:
        - 양수: 순유입 우세
        - 음수: 순유출 우세
        - 극단값: 강한 자금 이동
    """
    flow = volume * price_change
    return flow.rolling(window=period).mean()

# 기존 함수 유지
def exchange_flow_sentiment(volume, price_change, period=14):
    return calculate_exchange_flow_sentiment(volume, price_change, period)

#12. Social Engagement: 소셜 미디어 참여도 기반의 관심도 측정 지표
def calculate_social_engagement(social_data, period=14):
    """Social Engagement 계산
    
    Args:
        social_data: 소셜 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14일)
        
    Returns:
        소셜 미디어 참여도 지수 (Pandas Series)
        
    Note:
        - 상승: 관심도 증가
        - 하락: 관심도 감소
        - 급변: 중요 이벤트 발생
    """
    normalized = (social_data - social_data.rolling(period).min()) / \
                (social_data.rolling(period).max() - social_data.rolling(period).min())
    return normalized * 100

# 기존 함수 유지
def social_engagement(social_data, period=14):
    return calculate_social_engagement(social_data, period)

class SentimentIndicator:
    """감성 지표 클래스"""
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        self.data = data
        if data is not None:
            self._validate_data()
    
    def _validate_data(self) -> None:
        required = ['social_data', 'news_data', 'market_data']
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Required columns missing: {required}")
    
    def set_data(self, data: pd.DataFrame) -> None:
        self.data = data
        self._validate_data()
    
    def calculate_all(self, periods: List[int] = [7, 14, 30]) -> pd.DataFrame:
        """모든 감성 지표 계산"""
        if self.data is None:
            raise ValueError("Data not set. Use set_data() first.")
            
        results = pd.DataFrame(index=self.data.index)
        
        # 기간별 지표 계산
        for period in periods:
            results[f'fear_greed_{period}'] = fear_greed(
                self.data['volatility'],
                self.data['momentum'],
                self.data['volume'],
                self.data['dominance'],
                self.data['social_data']
            )
            
            results[f'google_trends_{period}'] = google_trends(
                self.data['search_data'],
                period
            )
            
            results[f'crypto_fear_{period}'] = crypto_fear_greed(
                self.data['volatility'],
                period
            )
            
            results[f'whale_{period}'] = whale_sentiment(
                self.data['volume'],
                self.data['price_change'],
                period
            )
            
            results[f'funding_{period}'] = funding_sentiment(
                self.data['funding_rate'],
                period
            )
            
            results[f'long_short_{period}'] = long_short_ratio(
                self.data['long_volume'],
                self.data['short_volume'],
                period
            )
            
            results[f'liquidation_{period}'] = liquidation_sentiment(
                self.data['liquidation_data'],
                period
            )
            
            results[f'exchange_flow_{period}'] = exchange_flow_sentiment(
                self.data['volume'],
                self.data['price_change'],
                period
            )
            
            results[f'social_engagement_{period}'] = social_engagement(
                self.data['social_data'],
                period
            )
        
        # 고정 지표 계산
        results['social_sentiment'] = social_sentiment(
            self.data['social_texts']
        )
        
        results['news_sentiment'] = news_sentiment(
            self.data['news_headlines'],
            self.data['news_contents']
        )
        
        results['options_sentiment'] = options_sentiment(
            self.data['put_volume'],
            self.data['call_volume']
        )
        
        return results
