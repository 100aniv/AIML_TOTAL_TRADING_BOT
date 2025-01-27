# 🗋 Docs/Plan/Phase1/module/real_time_collector.md

---

## 📌 목적
- 실시간으로 거래 데이터를 수징하여 프로젝트의 즉각적 의사결정을 지원하는 모듈입니다.
- WebSocket 결합을 통해 실시간 데이터를 처리하고, 이를 데이터 저장 모듈과 연계합니다.

---

## 🗋 디렉터리 구조
```plaintext
data/
├── __init__.py                # 모듈 초기화 파일
├── arbitrage_collector.py     # 아비트라지 거래를 위한 데이터 수징
├── collector.py               # 일반 거래 데이터를 수징하는 메인 모듈
├── data_storage.py            # 수징된 데이터를 저장하는 모듈
├── logger.py                  # 로긍 및 오류 기록 모듈
├── onchain_collector.py       # 온체인 데이터를 수징하는 모듈
├── preprocessor.py            # 데이터 전체리를 수행하는 모듈
└── real_time_collector.py     # 실시간 데이터 수징 모듈
```

---

## 📄 주요 파일 설명

### 1. `real_time_collector.py`

**목적:**
- WebSocket API를 활용하여 실시간 데이터를 수징.
- 필요한 자사와 시장 정보를 설정하여 제한된 데이터를 수징.

**관련 기능:**
1. WebSocket 결합을 통해 실시간 데이터 수징.
2. 수징된 데이터의 검증 및 저장 개선.
3. 배우와 데이터 컨지시 구현.

---

## 📄 주요 역할 및 기능
### 1️⃣ 실시간 거래 데이터 수집

- WebSocket API를 활용하여 실시간으로 데이터를 수집.
- 필요한 자산과 시장 정보를 설정하여 제한된 데이터를 수집.

### 2️⃣ 데이터 처리

- 수집된 데이터를 검증하고 저장 가능한 형태로 정리.
- 이상 데이터 필터링 및 정규화 작업.

### 3️⃣ 실시간 데이터 저장

- `data_storage.py`와 통합하여 데이터베이스에 저장.
- 처리된 데이터를 바로 저장하거나 로깅.

### 4️⃣ 버퍼링 및 데이터 캐싱

- 일시적으로 데이터 손실을 방지하기 위해 버퍼를 사용.
- 캐싱된 데이터를 주기적으로 확인 및 저장.

---

## 📋 주요 함수
### 1️⃣ `connect_to_websocket`
- **설명:** WebSocket 결합을 초기화 하고 서버와 통신.
- **입력:** `url` (string) - WebSocket 서버의 URL.
- **출력:** WebSocket 결합 객체.
```python
def connect_to_websocket(url: str):
    """
    WebSocket 결합을 초기화합니다.

    Args:
        url (str): WebSocket 서버의 URL.

    Returns:
        websocket.WebSocketApp: WebSocket 결합 객체.
    """
    import websocket

    def on_message(ws, message):
        process_real_time_data(message)

    def on_error(ws, error):
        log_error(f"WebSocket Error: {error}")

    ws = websocket.WebSocketApp(
        url,
        on_message=on_message,
        on_error=on_error
    )
    return ws
```

---

### 2. `process_real_time_data`
- **설명:** 실시간 데이터를 처리하여 저장 가능한 형태로 변환.
- **입력:** `data` (json/dict) - 수신된 데이터.
- **출력:** None (데이터는 저장 모듈에 전달되면).
```python
def process_real_time_data(data: dict):
    """
    수신된 실시간 데이터를 처리합니다.

    Args:
        data (dict): WebSocket으로 수신된 데이터.

    Returns:
        None
    """
    from data_storage import store_data

    # 데이터 필터링
    if "price" not in data or "volume" not in data:
        log_error("Incomplete data received.")
        return

    # 데이터 저장
    formatted_data = {
        "price": data["price"],
        "volume": data["volume"],
        "timestamp": data.get("timestamp", None)
    }
    store_data("real_time_table", formatted_data)
```

---

### 3. `start_real_time_collection`
- **설명:** WebSocket 결합을 시작하여 실시간 데이터 수징 루프 실행.
- **입력:** `url` (string) - WebSocket URL.
- **출력:** None.
```python
def start_real_time_collection(url: str):
    """
    실시간 데이터 수징을 시작합니다.

    Args:
        url (str): WebSocket 서버의 URL.

    Returns:
        None
    """
    ws = connect_to_websocket(url)
    ws.run_forever()
```

---

## 🔗 통신 구조 및 의존성

1. **통신 구조**
- 실시간 데이터(WebSocket) → `process_real_time_data` → 데이터 저장(SQL).
- 오류 및 이벤트 기록: `logger.py` 통합.

2. **의종 관계**
- `websocket`: 실시간 데이터 통신.
- `data_storage`: 데이터 저장.
- `logger`: 로긍 및 오류 처리.

---

## 📘 참고 문서 및 링크
- [Docs/Plan/Phase1/module_data.md](../module_data.md)
- [Docs/Plan/Phase1/module/data_storage.md](data_storage.md)
- [Docs/Plan/Phase1/module/logger.md](logger.md)

---
