'''
5. 심리 지표 (Sentiment Indicators)
정의
심리 지표는 투자자 심리를 직접적으로 반영하며, 과매수/과매도 상태를 평가하거나 시장 심리를 수치화합니다.
목적
•	투자자 심리 측정
•	과매수/과매도 상태 평가
지표 목록 (5개)
'''
#1.	Put/Call Ratio: 풋 옵션과 콜 옵션의 거래량 비율.
def put_call_ratio(put_volume, call_volume):
    """
    Put/Call Ratio 계산
    :param put_volume: 풋 옵션 거래량 데이터 (Pandas Series)
    :param call_volume: 콜 옵션 거래량 데이터 (Pandas Series)
    :return: Put/Call Ratio 값 (Pandas Series)
    """
    return put_volume / call_volume

#2.	Bullish Percent Index(BPI): 상승 신호를 보이는 종목의 비율.
def put_call_ratio(put_volume, call_volume):
    """
    Put/Call Ratio 계산
    :param put_volume: 풋 옵션 거래량 데이터 (Pandas Series)
    :param call_volume: 콜 옵션 거래량 데이터 (Pandas Series)
    :return: Put/Call Ratio 값 (Pandas Series)
    """
    return put_volume / call_volume

#3.	Fear and Greed Index: 시장 탐욕/공포 수준 측정.
def fear_and_greed_index(volatility, volume, market_sentiment):
    """
    Fear and Greed Index 계산
    :param volatility: 변동성 데이터 (Pandas Series)
    :param volume: 거래량 데이터 (Pandas Series)
    :param market_sentiment: 시장 심리 데이터 (Pandas Series)
    :return: Fear and Greed Index 값 (Pandas Series)
    """
    # 예제: 단순 가중 평균으로 계산
    return (0.5 * volatility + 0.3 * volume + 0.2 * market_sentiment)

#4.	High-Low Index: 고점/저점 비율 측정.
def high_low_index(high, low, period=14):
    """
    High-Low Index 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 14일)
    :return: High-Low Index 값 (Pandas Series)
    """
    high_count = high.rolling(window=period).apply(lambda x: (x > x.shift(1)).sum(), raw=True)
    low_count = low.rolling(window=period).apply(lambda x: (x < x.shift(1)).sum(), raw=True)
    return high_count / (high_count + low_count)

#5.	Market Sentiment: 설문조사나 외부 데이터를 기반으로 심리 측정.
def market_sentiment(advances, declines):
    """
    Market Sentiment 계산
    :param advances: 상승 종목 수 (Pandas Series)
    :param declines: 하락 종목 수 (Pandas Series)
    :return: Market Sentiment 값 (Pandas Series)
    """
    return advances / (advances + declines)
