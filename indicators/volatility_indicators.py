'''
3. 변동성 지표 (Volatility Indicators)
정의
변동성 지표는 가격의 변동성을 측정하며, 시장의 위험성과 안정성을 평가합니다. 가격 움직임이 클수록 변동성이 높으며, 이는 시장의 불확실성을 반영합니다.
목적
•	시장 위험성 평가
•	매매 시점 식별
•	추세 강도 보조
지표 목록 (9개)
'''
#1.	ATR (Average True Range): 변동폭의 평균값.
def atr(high, low, close, period=14):
    """
    ATR (Average True Range) 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param close: 종가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 14일)
    :return: ATR 값 (Pandas Series)
    """
    # True Range 계산
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    # ATR 계산
    atr = true_range.rolling(window=period).mean()
    return atr

#2.	Standard Deviation: 가격의 표준편차 측정.
def std_deviation(close, period=14):
    """
    Standard Deviation 계산
    :param close: 종가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 14일)
    :return: Standard Deviation 값 (Pandas Series)
    """
    return close.rolling(window=period).std()

#3. Choppiness Index: 시장의 추세적 특성을 평가.
def choppiness_index(high, low, close, period=14):
    """
    Choppiness Index 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param close: 종가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 14일)
    :return: Choppiness Index 값 (Pandas Series)
    """
    true_range = atr(high, low, close, period=1)  # 일일 True Range
    tr_sum = true_range.rolling(window=period).sum()
    high_low_diff = high.rolling(window=period).max() - low.rolling(window=period).min()
    choppiness = 100 * np.log10(tr_sum / high_low_diff) / np.log10(period)
    return choppiness

#4.	Historical Volatility: 과거 변동성을 연간화.
def historical_volatility(close, period=14):
    """
    Historical Volatility 계산
    :param close: 종가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 14일)
    :return: Historical Volatility 값 (Pandas Series)
    """
    log_returns = np.log(close / close.shift(1))
    return log_returns.rolling(window=period).std() * np.sqrt(252)  # 연율화

#5.	Bollinger Bandwidth: 볼린저 밴드 폭으로 변동성을 평가.
def bollinger_bandwidth(close, period=20):
    """
    Bollinger Bandwidth 계산
    :param close: 종가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 20일)
    :return: Bollinger Bandwidth 값 (Pandas Series)
    """
    sma = close.rolling(window=period).mean()
    std_dev = close.rolling(window=period).std()
    upper_band = sma + (2 * std_dev)
    lower_band = sma - (2 * std_dev)
    bandwidth = (upper_band - lower_band) / sma
    return bandwidth

#6.	Ulcer Index: 하락 위험을 평가.
def ulcer_index(close, period=14):
    """
    Ulcer Index 계산
    :param close: 종가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 14일)
    :return: Ulcer Index 값 (Pandas Series)
    """
    max_close = close.rolling(window=period).max()
    percent_drawdown = ((close - max_close) / max_close) ** 2
    ulcer_index = np.sqrt(percent_drawdown.rolling(window=period).mean())
    return ulcer_index

#7.	Chaikin Volatility: 고가와 저가의 차이를 이용.
def chaikin_volatility(high, low, period=14):
    """
    Chaikin Volatility 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 14일)
    :return: Chaikin Volatility 값 (Pandas Series)
    """
    hl_diff = high - low
    hl_ema = hl_diff.ewm(span=period, adjust=False).mean()
    chaikin_volatility = ((hl_ema - hl_ema.shift(period)) / hl_ema.shift(period)) * 100
    return chaikin_volatility

#8.	Donchian Channel: 고가/저가 범위를 기반으로 변동성 평가.
def donchian_channel(high, low, period=20):
    """
    Donchian Channel 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 20일)
    :return: 상단 밴드, 하단 밴드 (튜플 형태)
    """
    upper_band = high.rolling(window=period).max()
    lower_band = low.rolling(window=period).min()
    return upper_band, lower_band

#9.	Keltner Channel: 평균 가격과 ATR을 결합한 채널
def keltner_channel(high, low, close, period=20, multiplier=2):
    """
    Keltner Channel 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param close: 종가 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 20일)
    :param multiplier: ATR에 곱할 배수 (기본값: 2)
    :return: 상단 밴드, 중앙 밴드, 하단 밴드 (튜플 형태)
    """
    atr_value = atr(high, low, close, period)
    middle_band = close.rolling(window=period).mean()
    upper_band = middle_band + (multiplier * atr_value)
    lower_band = middle_band - (multiplier * atr_value)
    return upper_band, middle_band, lower_band

