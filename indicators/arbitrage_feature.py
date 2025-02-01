import pandas as pd
import numpy as np
from scipy.stats import norm  # liquidation_risk 함수에서 사용

'''
8. 차익거래 특징 (Arbitrage Features)

정의
거래소 간 가격 차이와 차익거래 기회를 분석하는 특징들입니다.

목적
• 거래소 간 가격 차이 분석
• 실현 가능한 차익거래 기회 탐지
• 거래 비용 고려한 수익성 분석
• 시장 효율성 측정
• 리스크 관리

특징 목록 (15개)
1. Price Spread: 거래소 간 단순 가격 차이 분석
2. Volume-Weighted Spread: 거래량 가중 스프레드 분석
3. Cost-Adjusted Spread: 거래 비용 반영 스프레드
4. Order Book Depth: 호가창 깊이 기반 유동성 분석
5. Market Impact Cost: 거래 규모별 시장 충격 비용
6. Execution Speed: 거래 실행 속도 및 지연 시간
7. Risk-Adjusted Return: 리스크 조정 수익률
8. Triangular Arbitrage: 삼각 차익거래 기회 분석
9. Futures-Spot Spread: 선물-현물 간 차익거래 기회
10. Statistical Arbitrage: 통계적 차익거래 신호
11. Funding Rate Arbitrage: 펀딩비 차익거래 기회
12. Basis Trading: 베이시스 트레이딩 기회
13. Capital Efficiency: 자금 효율성 최적화 지표
14. Liquidation Risk: 청산 리스크 최적화 지표
15. Portfolio Balance: 포트폴리오 밸런싱 지표

참고 사항
• 실시간 데이터 처리 필요
• 거래소별 API 특성 고려
• 네트워크 지연 고려
• 수수료 구조 반영
• 마진/레버리지 고려
• 청산 리스크 관리
• 자금 효율성 최적화

[2024.03.XX] 함수명 패턴 표준화
기존 함수명 -> 변경된 함수명:
- calculate_price_spread -> price_spread
- calculate_volume_weighted -> volume_weighted_spread
- calculate_cost_adjusted -> cost_adjusted_spread
- calculate_order_book -> order_book_depth
- calculate_market_impact -> market_impact_cost
- calculate_execution_speed -> execution_speed
- calculate_risk_adjusted -> risk_adjusted_return
- calculate_triangular -> triangular_arbitrage
- calculate_futures_spot -> futures_spot_spread
- calculate_statistical -> statistical_arbitrage
- calculate_funding_rate -> funding_rate_arbitrage
- calculate_basis -> basis_trading
- calculate_capital -> capital_efficiency
- calculate_liquidation -> liquidation_risk
- calculate_portfolio -> portfolio_balance
'''

from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np

#1. Price Spread: 거래소 간 단순 가격 차이를 측정하는 특징.
def price_spread(price1: pd.Series, price2: pd.Series) -> pd.Series:
    """거래소 간 가격 스프레드 계산
    
    Args:
        price1: 첫 번째 거래소 가격 (Pandas Series)
        price2: 두 번째 거래소 가격 (Pandas Series)
        
    Returns:
        가격 스프레드 비율 (%) (Pandas Series)
        
    Note:
        - 양수: price1이 더 높음
        - 음수: price2가 더 높음
        - 절대값이 클수록 차익기회
    """
    return ((price1 - price2) / price2) * 100

#2. Volume-Weighted Spread: 거래량으로 가중치를 준 스프레드 특징.
def volume_weighted_spread(price1: pd.Series, price2: pd.Series,
                         volume1: pd.Series, volume2: pd.Series) -> pd.Series:
    """거래량 가중 스프레드 계산
    
    Args:
        price1: 첫 번째 거래소 가격 (Pandas Series)
        price2: 두 번째 거래소 가격 (Pandas Series)
        volume1: 첫 번째 거래소 거래량 (Pandas Series)
        volume2: 두 번째 거래소 거래량 (Pandas Series)
        
    Returns:
        거래량 가중 스프레드 (Pandas Series)
        
    Note:
        - 거래량이 많은 쪽에 더 큰 가중치
        - 유동성을 고려한 실질적 차이
    """
    total_volume = volume1 + volume2
    weight1 = volume1 / total_volume
    weight2 = volume2 / total_volume
    return ((price1 * weight1) - (price2 * weight2)) / ((price1 * weight1 + price2 * weight2) / 2) * 100

#3. Cost-Adjusted Spread: 거래 비용 반영 스프레드
def cost_adjusted_spread(price1: pd.Series, price2: pd.Series,
                        fee1: float, fee2: float,
                        slippage: float = 0.0005) -> pd.Series:
    """거래 비용 반영 스프레드 계산
    
    Args:
        price1: 첫 번째 거래소 가격 (Pandas Series)
        price2: 두 번째 거래소 가격 (Pandas Series)
        fee1: 첫 번째 거래소 수수료율
        fee2: 두 번째 거래소 수수료율
        slippage: 예상 슬리피지 (기본값: 0.05%)
        
    Returns:
        비용 조정 스프레드 (Pandas Series)
        
    Note:
        - 수수료 고려
        - 슬리피지 고려
        - 실질적 차익 가능성
    """
    base_spread = ((price1 - price2) / price2) * 100
    total_cost = (fee1 + fee2 + slippage) * 100
    return base_spread - total_cost

#4. Order Book Depth: 호가창 깊이 기반 유동성 분석
def order_book_depth(bids: pd.DataFrame, asks: pd.DataFrame, 
                    depth_levels: List[float] = [0.1, 0.5, 1.0]) -> pd.DataFrame:
    """호가창 깊이 분석
    
    Args:
        bids: 매수 호가 데이터 (price, volume columns)
        asks: 매도 호가 데이터 (price, volume columns)
        depth_levels: 분석할 가격 수준 (% 기준)
        
    Returns:
        호가창 깊이 특징 DataFrame
        
    Note:
        - 각 가격 수준별 유동성
        - 매수/매도 불균형
        - 스프레드 분포
    """
    results = pd.DataFrame()
    mid_price = (bids['price'].iloc[0] + asks['price'].iloc[0]) / 2
    
    for level in depth_levels:
        price_range = mid_price * level / 100
        bid_depth = bids[bids['price'] >= mid_price - price_range]['volume'].sum()
        ask_depth = asks[asks['price'] <= mid_price + price_range]['volume'].sum()
        
        results[f'bid_depth_{level}'] = bid_depth
        results[f'ask_depth_{level}'] = ask_depth
        results[f'depth_imbalance_{level}'] = (bid_depth - ask_depth) / (bid_depth + ask_depth)
    
    return results

#5. Market Impact Cost: 거래 규모별 시장 충격 비용
def market_impact_cost(order_size: pd.Series, orderbook: pd.DataFrame,
                      side: str = 'buy') -> pd.DataFrame:
    """시장 충격 비용 계산
    
    Args:
        order_size: 주문 크기 (Pandas Series)
        orderbook: 호가창 데이터 (price, volume columns)
        side: 거래 방향 ('buy' or 'sell')
        
    Returns:
        예상 시장 충격 비용 (Pandas DataFrame)
        
    Note:
        - 주문 크기별 슬리피지
        - 유동성 소진 영향
        - 가격 영향 추정
    """
    def calculate_impact(size, book):
        remaining_size = size
        weighted_price = 0
        for _, level in book.iterrows():
            if remaining_size <= 0:
                break
            executed = min(remaining_size, level['volume'])
            weighted_price += executed * level['price']
            remaining_size -= executed
        return weighted_price / size if size > 0 else 0
    
    if side == 'buy':
        base_price = orderbook['price'].iloc[0]
        impact_price = order_size.apply(lambda x: calculate_impact(x, orderbook))
    else:
        base_price = orderbook['price'].iloc[-1]
        impact_price = order_size.apply(lambda x: calculate_impact(x, orderbook.iloc[::-1]))
    
    results = pd.DataFrame()
    results['impact_cost'] = ((impact_price - base_price) / base_price) * 100
    results['impact_ratio'] = impact_price / base_price
    results['liquidity_score'] = 1 / (1 + results['impact_cost'])
    return results

#6. Execution Speed: 거래 실행 속도 및 지연 시간
def execution_speed(latency: pd.Series, order_process_time: pd.Series,
                   network_delay: pd.Series) -> pd.DataFrame:
    """거래 실행 속도 분석
    
    Args:
        latency: API 지연 시간 (ms)
        order_process_time: 주문 처리 시간 (ms)
        network_delay: 네트워크 지연 시간 (ms)
        
    Returns:
        실행 속도 관련 특징들 (DataFrame)
        
    Note:
        - 총 실행 시간
        - 병목 구간 식별
        - 속도 최적화 지표
    """
    results = pd.DataFrame()
    results['total_delay'] = latency + order_process_time + network_delay
    results['processing_ratio'] = order_process_time / results['total_delay']
    results['network_ratio'] = network_delay / results['total_delay']
    results['speed_score'] = 1000 / results['total_delay']  # 속도 점수 (높을수록 빠름)
    
    return results

#7. Risk-Adjusted Return: 리스크 조정 수익률
def risk_adjusted_return(returns: pd.Series, volatility: pd.Series,
                        risk_free_rate: float = 0.0) -> pd.DataFrame:
    """리스크 조정 수익률 계산
    
    Args:
        returns: 차익거래 수익률 (Pandas Series)
        volatility: 변동성 (Pandas Series)
        risk_free_rate: 무위험 수익률 (기본값: 0.0)
        
    Returns:
        리스크 조정 지표들 (DataFrame)
        
    Note:
        - Sharpe Ratio
        - Sortino Ratio
        - Calmar Ratio
    """
    results = pd.DataFrame()
    
    # Sharpe Ratio
    results['sharpe'] = (returns - risk_free_rate) / volatility
    
    # Sortino Ratio (하방 리스크만 고려)
    downside_vol = returns[returns < 0].std()
    results['sortino'] = (returns - risk_free_rate) / downside_vol
    
    # Calmar Ratio (최대 낙폭 대비)
    max_drawdown = (returns.cummax() - returns).max()
    results['calmar'] = (returns.mean() - risk_free_rate) / max_drawdown
    
    return results

#8. Triangular Arbitrage: 삼각 차익거래 기회 분석
def triangular_arbitrage(pair1: pd.Series, pair2: pd.Series, 
                        pair3: pd.Series) -> pd.DataFrame:
    """삼각 차익거래 기회 분석
    
    Args:
        pair1: 첫 번째 페어 가격 (예: BTC/USD)
        pair2: 두 번째 페어 가격 (예: ETH/USD)
        pair3: 세 번째 페어 가격 (예: ETH/BTC)
        
    Returns:
        삼각 차익거래 특징들 (DataFrame)
        
    Note:
        - 차익거래 수익률
        - 기회 발생 빈도
        - 최적 실행 경로
    """
    results = pd.DataFrame()
    
    # 정방향 거래
    forward_rate = pair1 * pair2 / pair3
    # 역방향 거래
    reverse_rate = 1 / (pair3 * pair2 / pair1)
    
    results['forward_profit'] = (forward_rate - 1) * 100
    results['reverse_profit'] = (reverse_rate - 1) * 100
    results['best_profit'] = results[['forward_profit', 'reverse_profit']].max(axis=1)
    results['trade_direction'] = results['forward_profit'] > results['reverse_profit']
    
    return results

#9. Futures-Spot Spread: 선물-현물 간 차익거래 기회
def futures_spot_spread(spot_price: pd.Series, futures_price: pd.Series,
                       days_to_expiry: int, funding_rate: float = 0.0) -> pd.DataFrame:
    """선물-현물 차익거래 분석
    
    Args:
        spot_price: 현물 가격 (Pandas Series)
        futures_price: 선물 가격 (Pandas Series)
        days_to_expiry: 만기까지 남은 일수
        funding_rate: 펀딩비율 (선물 계약의 경우)
        
    Returns:
        선물-현물 차익거래 특징들 (DataFrame)
        
    Note:
        - 베이시스 수익률
        - 연율화 수익률
        - 펀딩비용 고려
    """
    results = pd.DataFrame()
    
    # 베이시스 계산
    basis = futures_price - spot_price
    basis_return = basis / spot_price * 100
    
    # 연율화 수익률 계산
    annual_return = basis_return * (365 / days_to_expiry)
    funding_cost = funding_rate * 365  # 연간 펀딩 비용
    
    results['basis'] = basis
    results['basis_return'] = basis_return
    results['annual_return'] = annual_return
    results['net_return'] = annual_return - funding_cost
    
    return results

#10. Statistical Arbitrage: 통계적 차익거래 신호
def statistical_arbitrage(price1: pd.Series, price2: pd.Series,
                        spread: pd.Series, threshold: float) -> pd.DataFrame:
    """통계적 차익거래 신호 계산
    
    Args:
        price1: 첫 번째 거래소 가격 (Pandas Series)
        price2: 두 번째 거래소 가격 (Pandas Series)
        spread: 가격 스프레드 (Pandas Series)
        threshold: 임계값
        
    Returns:
        통계적 차익거래 신호 (Pandas DataFrame)
        
    Note:
        - 스프레드가 임계값을 넘어서면 차익거래 기회
    """
    results = pd.DataFrame()
    results['signal'] = (spread > threshold).astype(int)
    results['spread_ratio'] = spread / threshold
    return results

#11. Funding Rate Arbitrage: 펀딩비 차익거래 기회
def funding_rate_arbitrage(funding_rate: pd.Series, spot_price: pd.Series,
                          futures_price: pd.Series, days_to_expiry: int) -> pd.DataFrame:
    """펀딩비 차익거래 기회 계산
    
    Args:
        funding_rate: 펀딩비율 (Pandas Series)
        spot_price: 현물 가격 (Pandas Series)
        futures_price: 선물 가격 (Pandas Series)
        days_to_expiry: 만기까지 남은 일수
        
    Returns:
        펀딩비 차익거래 기회 (Pandas DataFrame)
        
    Note:
        - 펀딩비율 차이 이용
        - 선물 가격 영향 고려
    """
    basis = futures_price - spot_price
    annual_return = (funding_rate * 365 / days_to_expiry) * basis / spot_price * 100
    results = pd.DataFrame()
    results['annual_return'] = annual_return
    results['funding_impact'] = funding_rate * 365 / days_to_expiry
    return results

#12. Basis Trading: 베이시스 트레이딩 기회
def basis_trading(basis: pd.Series, threshold: float) -> pd.DataFrame:
    """베이시스 트레이딩 기회 계산
    
    Args:
        basis: 베이시스 (Pandas Series)
        threshold: 임계값
        
    Returns:
        베이시스 트레이딩 기회 (Pandas DataFrame)
        
    Note:
        - 베이시스가 임계값을 넘어서면 기회
        - 베이시스 비율로 기회 강도 측정
        - 추세 분석에 활용
    """
    results = pd.DataFrame()
    results['signal'] = (basis > threshold).astype(int)
    results['basis_ratio'] = basis / threshold
    results['trend'] = basis.diff().rolling(window=14).mean()
    return results

#13. Capital Efficiency: 자금 효율성 최적화 지표
def capital_efficiency(returns: pd.Series, capital_used: pd.Series,
                      margin_ratio: float) -> pd.DataFrame:
    """자금 효율성 최적화 지표 계산
    
    Args:
        returns: 차익거래 수익률 (Pandas Series)
        capital_used: 사용된 자금 (Pandas Series)
        margin_ratio: 마진 비율
        
    Returns:
        자금 효율성 지표들 (DataFrame)
        
    Note:
        - ROE (Return on Equity)
        - 자금 회전율
        - 마진 활용도
    """
    results = pd.DataFrame()
    
    # ROE 계산
    results['roe'] = returns / capital_used * 100
    
    # 자금 회전율
    results['capital_turnover'] = capital_used.diff() / capital_used
    
    # 마진 활용도
    results['margin_utilization'] = capital_used / (capital_used / margin_ratio)
    
    return results

#14. Liquidation Risk: 청산 리스크 최적화 지표
def liquidation_risk(position_size: pd.Series, margin: pd.Series,
                    volatility: pd.Series) -> pd.DataFrame:
    """청산 리스크 최적화 지표 계산
    
    Args:
        position_size: 포지션 크기 (Pandas Series)
        margin: 증거금 (Pandas Series)
        volatility: 변동성 (Pandas Series)
        
    Returns:
        청산 리스크 지표들 (DataFrame)
        
    Note:
        - 청산 가능성
        - 안전 마진 비율
        - 리스크 점수
    """
    results = pd.DataFrame()
    
    # 청산 가능성 계산
    margin_ratio = margin / position_size
    results['liquidation_probability'] = 1 - norm.cdf(margin_ratio / volatility)
    
    # 안전 마진 비율
    results['safe_margin_ratio'] = (margin_ratio / volatility) * 100
    
    # 리스크 점수 (낮을수록 안전)
    results['risk_score'] = position_size * volatility / margin
    
    return results

#15. Portfolio Balance: 포트폴리오 밸런싱 지표
def portfolio_balance(positions: pd.DataFrame, correlations: pd.DataFrame,
                     risk_limits: Dict[str, float]) -> pd.DataFrame:
    """포트폴리오 밸런싱 지표 계산
    
    Args:
        positions: 포지션 정보 DataFrame
        correlations: 자산 간 상관관계 DataFrame
        risk_limits: 리스크 한도 설정
        
    Returns:
        포트폴리오 밸런스 지표들 (DataFrame)
        
    Note:
        - 포지션 분산도
        - 리스크 집중도
        - 상관관계 점수
    """
    results = pd.DataFrame()
    
    # 포지션 분산도
    total_position = positions.abs().sum()
    results['position_diversity'] = 1 - (positions ** 2).sum() / (total_position ** 2)
    
    # 리스크 집중도
    position_weights = positions / total_position
    risk_concentration = (position_weights * correlations).sum()
    results['risk_concentration'] = risk_concentration
    
    # 리스크 한도 활용률
    for asset, limit in risk_limits.items():
        if asset in positions:
            results[f'{asset}_limit_usage'] = positions[asset].abs() / limit
    
    return results

class ArbitrageFeature:
    """차익거래 특징 클래스"""
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        """차익거래 특징 클래스 초기화
        
        Args:
            data: 거래소별 데이터프레임 (선택사항)
                필수 컬럼: price, volume, orderbook, fees
        """
        self.data = data
        if data is not None:
            self._validate_data()

    def _validate_data(self) -> None:
        """데이터 유효성 검증"""
        required = [
            'price', 'volume', 'orderbook', 'fees',
            'bids', 'asks', 'latency', 'funding_rate'
        ]
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Required columns missing: {required}")

    def generate_all(self) -> pd.DataFrame:
        """모든 차익거래 특징 생성"""
        results = pd.DataFrame(index=self.data.index)
        
        # 기본 특징들
        results = pd.concat([
            price_spread(self.data['price1'], self.data['price2']),
            volume_weighted_spread(
                self.data['price1'], self.data['price2'],
                self.data['volume1'], self.data['volume2']
            ),
            cost_adjusted_spread(
                self.data['price1'], self.data['price2'],
                self.data['fee1'], self.data['fee2']
            )
        ], axis=1)
        
        # 고급 특징들
        results = pd.concat([
            results,
            order_book_depth(self.data['bids'], self.data['asks']),
            market_impact_cost(self.data['order_size'], self.data['orderbook']),
            execution_speed(
                self.data['latency'],
                self.data['process_time'],
                self.data['network_delay']
            ),
            risk_adjusted_return(
                self.data['returns'],
                self.data['volatility']
            )
        ], axis=1)
        
        # 특수 차익거래 특징들
        results = pd.concat([
            results,
            triangular_arbitrage(
                self.data['pair1'],
                self.data['pair2'],
                self.data['pair3']
            ),
            futures_spot_spread(
                self.data['spot_price'],
                self.data['futures_price'],
                self.data['days_to_expiry'],
                self.data['funding_rate']
            )
        ], axis=1)
        
        return results 