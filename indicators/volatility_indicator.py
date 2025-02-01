'''
1. 변동성 지표 (Volatility Indicators)

정의
변동성 지표는 가격의 변동 폭과 속도를 측정하며, 시장의 불안정성과 위험을 평가합니다.

목적
• 시장 변동성 측정
• 가격 변동 범위 파악
• 위험 수준 평가
• 추세 전환점 식별
• 매매 시점 결정

지표 목록 (5개):
1. ATR (Average True Range): 실제 가격 변동폭
2. SD (Standard Deviation): 가격 변동의 통계적 분산
3. CI (Choppiness Index): 시장의 방향성/횡보성
4. HV (Historical Volatility): 과거 가격 변동성
5. UI (Ulcer Index): 하락 위험 측정
6. DC (Donchian Channel): 고가/저가 기반 채널
7. KC (Keltner Channel): ATR 기반 채널
8. BB (Bollinger Bands): 볼린저 밴드

참고 사항
• 변동성 확대는 추세 전환의 신호일 수 있음
• 변동성 수축은 큰 움직임의 전조일 수 있음
• 여러 지표를 조합하여 신뢰도 향상
'''
from typing import List, Optional, Tuple
import pandas as pd
import numpy as np

#1.	ATR (Average True Range): 변동폭의 평균값.
def atr(high: pd.Series, low: pd.Series, close: pd.Series, 
       period: int = 14) -> pd.Series:
    """Average True Range (ATR) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        ATR 값 (Pandas Series)
        
    Note:
        - 높은 값: 높은 변동성
        - 낮은 값: 낮은 변동성
        - 추세 강도 측정에 활용
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
def sd(close: pd.Series, period: int = 14) -> pd.Series:
    """Standard Deviation (SD) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        SD 값 (Pandas Series)
        
    Note:
        - 높은 값: 큰 가격 변동성
        - 낮은 값: 작은 가격 변동성
        - 추세 전환점 식별에 활용
    """
    return close.rolling(window=period).std()

#3. CI (Choppiness Index): 시장의 방향성/횡보성
def ci(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """Choppiness Index (CI) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        CI 값 (0-100)
        
    Note:
        - 100에 가까울수록: 횡보장
        - 0에 가까울수록: 추세장
        - 38.2 이하: 강한 추세 구간
    """
    true_range = atr(high, low, close, period=1)  # 일일 True Range
    tr_sum = true_range.rolling(window=period).sum()
    high_low_diff = high.rolling(window=period).max() - low.rolling(window=period).min()
    choppiness = 100 * np.log10(tr_sum / high_low_diff) / np.log10(period)
    return choppiness

#4.	Historical Volatility: 과거 변동성을 연간화.
def hv(close: pd.Series, period: int = 14) -> pd.Series:
    """Historical Volatility (HV) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        HV 값 (Pandas Series)
        
    Note:
        - 높은 값: 큰 가격 변동성
        - 낮은 값: 작은 가격 변동성
        - 연간화된 표준편차로 표현
    """
    log_returns = np.log(close / close.shift(1))
    return log_returns.rolling(window=period).std() * np.sqrt(252)  # 연율화

#5.	Ulcer Index: 하락 위험을 평가.
def ui(close: pd.Series, period: int = 14) -> pd.Series:
    """Ulcer Index (UI) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        UI 값 (Pandas Series)
        
    Note:
        - 높은 값: 큰 하락 위험
        - 낮은 값: 작은 하락 위험
        - 하락 깊이와 지속성 측정
    """
    max_close = close.rolling(window=period).max()
    percent_drawdown = ((close - max_close) / max_close) ** 2
    ulcer_index = np.sqrt(percent_drawdown.rolling(window=period).mean())
    return ulcer_index

#6. DC (Donchian Channel): 고가/저가 범위를 기반으로 변동성 평가.
def dc(high: pd.Series, low: pd.Series, period: int = 20) -> tuple:
    """Donchian Channel (DC) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 20)
        
    Returns:
        (상단선, 중간선, 하단선) (tuple of Series)
        
    Note:
        - 상단: 기간 내 최고가
        - 하단: 기간 내 최저가
        - 중간: 상단과 하단의 중간값
    """
    upper_band = high.rolling(window=period).max()
    lower_band = low.rolling(window=period).min()
    return upper_band, (upper_band + lower_band) / 2, lower_band

#7. KC (Keltner Channel): 평균 가격과 ATR을 결합한 채널
def kc(high: pd.Series, low: pd.Series, close: pd.Series, 
      period: int = 20, atr_multiplier: float = 2) -> tuple:
    """Keltner Channel (KC) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 20)
        atr_multiplier: ATR 승수 (기본값: 2)
        
    Returns:
        (상단선, 중간선, 하단선) (tuple of Series)
        
    Note:
        - 상단: EMA + ATR * multiplier
        - 하단: EMA - ATR * multiplier
        - 중간: EMA
    """
    atr_value = atr(high, low, close, period)
    middle_band = close.rolling(window=period).mean()
    upper_band = middle_band + (atr_multiplier * atr_value)
    lower_band = middle_band - (atr_multiplier * atr_value)
    return upper_band, middle_band, lower_band

#8. BB (Bollinger Bands): 볼린저 밴드
def bb(close: pd.Series, period: int = 20, num_std: int = 2) -> pd.Series:
    """Bollinger Bandwidth 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 20)
        num_std: 표준편차 승수 (기본값: 2)
        
    Returns:
        BB Width 값 (Pandas Series)
        
    Note:
        - 밴드 폭이 좁아짐: 변동성 수축
        - 밴드 폭이 넓어짐: 변동성 확장
        - 극단적으로 좁아진 후 확장: 큰 움직임 예고
    """
    sma = close.rolling(window=period).mean()
    std_dev = close.rolling(window=period).std()
    upper_band = sma + (num_std * std_dev)
    lower_band = sma - (num_std * std_dev)
    return (upper_band - lower_band) / sma

class VolatilityIndicator:
    """변동성 지표 클래스
    
    모든 변동성 지표를 계산하고 관리하는 클래스입니다.
    """
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        """변동성 지표 클래스 초기화
        
        Args:
            data: OHLCV 데이터프레임 (선택사항)
                필수 컬럼: high, low, close
        
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
        required = ['high', 'low', 'close']
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Required columns missing: {required}")

    def calculate_all(self, periods: List[int] = [14]) -> pd.DataFrame:
        """모든 변동성 지표 계산
        
        Args:
            periods: 계산에 사용할 기간 리스트 (기본값: [14])
            
        Returns:
            계산된 모든 지표가 포함된 DataFrame
            
        Note:
            - 모든 변동성 지표 포함
            - 멀티 기간 분석 지원
            - 자동으로 컬럼명 생성
        """
        results = pd.DataFrame(index=self.data.index)
        
        results['atr'] = atr(self.data['high'], self.data['low'], self.data['close'])
        results['sd'] = sd(self.data['close'])
        results['ci'] = ci(self.data['high'], self.data['low'], self.data['close'])
        results['hv'] = hv(self.data['close'])
        results['ui'] = ui(self.data['close'])
        
        upper, middle, lower = dc(self.data['high'], self.data['low'])
        results['dc_upper'] = upper
        results['dc_middle'] = middle
        results['dc_lower'] = lower
        
        upper, middle, lower = kc(self.data['high'], self.data['low'], self.data['close'])
        results['kc_upper'] = upper
        results['kc_middle'] = middle
        results['kc_lower'] = lower
        
        results['bb'] = bb(self.data['close'])
        
        return results

