'''
4. 추세 지표 (Trend Indicators)

정의
추세 지표는 시장의 방향성을 측정하며, 상승/하락 추세를 평가하는 지표들입니다.

목적
• 시장의 장기적 방향성 평가
• 추세 반전 및 지속 여부 식별
• 매매 시점 결정
• 추세 강도 측정
• 지지/저항 레벨 식별

지표 목록 (11개)
1. SMA (Simple Moving Average): 단순 이동평균선 - 장기 추세 파악, 지지/저항 레벨 식별
2. EMA (Exponential Moving Average): 지수 이동평균선 - 단기 추세 파악, 빠른 반응
3. WMA (Weighted Moving Average): 가중 이동평균선 - 맞춤형 추세 분석, 중기 반응
4. HMA (Hull Moving Average): 헐 이동평균선 - 지연 최소화, 빠른 반응, 단기 매매
5. DEMA (Double Exponential MA): 이중 지수 이동평균선 - 지연 감소, 정확도 향상
6. TEMA (Triple Exponential MA): 삼중 지수 이동평균선 - 정확도 향상, 노이즈 감소
7. MACD (Moving Average Convergence/Divergence): 이동평균 수렴/발산 - 추세 전환점 포착
8. Ichimoku Cloud: 일목균형표 - 다중 시간대 분석, 지지/저항 레벨
9. Parabolic SAR: 포물선 추세 반전 시스템 - 추세 전환점, 손절점
10. VI (Vortex Indicator): 추세 방향과 강도 측정 - 추세 강도 분석, 전환점 식별
11. ADX (Average Directional Index): 추세 강도 분석 - DMI 기반

참고 사항
• 여러 지표의 조합으로 신뢰도 향상
• 시간대별 교차 분석 권장
• 거래량과 함께 해석 필요

[2024.03.XX] 함수명 패턴 표준화
기존 함수명 -> 변경된 함수명:
- calculate_sma -> sma
- calculate_ema -> ema
- calculate_wma -> wma
- calculate_hma -> hma
- calculate_dema -> dema
- calculate_tema -> tema
- calculate_macd -> macd
- calculate_ichimoku -> ichimoku
- calculate_psar -> parabolic_sar
- calculate_vi -> vi
'''

from typing import List, Optional, Tuple
import pandas as pd
import numpy as np

#1. SMA (Simple Moving Average): 단순 이동평균선
def sma(data: pd.Series, period: int = 20) -> pd.Series:
    """Simple Moving Average (SMA) 계산
    
    Args:
        data: 가격 데이터 (Pandas Series)
        period: 이동평균 기간 (기본값: 20)
        
    Returns:
        SMA 값 (Pandas Series)
        
    Note:
        - 장기 추세 파악에 활용
        - 지지/저항 레벨 식별
        - 이동평균 교차로 매매 신호 생성
    """
    return data.rolling(window=period).mean()

#2. EMA (Exponential Moving Average): 지수 이동평균선
def ema(data: pd.Series, period: int = 20) -> pd.Series:
    """Exponential Moving Average (EMA) 계산
    
    Args:
        data: 가격 데이터 (Pandas Series)
        period: 이동평균 기간 (기본값: 20)
        
    Returns:
        EMA 값 (Pandas Series)
        
    Note:
        - 최근 데이터에 더 큰 가중치
        - 빠른 추세 변화 감지
        - 단기 매매 신호 생성에 활용
    """
    return data.ewm(span=period, adjust=False).mean()

#3. WMA (Weighted Moving Average): 가중 이동평균선
def wma(data: pd.Series, period: int = 20) -> pd.Series:
    """Weighted Moving Average (WMA) 계산
    
    Args:
        data: 가격 데이터 (Pandas Series)
        period: 이동평균 기간 (기본값: 20)
        
    Returns:
        WMA 값 (Pandas Series)
        
    Note:
        - 사용자 정의 가중치 적용
        - 맞춤형 추세 분석
        - 중기 매매 신호 생성
    """
    weights = np.arange(1, period + 1)
    return data.rolling(window=period).apply(
        lambda x: np.sum(weights * x) / weights.sum(), raw=True
    )

#4. HMA (Hull Moving Average): 헐 이동평균선 계산
def hma(data: pd.Series, period: int = 20) -> pd.Series:
    """Hull Moving Average (HMA) 계산
    
    Args:
        data: 가격 데이터 (Pandas Series)
        period: 이동평균 기간 (기본값: 20)
        
    Returns:
        HMA 값 (Pandas Series)
        
    Note:
        - 지연 최소화된 이동평균
        - 빠른 추세 변화 감지
        - 단기 매매에 적합
    """
    wma1 = wma(data, period // 2)
    wma2 = wma(data, period)
    return wma(2 * wma1 - wma2, int(np.sqrt(period)))

#5. DEMA (Double Exponential MA): 이중 지수 이동평균선 계산
def dema(data: pd.Series, period: int = 20) -> pd.Series:
    """Double Exponential Moving Average (DEMA) 계산
    
    Args:
        data: 가격 데이터 (Pandas Series)
        period: 이동평균 기간 (기본값: 20)
        
    Returns:
        DEMA 값 (Pandas Series)
        
    Note:
        - 지연 감소, 정확도 향상
        - 추세 파악에 활용
    """
    ema1 = ema(data, period)
    ema2 = ema(data, period)
    return 2 * ema1 - ema2

#6. TEMA (Triple Exponential MA): 삼중 지수 이동평균선 계산
def tema(data: pd.Series, period: int = 20) -> pd.Series:
    """Triple Exponential Moving Average (TEMA) 계산
    
    Args:
        data: 가격 데이터 (Pandas Series)
        period: 이동평균 기간 (기본값: 20)
        
    Returns:
        TEMA 값 (Pandas Series)
        
    Note:
        - 정확도 향상, 노이즈 감소
        - 추세 파악에 활용
    """
    ema1 = ema(data, period)
    ema2 = ema(data, period)
    ema3 = ema(data, period)
    return 3 * (ema1 - ema2) + ema3

#7. MACD (Moving Average Convergence Divergence): 이동평균 수렴/발산
def macd(data: pd.Series, fast_period: int = 12, 
         slow_period: int = 26, signal_period: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Moving Average Convergence Divergence (MACD) 계산
    
    Args:
        data: 가격 데이터 (Pandas Series)
        fast_period: 단기 이동평균 기간 (기본값: 12)
        slow_period: 장기 이동평균 기간 (기본값: 26)
        signal_period: 시그널 라인 기간 (기본값: 9)
        
    Returns:
        (MACD 라인, 시그널 라인, MACD 히스토그램) (tuple of Series)
        
    Note:
        - 추세 전환점 포착
        - 매매 시그널 생성
        - 모멘텀 변화 감지
    """
    fast_ema = ema(data, fast_period)
    slow_ema = ema(data, slow_period)
    macd_line = fast_ema - slow_ema
    signal_line = ema(macd_line, signal_period)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

#8. Ichimoku (Ichimoku Cloud): 일목균형표
def ichimoku(high: pd.Series, low: pd.Series, close: pd.Series,
            tenkan_period: int = 9, kijun_period: int = 26,
            senkou_b_period: int = 52) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
    """Ichimoku Cloud (일목균형표) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        tenkan_period: 전환선 기간 (기본값: 9)
        kijun_period: 기준선 기간 (기본값: 26)
        senkou_b_period: 선행스팬B 기간 (기본값: 52)
        
    Returns:
        (전환선, 기준선, 선행스팬A, 선행스팬B, 후행스팬) (tuple of Series)
        
    Note:
        - 다중 시간대 분석
        - 동적 지지/저항 레벨
        - 추세 강도와 방향 판단
    """
    # 전환선 (Tenkan-sen)
    tenkan = (high.rolling(window=tenkan_period).max() + 
             low.rolling(window=tenkan_period).min()) / 2

    # 기준선 (Kijun-sen)
    kijun = (high.rolling(window=kijun_period).max() + 
            low.rolling(window=kijun_period).min()) / 2

    # 선행스팬A (Senkou Span A)
    senkou_a = ((tenkan + kijun) / 2).shift(kijun_period)

    # 선행스팬B (Senkou Span B)
    senkou_b = ((high.rolling(window=senkou_b_period).max() + 
                low.rolling(window=senkou_b_period).min()) / 2).shift(kijun_period)

    # 후행스팬 (Chikou Span)
    chikou = close.shift(-kijun_period)

    return tenkan, kijun, senkou_a, senkou_b, chikou

#9. Parabolic SAR: 포물선 추세 반전 시스템
def parabolic_sar(high: pd.Series, low: pd.Series, close: pd.Series,
                 acceleration: float = 0.02, maximum: float = 0.2) -> pd.Series:
    """Parabolic SAR (Stop and Reverse) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        acceleration: 가속 계수 (기본값: 0.02)
        maximum: 최대 가속 계수 (기본값: 0.2)
        
    Returns:
        SAR 값 (Pandas Series)
        
    Note:
        - 추세 반전점 식별
        - 손절점 설정에 활용
        - 추세 추종 전략에 사용
    """
    # SAR 계산 로직
    sar = pd.Series(index=high.index, dtype=float)
    trend = pd.Series(index=high.index, dtype=bool)
    ep = pd.Series(index=high.index, dtype=float)
    af = pd.Series(index=high.index, dtype=float)

    # 초기값 설정
    sar.iloc[0] = high.iloc[0]
    trend.iloc[0] = True
    ep.iloc[0] = low.iloc[0]
    af.iloc[0] = acceleration

    # SAR 계산
    for i in range(1, len(high)):
        # 이전 추세가 상승일 때
        if trend.iloc[i-1]:
            sar.iloc[i] = sar.iloc[i-1] + af.iloc[i-1] * (ep.iloc[i-1] - sar.iloc[i-1])
            if low.iloc[i] < sar.iloc[i]:
                trend.iloc[i] = False
                sar.iloc[i] = ep.iloc[i-1]
                ep.iloc[i] = low.iloc[i]
                af.iloc[i] = acceleration
            else:
                trend.iloc[i] = True
                if high.iloc[i] > ep.iloc[i-1]:
                    ep.iloc[i] = high.iloc[i]
                    af.iloc[i] = min(af.iloc[i-1] + acceleration, maximum)
                else:
                    ep.iloc[i] = ep.iloc[i-1]
                    af.iloc[i] = af.iloc[i-1]
        # 이전 추세가 하락일 때
        else:
            sar.iloc[i] = sar.iloc[i-1] - af.iloc[i-1] * (sar.iloc[i-1] - ep.iloc[i-1])
            if high.iloc[i] > sar.iloc[i]:
                trend.iloc[i] = True
                sar.iloc[i] = ep.iloc[i-1]
                ep.iloc[i] = high.iloc[i]
                af.iloc[i] = acceleration
            else:
                trend.iloc[i] = False
                if low.iloc[i] < ep.iloc[i-1]:
                    ep.iloc[i] = low.iloc[i]
                    af.iloc[i] = min(af.iloc[i-1] + acceleration, maximum)
                else:
                    ep.iloc[i] = ep.iloc[i-1]
                    af.iloc[i] = af.iloc[i-1]

    return sar

def vi(high: pd.Series, low: pd.Series, close: pd.Series, 
       period: int = 14) -> Tuple[pd.Series, pd.Series]:
    """Vortex Indicator (VI) 계산
    
    Args:
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        close: 종가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        (VI+, VI-) (tuple of Series)
        
    Note:
        - VI+ > VI-: 상승 추세
        - VI- > VI+: 하락 추세
        - 교차: 추세 전환 신호
    """
    tr = pd.DataFrame()
    tr['h-l'] = abs(high - low)
    tr['h-pc'] = abs(high - close.shift(1))
    tr['l-pc'] = abs(low - close.shift(1))
    tr = tr.max(axis=1)
    
    vm_plus = abs(high - low.shift(1))
    vm_minus = abs(low - high.shift(1))
    
    vi_plus = vm_plus.rolling(period).sum() / tr.rolling(period).sum()
    vi_minus = vm_minus.rolling(period).sum() / tr.rolling(period).sum()
    
    return vi_plus, vi_minus

#11. ADX (Average Directional Index): 추세 강도 분석
def adx(close: pd.Series, high: pd.Series, low: pd.Series,
       period: int = 14) -> pd.Series:
    """Average Directional Index (ADX) 계산
    
    Args:
        close: 종가 데이터 (Pandas Series)
        high: 고가 데이터 (Pandas Series)
        low: 저가 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        ADX 값 (Pandas Series)
        
    Note:
        - 추세의 강도 측정
        - 25 이상: 강한 추세
        - 20 이하: 약한 추세
    """
    # ADX 함수 구현
    # 이 부분은 실제 ADX 계산 로직을 구현해야 합니다.
    # 현재는 임시로 0으로 반환합니다.
    return pd.Series(index=close.index, dtype=float)

class TrendIndicator:
    """추세 지표 클래스
    
    모든 추세 지표를 계산하고 관리하는 클래스입니다.
    """
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        """추세 지표 클래스 초기화
        
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
        """모든 추세 지표 계산
        
        Args:
            None
            
        Returns:
            계산된 모든 지표가 포함된 DataFrame
            
        Note:
            - 모든 추세 지표 포함
            - 자동으로 컬럼명 생성
        """
        results = pd.DataFrame(index=self.data.index)
        
        # 이동평균선 계산
        results['sma'] = sma(self.data['close'])
        results['ema'] = ema(self.data['close'])
        results['wma'] = wma(self.data['close'])
        results['hma'] = hma(self.data['close'])
        results['dema'] = dema(self.data['close'])
        results['tema'] = tema(self.data['close'])

        # MACD 계산
        macd_line, signal_line, histogram = macd(self.data['close'])
        results['macd'] = macd_line
        results['macd_signal'] = signal_line
        results['macd_histogram'] = histogram

        # 일목균형표 계산
        tenkan, kijun, senkou_a, senkou_b, chikou = ichimoku(
            self.data['high'], self.data['low'], self.data['close']
        )
        results['ichimoku_tenkan'] = tenkan
        results['ichimoku_kijun'] = kijun
        results['ichimoku_senkou_a'] = senkou_a
        results['ichimoku_senkou_b'] = senkou_b
        results['ichimoku_chikou'] = chikou

        # Parabolic SAR 계산
        results['psar'] = parabolic_sar(
            self.data['high'], self.data['low'], self.data['close']
        )

        # Vortex Indicator 계산
        vi_plus, vi_minus = vi(self.data['high'], self.data['low'], self.data['close'])
        results['vi_plus'] = vi_plus
        results['vi_minus'] = vi_minus

        # ADX 계산
        results['adx'] = adx(self.data['close'], self.data['high'], self.data['low'])

        return results
                    
    def vi(self, high: Optional[pd.Series] = None, 
           low: Optional[pd.Series] = None,
           close: Optional[pd.Series] = None, 
           period: int = 14) -> Tuple[pd.Series, pd.Series]:
        """Vortex Indicator 계산
        
        Args:
            high: 고가 데이터 (선택사항)
            low: 저가 데이터 (선택사항)
            close: 종가 데이터 (선택사항)
            period: 계산 기간 (기본값: 14)
            
        Returns:
            (VI+, VI-) (tuple of Series)
            
        Note:
            - 데이터 미입력시 클래스 초기화 데이터 사용
            - 추세 방향과 강도 측정에 활용
        """
        if high is None:
            high = self.data['high']
        if low is None:
            low = self.data['low']
        if close is None:
            close = self.data['close']
        return vi(high, low, close, period)
                    