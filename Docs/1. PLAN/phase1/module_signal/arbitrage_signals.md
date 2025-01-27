# 📁 Docs/Plan/Phase1/Signals/arbitrage_signals.md

---

## 📌 목적
- **arbitrage_signals.py** 파일은 아비트라지 기회를 탐지하고 신호를 생성하는 기능을 제공합니다.
- 여러 거래소 간의 가격 차이를 활용하여 수익을 극대화합니다.

---

## 📁 디렉터리 구조
```plaintext
signals/
├── __init__.py           # 모듈 초기화 파일
├── generator.py          # 신호 생성
├── filters.py            # 신호 필터링
├── arbitrage_signals.py  # 아비트라지 신호
├── risk_management.py    # 리스크 관리
└── optimizer.py          # 전략 최적화
```

---

## ✨ 주요 기능

1️⃣ **거래소 간 가격 차이 탐지**
- 여러 거래소에서 동일 자산의 가격을 비교.

2️⃣ **최적의 매수/매도 거래소 선택**
- 거래 비용 및 슬리피지를 고려하여 신호 생성.

3️⃣ **수익성 평가**
- 수익성이 있는 거래만 신호로 생성.

---

## 📄 주요 파일 설명

### 1️⃣ arbitrage_signals.py
#### 목적
- 거래소 간 아비트라지 기회를 탐지하고 신호를 생성.

#### 주요 함수

##### (1) `detect_arbitrage_opportunities`
- 거래소 간 가격 차이를 계산하여 아비트라지 기회를 탐지.

```python
def detect_arbitrage_opportunities(prices):
    """
    아비트라지 기회 탐지 함수
    :param prices: 거래소 별 자산 가격 (Dictionary)
    :return: 아비트라지 기회 목록
    """
    opportunities = []
    for asset, price_data in prices.items():
        min_price_exchange = min(price_data, key=price_data.get)
        max_price_exchange = max(price_data, key=price_data.get)
        price_difference = price_data[max_price_exchange] - price_data[min_price_exchange]

        if price_difference > 0:
            opportunities.append({
                "asset": asset,
                "buy_from": min_price_exchange,
                "sell_to": max_price_exchange,
                "profit": price_difference
            })
    return opportunities
```

##### (2) `evaluate_profitability`
- 거래 비용 및 슬리피지를 고려하여 수익성을 평가.

```python
def evaluate_profitability(opportunity, trading_fee):
    """
    수익성 평가 함수
    :param opportunity: 아비트라지 기회 데이터
    :param trading_fee: 거래 수수료 비율
    :return: 수익성 여부 (True/False)
    """
    profit_after_fee = opportunity['profit'] - (opportunity['profit'] * trading_fee)
    return profit_after_fee > 0
```

##### (3) `generate_arbitrage_signals`
- 유효한 아비트라지 기회를 기반으로 신호를 생성.

```python
def generate_arbitrage_signals(prices, trading_fee):
    """
    아비트라지 신호 생성 함수
    :param prices: 거래소 별 자산 가격 (Dictionary)
    :param trading_fee: 거래 수수료 비율
    :return: 아비트라지 신호 목록
    """
    opportunities = detect_arbitrage_opportunities(prices)
    signals = [
        opp for opp in opportunities if evaluate_profitability(opp, trading_fee)
    ]
    return signals
```

---

## 🔗 통신 구조 및 의존성

### 통신 구조
```plaintext
collector.py → arbitrage_signals.py → execution/arbitrage_executor.py
```

### 주요 의존성
1. **외부 라이브러리:**
   - NumPy: 수치 계산.
2. **내부 모듈:**
   - signals/generator.py: 생성된 신호 데이터를 아비트라지 신호로 변환.
   - data/collector.py: 거래소 가격 데이터 수집.

---

## 📑 테스트 계획

### 1. 유닛 테스트
- `detect_arbitrage_opportunities`가 가격 차이를 올바르게 계산하는지 확인.
- `evaluate_profitability`가 수익성을 정확히 평가하는지 테스트.

### 2. 통합 테스트
- collector.py → arbitrage_signals.py → execution/arbitrage_executor.py의 데이터 흐름 검증.

---

## 📘 참고 문서 및 링크
- [NumPy Documentation](https://numpy.org/doc/)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- Docs/Plan/Phase1/module_data.md
- Docs/Plan/Phase1/module_indicators.md
- Docs/Plan/Phase1/module_models.md
- Docs/Plan/Phase1/module_signals.md
- Docs/Plan/Phase1/module_execution.md
- Docs/Plan/Phase1/module_uiux.md
- Docs/Plan/Phase1/module_logger.md
- Docs/Plan/Phase1/module_data_storage.md