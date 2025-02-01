'''
2. 거래량 지표 (Volume Indicators)

정의
거래량과 가격의 관계를 분석하여 시장의 강도와 참여도를 측정하는 지표들입니다.

목적
• 거래량 기반 추세 확인
• 가격 움직임의 신뢰도 평가
• 시장 참여도 측정
• 자금 흐름 분석
• 매매 시점 결정

지표 목록 (22개)
1. VROC (Volume Rate of Change): 거래량 변화율 측정
2. OBV (On-Balance Volume): 누적 거래량으로 자금 흐름 추적
3. A/D (Accumulation/Distribution): 가격과 거래량의 관계를 통한 자금 흐름 분석
4. CMF (Chaikin Money Flow): 거래량 가중 자금 흐름 측정
5. MFI (Money Flow Index): 가격과 거래량 기반 과매수/과매도 분석
6. VPT (Volume Price Trend): 가격 변화와 거래량의 상관관계 분석
7. NVI (Negative Volume Index): 거래량 감소 시의 가격 변화 분석
8. PVI (Positive Volume Index): 거래량 증가 시의 가격 변화 분석
9. PVT (Price Volume Trend): 가격 변동폭과 거래량의 관계 분석
10. VWMA (Volume Weighted MA): 거래량 가중 이동평균
11. A/D Line (Advance/Decline Line): 상승/하락 종목 수의 누적 차이 분석
12. FI (Force Index): 가격 변화와 거래량의 힘 측정
13. VZO (Volume Zone): 거래량 기반 오실레이터
14. KVO (Klinger Volume): 거래량과 가격 변화의 발산/수렴
15. EMV (Ease of Movement): 가격과 거래량의 움직임 용이성
16. VRSI (Volume RSI): 거래량 기반 RSI
17. VMI (Volume Momentum): 거래량 모멘텀
18. DI (Demand Index): 수요 강도 측정
19. TRIN (Trading Index): 거래량 기반 시장 강도
20. UVDR (Up/Down Volume): 상승/하락 거래량 비율
21. CV (Chaikin Volatility): 거래량 가중 변동성 측정

참고 사항
• 거래량은 가격 움직임의 신뢰도를 보여줌
• 거래량 증가는 현재 추세의 강도를 나타냄
• 거래량 감소는 추세 약화/전환 가능성을 시사

[2024.03.XX] 함수명 패턴 표준화
기존 함수명 -> 변경된 함수명:
- calculate_vroc -> vroc
- calculate_obv -> obv
- calculate_ad_line -> ad_line
- calculate_cmf -> cmf
- calculate_mfi -> mfi
- calculate_vpt -> vpt
- calculate_nvi -> nvi
- calculate_pvi -> pvi
- calculate_pvt -> pvt
- calculate_vwma -> vwma
- calculate_advance_decline -> ad_line
- calculate_mcclellan -> mcclellan_oscillator
- calculate_breadth -> market_breadth
- calculate_fi -> force_index
- calculate_vzo -> volume_zone_oscillator
- calculate_kvo -> klinger_oscillator
- calculate_efi -> elder_force_index
- calculate_vrsi -> volume_rsi
- calculate_vmi -> volume_momentum
- calculate_di -> demand_index
- calculate_trin -> arms_index
- calculate_udvr -> updown_volume_ratio

주요 변경사항 [2024.03.XX]
1. 지표 추가: Chaikin Volatility (CV)
2. 함수명 패턴 표준화
3. 문서화 형식 통일
'''

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Union, List, Optional

#1. Volume Rate of Change (VROC): 거래량 변화율 측정
def vroc(volume: pd.Series, period: int = 14) -> pd.Series:
    """VROC (Volume Rate of Change) 계산
    
    Args:
        volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        VROC 값 (백분율)
        
    Note:
        - 양수: 거래량 증가
        - 음수: 거래량 감소
        - 극단값: 시장 과열/침체
    """
    return ((volume - volume.shift(period)) / volume.shift(period)) * 100

#2. On-Balance Volume (OBV): 누적 거래량으로 자금 흐름 추적
def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """OBV (On Balance Volume) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        
    Returns:
        OBV 값 (누적 합계)
        
    Note:
        - 상승: 매수 압력 우세
        - 하락: 매도 압력 우세
        - 가격과의 괴리: 추세 전환 가능성
    """
    return volume.where(close.diff() > 0, -volume).cumsum()

#3. Chaikin Money Flow (CMF): 거래량 기반 자금 흐름 측정.
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

#4. Money Flow Index (MFI): 거래량 가중 RSI.
def money_flow_index(high: pd.Series, low: pd.Series, close: pd.Series, 
                     volume: pd.Series, period: int = 14) -> pd.Series:
    """Money Flow Index (MFI) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        MFI 값 (0-100)
        
    Note:
        - 80 이상: 과매수 구간
        - 20 이하: 과매도 구간
        - 거래량 가중 RSI
    """
    # Typical Price 계산
    typical_price = (high + low + close) / 3
    # Money Flow 계산
    money_flow = typical_price * volume
    # Positive Money Flow 계산
    positive_mf = money_flow.where(typical_price > typical_price.shift(1), money_flow)
    # Negative Money Flow 계산
    negative_mf = money_flow.where(typical_price < typical_price.shift(1), money_flow)
    # Positive Money Flow 누적합 계산
    positive_mf_sum = positive_mf.rolling(window=period).sum()
    # Negative Money Flow 누적합 계산
    negative_mf_sum = negative_mf.rolling(window=period).sum()
    # Money Ratio 계산
    money_ratio = positive_mf_sum / negative_mf_sum
    # MFI 계산
    mfi = 100 - (100 / (1 + money_ratio))
    return mfi

#5. Volume Price Trend (VPT): 가격과 거래량의 누적 추세.
def volume_price_trend(close: pd.Series, volume: pd.Series) -> pd.Series:
    """Volume Price Trend (VPT) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        
    Returns:
        VPT 값 (Pandas Series)
        
    Note:
        - 가격 변화율에 거래량 가중
        - 누적 추세 분석에 활용
        - 주가와의 괴리 발생시 추세 전환 가능성
    """
    # VPT 계산: 가격 변화율에 거래량 가중
    return ((close.diff() / close.shift(1)) * volume).cumsum()

#6. Negative Volume Index (NVI): 거래량 감소 시의 가격 변화.
def negative_volume_index(close: pd.Series, volume: pd.Series) -> pd.Series:
    """Negative Volume Index (NVI) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        
    Returns:
        NVI 값 (Pandas Series)
        
    Note:
        - 거래량 감소 시 가격 변화 반영
        - 거래량 증가 시 이전 값 유지
        - 스마트머니 추적에 활용
    """
    nvi = pd.Series(1000, index=close.index)  # 초기값 설정
    for i in range(1, len(close)):
        if volume[i] < volume[i - 1]:
            nvi[i] = nvi[i - 1] + (close[i] - close[i - 1]) / close[i - 1] * nvi[i - 1]
        else:
            nvi[i] = nvi[i - 1]
    return nvi

#7. Positive Volume Index (PVI): 거래량 증가 시의 가격 변화.
def positive_volume_index(close: pd.Series, volume: pd.Series) -> pd.Series:
    """Positive Volume Index (PVI) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        
    Returns:
        PVI 값 (Pandas Series)
        
    Note:
        - 거래량 증가 시 가격 변화 반영
        - 거래량 감소 시 이전 값 유지
        - 추세 강도 측정에 활용
    """
    pvi = pd.Series(1000, index=close.index)  # 초기값 설정
    for i in range(1, len(close)):
        if volume[i] > volume[i - 1]:
            pvi[i] = pvi[i - 1] + (close[i] - close[i - 1]) / close[i - 1] * pvi[i - 1]
        else:
            pvi[i] = pvi[i - 1]
    return pvi

#8. Accumulation/Distribution Index (ADI): 가격 위치와 거래량 관계.
def accumulation_distribution_index(high: pd.Series, low: pd.Series, 
                                   close: pd.Series, volume: pd.Series) -> pd.Series:
    """Accumulation/Distribution Index (ADI) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        
    Returns:
        ADI 값 (Pandas Series)
        
    Note:
        - 가격 위치와 거래량의 관계 분석
        - 누적 자금 흐름 측정
        - 가격과의 괴리 발생시 추세 전환 가능성
    """
    # Money Flow Multiplier 계산
    mfm = ((close - low) - (high - close)) / (high - low)
    # Money Flow Volume 계산
    mf_volume = mfm * volume
    # ADI 누적합 계산
    return mf_volume.cumsum()

#9. Ease of Movement (EOM): 가격 변동의 용이성 측정.
def ease_of_movement(high: pd.Series, low: pd.Series, 
                     volume: pd.Series, period: int = 14) -> pd.Series:
    """Ease of Movement (EOM) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        EOM 값 (Pandas Series)
        
    Note:
        - 양수: 가격 상승 용이
        - 음수: 가격 하락 용이
        - 거래량 대비 가격 변동의 효율성 측정
    """
    # 중간점 변화 계산
    mid_point_move = ((high + low) / 2).diff()
    # 가격 변화 대비 거래량 계산
    box_ratio = volume / (high - low)
    eom = mid_point_move / box_ratio
    # 이동평균 적용
    return eom.rolling(window=period).mean()

#10. Volume Weighted Moving Average (VWMA): 거래량 가중 이동평균.
def volume_weighted_moving_average(close: pd.Series, volume: pd.Series, 
                                  period: int = 14) -> pd.Series:
    """Volume Weighted Moving Average (VWMA) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        VWMA 값 (Pandas Series)
        
    Note:
        - 거래량으로 가중된 이동평균
        - 거래량이 많은 가격에 더 큰 가중치
        - 가격 지지/저항 레벨 식별에 활용
    """
    # VWMA 계산: 가중 이동평균
    return (close * volume).rolling(window=period).sum() / volume.rolling(window=period).sum()

#11. Advance-Decline Line (AD Line): 상승/하락 종목 수의 누적 차이 분석
def ad_line(advances: pd.Series, declines: pd.Series) -> pd.Series:
    """Advance-Decline Line 계산

    Args:
        advances: 상승 종목 수 (Pandas Series)
        declines: 하락 종목 수 (Pandas Series)

    Returns:
        A/D Line 값 (누적 합계)

    Note:
        - 상승: 시장 전반적 강세
        - 하락: 시장 전반적 약세
        - 주가와의 괴리: 추세 전환 가능성
    """
    ad_diff = advances - declines
    return ad_diff.cumsum()

#13. FI (Force Index): 가격 변화와 거래량의 힘 측정
def force_index(close: pd.Series, volume: pd.Series, period: int = 13) -> pd.Series:
    """Force Index 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 13)
        
    Returns:
        Force Index 값 (Pandas Series)
        
    Note:
        - 양수: 매수 압력 우세
        - 음수: 매도 압력 우세
        - 극단값: 추세 전환 가능성
    """
    return (close.diff(period) * volume.diff(period)).rolling(window=period).mean()

#14. VZO (Volume Zone): 거래량 기반 오실레이터
def vzo(close=None, volume=None, period: int = 14) -> pd.Series:
    """Volume Zone Oscillator 계산
    
    Args:
        close: 종가 데이터 (선택사항)
        volume: 거래량 데이터 (선택사항)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        VZO 값 (-100 ~ 100)
        
    Note:
        - 60 이상: 과매수 구간
        - -60 이하: 과매도 구간
        - 0선 교차: 추세 전환 신호
    """
    if close is None:
        close = self.data['close']
    if volume is None:
        volume = self.data['volume']
    price_up = (close > close.shift(1)).astype(int)
    vol_ma = volume.rolling(window=period).mean()
    up_vol = (volume * price_up).rolling(window=period).sum()
    return ((up_vol - (vol_ma - up_vol)) / vol_ma) * 100

#15. KVO (Klinger Volume): 거래량과 가격 변화의 발산/수렴
def kvo(high: pd.Series, low: pd.Series, close: pd.Series, 
        volume: pd.Series, short_period: int = 34, long_period: int = 55) -> pd.Series:
    """Klinger Volume Oscillator 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        short_period: 단기 기간 (기본값: 34)
        long_period: 장기 기간 (기본값: 55)
        
    Returns:
        KVO 값
        
    Note:
        - 양수: 매수 압력 우세
        - 음수: 매도 압력 우세
        - 시그널선 교차: 매매 신호
    """
    trend = (high + low + close).diff().ewm(span=short_period).mean()
    volume_force = volume * abs(trend)
    short_ema = volume_force.ewm(span=short_period).mean()
    long_ema = volume_force.ewm(span=long_period).mean()
    return short_ema - long_ema

#16. EMV (Ease of Movement): 가격과 거래량의 움직임 용이성
def emv(high: Optional[pd.Series] = None, 
        low: Optional[pd.Series] = None,
        volume: Optional[pd.Series] = None, 
        period: int = 14) -> pd.Series:
    """Ease of Movement 계산
    
    Args:
        high: 고가 데이터 (선택사항)
        low: 저가 데이터 (선택사항)
        volume: 거래량 데이터 (선택사항)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        EMV 값
        
    Note:
        - 양수: 상승 용이
        - 음수: 하락 용이
        - 0선 교차: 추세 전환 가능성
    """
    if high is None:
        high = self.data['high']
    if low is None:
        low = self.data['low']
    if volume is None:
        volume = self.data['volume']
    distance = ((high + low) / 2) - ((high.shift(1) + low.shift(1)) / 2)
    box_ratio = volume / (high - low)
    emv = distance / box_ratio
    return emv.rolling(window=period).mean()

#17. VRSI (Volume RSI): 거래량 기반 RSI
def vrsi(volume: pd.Series, period: int = 14) -> pd.Series:
    """Volume RSI 계산
    
    Args:
        volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        VRSI 값 (0-100)
        
    Note:
        - 70 이상: 과매수 구간
        - 30 이하: 과매도 구간
        - 중간값: 50
    """
    vol_change = volume.diff()
    gain = vol_change.where(vol_change > 0, 0)
    loss = -vol_change.where(vol_change < 0, 0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

#18. VMI (Volume Momentum): 거래량 모멘텀
def vmi(volume: pd.Series, period: int = 14) -> pd.Series:
    """Volume Momentum Index 계산
    
    Args:
        volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        VMI 값
        
    Note:
        - 양수: 거래량 증가 추세
        - 음수: 거래량 감소 추세
        - 극단값: 추세 전환 가능성
    """
    return ((volume - volume.shift(period)) / volume.shift(period)) * 100

#19. DI (Demand Index): 수요 강도 측정
def di(high: pd.Series, low: pd.Series, close: pd.Series, 
       volume: pd.Series, period: int = 13) -> pd.Series:
    """Demand Index 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 13)
        
    Returns:
        DI 값
        
    Note:
        - 양수: 매수 수요 강함
        - 음수: 매도 수요 강함
        - 극단값: 추세 전환 가능성
    """
    price_range = high - low
    buying_pressure = close - low
    selling_pressure = high - close
    
    demand_ratio = (buying_pressure / price_range) * volume
    supply_ratio = (selling_pressure / price_range) * volume
    
    return (demand_ratio.rolling(window=period).mean() - 
            supply_ratio.rolling(window=period).mean())

#20. TRIN (Trading Index): 거래량 기반 시장 강도
def trin(advances: pd.Series, declines: pd.Series, 
         advance_volume: pd.Series, decline_volume: pd.Series) -> pd.Series:
    """Trading Index (ARMS Index) 계산
    
    Args:
        advances: 상승 종목 수 (Pandas Series)
        declines: 하락 종목 수 (Pandas Series)
        advance_volume: 상승 종목 거래량 (Pandas Series)
        decline_volume: 하락 종목 거래량 (Pandas Series)
        
    Returns:
        TRIN 값
        
    Note:
        - 1 미만: 상승 추세 강도 높음
        - 1 초과: 하락 추세 강도 높음
        - 1: 중립
    """
    ad_ratio = advances / declines
    volume_ratio = advance_volume / decline_volume
    return (ad_ratio / volume_ratio)

#21. UVDR (Up/Down Volume): 상승/하락 거래량 비율
def uvdr(close: pd.Series, volume: pd.Series, period: int = 14) -> pd.Series:
    """Up/Down Volume Ratio 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        UVDR 값
        
    Note:
        - 1 초과: 상승 거래량 우세
        - 1 미만: 하락 거래량 우세
        - 1: 중립
    """
    up_volume = volume.where(close > close.shift(1), 0)
    down_volume = volume.where(close < close.shift(1), 0)
    
    up_sum = up_volume.rolling(window=period).sum()
    down_sum = down_volume.rolling(window=period).sum()
    
    return up_sum / down_sum

#22. CV (Chaikin Volatility): 거래량 가중 변동성 측정
def cv(high: pd.Series, low: pd.Series, period: int = 10) -> pd.Series:
    """Chaikin Volatility (CV) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 10)
        
    Returns:
        CV 값 (Pandas Series)
        
    Note:
        - 양수: 변동성 증가
        - 음수: 변동성 감소
        - 극단값: 추세 전환 가능성
    """
    hl_diff = high - low
    hl_ema = hl_diff.ewm(span=period, adjust=False).mean()
    return ((hl_ema - hl_ema.shift(period)) / hl_ema.shift(period)) * 100

class VolumeIndicator:
    """거래량 지표 클래스
    
    모든 거래량 지표를 계산하고 관리하는 클래스입니다.
    """
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        """거래량 지표 클래스 초기화
        
        Args:
            data: OHLCV 데이터프레임 (선택사항)
                필수 컬럼: high, low, close, volume
        
        Note:
            - 데이터가 주어지면 자동으로 유효성 검증 수행
            - 데이터는 나중에 set_data()로도 설정 가능
        """
        self.data = data
        if data is not None:
            self._validate_data()

    def _validate_data(self) -> None:
        """데이터 유효성 검증
        
        Args:
            None
            
        Returns:
            None
            
        Note:
            - 필수 컬럼 존재 여부 확인
            - 데이터 타입 및 무결성 검증
        """
        required = ['high', 'low', 'close', 'volume']
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Required columns missing: {required}")

    def obv(self, close: Optional[pd.Series] = None, 
            volume: Optional[pd.Series] = None) -> pd.Series:
        """OBV (On-Balance Volume) 계산
        
        Args:
            close: 종가 데이터 (선택사항)
            volume: 거래량 데이터 (선택사항)
            
        Returns:
            OBV 값 (Pandas Series)
            
        Note:
            - 데이터 미입력시 클래스 초기화 데이터 사용
            - 누적 거래량으로 자금 흐름 추적
        """
        if close is None:
            close = self.data['close']
        if volume is None:
            volume = self.data['volume']
        return obv(close, volume)

    def vwap(self, high=None, low=None, close=None, volume=None):
        """VWAP (Volume Weighted Average Price) 계산"""
        if high is None:
            high = self.data['high']
        if low is None:
            low = self.data['low']
        if close is None:
            close = self.data['close']
        if volume is None:
            volume = self.data['volume']
        return vwap(high, low, close, volume)

    def cmf(self, high=None, low=None, close=None, volume=None, period=20):
        """Chaikin Money Flow (CMF) 계산"""
        if high is None:
            high = self.data['high']
        if low is None:
            low = self.data['low']
        if close is None:
            close = self.data['close']
        if volume is None:
            volume = self.data['volume']
        return chaikin_money_flow(high, low, close, volume, period)

    def mfi(self, high=None, low=None, close=None, volume=None, period=14):
        """Money Flow Index (MFI) 계산"""
        if high is None:
            high = self.data['high']
        if low is None:
            low = self.data['low']
        if close is None:
            close = self.data['close']
        if volume is None:
            volume = self.data['volume']
        return money_flow_index(high, low, close, volume, period)

    def vpt(self, close=None, volume=None):
        """Volume Price Trend (VPT) 계산"""
        if close is None:
            close = self.data['close']
        if volume is None:
            volume = self.data['volume']
        return volume_price_trend(close, volume)

    def nvi(self, close=None, volume=None):
        """Negative Volume Index (NVI) 계산"""
        if close is None:
            close = self.data['close']
        if volume is None:
            volume = self.data['volume']
        return negative_volume_index(close, volume)

    def pvi(self, close=None, volume=None):
        """Positive Volume Index (PVI) 계산"""
        if close is None:
            close = self.data['close']
        if volume is None:
            volume = self.data['volume']
        return positive_volume_index(close, volume)

    def adi(self, high=None, low=None, close=None, volume=None):
        """Accumulation/Distribution Index (ADI) 계산"""
        if high is None:
            high = self.data['high']
        if low is None:
            low = self.data['low']
        if close is None:
            close = self.data['close']
        if volume is None:
            volume = self.data['volume']
        return accumulation_distribution_index(high, low, close, volume)

    def eom(self, high=None, low=None, volume=None, period=14):
        """Ease of Movement (EOM) 계산"""
        if high is None:
            high = self.data['high']
        if low is None:
            low = self.data['low']
        if volume is None:
            volume = self.data['volume']
        return ease_of_movement(high, low, volume, period)

    def vwma(self, close=None, volume=None, period=14):
        """Volume Weighted Moving Average (VWMA) 계산"""
        if close is None:
            close = self.data['close']
        if volume is None:
            volume = self.data['volume']
        return volume_weighted_moving_average(close, volume, period)

    def ad_line(self, advances: pd.Series, declines: pd.Series):
        """Advance-Decline Line 계산"""
        return ad_line(advances, declines)

    def vzo(self, close=None, volume=None, period: int = 14) -> pd.Series:
        """Volume Zone Oscillator 계산"""
        if close is None:
            close = self.data['close']
        if volume is None:
            volume = self.data['volume']
        return vzo(close, volume, period)

    def kvo(self, high: Optional[pd.Series] = None, 
            low: Optional[pd.Series] = None,
            close: Optional[pd.Series] = None, 
            volume: Optional[pd.Series] = None,
            short_period: int = 34, 
            long_period: int = 55) -> pd.Series:
        """Klinger Volume Oscillator 계산"""
        if high is None:
            high = self.data['high']
        if low is None:
            low = self.data['low']
        if close is None:
            close = self.data['close']
        if volume is None:
            volume = self.data['volume']
        return kvo(high, low, close, volume, short_period, long_period)

    def emv(self, high: Optional[pd.Series] = None, 
            low: Optional[pd.Series] = None,
            volume: Optional[pd.Series] = None, 
            period: int = 14) -> pd.Series:
        """Ease of Movement 계산"""
        if high is None:
            high = self.data['high']
        if low is None:
            low = self.data['low']
        if volume is None:
            volume = self.data['volume']
        return emv(high, low, volume, period)

    def vrsi(self, volume: pd.Series, period: int = 14) -> pd.Series:
        """Volume RSI 계산"""
        return vrsi(volume, period)

    def vmi(self, volume: pd.Series, period: int = 14) -> pd.Series:
        """Volume Momentum Index 계산"""
        return vmi(volume, period)

    def di(self, high: pd.Series, low: pd.Series, close: pd.Series, 
           volume: pd.Series, period: int = 13) -> pd.Series:
        """Demand Index 계산"""
        return di(high, low, close, volume, period)

    def trin(self, advances: pd.Series, declines: pd.Series, 
             advance_volume: pd.Series, decline_volume: pd.Series) -> pd.Series:
        """Trading Index (ARMS Index) 계산"""
        return trin(advances, declines, advance_volume, decline_volume)

    def uvdr(self, close: pd.Series, volume: pd.Series, period: int = 14) -> pd.Series:
        """Up/Down Volume Ratio 계산"""
        return uvdr(close, volume, period)

    def cv(self, high: Optional[pd.Series] = None, 
           low: Optional[pd.Series] = None, 
           period: int = 10) -> pd.Series:
        """Chaikin Volatility 계산"""
        if high is None:
            high = self.data['high']
        if low is None:
            low = self.data['low']
        return cv(high, low, period)

    def calculate_all(self):
        results = pd.DataFrame(index=self.data.index)
        
        # 기존 계산 유지
        results['obv'] = obv(self.data['close'], self.data['volume'])
        results['vwap'] = vwap(self.data['close'], self.data['volume'])
        results['ad_line'] = ad_line(self.data['high'], self.data['low'], 
                                   self.data['close'], self.data['volume'])
        results['cmf'] = cmf(self.data['high'], self.data['low'],
                           self.data['close'], self.data['volume'])
        results['mfi'] = mfi(self.data['high'], self.data['low'],
                           self.data['close'], self.data['volume'])
        results['vpt'] = vpt(self.data['close'], self.data['volume'])
        results['nvi'] = nvi(self.data['close'], self.data['volume'])
        results['pvi'] = pvi(self.data['close'], self.data['volume'])
        results['pvt'] = pvt(self.data['close'], self.data['volume'])
        
        # 새로운 지표 계산 추가
        results['vzo'] = self.vzo(period=periods[0])
        results['kvo'] = self.kvo(short_period=34, long_period=55)
        results['emv'] = self.emv(period=periods[0])
        results['vrsi'] = self.vrsi(volume=self.data['volume'], period=periods[0])
        results['vmi'] = self.vmi(volume=self.data['volume'], period=periods[0])
        results['di'] = self.di(
            high=self.data['high'],
            low=self.data['low'],
            close=self.data['close'],
            volume=self.data['volume']
        )
        results['trin'] = self.trin(
            advances=self.data['advances'],
            declines=self.data['declines'],
            advance_volume=self.data['advance_volume'],
            decline_volume=self.data['decline_volume']
        )
        results['uvdr'] = self.uvdr(
            close=self.data['close'],
            volume=self.data['volume'],
            period=periods[0]
        )
        results['cv'] = self.cv()
        
        return results
