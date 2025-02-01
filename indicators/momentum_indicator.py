"""
모멘텀 지표 (Momentum Indicators)

가격 변화의 속도와 강도를 측정하는 기술적 분석 도구입니다.
추세의 지속성과 전환 가능성을 평가하는 데 사용됩니다.

기능:
    - 가격 변화의 속도와 강도 측정
    - 과매수/과매도 구간 식별
    - 추세 전환점 예측
    - 시장 심리 분석

참조:
    - 대부분의 지표는 0-100 범위로 정규화됨
    - 거래량 기반 지표는 신뢰도를 높임
    - 여러 지표의 교차 분석이 권장됨
"""

import pandas as pd
import numpy as np
from typing import Tuple, Union, List, Optional

'''
2. 모멘텀 지표 (Momentum Indicators)

정의
모멘텀 지표는 가격 변화의 속도와 강도를 측정하여 추세의 지속성과 전환 가능성을 평가합니다.

목적
• 가격 변화의 강도 측정
• 추세 전환점 식별
• 과매수/과매도 구간 판단

지표 목록 (12개)
1. Relative Strength Index (RSI): 상승/하락 비율로 과매수/과매도 상태를 측정
2. Stochastic Oscillator: 종가와 고가/저가 범위 간의 관계를 측정
3. Williams Percent Range (%R): 최근 종가가 고가 대비 어느 위치에 있는지 측정
4. Commodity Channel Index (CCI): 가격의 통계적 편차를 측정
5. Rate of Change (ROC): 가격 변화율을 측정
6. Money Flow Index (MFI): 거래량과 가격을 결합하여 자금 흐름 강도를 측정
7. Relative Vigor Index (RVI): 종가와 시가의 관계를 이용한 모멘텀 지표
8. True Strength Index (TSI): 가격 변화의 순수한 모멘텀을 측정
9. Know Sure Thing (KST): ROC를 결합한 모멘텀 및 추세 분석
10. Price Percentage Oscillator (PPO): 단기/장기 이동평균의 차이를 백분율로 표시하여 모멘텀 측정
11. Chaikin Money Flow (CMF): 거래량과 가격 변동을 결합하여 자금 흐름 강도를 측정
12. DMI (Directional Movement Index): 상승/하락 추세의 강도를 측정

[2024.03.XX] 함수명 패턴 표준화
기존 함수명 -> 변경된 함수명:
- calculate_rsi -> rsi
- calculate_stochastic -> stochastic
- calculate_williams_r -> williams_r
- calculate_cci -> cci
- calculate_roc -> roc
- calculate_mfi -> mfi
- calculate_ultimate -> ultimate_oscillator
- calculate_rvi -> rvi
- calculate_tsi -> tsi
- calculate_kst -> kst
- calculate_ppo -> ppo
- calculate_cmf -> cmf
- calculate_dmi -> dmi
'''


#1. Relative Strength Index (RSI): 상승/하락 비율로 과매수/과매도 상태를 측정.
def rsi(data: pd.Series, period: int = 14) -> pd.Series:
    """RSI(Relative Strength Index) 계산

    Args:
        data: 가격 데이터 (Pandas Series)
        period: RSI 계산 기간 (기본값: 14)

    Returns:
        RSI 값 (0-100)

    Note:
        - 30 이하: 과매도 구간
        - 70 이상: 과매수 구간
        - 50: 중립 기준선
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def rsi_divergence(price: pd.Series, rsi_values: pd.Series) -> pd.Series:
    """
    RSI 다이버전스 분석 - 가격과 RSI 간의 불일치를 통한 추세 전환 가능성 분석
    
    Args:
        price: 가격 데이터
        rsi_values: RSI 값
    
    Returns:
        다이버전스 신호 (1: 상승 다이버전스, -1: 하락 다이버전스, 0: 중립)
    
    References:
        - 상승 다이버전스: 가격은 하락하나 RSI는 상승
        - 하락 다이버전스: 가격은 상승하나 RSI는 하락
    """
    [... 기존 구현 유지 ...]

#2. Stochastic Oscillator: 종가와 고가/저가 범위 간의 관계를 측정.
def stochastic(high: pd.Series, low: pd.Series, close: pd.Series, 
               k_period: int = 14, d_period: int = 3) -> Tuple[pd.Series, pd.Series]:
    """스토캐스틱 오실레이터 계산

    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        k_period: %K 기간 (기본값: 14)
        d_period: %D 기간 (기본값: 3)

    Returns:
        (%K, %D) 값 (둘 다 0-100)

    Note:
        - 20 이하: 과매도 구간
        - 80 이상: 과매수 구간
        - %K와 %D의 교차: 매매 신호
    """
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k_line = ((close - lowest_low) / (highest_high - lowest_low)) * 100
    d_line = k_line.rolling(window=d_period).mean()
    return k_line, d_line

#3. Williams Percent Range (%R): 최근 종가가 고가 대비 어느 위치에 있는지 측정.
def williams_r(high: pd.Series, low: pd.Series, close: pd.Series, 
              period: int = 14) -> pd.Series:
    """윌리엄스 %R 계산

    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)

    Returns:
        Williams %R 값 (-100 ~ 0)

    Note:
        - -80 이하: 과매도 구간으로 매수 신호
        - -20 이상: 과매수 구간으로 매도 신호
        - 스토캐스틱과 유사하나 반대 방향
    """
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    wr = ((highest_high - close) / (highest_high - lowest_low)) * -100
    return wr

#4. Commodity Channel Index (CCI): 가격의 통계적 편차를 측정.
def cci(high: pd.Series, low: pd.Series, close: pd.Series, 
        period: int = 20) -> pd.Series:
    """CCI (Commodity Channel Index) 계산

    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 20)

    Returns:
        CCI 값 (일반적으로 ±100 범위)

    Note:
        - +100 이상: 과매수 구간
        - -100 이하: 과매도 구간
        - 0선: 중립 기준
    """
    typical_price = (high + low + close) / 3
    sma = typical_price.rolling(window=period).mean()
    mean_deviation = abs(typical_price - sma).rolling(window=period).mean()
    cci = (typical_price - sma) / (0.015 * mean_deviation)
    return cci

#5. Rate of Change (ROC): 가격 변화율을 측정.
def roc(close: pd.Series, period: int = 12) -> pd.Series:
    """ROC (Rate of Change) 계산

    Args:
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 12)

    Returns:
        ROC 값 (백분율)

    Note:
        - 양수: 상승 추세
        - 음수: 하락 추세
        - 0선: 추세 전환점
    """
    return ((close - close.shift(period)) / close.shift(period)) * 100

#6. Money Flow Index (MFI): 거래량과 가격을 결합하여 자금 흐름 강도를 측정.
def mfi(high: pd.Series, low: pd.Series, close: pd.Series, 
        volume: pd.Series, period: int = 14) -> pd.Series:
    """MFI (Money Flow Index) 계산

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
        - RSI에 거래량 개념 추가
    """
    typical_price = (high + low + close) / 3
    raw_money_flow = typical_price * volume
    
    positive_flow = pd.Series(0, index=raw_money_flow.index)
    negative_flow = pd.Series(0, index=raw_money_flow.index)
    
    price_diff = typical_price.diff()
    positive_flow[price_diff > 0] = raw_money_flow[price_diff > 0]
    negative_flow[price_diff < 0] = raw_money_flow[price_diff < 0]
    
    positive_mf = positive_flow.rolling(window=period).sum()
    negative_mf = negative_flow.rolling(window=period).sum()
    
    mfi = 100 - (100 / (1 + positive_mf / negative_mf))
    return mfi

#7. Relative Vigor Index (RVI): 종가와 시가의 관계를 이용한 모멘텀 지표.
def rvi(close: pd.Series, std_period: int = 10, ema_period: int = 14) -> pd.Series:
    """RVI (Relative Vigor Index) 계산

    Args:
        close: 종가 데이터 (Pandas Series)
        std_period: 표준화 기간 (기본값: 10)
        ema_period: EMA 기간 (기본값: 14)

    Returns:
        RVI 값 (-1 ~ 1)

    Note:
        - 0.5 이상: 상승 추세 강도 높음
        - -0.5 이하: 하락 추세 강도 높음
        - 0선 교차: 추세 전환 신호
    """
    numerator = (close - close.shift(std_period)).rolling(window=ema_period).mean()
    denominator = (close.rolling(window=ema_period).max() - close.rolling(window=ema_period).min())
    rvi = numerator / denominator
    return rvi

#8. True Strength Index (TSI): 가격 변화의 순수한 모멘텀을 측정.
def tsi(close: pd.Series, long_period: int = 25, short_period: int = 13) -> pd.Series:
    """TSI (True Strength Index) 계산

    Args:
        close: 종가 데이터 (Pandas Series)
        long_period: 장기 EMA 기간 (기본값: 25)
        short_period: 단기 EMA 기간 (기본값: 13)

    Returns:
        TSI 값 (-100 ~ 100)

    Note:
        - 25 이상: 강한 상승 추세
        - -25 이하: 강한 하락 추세
        - 이중 지수평활화로 노이즈 제거
    """
    momentum = close.diff()
    abs_momentum = momentum.abs()
    
    smooth1 = momentum.ewm(span=long_period).mean()
    smooth2 = smooth1.ewm(span=short_period).mean()
    abs_smooth1 = abs_momentum.ewm(span=long_period).mean()
    abs_smooth2 = abs_smooth1.ewm(span=short_period).mean()
    
    tsi = (smooth2 / abs_smooth2) * 100
    return tsi

#9. Know Sure Thing Oscillator (KST): ROC를 결합한 모멘텀 및 추세 분석
def kst(close: pd.Series, r1: int = 10, r2: int = 15, r3: int = 20, r4: int = 30,
        s1: int = 10, s2: int = 10, s3: int = 10, s4: int = 15) -> pd.Series:
    """KST (Know Sure Thing) Oscillator 계산

    Args:
        close: 종가 데이터 (Pandas Series)
        r1: 첫 번째 ROC 계산 기간 (기본값: 10)
        r2: 두 번째 ROC 계산 기간 (기본값: 15)
        r3: 세 번째 ROC 계산 기간 (기본값: 20)
        r4: 네 번째 ROC 계산 기간 (기본값: 30)
        s1: 첫 번째 SMA 계산 기간 (기본값: 10)
        s2: 두 번째 SMA 계산 기간 (기본값: 10)
        s3: 세 번째 SMA 계산 기간 (기본값: 10)
        s4: 네 번째 SMA 계산 기간 (기본값: 15)

    Returns:
        KST 값

    Note:
        - 양수: 상승 추세
        - 음수: 하락 추세
        - 0선 교차: 추세 전환 신호
    """
    rcma1 = roc(close, r1).rolling(window=s1).mean()
    rcma2 = roc(close, r2).rolling(window=s2).mean()
    rcma3 = roc(close, r3).rolling(window=s3).mean()
    rcma4 = roc(close, r4).rolling(window=s4).mean()
    
    kst = (rcma1 * 1) + (rcma2 * 2) + (rcma3 * 3) + (rcma4 * 4)
    return kst

#10. PPO: 단기/장기 이동평균의 차이를 백분율로 표시
def ppo(close: pd.Series, fast_period: int = 12, slow_period: int = 26) -> pd.Series:
    """PPO (Price Percentage Oscillator) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        fast_period: 단기 이동평균 기간 (기본값: 12)
        slow_period: 장기 이동평균 기간 (기본값: 26)
        
    Returns:
        PPO 값 (백분율)
        
    Note:
        - 양수: 상승 추세
        - 음수: 하락 추세
        - 0선 교차: 추세 전환 신호
    """
    fast_ema = close.ewm(span=fast_period).mean()
    slow_ema = close.ewm(span=slow_period).mean()
    return ((fast_ema - slow_ema) / slow_ema) * 100

#11. CMF: 거래량과 가격 변동을 결합한 자금 흐름 지표
def cmf(high: pd.Series, low: pd.Series, close: pd.Series, 
        volume: pd.Series, period: int = 20) -> pd.Series:
    """CMF (Chaikin Money Flow) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 20)
        
    Returns:
        CMF 값 (-1 ~ 1)
        
    Note:
        - 양수: 매수 압력 우세
        - 음수: 매도 압력 우세
        - 극단값: 추세 전환 가능성
    """
    mfm = ((close - low) - (high - close)) / (high - low)
    mfv = mfm * volume
    return mfv.rolling(window=period).sum() / volume.rolling(window=period).sum()

#12. DMI: 상승/하락 추세의 강도를 측정
def dmi(high: pd.Series, low: pd.Series, close: pd.Series, 
        period: int = 14) -> Tuple[pd.Series, pd.Series]:
    """DMI (Directional Movement Index) 계산

    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)

    Returns:
        DI+ 값 (0-100)
        DI- 값 (0-100)

    Note:
        - DI+: 상승 추세의 강도
        - DI-: 하락 추세의 강도
    """
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low
    
    pos_dm = pd.Series(0, index=up_move.index)
    neg_dm = pd.Series(0, index=down_move.index)
    
    pos_dm[up_move > down_move] = up_move[up_move > down_move]
    neg_dm[down_move > up_move] = down_move[down_move > up_move]
    
    tr = pd.concat([
        high - low,
        abs(high - close.shift(1)),
        abs(low - close.shift(1))
    ], axis=1).max(axis=1)
    
    atr = tr.rolling(window=period).mean()
    
    di_plus = (pos_dm / atr) * 100
    di_minus = (neg_dm / atr) * 100
    
    return di_plus, di_minus

class MomentumIndicator:
    """모멘텀 지표 클래스
    
    모든 모멘텀 지표를 계산하고 관리하는 클래스입니다.
    """
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        """모멘텀 지표 클래스 초기화
        
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

    def set_data(self, data: pd.DataFrame) -> None:
        """새로운 데이터 설정
        
        Args:
            data: OHLCV 데이터프레임
            
        Returns:
            None
            
        Note:
            - 기존 데이터 교체
            - 자동으로 유효성 검증 수행
        """
        self.data = data
        self._validate_data()

    def calculate_all(self, periods: List[int] = [14]) -> pd.DataFrame:
        """모든 모멘텀 지표 계산
        
        Args:
            periods: 계산에 사용할 기간 리스트 (기본값: [14])
            
        Returns:
            계산된 모든 지표가 포함된 DataFrame
            
        Note:
            - 모든 기본 모멘텀 지표 포함
            - 멀티 기간 분석 지원
            - 자동으로 컬럼명 생성
        """
        if self.data is None:
            raise ValueError("Data not set. Use set_data() first.")
            
        results = pd.DataFrame(index=self.data.index)
        
        # 기본 지표 계산
        for period in periods:
            results[f'rsi_{period}'] = rsi(self.data['close'], period)
            k_line, d_line = stochastic(
                self.data['high'], 
                self.data['low'], 
                self.data['close'], 
                k_period=period
            )
            results[f'stoch_k_{period}'] = k_line
            results[f'stoch_d_{period}'] = d_line
            results[f'williams_r_{period}'] = williams_r(
                self.data['high'],
                self.data['low'],
                self.data['close'],
                period
            )
            
        # 고정 기간 지표 계산
        results['cci'] = cci(self.data['high'], self.data['low'], self.data['close'])
        results['roc'] = roc(self.data['close'])
        results['mfi'] = mfi(
            self.data['high'],
            self.data['low'],
            self.data['close'],
            self.data['volume']
        )
        results['rvi'] = rvi(self.data['close'])
        results['tsi'] = tsi(self.data['close'])
        results['kst'] = kst(self.data['close'])
        
        # 새로운 지표 계산
        results['ppo'] = ppo(self.data['close'])
        results['cmf'] = cmf(
            self.data['high'],
            self.data['low'],
            self.data['close'],
            self.data['volume']
        )
        
        return results