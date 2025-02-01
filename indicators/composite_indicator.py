from typing import List, Optional, Tuple
import pandas as pd
import numpy as np
from .trend_indicator import sma, ema, macd
from .momentum_indicator import rsi, stochastic
from .volume_indicator import obv, vwap
from .sentiment_indicator import fear_greed_index
from .onchain_indicator import nvt_ratio, active_addresses

'''
5. 복합 지표 (Composite Indicators)

정의
복합 지표는 여러 지표를 조합하여 더 강력한 매매 신호를 생성하는 지표들입니다.

목적
• 단일 지표의 한계 극복
• 허위 신호 감소
• 매매 신호의 신뢰도 향상
• 시장 상황 종합 분석
• 리스크 관리 강화

지표 목록 (8개)
1. KST (Know Sure Thing): 장기 모멘텀 분석 - 복합 ROC 기반
2. Supertrend: 추세 추종 - ATR/가격 통합
3. TII (Trend Intensity Index): 추세 강도 - 가격/거래량 통합
4. DPO (Detrended Price Oscillator): 추세 제거 진동자 - 가격/주기 통합
5. Aroon Oscillator: 추세 방향과 강도 - 시간/가격 통합
6. Elder Ray Index: 매수/매도 압력 - EMA/고저가 통합
7. Ultimate Oscillator: 다중 시간대 모멘텀
8. Mass Index: 변동성/추세 통합

참고 사항
• 여러 시간대 분석 권장
• 보조 지표와 함께 사용
• 시장 상황별 가중치 조정

[2024.03.XX] 함수명 패턴 표준화
기존 함수명 -> 변경된 함수명:
- calculate_kst -> kst
- calculate_supertrend -> supertrend
- calculate_tii -> tii
- calculate_dpo -> dpo
- calculate_aroon -> aroon
- calculate_elder -> elder_ray
- calculate_uo -> ultimate_oscillator
- calculate_mi -> mass_index
'''

#1. BB (Bollinger Bands) 제거

#2. KST (Know Sure Thing): 장기 모멘텀 분석 - 복합 ROC 기반
def kst(close: pd.Series, period: int = 20) -> pd.Series:
    """Know Sure Thing (KST) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 20)
        
    Returns:
        KST 값 (Pandas Series)
        
    Note:
        - 복합 ROC 기반 장기 모멘텀
        - 추세 전환점 식별
        - 과매수/과매도 판단
    """
    roc1 = ((close - close.shift(10)) / close.shift(10)).rolling(10).mean()
    roc2 = ((close - close.shift(15)) / close.shift(15)).rolling(10).mean()
    roc3 = ((close - close.shift(20)) / close.shift(20)).rolling(10).mean()
    roc4 = ((close - close.shift(30)) / close.shift(30)).rolling(15).mean()
    
    kst = (roc1 * 1) + (roc2 * 2) + (roc3 * 3) + (roc4 * 4)
    return kst

#3. CMF (Chaikin Money Flow) 제거

#4. ADX (Average Directional Index) 제거

#5. Supertrend: 추세 추종 - 변동성/추세 통합
def supertrend(close: pd.Series, high: pd.Series, low: pd.Series,
                period: int = 7, multiplier: float = 3.0) -> pd.Series:
    """Supertrend 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 7)
        multiplier: 승수 (기본값: 3.0)
        
    Returns:
        Supertrend 값 (Pandas Series)
        
    Note:
        - 추세 추종 전략에 활용
        - ATR 기반 밴드 설정
        - 추세 전환점 식별
    """
    hl2 = (high + low) / 2
    atr = pd.Series(np.maximum(high - low, 
                             np.maximum(abs(high - close.shift(1)),
                                      abs(low - close.shift(1)))))
    atr = atr.rolling(window=period).mean()
    up = hl2 - (multiplier * atr)
    down = hl2 + (multiplier * atr)
    trend = pd.Series(np.where(close > up, 1, np.where(close < down, -1, 0)))
    trend = trend.rolling(window=period).mean()
    return trend

#3. TII (Trend Intensity Index): 추세 강도
def tii(close: pd.Series, volume: pd.Series, period: int = 20) -> pd.Series:
    """Trend Intensity Index (TII) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 20)
        
    Returns:
        TII 값 (Pandas Series)
        
    Note:
        - 추세의 강도 측정
        - 거래량으로 가중치 부여
        - 추세 전환점 식별
    """
    price_change = close - close.shift(1)
    volume_weighted = price_change * volume
    tii = volume_weighted.rolling(window=period).sum() / volume.rolling(window=period).sum()
    return tii * 100

#4. DPO (Detrended Price Oscillator): 추세 제거 진동자
def dpo(close: pd.Series, period: int = 20) -> pd.Series:
    """Detrended Price Oscillator (DPO) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 20)
        
    Returns:
        DPO 값 (Pandas Series)
        
    Note:
        - 추세 제거로 순수 가격 진동 분석
        - 주기적 순환 패턴 식별
        - 과매수/과매도 판단
    """
    shifted_ma = close.rolling(window=period).mean().shift(period // 2 + 1)
    return close - shifted_ma

#5. Aroon Oscillator: 추세 방향과 강도
def aroon(high: pd.Series, low: pd.Series, period: int = 25) -> pd.Series:
    """Aroon Oscillator 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 25)
        
    Returns:
        Aroon Oscillator 값 (Pandas Series)
        
    Note:
        - 추세의 방향과 강도 측정
        - 상승/하락 추세 구분
        - 횡보장 식별
    """
    high_days = pd.Series(dtype=float)
    low_days = pd.Series(dtype=float)
    
    for i in range(period, len(high)):
        high_days.iloc[i] = period - high[i-period:i+1].argmax()
        low_days.iloc[i] = period - low[i-period:i+1].argmin()
    
    aroon_up = ((period - high_days) / period) * 100
    aroon_down = ((period - low_days) / period) * 100
    return aroon_up - aroon_down

#6. Elder Ray Index: 매수/매도 압력
def elder_ray(close: pd.Series, high: pd.Series, low: pd.Series, 
             period: int = 13) -> Tuple[pd.Series, pd.Series]:
    """Elder Ray Index 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 13)
        
    Returns:
        (Bull Power, Bear Power) (tuple of Series)
        
    Note:
        - EMA 기준 강도 측정
        - 매수/매도 압력 분석
        - 다이버전스 형성 확인
    """
    ema_val = ema(close, period)
    bull_power = high - ema_val
    bear_power = low - ema_val
    return bull_power, bear_power

#7. Ultimate Oscillator: 다중 시간대 모멘텀
def ultimate_oscillator(close: pd.Series, high: pd.Series, low: pd.Series,
                        period1: int = 7, period2: int = 14, period3: int = 28) -> pd.Series:
    """Ultimate Oscillator 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        period1: 단기 기간 (기본값: 7)
        period2: 중기 기간 (기본값: 14)
        period3: 장기 기간 (기본값: 28)
        
    Returns:
        Ultimate Oscillator 값 (Pandas Series)
        
    Note:
        - 3개 시간대 통합 분석
        - 과매수/과매도 판단
        - 다이버전스 형성 확인
    """
    bp = close - pd.Series(np.minimum(low, close.shift(1)))
    tr = pd.Series(np.maximum(high - low, 
                             np.maximum(abs(high - close.shift(1)),
                                      abs(low - close.shift(1)))))
    
    avg7 = bp.rolling(period1).sum() / tr.rolling(period1).sum()
    avg14 = bp.rolling(period2).sum() / tr.rolling(period2).sum()
    avg28 = bp.rolling(period3).sum() / tr.rolling(period3).sum()
    
    return (100 * ((4 * avg7) + (2 * avg14) + avg28) / 7)

#8. Mass Index: 변동성/추세 통합
def mass_index(high: pd.Series, low: pd.Series, period: int = 25) -> pd.Series:
    """Mass Index 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 25)
        
    Returns:
        Mass Index 값 (Pandas Series)
        
    Note:
        - 변동성 확대/수축 패턴
        - 추세 반전 가능성 측정
        - 고점/저점 형성 예측
    """
    range_ema1 = (high - low).ewm(span=9, adjust=False).mean()
    range_ema2 = range_ema1.ewm(span=9, adjust=False).mean()
    mass = range_ema1 / range_ema2
    return mass.rolling(window=period).sum()

class CompositeIndicator:
    """복합 지표 클래스
    
    모든 복합 지표를 계산하고 관리하는 클래스입니다.
    """
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        """복합 지표 클래스 초기화
        
        Args:
            data: OHLCV 데이터프레임 (선택사항)
                필수 컬럼: open, high, low, close, volume
        
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
        required = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Required columns missing: {required}")

    def calculate_all(self) -> pd.DataFrame:
        """모든 복합 지표 계산
        
        Args:
            None
            
        Returns:
            계산된 모든 지표가 포함된 DataFrame
            
        Note:
            - 모든 복합 지표 포함
            - 자동으로 컬럼명 생성
        """
        results = pd.DataFrame(index=self.data.index)
        
        results['kst'] = kst(self.data['close'])
        results['supertrend'] = supertrend(self.data['close'], self.data['high'], self.data['low'])
        results['tii'] = tii(self.data['close'], self.data['volume'])
        results['dpo'] = dpo(self.data['close'])
        results['aroon'] = aroon(self.data['high'], self.data['low'])
        bull_power, bear_power = elder_ray(self.data['close'], self.data['high'], self.data['low'])
        results['elder_bull'] = bull_power
        results['elder_bear'] = bear_power
        results['ultimate'] = ultimate_oscillator(self.data['close'], self.data['high'], self.data['low'])
        results['mass_index'] = mass_index(self.data['high'], self.data['low'])
        
        return results

    def kst(self, close: pd.Series, period: int = 20) -> pd.Series:
        """Know Sure Thing (KST) 계산"""
        return kst(close, period)

    def supertrend(self, close: pd.Series, high: pd.Series, low: pd.Series,
                    period: int = 7, multiplier: float = 3.0) -> pd.Series:
        """Supertrend 계산
        
        Args:
            close: 종가 데이터 (Pandas Series)
            high: 고가 데이터 (Pandas Series)
            low: 저가 데이터 (Pandas Series)
            period: 계산 기간 (기본값: 7)
            multiplier: 승수 (기본값: 3.0)
            
        Returns:
            Supertrend 값 (Pandas Series)
            
        Note:
            - 추세 추종 전략에 활용
            - ATR 기반 밴드 설정
            - 추세 전환점 식별
        """
        return supertrend(close, high, low, period, multiplier)

