# 📁 Docs/Plan/Phase1/Signals/risk_management.md

---

## 📌 목적
- **risk_management.py** 파일은 트레이딩 신호 실행 시 리스크를 관리하고 한도를 초과하지 않도록 제어하는 기능을 제공합니다.
- 포트폴리오 손실 최소화 및 자산 보호를 목표로 합니다.

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

1️⃣ **리스크 한도 초과 방지**
- 트레이딩 시 사전에 정의된 리스크 한도를 초과하지 않도록 제어.

2️⃣ **포트폴리오 다변화**
- 동일 자산에 대한 과도한 투자를 방지.

3️⃣ **실시간 손실 모니터링**
- 포지션 손실을 실시간으로 모니터링하여 자동으로 대응.

---

## 📄 주요 파일 설명

### 1️⃣ risk_management.py
#### 목적
- 트레이딩 신호 실행 시 리스크를 관리하고 손실을 최소화.

#### 주요 함수

##### (1) `check_risk_limit`
- 신호 실행 전에 리스크 한도를 확인.

```python
def check_risk_limit(portfolio, risk_limit):
    """
    리스크 한도 확인 함수
    :param portfolio: 현재 포트폴리오 상태
    :param risk_limit: 사전 정의된 리스크 한도
    :return: 리스크 초과 여부 (True/False)
    """
    total_risk = sum(asset['value'] for asset in portfolio)
    return total_risk <= risk_limit
```

##### (2) `monitor_loss`
- 포지션 손실을 실시간으로 모니터링.

```python
def monitor_loss(position, stop_loss):
    """
    손실 모니터링 함수
    :param position: 개별 포지션 상태
    :param stop_loss: 손절매 한도
    :return: 손실 상태 (True/False)
    """
    loss = position['entry_price'] - position['current_price']
    return loss >= stop_loss
```

##### (3) `diversify_portfolio`
- 포트폴리오를 다변화하여 리스크를 분산.

```python
def diversify_portfolio(portfolio, max_allocation):
    """
    포트폴리오 다변화 함수
    :param portfolio: 현재 포트폴리오 상태
    :param max_allocation: 개별 자산에 대한 최대 할당 비율
    :return: 조정된 포트폴리오
    """
    for asset in portfolio:
        if asset['allocation'] > max_allocation:
            asset['allocation'] = max_allocation
    return portfolio
```

---

## 🔗 통신 구조 및 의존성

### 통신 구조
```plaintext
signals/generator.py → signals/risk_management.py → execution/order_manager.py
```

### 주요 의존성
1. **외부 라이브러리:**
   - Pandas: 포트폴리오 데이터 처리.
2. **내부 모듈:**
   - signals/generator.py: 생성된 신호 데이터를 기반으로 리스크 관리.
   - execution/order_manager.py: 리스크 관리 결과를 기반으로 주문 실행.

---

## 📑 테스트 계획

### 1. 유닛 테스트
- `check_risk_limit`가 포트폴리오의 리스크를 정확히 계산하는지 확인.
- `monitor_loss`가 손절매 한도를 초과했는지 감지하는지 테스트.

### 2. 통합 테스트
- generator.py → risk_management.py → order_manager.py의 데이터 흐름 검증.

---

## 📘 참고 문서 및 링크
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
