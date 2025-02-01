# 📁 Docs/Plan/Phase1/arbitrage_collector.md

---

## 📌 목적
- **아비트라지(차익거래)** 전략에 필요한 데이터를 수집하고, 거래소 간 가격 차이를 분석하여 기회를 포착하기 위한 모듈입니다.
- 실시간으로 데이터를 수집하여 시장의 변동성을 파악하고, 최적의 거래 기회를 제공합니다.

---

## 📁 디렉터리 구조
```plaintext
Docs/
└── Plan/
    └── Phase1/
        └── arbitrage_collector.md
project/
└── data/
    ├── __init__.py
    ├── arbitrage_collector.py  # 해당 파일
    ├── collector.py
    ├── data_storage.py
    ├── logger.py
    ├── onchain_collector.py
    ├── preprocessor.py
    └── real_time_collector.py
```

---

## ✨ 주요 기능

1️⃣ **거래소 데이터 수집**
   - 다중 거래소(Binance, Upbit 등)에서 실시간 가격 데이터를 수집.

2️⃣ **가격 차이 계산**
   - 거래소 간 가격 차이를 분석하고, 아비트라지 기회 포착.

3️⃣ **알림 시스템**
   - 아비트라지 기회 발생 시 알림 전송(텔레그램, 로깅).

4️⃣ **오류 처리**
   - 데이터 수집 실패 시 재시도 로직 구현.

---

## 🛠️ 주요 함수

### 1️⃣ `fetch_arbitrage_data(exchange_list, symbols)`
- **목적**: 거래소 목록과 자산 심볼을 입력받아 가격 데이터를 수집.
- **입력**:
  - `exchange_list`: 거래소 목록 (예: `["Binance", "Upbit"]`).
  - `symbols`: 자산 심볼 목록 (예: `["BTC/USDT", "ETH/USDT"]`).
- **출력**: 각 거래소의 가격 데이터 리스트.
- **구현**:
```python
import ccxt

def fetch_arbitrage_data(exchange_list, symbols):
    data = {}
    for exchange_name in exchange_list:
        try:
            exchange = getattr(ccxt, exchange_name.lower())()
            data[exchange_name] = {}
            for symbol in symbols:
                ticker = exchange.fetch_ticker(symbol)
                data[exchange_name][symbol] = ticker['last']
        except Exception as e:
            print(f"Error fetching data from {exchange_name}: {e}")
    return data
```

### 2️⃣ `calculate_arbitrage_opportunity(data)`
- **목적**: 수집된 가격 데이터를 비교하여 아비트라지 기회를 계산.
- **입력**:
  - `data`: 거래소별 가격 데이터 (딕셔너리 형태).
- **출력**: 아비트라지 기회가 있는 거래소와 자산 정보.
- **구현**:
```python
def calculate_arbitrage_opportunity(data):
    opportunities = []
    for symbol in data[list(data.keys())[0]]:
        prices = [(exchange, data[exchange][symbol]) for exchange in data]
        prices.sort(key=lambda x: x[1])
        lowest = prices[0]
        highest = prices[-1]
        if highest[1] / lowest[1] > 1.01:  # 1% 이상 차이
            opportunities.append({
                'symbol': symbol,
                'buy_from': lowest[0],
                'sell_to': highest[0],
                'profit_percent': (highest[1] / lowest[1] - 1) * 100
            })
    return opportunities
```

### 3️⃣ `send_arbitrage_alert(opportunities)`
- **목적**: 발견된 아비트라지 기회를 텔레그램 알림 또는 로깅 시스템으로 전송.
- **입력**:
  - `opportunities`: 아비트라지 기회 리스트.
- **출력**: 알림 전송 결과.
- **구현**:
```python
import requests

def send_arbitrage_alert(opportunities):
    for opportunity in opportunities:
        message = (f"Arbitrage Opportunity Detected:\n"
                   f"Symbol: {opportunity['symbol']}\n"
                   f"Buy from: {opportunity['buy_from']}\n"
                   f"Sell to: {opportunity['sell_to']}\n"
                   f"Profit: {opportunity['profit_percent']:.2f}%")
        # 텔레그램 알림
        requests.post(
            url=f"https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage",
            data={"chat_id": "<YOUR_CHAT_ID>", "text": message}
        )
        print(message)
```

### 4️⃣ `handle_api_error(exception)`
- **목적**: API 호출 실패 시 로그 기록 및 재시도 로직 구현.
- **입력**: 발생한 예외 객체.
- **출력**: 없음.
- **구현**:
```python
import logging

def handle_api_error(exception):
    logging.error(f"API Error: {exception}")
    # 필요 시 재시도 로직 구현
```

---

## 🔗 통신 구조 및 의존성

### 통신 구조
1️⃣ **데이터 흐름**:
- `fetch_arbitrage_data` → 거래소별 데이터 수집
- `calculate_arbitrage_opportunity` → 가격 차이 분석
- `send_arbitrage_alert` → 알림 시스템으로 결과 전송

### 의존성
- **`ccxt`**: 거래소 API와 통신.
- **`requests`**: 텔레그램 알림 전송.
- **`logging`**: 오류 기록.

---

## 📘 참고 문서 및 링크
- [Docs/Plan/Phase1/module_data.md](Docs/Plan/Phase1/module_data.md)
- [Docs/Plan/Phase1/logger.md](Docs/Plan/Phase1/logger.md)
- [Docs/Plan/Phase1/data_storage.md](Docs/Plan/Phase1/data_storage.md)
