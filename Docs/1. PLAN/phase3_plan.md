## 📁 Docs/Plan/Phase3/README.md

---

## 📌 Phase 3: 실시간 트레이딩 시스템 구축

---

## 📌 목적
- 실시간 데이터를 수집하여 매수/매도 신호를 생성하고, 트레이딩 전략을 즉시 실행.
- 리스크 관리와 주문 최적화를 통해 안정적이고 효율적인 실시간 트레이딩 시스템 구현.

---

## 📂 디렉터리 구조

```
Docs/
└── Plan/
    └── Phase3/
        ├── README.md
project/
├── data/
│   ├── real_time_collector.py    # 실시간 데이터 수집
│   ├── logger.py                 # 실시간 로깅
├── signals/
│   ├── generator.py              # 실시간 신호 생성
│   ├── risk_management.py        # 리스크 관리
│   └── filters.py                # 신호 필터링
├── execution/
│   ├── api/                      # 거래소 API 통합
│   │   ├── binance_api.py        # Binance API
│   │   └── other_exchange_api.py # 기타 거래소 API
│   ├── order_manager.py          # 매수/매도 주문 실행
│   ├── position_tracker.py       # 포지션 상태 추적
│   └── error_handler.py          # 장애 복구

---

## 🛠️ 주요 모듈과 함수

### 1️⃣ Data 모듈

#### (1) real_time_collector.py

기능: WebSocket을 통해 실시간 데이터 수집.
주요 함수:
```python
def collect_real_time_data(exchange, symbols):
    """
    실시간 데이터 수집
    :param exchange: 거래소 객체 (예: Binance)
    :param symbols: 거래 심볼 리스트 (예: ['BTC/USDT'])
    """
    for symbol in symbols:
        exchange.websocket_ticker(symbol, callback=handle_real_time_data)
```

#### (2) logger.py

기능: 실시간 데이터 로깅.
주요 함수:
```python
def log_real_time_data(data):
    """
    실시간 데이터 로깅
    :param data: 실시간으로 수집된 데이터
    """
    print(f"[LOG] {data}")
```

### 2️⃣ Signals 모듈

#### (1) generator.py

기능: 실시간 데이터를 기반으로 신호 생성.
주요 함수:
```python
def generate_real_time_signals(data):
    """
    실시간 데이터를 기반으로 매수/매도 신호 생성
    :param data: 실시간 데이터 (가격, 거래량 등)
    :return: 매수/매도 신호
    """
    if data['price'] > data['MA']:
        return 'BUY'
    elif data['price'] < data['MA']:
        return 'SELL'
    else:
        return 'HOLD'
```

#### (2) risk_management.py

기능: 주문 전 리스크 관리 수행.
주요 함수:
```python
def calculate_risk_position(account_balance, risk_tolerance, price):
    """
    리스크 기반 포지션 크기 계산
    :param account_balance: 계좌 잔액
    :param risk_tolerance: 최대 허용 손실 비율
    :param price: 현재 자산 가격
    :return: 계산된 포지션 크기
    """
    return (account_balance * risk_tolerance) / price
```

#### (3) filters.py

기능: 신호 필터링 및 유효성 검증.
주요 함수:
```python
def filter_signals(signal, market_conditions):
    """
    신호 필터링
    :param signal: 생성된 신호
    :param market_conditions: 현재 시장 상황
    :return: 유효성 검증된 신호
    """
    if market_conditions['volatility'] > threshold:
        return 'HOLD'
    return signal
```

### 3️⃣ Execution 모듈

#### (1) order_manager.py

기능: 매수/매도 주문 실행.
주요 함수:
```python
def execute_order(exchange, symbol, order_type, amount):
    """
    매수/매도 주문 실행
    :param exchange: 거래소 객체
    :param symbol: 거래 심볼
    :param order_type: 주문 유형 ('BUY' 또는 'SELL')
    :param amount: 주문 수량
    """
    if order_type == 'BUY':
        exchange.create_market_buy_order(symbol, amount)
    elif order_type == 'SELL':
        exchange.create_market_sell_order(symbol, amount)
```

#### (2) position_tracker.py

기능: 현재 포지션 상태 추적.
주요 함수:
```python
def track_position(exchange, symbol):
    """
    현재 포지션 상태 추적
    :param exchange: 거래소 객체
    :param symbol: 거래 심볼
    """
    return exchange.fetch_positions(symbol)
```

#### (3) error_handler.py

기능: 장애 복구 처리.
주요 함수:
```python
def handle_error(error):
    """
    장애 발생 시 복구 처리
    :param error: 발생한 오류
    """
    print(f"Error: {error}")
    # 재시도 로직 추가
```

---

## 🔗 통신 구조 및 의존성

### 1️⃣ 통신 구조

```
real_time_collector.py → generator.py → filters.py → risk_management.py → order_manager.py → position_tracker.py
```

### 2️⃣ 의존성

외부 라이브러리:
- ccxt: 거래소 API 호출.
- websockets: 실시간 데이터 수집.
- pandas: 데이터 처리.

내부 모듈:
- logger: 실시간 데이터 로깅.
- error_handler: 장애 복구 처리.

---

## 📅 개발 일정

### 1. 설계 및 검토
실시간 데이터 수집 설계: 3일
신호 생성 및 리스크 관리 설계: 3일
주문 실행 및 상태 관리 설계: 3일

### 2. 개발 및 테스트
실시간 데이터 수집 구현: 5일
실시간 신호 생성 및 리스크 관리 구현: 5일
주문 실행 및 상태 관리 구현: 5일

### 3. 통합 및 프로토타입 테스트
실시간 데이터 → 신호 생성 → 매매 실행 통합 테스트: 5일

## 📑 테스트 계획

### 1. 유닛 테스트
실시간 데이터 수집(WebSocket) 테스트.
신호 생성 및 리스크 관리 테스트.
주문 실행 및 상태 관리 테스트.

### 2. 통합 테스트
실시간 데이터 → 신호 생성 → 주문 실행 흐름 검증.

### 3. 성능 테스트
실시간 데이터 처리 속도 및 주문 실행 속도 검증.






