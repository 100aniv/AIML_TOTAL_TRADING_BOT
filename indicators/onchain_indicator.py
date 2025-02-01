"""
온체인 지표 (On-Chain Indicators)

블록체인 네트워크의 실시간 데이터를 기반으로 하는 기술적 분석 도구입니다.
네트워크 활동과 가격 움직임의 관계를 분석합니다.

기능:
    - 네트워크 활성도 측정
    - 대형 거래자 행동 분석
    - 채굴자 활동 모니터링
    - 온체인 자금 흐름 추적

참조:
    - 대부분의 지표는 실시간 블록체인 데이터 필요
    - 거래소 데이터와 결합하여 분석 시 효과적
    - 장기 추세 분석에 유용
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Union, List, Optional

''' 
6. 온체인 지표 (Onchain Indicators)

정의
온체인 지표는 블록체인 네트워크의 실제 데이터를 기반으로 계산되는 지표들입니다.

목적
• 네트워크 활성도 측정
• 자금 흐름 분석
• 장기 투자자 행동 파악
• 채굴 활동 모니터링
• 네트워크 가치 평가

지표 목록 (20개)
1. NVT (Network Value to Transactions): 시가총액 대비 거래량 비율을 통해 네트워크의 가치를 평가하는 지표
2. MVRV (Market Value to Realized Value): 시장가치와 실현가치의 비율을 통해 과대/과소 평가를 판단하는 지표
3. SOPR (Spent Output Profit Ratio): 코인 이동 시점의 수익률을 측정하여 투자자 심리를 분석하는 지표
4. Active Addresses: 일일 활성 주소 수를 통해 네트워크 활성도를 측정하는 지표
5. Transaction Volume: 온체인 거래량을 분석하여 네트워크 사용도를 평가하는 지표
6. Exchange Flow: 거래소 입출금 데이터를 통해 시장 참여자들의 행동을 분석하는 지표
7. HODL Waves: 코인 보유 기간별 분포를 통해 장기/단기 투자자 비율을 분석하는 지표
8. Mining Difficulty: 채굴 난이도 변화를 통해 네트워크 보안성과 채굴자 참여도를 측정하는 지표
9. Hash Rate: 네트워크의 총 해시파워를 통해 보안성과 채굴 경쟁력을 평가하는 지표
10. Realized Cap: 코인이 마지막으로 이동한 시점의 가격을 기준으로 시가총액을 계산하는 지표
11. Stock to Flow: 현재 유통량 대비 신규 발행량 비율을 통해 희소성을 측정하는 지표
12. UTXO Age Distribution: 미사용 트랜잭션 출력의 연령 분포를 통해 보유 패턴을 분석하는 지표
13. Miner's Rolling Inventory: 채굴자들의 코인 보유량 변화를 통해 매도 압력을 예측하는 지표
14. Coin Days Destroyed: 장기 보유자들의 코인 이동을 감지하여 시장 변화를 예측하는 지표
15. Thermocap: 채굴자들의 총 수익을 기반으로 네트워크 가치를 평가하는 지표
16. RHODL Ratio: 실현 HODL 비율을 통해 장기 투자자들의 수익 실현 패턴을 분석하는 지표
17. Puell Multiple: 채굴 수익의 변동성을 통해 시장 사이클을 분석하는 지표
18. Difficulty Ribbon: 다중 기간 채굴 난이도 이동평균을 통해 채굴자 투항을 감지하는 지표
19. Reserve Risk: 장기 보유자들의 확신 대비 가격을 평가하는 지표
20. Relative Unrealized PnL: 미실현 손익 비율을 통해 시장 심리를 분석하는 지표

참고 사항
• 장기 추세 분석에 유용
• 거래소 데이터와 연계 분석
• 네트워크별 특성 고려
• 실시간 데이터 업데이트 필요

[2024.03.XX] 함수명 패턴 표준화
기존 함수명 -> 변경된 함수명:
- calculate_nvt -> nvt
- calculate_mvrv -> mvrv
- calculate_sopr -> sopr
- calculate_active_addresses -> active_addresses
- calculate_transaction_volume -> transaction_volume
- calculate_exchange_flow -> exchange_flow
- calculate_hodl_waves -> hodl_waves
- calculate_mining_difficulty -> mining_difficulty
- calculate_hash_rate -> hash_rate
- calculate_realized_cap -> realized_cap
- calculate_stock_to_flow -> stock_to_flow
- calculate_utxo_age -> utxo_age_distribution
- calculate_miners_inventory -> miners_rolling_inventory
- calculate_coin_days -> coin_days_destroyed
- calculate_thermocap -> thermocap
- calculate_rhodl -> rhodl_ratio
- calculate_puell -> puell_multiple
- calculate_difficulty_ribbon -> difficulty_ribbon
- calculate_reserve_risk -> reserve_risk
- calculate_unrealized_pnl -> relative_unrealized_pnl
'''

#1. NVT (Network Value to Transactions): 시가총액 대비 거래량 비율을 통해 네트워크의 가치를 평가하는 지표
def nvt_ratio(market_cap: pd.Series, transaction_volume: pd.Series, 
             period: int = 14) -> pd.Series:
    """Network Value to Transactions Ratio 계산
    
    Args:
        market_cap: 시가총액 데이터 (Pandas Series)
        transaction_volume: 거래량 데이터 (Pandas Series)
        period: 계산 기간 (기본값: 14)
        
    Returns:
        NVT 값 (Pandas Series)
        
    Note:
        - 높은 값: 과대평가 가능성
        - 낮은 값: 과소평가 가능성
        - 이동평균으로 노이즈 제거
    """
    nvt = market_cap / transaction_volume
    return nvt.rolling(window=period).mean()

#2. MVRV (Market Value to Realized Value): 시장가치와 실현가치의 비율을 통해 과대/과소 평가를 판단하는 지표
def mvrv_ratio(market_cap: pd.Series, realized_cap: pd.Series) -> pd.Series:
    """MVRV (Market Value to Realized Value) Ratio 계산
    
    Args:
        market_cap: 시가총액 데이터 (Pandas Series)
        realized_cap: 실현 시가총액 데이터 (Pandas Series)
        
    Returns:
        MVRV 값 (Pandas Series)
        
    Note:
        - 3.5 이상: 시장 과열 구간
        - 1.0 이하: 시장 저평가 구간
        - 장기 투자 지표로 활용
    """
    return market_cap / realized_cap

#3. SOPR (Spent Output Profit Ratio): 코인 이동 시점의 수익률을 측정하여 투자자 심리를 분석하는 지표
def sopr_ratio(realized_price: pd.Series, current_price: pd.Series) -> pd.Series:
    """SOPR (Spent Output Profit Ratio) 계산
    
    Args:
        realized_price: 실현 가격 데이터 (Pandas Series)
        current_price: 현재 가격 데이터 (Pandas Series)
        
    Returns:
        SOPR 값 (Pandas Series)
        
    Note:
        - 1 초과: 수익 실현 구간
        - 1 미만: 손실 실현 구간
        - 1: 손익분기점
    """
    return current_price / realized_price

#4. Active Addresses: 일일 활성 주소 수를 통해 네트워크 활성도를 측정하는 지표
def active_addresses(address_counts: pd.Series, period: int = 7) -> pd.Series:
    """활성 주소 수 분석
    
    Args:
        address_counts: 일일 활성 주소 수 (Pandas Series)
        period: 이동평균 기간 (기본값: 7)
        
    Returns:
        활성 주소 수 이동평균 (Pandas Series)
        
    Note:
        - 증가: 네트워크 활성도 상승
        - 감소: 네트워크 활성도 하락
        - 가격과의 괴리 주시
    """
    return address_counts.rolling(window=period).mean()

#5. Transaction Volume: 온체인 거래량을 분석하여 네트워크 사용도를 평가하는 지표
def transaction_volume(volume: pd.Series, period: int = 7) -> pd.Series:
    """온체인 거래량 분석
    
    Args:
        volume: 일일 거래량 데이터 (Pandas Series)
        period: 이동평균 기간 (기본값: 7)
        
    Returns:
        거래량 이동평균 (Pandas Series)
        
    Note:
        - 급증: 큰 시장 변동 신호
        - 저점: 관심도 감소
        - 추세 전환점 식별에 활용
    """
    return volume.rolling(window=period).mean()

#6. Exchange Flow: 거래소 입출금 데이터를 통해 시장 참여자들의 행동을 분석하는 지표
def exchange_flow(inflow: pd.Series, outflow: pd.Series, 
                 period: int = 7) -> pd.Series:
    """거래소 자금 흐름 분석
    
    Args:
        inflow: 거래소 유입량 (Pandas Series)
        outflow: 거래소 유출량 (Pandas Series)
        period: 이동평균 기간 (기본값: 7)
        
    Returns:
        순 자금 흐름 (유입 - 유출) (Pandas Series)
        
    Note:
        - 양수: 순 유입 (매도 압력)
        - 음수: 순 유출 (매수 압력)
        - 극단값: 큰 시장 변동 신호
    """
    net_flow = inflow - outflow
    return net_flow.rolling(window=period).mean()

#7. HODL Waves: 코인 보유 기간별 분포를 통해 장기/단기 투자자 비율을 분석하는 지표
def hodl_waves(coin_ages: pd.Series, bins: List[int] = None) -> pd.Series:
    """HODL Waves 분석
    
    Args:
        coin_ages: 코인 보유 기간 데이터 (Pandas Series)
        bins: 기간 구분 기준 (기본값: [1,7,30,90,180,365,730])
        
    Returns:
        기간별 보유 비율 (Pandas Series)
        
    Note:
        - 장기 보유 증가: 강한 홀더 신뢰
        - 단기 보유 증가: 투기 심리 강화
        - 시장 심리 판단에 활용
    """
    if bins is None:
        bins = [1, 7, 30, 90, 180, 365, 730]
    return pd.cut(coin_ages, bins=bins).value_counts(normalize=True)

#8. Mining Difficulty: 채굴 난이도 변화를 통해 네트워크 보안성과 채굴자 참여도를 측정하는 지표
def mining_difficulty(difficulty: pd.Series, period: int = 14) -> pd.Series:
    """채굴 난이도 분석
    
    Args:
        difficulty: 채굴 난이도 데이터 (Pandas Series)
        period: 이동평균 기간 (기본값: 14)
        
    Returns:
        채굴 난이도 이동평균 (Pandas Series)
        
    Note:
        - 상승: 채굴자 참여 증가
        - 하락: 채굴자 수익성 악화
        - 네트워크 보안성 지표
    """
    return difficulty.rolling(window=period).mean()

#9. Hash Rate: 네트워크의 총 해시파워를 통해 보안성과 채굴 경쟁력을 평가하는 지표
def hash_rate(hash_power: pd.Series, period: int = 14) -> pd.Series:
    """해시레이트 분석
    
    Args:
        hash_power: 해시파워 데이터 (Pandas Series)
        period: 이동평균 기간 (기본값: 14)
        
    Returns:
        해시레이트 이동평균 (Pandas Series)
        
    Note:
        - 상승: 네트워크 보안성 강화
        - 하락: 채굴자 이탈 가능성
        - 채굴 경쟁력 지표
    """
    return hash_power.rolling(window=period).mean()

#10. Realized Cap: 코인이 마지막으로 이동한 시점의 가격을 기준으로 시가총액을 계산하는 지표
def realized_cap(utxo_price: pd.Series, utxo_size: pd.Series) -> pd.Series:
    """Realized Cap 계산
    
    Args:
        utxo_price: UTXO 생성 시점의 가격 (Pandas Series)
        utxo_size: UTXO 크기 (Pandas Series)
        
    Returns:
        Realized Cap 값 (Pandas Series)
        
    Note:
        - 시장가치와의 괴리 분석
        - 장기 투자자 기준가치
        - 손익분기점 식별
    """
    return (utxo_price * utxo_size).sum()

#11. Stock to Flow: 현재 유통량 대비 신규 발행량 비율을 통해 희소성을 측정하는 지표
def stock_to_flow(circulating_supply: pd.Series, new_issuance: pd.Series) -> pd.Series:
    """Stock to Flow Ratio 계산
    
    Args:
        circulating_supply: 유통량 데이터 (Pandas Series)
        new_issuance: 신규 발행량 데이터 (Pandas Series)
        
    Returns:
        Stock to Flow 값 (Pandas Series)
        
    Note:
        - 높은 값: 강한 희소성
        - 낮은 값: 약한 희소성
        - 장기 가치 평가 지표
    """
    return circulating_supply / new_issuance

#12. UTXO Age Distribution: 미사용 트랜잭션 출력의 연령 분포를 통해 보유 패턴을 분석하는 지표
def utxo_age_distribution(utxo_ages: pd.Series, bins: List[int] = None) -> pd.Series:
    """UTXO 연령 분포 분석
    
    Args:
        utxo_ages: UTXO 연령 데이터 (Pandas Series)
        bins: 연령 구분 기준 (기본값: [1,7,30,90,180,365,730])
        
    Returns:
        연령별 UTXO 분포 (Pandas Series)
        
    Note:
        - 장기 UTXO 증가: 강한 보유 심리
        - 단기 UTXO 증가: 활발한 거래
        - 보유자 행동 패턴 분석
    """
    if bins is None:
        bins = [1, 7, 30, 90, 180, 365, 730]
    return pd.cut(utxo_ages, bins=bins).value_counts(normalize=True)

#13. Miner's Rolling Inventory: 채굴자들의 코인 보유량 변화를 통해 매도 압력을 예측하는 지표
def miners_rolling_inventory(mined_coins: pd.Series, sold_coins: pd.Series, 
                           period: int = 14) -> pd.Series:
    """채굴자 재고 분석
    
    Args:
        mined_coins: 채굴된 코인 수 (Pandas Series)
        sold_coins: 판매된 코인 수 (Pandas Series)
        period: 이동평균 기간 (기본값: 14)
        
    Returns:
        채굴자 재고 비율 (Pandas Series)
        
    Note:
        - 100% 초과: 재고 축적 (매도 압력 증가)
        - 100% 미만: 재고 감소 (매도 압력 감소)
        - 채굴자 심리 지표
    """
    inventory_ratio = (mined_coins - sold_coins) / mined_coins * 100
    return inventory_ratio.rolling(window=period).mean()

#14. Coin Days Destroyed: 장기 보유자들의 코인 이동을 감지하여 시장 변화를 예측하는 지표
def coin_days_destroyed(amount: pd.Series, holding_period: pd.Series) -> pd.Series:
    """Coin Days Destroyed 계산
    
    Args:
        amount: 이동된 코인 수량 (Pandas Series)
        holding_period: 보유 기간(일) (Pandas Series)
        
    Returns:
        CDD 값 (Pandas Series)
        
    Note:
        - 급증: 장기 보유자 이동 감지
        - 저점: 장기 보유자 홀딩
        - 시장 전환점 예측
    """
    return amount * holding_period

#15. Thermocap: 채굴자들의 총 수익을 기반으로 네트워크 가치를 평가하는 지표
def thermocap(mining_revenue: pd.Series, period: int = 14) -> pd.Series:
    """Thermocap 계산
    
    Args:
        mining_revenue: 채굴 수익 데이터 (Pandas Series)
        period: 이동평균 기간 (기본값: 14)
        
    Returns:
        Thermocap 값 (Pandas Series)
        
    Note:
        - 상승: 채굴자 수익성 개선
        - 하락: 채굴자 수익성 악화
        - 네트워크 가치 평가 지표
    """
    return mining_revenue.cumsum().rolling(window=period).mean()

#16. RHODL Ratio: 실현 HODL 비율을 통해 장기 투자자들의 수익 실현 패턴을 분석하는 지표
def rhodl_ratio(realized_price: pd.Series, hodl_price: pd.Series, 
                period: int = 7) -> pd.Series:
    """RHODL (Realized HODL) Ratio 계산
    
    Args:
        realized_price: 실현 가격 데이터 (Pandas Series)
        hodl_price: HODL 가격 데이터 (Pandas Series)
        period: 이동평균 기간 (기본값: 7)
        
    Returns:
        RHODL 값 (Pandas Series)
        
    Note:
        - 상승: 장기 보유자 수익 실현
        - 하락: 장기 보유자 홀딩
        - 시장 사이클 분석 지표
    """
    rhodl = realized_price / hodl_price
    return rhodl.rolling(window=period).mean()

#17. Puell Multiple: 채굴 수익의 변동성을 통해 시장 사이클을 분석하는 지표
def puell_multiple(daily_revenue: pd.Series, ma_revenue: pd.Series) -> pd.Series:
    """Puell Multiple 계산
    
    Args:
        daily_revenue: 일일 채굴 수익 (Pandas Series)
        ma_revenue: 이동평균 채굴 수익 (Pandas Series)
        
    Returns:
        Puell Multiple 값 (Pandas Series)
        
    Note:
        - 4.0 이상: 과열 구간
        - 0.5 이하: 저평가 구간
        - 채굴자 수익성 분석
    """
    return daily_revenue / ma_revenue

#18. Difficulty Ribbon: 다중 기간 채굴 난이도 이동평균을 통해 채굴자 투항을 감지하는 지표
def difficulty_ribbon(difficulty: pd.Series, 
                     periods: List[int] = [9,14,25,40,60,90,128,200]) -> pd.DataFrame:
    """Difficulty Ribbon 계산
    
    Args:
        difficulty: 채굴 난이도 데이터 (Pandas Series)
        periods: 이동평균 기간 리스트 (기본값: [9,14,25,40,60,90,128,200])
        
    Returns:
        다중 기간 이동평균 (Pandas DataFrame)
        
    Note:
        - 리본 압축: 채굴자 투항 신호
        - 리본 확장: 채굴자 참여 증가
        - 바닥 형성 지표
    """
    ribbon = pd.DataFrame(index=difficulty.index)
    for period in periods:
        ribbon[f'MA_{period}'] = difficulty.rolling(window=period).mean()
    return ribbon

#19. Reserve Risk: 장기 보유자들의 확신 대비 가격을 평가하는 지표
def reserve_risk(price: pd.Series, hodl_waves: pd.Series) -> pd.Series:
    """Reserve Risk 계산
    
    Args:
        price: 가격 데이터 (Pandas Series)
        hodl_waves: HODL Waves 데이터 (Pandas Series)
        
    Returns:
        Reserve Risk 값 (Pandas Series)
        
    Note:
        - 높은 값: 리스크 대비 낮은 확신
        - 낮은 값: 리스크 대비 높은 확신
        - 장기 투자 기회 지표
    """
    return price / hodl_waves

#20. Relative Unrealized PnL: 미실현 손익 비율을 통해 시장 심리를 분석하는 지표
def relative_unrealized_pnl(market_cap: pd.Series, realized_cap: pd.Series) -> pd.Series:
    """Relative Unrealized Profit/Loss 계산
    
    Args:
        market_cap: 시가총액 데이터 (Pandas Series)
        realized_cap: 실현 시가총액 데이터 (Pandas Series)
        
    Returns:
        미실현 손익 비율 (Pandas Series)
        
    Note:
        - 0.75 이상: 과도한 미실현 이익
        - 0.25 이하: 과도한 미실현 손실
        - 시장 심리 분석 지표
    """
    return (market_cap - realized_cap) / market_cap

class OnchainIndicator:
    """온체인 지표 클래스
    
    블록체인 네트워크 데이터 기반 지표를 계산하고 관리하는 클래스입니다.
    """
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        """온체인 지표 클래스 초기화
        
        Args:
            data: 온체인 데이터프레임 (선택사항)
                필수 컬럼: market_cap, transaction_volume, realized_cap 등
        
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
        required = ['market_cap', 'transaction_volume', 'realized_cap']
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Required columns missing: {required}")

    def set_data(self, data: pd.DataFrame) -> None:
        """새로운 데이터 설정
        
        Args:
            data: 온체인 데이터프레임
            
        Returns:
            None
            
        Note:
            - 기존 데이터 교체
            - 자동으로 유효성 검증 수행
        """
        self.data = data
        self._validate_data()

    def calculate_all(self, periods: List[int] = [7, 14, 30]) -> pd.DataFrame:
        """모든 온체인 지표 계산
        
        Args:
            periods: 계산에 사용할 기간 리스트 (기본값: [7, 14, 30])
            
        Returns:
            계산된 모든 지표가 포함된 DataFrame
        """
        if self.data is None:
            raise ValueError("Data not set. Use set_data() first.")
            
        results = pd.DataFrame(index=self.data.index)
        
        # 기간별 지표 계산
        for period in periods:
            results[f'nvt_{period}'] = nvt_ratio(
                self.data['market_cap'], 
                self.data['transaction_volume'],
                period
            )
            results[f'active_addresses_{period}'] = active_addresses(
                self.data['active_addresses'],
                period
            )
            results[f'transaction_volume_{period}'] = transaction_volume(
                self.data['transaction_volume'],
                period
            )
            
        # 고정 지표 계산
        results['mvrv'] = mvrv_ratio(
            self.data['market_cap'],
            self.data['realized_cap']
        )
        
        results['sopr'] = sopr_ratio(
            self.data['realized_price'],
            self.data['current_price']
        )
        
        results['hodl_waves'] = hodl_waves(
            self.data['coin_ages']
        )
        results['difficulty'] = mining_difficulty(
            self.data['difficulty']
        )
        results['hashrate'] = hash_rate(
            self.data['hash_power']
        )
        results['realized'] = realized_cap(
            self.data['utxo_price'],
            self.data['utxo_size']
        )
        results['stf'] = stock_to_flow(
            self.data['circulating_supply'],
            self.data['new_issuance']
        )
        results['utxo_age'] = utxo_age_distribution(
            self.data['utxo_ages']
        )
        results['mri'] = miners_rolling_inventory(
            self.data['mined_coins'],
            self.data['sold_coins']
        )
        results['cdd'] = coin_days_destroyed(
            self.data['amount'],
            self.data['holding_period']
        )
        results['thermocap'] = thermocap(
            self.data['mining_revenue']
        )
        results['rhodl'] = rhodl_ratio(
            self.data['realized_price'],
            self.data['hodl_price']
        )
        results['puell'] = puell_multiple(
            self.data['daily_revenue'],
            self.data['ma_revenue']
        )
        results['diff_ribbon'] = difficulty_ribbon(
            self.data['difficulty']
        )
        results['rr'] = reserve_risk(
            self.data['price'],
            self.data['hodl_waves']
        )
        results['unrealized_pnl'] = relative_unrealized_pnl(
            self.data['market_cap'],
            self.data['realized_cap']
        )
        
        return results

    def get_indicator(self, indicator_name: str, **kwargs) -> pd.Series:
        """특정 지표 계산
        
        Args:
            indicator_name: 지표 이름
            **kwargs: 지표별 필요 매개변수
            
        Returns:
            계산된 지표 값 (Pandas Series)
        """
        if self.data is None:
            raise ValueError("Data not set. Use set_data() first.")
            
        indicator_funcs = {
            'nvt': nvt,
            'mvrv': mvrv,
            'sopr': sopr,
            'active_addresses': active_addresses,
            'transaction_volume': transaction_volume,
            'exchange_flow': exchange_flow,
            'hodl_waves': hodl_waves,
            'difficulty': mining_difficulty,
            'hashrate': hash_rate,
            'realized': realized_cap,
            'stf': stock_to_flow,
            'utxo_age': utxo_age_distribution,
            'mri': miners_rolling_inventory,
            'cdd': coin_days_destroyed,
            'thermocap': thermocap,
            'rhodl': rhodl_ratio,
            'puell': puell_multiple,
            'diff_ribbon': difficulty_ribbon,
            'rr': reserve_risk,
            'unrealized_pnl': relative_unrealized_pnl
        }
        
        if indicator_name not in indicator_funcs:
            raise ValueError(f"Unknown indicator: {indicator_name}")
            
        return indicator_funcs[indicator_name](**kwargs)
