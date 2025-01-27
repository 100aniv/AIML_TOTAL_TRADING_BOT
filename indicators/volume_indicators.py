'''
1. 거래량 지표 (Volume Indicators)
정의
거래량 데이터는 시장의 강도와 활동성을 측정하는 핵심 자료입니다. 거래량 지표는 가격 변화의 신뢰성을 평가하고, 시장 참여자의 의도를 반영합니다. 거래량이 상승 또는 하락할 때, 그 움직임이 시장 심리나 추세와 일치하는지 확인할 수 있습니다.
목적
•	추세 지속 여부 확인
•	시장 강도 평가
•	거래 타이밍 식별
지표 목록 (8개)
'''

#1. OBV (On-Balance Volume): 거래량의 누적 합계를 기반으로 추세 분석.
def obv(close, volume):
    """
    OBV (On-Balance Volume) 계산
    :param close: 종가 데이터 (Pandas Series)
    :param volume: 거래량 데이터 (Pandas Series)
    :return: OBV 값 (Pandas Series)
    """
    # OBV 계산: 가격 상승/하락에 따라 거래량 가중
    return volume.where(close.diff() > 0, -volume).cumsum()

#2. VWAP (Volume Weighted Average Price): 거래량에 가중치를 둔 평균 가격.
def vwap(high, low, close, volume):
    """
    VWAP (Volume Weighted Average Price) 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param close: 종가 데이터 (Pandas Series)
    :param volume: 거래량 데이터 (Pandas Series)
    :return: VWAP 값 (Pandas Series)
    """
    # Typical Price 계산
    typical_price = (high + low + close) / 3
    # VWAP 계산: 가중 평균
    return (typical_price * volume).cumsum() / volume.cumsum()

#3. A/D 라인 (Accumulation/Distribution Line): 거래량과 가격 움직임을 종합.
def ad_line(high, low, close, volume):
    """
    A/D 라인 (Accumulation/Distribution Line) 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param close: 종가 데이터 (Pandas Series)
    :param volume: 거래량 데이터 (Pandas Series)
    :return: A/D 라인 값 (Pandas Series)
    """
    # Money Flow Multiplier 계산
    mfm = ((close - low) - (high - close)) / (high - low)
    # Money Flow Volume 계산
    mf_volume = mfm * volume
    # A/D 라인 누적합 계산
    return mf_volume.cumsum()

#4. Chaikin Money Flow (CMF): 시장 강도를 측정.
def chaikin_money_flow(high, low, close, volume, period=20):
    """
    Chaikin Money Flow (CMF) 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param close: 종가 데이터 (Pandas Series)
    :param volume: 거래량 데이터 (Pandas Series)
    :param period: 계산 기간
    :return: CMF 값 (Pandas Series)
    """
    # Money Flow Multiplier 계산
    mfm = ((close - low) - (high - close)) / (high - low)
    # Money Flow Volume 계산
    mf_volume = mfm * volume
    # CMF 계산
    return mf_volume.rolling(window=period).sum() / volume.rolling(window=period).sum()

#5. Ease of Movement (EOM): 가격 이동의 용이성을 거래량과 함께 분석.
def ease_of_movement(high, low, volume, period=14):
    """
    Ease of Movement (EOM) 계산
    :param high: 고가 데이터 (Pandas Series)
    :param low: 저가 데이터 (Pandas Series)
    :param volume: 거래량 데이터 (Pandas Series)
    :param period: 계산 기간
    :return: EOM 값 (Pandas Series)
    """
    # 중간점 변화 계산
    mid_point_move = ((high + low) / 2).diff()
    # 가격 변화 대비 거래량 계산
    box_ratio = volume / (high - low)
    eom = mid_point_move / box_ratio
    # 이동평균 적용
    return eom.rolling(window=period).mean()

#6. Volume Price Trend (VPT): 거래량과 가격 변화의 관계를 측정.
def volume_price_trend(close, volume):
    """
    Volume Price Trend (VPT) 계산
    :param close: 종가 데이터 (Pandas Series)
    :param volume: 거래량 데이터 (Pandas Series)
    :return: VPT 값 (Pandas Series)
    """
    # VPT 계산: 가격 변화율에 거래량 가중
    return ((close.diff() / close.shift(1)) * volume).cumsum()

#7. Negative/Positive Volume Index (NVI & PVI): 거래량이 적거나 많을 때의 시장 반응.
def negative_volume_index(close, volume):
    """
    Negative Volume Index (NVI) 계산
    :param close: 종가 데이터 (Pandas Series)
    :param volume: 거래량 데이터 (Pandas Series)
    :return: NVI 값 (Pandas Series)
    """
    nvi = pd.Series(1000, index=close.index)  # 초기값 설정
    for i in range(1, len(close)):
        if volume[i] < volume[i - 1]:
            nvi[i] = nvi[i - 1] + (close[i] - close[i - 1]) / close[i - 1] * nvi[i - 1]
        else:
            nvi[i] = nvi[i - 1]
    return nvi

def positive_volume_index(close, volume):
    """
    Positive Volume Index (PVI) 계산
    :param close: 종가 데이터 (Pandas Series)
    :param volume: 거래량 데이터 (Pandas Series)
    :return: PVI 값 (Pandas Series)
    """
    pvi = pd.Series(1000, index=close.index)  # 초기값 설정
    for i in range(1, len(close)):
        if volume[i] > volume[i - 1]:
            pvi[i] = pvi[i - 1] + (close[i] - close[i - 1]) / close[i - 1] * pvi[i - 1]
        else:
            pvi[i] = pvi[i - 1]
    return pvi

#8. Percentage Volume Oscillator (PVO): 단기/장기 거래량 이동평균선 차이를 기반으로 시장 강도 분석.
def percentage_volume_oscillator(volume, short_period=12, long_period=26, signal_period=9):
    """
    Percentage Volume Oscillator (PVO) 계산
    :param volume: 거래량 데이터 (Pandas Series)
    :param short_period: 단기 EMA 기간
    :param long_period: 장기 EMA 기간
    :param signal_period: 시그널 EMA 기간
    :return: PVO 라인, 시그널 라인 (Pandas Series)
    """
    short_ema = volume.ewm(span=short_period, adjust=False).mean()
    long_ema = volume.ewm(span=long_period, adjust=False).mean()
    pvo_line = ((short_ema - long_ema) / long_ema) * 100
    signal_line = pvo_line.ewm(span=signal_period, adjust=False).mean()
    return pvo_line, signal_line
