'''
4. 추세 지표 (Trend Indicators)
정의
추세 지표는 시장의 방향성을 측정하며, 상승 추세인지 하락 추세인지 평가합니다. 주로 추세를 따라 매매하는 전략에 사용될테야.
목적
•	시장의 장기적 방향성 평가
•	추세 반전 및 지속 여부 식별
지표 목록 (6개)
'''
#1.	SMA (Simple Moving Average): 단순 이동평균.
def sma(close, period=20):
    """
    SMA (Simple Moving Average) 계산
    :param close: 종가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 20일)
    :return: SMA 값 (Pandas Series)
    """
    return close.rolling(window=period).mean()

#2.	EMA (Exponential Moving Average): 지수 이동평균.
def ema(close, period=20):
    """
    EMA (Exponential Moving Average) 계산
    :param close: 종가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 20일)
    :return: EMA 값 (Pandas Series)
    """
    return close.ewm(span=period, adjust=False).mean()

#3.	WMA (Weighted Moving Average): 가중 이동평균.
def wma(close, period=20):
    """
    WMA (Weighted Moving Average) 계산
    :param close: 종가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 20일)
    :return: WMA 값 (Pandas Series)
    """
    weights = np.arange(1, period + 1)
    return close.rolling(window=period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

#4.	MACD (Moving Average Convergence Divergence): 이동평균 간의 관계를 분석.
def macd(close, short_period=12, long_period=26, signal_period=9):
    """
    MACD (Moving Average Convergence Divergence) 계산
    :param close: 종가 데이터 (Pandas Series)
    :param short_period: 단기 EMA 기간 (기본값: 12)
    :param long_period: 장기 EMA 기간 (기본값: 26)
    :param signal_period: 시그널 EMA 기간 (기본값: 9)
    :return: MACD 라인, 시그널 라인, 히스토그램 (Pandas Series)
    """
    short_ema = close.ewm(span=short_period, adjust=False).mean()
    long_ema = close.ewm(span=long_period, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

#5.	Ichimoku Cloud: 추세, 모멘텀, 지지/저항을 종합 분석.
def ichimoku(high, low, close, conversion_period=9, base_period=26, leading_span_b_period=52):
    """
    Ichimoku Cloud 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param close: 종가 데이터 (Pandas Series)
    :param conversion_period: 전환선 기간 (기본값: 9)
    :param base_period: 기준선 기간 (기본값: 26)
    :param leading_span_b_period: 선행 스팬 B 기간 (기본값: 52)
    :return: 전환선, 기준선, 선행 스팬 A, 선행 스팬 B (Pandas Series)
    """
    # 전환선
    conversion_line = (high.rolling(window=conversion_period).max() + low.rolling(window=conversion_period).min()) / 2
    # 기준선
    base_line = (high.rolling(window=base_period).max() + low.rolling(window=base_period).min()) / 2
    # 선행 스팬 A
    leading_span_a = ((conversion_line + base_line) / 2).shift(base_period)
    # 선행 스팬 B
    leading_span_b = ((high.rolling(window=leading_span_b_period).max() + low.rolling(window=leading_span_b_period).min()) / 2).shift(base_period)
    return conversion_line, base_line, leading_span_a, leading_span_b

#6.	Parabolic SAR: 추세 반전 지점을 예측.
def parabolic_sar(high, low, start_af=0.02, increment_af=0.02, max_af=0.2):
    """
    Parabolic SAR 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param start_af: 시작 가속 팩터 (기본값: 0.02)
    :param increment_af: 증가 가속 팩터 (기본값: 0.02)
    :param max_af: 최대 가속 팩터 (기본값: 0.2)
    :return: Parabolic SAR 값 (Pandas Series)
    """
    sar = pd.Series(index=high.index, dtype='float64')
    af = start_af
    uptrend = True
    ep = high.iloc[0] if uptrend else low.iloc[0]
    sar.iloc[0] = low.iloc[0] if uptrend else high.iloc[0]

    for i in range(1, len(high)):
        prev_sar = sar.iloc[i - 1]
        if uptrend:
            sar.iloc[i] = prev_sar + af * (ep - prev_sar)
            if high.iloc[i] > ep:
                ep = high.iloc[i]
                af = min(af + increment_af, max_af)
            if low.iloc[i] < sar.iloc[i]:
                uptrend = False
                ep = low.iloc[i]
                af = start_af
                sar.iloc[i] = ep
        else:
            sar.iloc[i] = prev_sar + af * (ep - prev_sar)
            if low.iloc[i] < ep:
                ep = low.iloc[i]
                af = min(af + increment_af, max_af)
            if high.iloc[i] > sar.iloc[i]:
                uptrend = True
                ep = high.iloc[i]
                af = start_af
                sar.iloc[i] = ep
    return sar
                    