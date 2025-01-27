
'''
7. 복합 지표 (Composite Indicators)
정의
복합 지표는 여러 데이터를 결합하여 시장 전반을 종합적으로 평가하는 고급 지표입니다.
목적
•	다차원적 분석
•	추세, 모멘텀, 변동성을 통합적으로 평가
•   실시간 및 백테스트를 위한 거래량 기반 데이터 반환
지표 목록 (7개)
'''

#1. ZigZag Indicator: 주요 가격 움직임을 단순화하여 분석.
def zigzag(high, low, percentage=5):
    """
    ZigZag Indicator 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param percentage: 변경 기준 비율 (기본값: 5%)
    :return: ZigZag 라인 (Pandas Series)
    """
    zigzag_line = pd.Series(index=high.index, dtype='float64')
    prev_high, prev_low = high.iloc[0], low.iloc[0]
    for i in range(1, len(high)):
        change = (high.iloc[i] - prev_high) / prev_high * 100 if high.iloc[i] > prev_high else \
                 (prev_low - low.iloc[i]) / prev_low * 100
        if abs(change) >= percentage:
            zigzag_line.iloc[i] = high.iloc[i] if high.iloc[i] > prev_high else low.iloc[i]
            prev_high, prev_low = high.iloc[i], low.iloc[i]
    return zigzag_line

#2. Fractal Indicator: 가격의 반복적 패턴을 감지.
def fractal_indicator(high, low, period=5):
    """
    Fractal Indicator 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param period: Fractal 계산 기간 (기본값 5)
    :return: 고가 Fractal, 저가 Fractal (Pandas Series)
    """
    high_fractal = high[(high.shift(2) < high) & (high.shift(1) < high) & 
                        (high.shift(-1) < high) & (high.shift(-2) < high)]
    
    low_fractal = low[(low.shift(2) > low) & (low.shift(1) > low) & 
                      (low.shift(-1) > low) & (low.shift(-2) > low)]
    
    return high_fractal, low_fractal  # 고가 및 저가 Fractal 반환

#3. Pivot Points: 가격 지지와 저항 수준 계산.
def pivot_points(high, low, close):
    """
    Pivot Points 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param close: 종가 데이터 (Pandas Series)
    :return: Pivot Points, 지지선 및 저항선 (Pandas Series)
    """
    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    r2 = pivot + (high - low)
    s1 = (2 * pivot) - high
    s2 = pivot - (high - low)
    return pivot, r1, r2, s1, s2

#4. Schaff Trend Cycle (STC): MACD 기반 추가 필터링 제공.
def stc(close, short_period=23, long_period=50, cycle_period=10):
    """
    STC (Schaff Trend Cycle) 계산
    :param close: 종가 데이터 (Pandas Series)
    :param short_period: 단기 EMA 기간 (기본값: 23)
    :param long_period: 장기 EMA 기간 (기본값: 50)
    :param cycle_period: 주기 기간 (기본값: 10)
    :return: STC 값 (Pandas Series)
    """
    macd_line = ema(close, short_period) - ema(close, long_period)
    stc = stochastic_oscillator(macd_line, macd_line, macd_line, cycle_period)
    return stc

#5. KST Oscillator (Know Sure Thing): 여러 ROC의 조합.
def kst(data, r1=10, r2=15, r3=20, r4=30, sma1=10, sma2=10, sma3=10, sma4=15):
    """
    KST (Know Sure Thing) Oscillator 계산
    :param data: 가격 데이터 (Pandas Series)
    :param r1, r2, r3, r4: ROC 계산 기간
    :param sma1, sma2, sma3, sma4: ROC 단순 이동평균 기간
    :return: KST 값 (Pandas Series)
    """
    roc1 = data.diff(r1) / data.shift(r1)
    roc2 = data.diff(r2) / data.shift(r2)
    roc3 = data.diff(r3) / data.shift(r3)
    roc4 = data.diff(r4) / data.shift(r4)

    kst = (roc1.rolling(sma1).mean() +
           roc2.rolling(sma2).mean() * 2 +
           roc3.rolling(sma3).mean() * 3 +
           roc4.rolling(sma4).mean() * 4)
    return kst  # KST 값 반환

#6. Arnaud Legoux Moving Average (ALMA): 노이즈를 줄이며 추세를 매끄럽게.
def alma(close, period=10, sigma=6, offset=0.85):
    """
    ALMA (Arnaud Legoux Moving Average) 계산
    :param close: 종가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 10일)
    :param sigma: 곡선 평활도 (기본값: 6)
    :param offset: 중심 오프셋 (기본값: 0.85)
    :return: ALMA 값 (Pandas Series)
    """
    m = int(offset * (period - 1))
    weights = np.exp(-0.5 * ((np.arange(period) - m) / sigma) ** 2)
    weights /= weights.sum()
    alma = close.rolling(window=period).apply(lambda x: np.dot(x, weights), raw=True)
    return alma

#7. Connors RSI: RSI와 추가적인 요소를 결합하여 신호 생성.
def connors_rsi(close, rsi_period=3, streak_period=2, percent_rank_period=100):
    """
    Connors RSI 계산
    :param close: 종가 데이터 (Pandas Series)
    :param rsi_period: RSI 계산 기간
    :param streak_period: 상승/하락 연속 기간 계산
    :param percent_rank_period: Percent Rank 계산 기간
    :return: Connors RSI 값 (Pandas Series)
    """
    # 기본 RSI 계산
    basic_rsi = rsi(close, period=rsi_period)
    # 상승/하락 연속 기간 계산
    streak = close.diff().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0)).rolling(window=streak_period).sum()
    streak_rsi = rsi(streak, period=rsi_period)
    # Percent Rank 계산
    percent_rank = close.rolling(window=percent_rank_period).apply(lambda x: (x.rank(pct=True).iloc[-1] * 100), raw=True)
    # Connors RSI
    connors_rsi_value = (basic_rsi + streak_rsi + percent_rank) / 3
    return connors_rsi_value

