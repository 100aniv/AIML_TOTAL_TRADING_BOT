6. 온체인 지표 (On-Chain Indicators)
정의
온체인 지표는 블록체인 네트워크 데이터를 분석하여 암호화폐의 내재적인 상태를 평가합니다.

목적
네트워크 강도 분석
시장 활동성 평가

지표 목록(10개)


#1. NVT Ratio (Network Value to Transactions Ratio): 네트워크 가치 대비 거래량 비율.
def nvt_ratio(market_cap, transaction_volume):
    """
    NVT Ratio (Network Value to Transactions Ratio) 계산
    :param market_cap: 네트워크 시가총액 데이터 (Pandas Series)
    :param transaction_volume: 네트워크 거래량 데이터 (Pandas Series)
    :return: NVT Ratio 값 (Pandas Series)
    """
    return market_cap / transaction_volume  # NVT Ratio 계산

#2. MVRV Ratio (Market Value to Realized Value Ratio): 시장 가치 대비 실현 가치.
def mvrv_ratio(market_cap, realized_cap):
    """
    MVRV Ratio (Market Value to Realized Value Ratio) 계산
    :param market_cap: 네트워크 시가총액 데이터 (Pandas Series)
    :param realized_cap: 실현된 시가총액 데이터 (Pandas Series)
    :return: MVRV Ratio 값 (Pandas Series)
    """
    return market_cap / realized_cap  # MVRV Ratio 계산

#3. Stock-to-Flow Ratio: 공급 희소성을 기반으로 가격 예측.
def stock_to_flow_ratio(stock, flow):
    """
    Stock-to-Flow Ratio 계산
    :param stock: 현재 총 공급량 (Pandas Series)
    :param flow: 연간 공급량 (Pandas Series)
    :return: Stock-to-Flow Ratio 값 (Pandas Series)
    """
    return stock / flow  # Stock-to-Flow Ratio 계산

#4. Active Addresses: 활성 주소 수를 통해 네트워크 활동 분석.
def active_addresses(address_counts, period=7):
    """
    활성 주소 계산
    :param address_counts: 활성 주소 수 데이터 (Pandas Series)
    :param period: 평균 계산 기간
    :return: 활성 주소 수 이동 평균 (Pandas Series)
    """
    return address_counts.rolling(window=period).mean()  # 활성 주소 이동 평균

#5. Transaction Volume: 총 거래량 분석.
def transaction_volume(transaction_data, period=7):
    """
    거래량 계산
    :param transaction_data: 거래량 데이터 (Pandas Series)
    :param period: 평균 계산 기간
    :return: 거래량 이동 평균 (Pandas Series)
    """
    return transaction_data.rolling(window=period).mean()  # 거래량 이동 평균

#6. Exchange Inflow/Outflow: 거래소 유입 및 유출 자금.
def exchange_flow(inflow, outflow):
    """
    거래소 유입 및 유출 계산
    :param inflow: 거래소 유입 자금 데이터 (Pandas Series)
    :param outflow: 거래소 유출 자금 데이터 (Pandas Series)
    :return: 순 유입/유출 값 (Pandas Series)
    """
    return inflow - outflow  # 순 유입/유출 계산

#7. HODL Waves: 장기 보유자의 보유 비율 분석.
def hodl_waves(coin_ages):
    """
    HODL Waves 계산
    :param coin_ages: 코인의 보유 기간 데이터 (Pandas Series)
    :return: HODL Waves 값 (Pandas Series)
    """
    return coin_ages.value_counts(normalize=True).sort_index()


#8. Mining Difficulty: 블록 생성 난이도.
def mining_difficulty(difficulty_values, period=7):
    """
    채굴 난이도 계산 (이동 평균)
    :param difficulty_values: 일일 채굴 난이도 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 7일)
    :return: 채굴 난이도 이동 평균 값 (Pandas Series)
    """
    return difficulty_values.rolling(window=period).mean()

#9. Hash Rate: 네트워크의 보안 강도를 나타냄.
def hash_rate(hash_values, period=7):
    """
    해시레이트 계산 (이동 평균)
    :param hash_values: 해시레이트 데이터 (Pandas Series)
    :param period: 계산 기간 (기본값: 7일)
    :return: 해시레이트 이동 평균 값 (Pandas Series)
    """
    return hash_values.rolling(window=period).mean()

#10. Realized Cap: 실현된 시가총액.
def realized_cap(transaction_values, transaction_prices):
    """
    Realized Cap 계산
    :param transaction_values: 거래량 데이터 (Pandas Series)
    :param transaction_prices: 거래 가격 데이터 (Pandas Series)
    :return: Realized Cap 값 (Pandas Series)
    """
    return (transaction_values * transaction_prices).sum()
