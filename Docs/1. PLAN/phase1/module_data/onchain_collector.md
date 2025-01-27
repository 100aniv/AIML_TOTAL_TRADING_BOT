# 📁 Docs/Plan/Phase1/module/onchain_collector.md

---

## 📌 목적
- 블록체인 네트워크의 온체인 데이터를 수집하여 추가적인 시장 정보를 제공합니다.
- 네트워크 트랜잭션 데이터를 기반으로 시장 분석과 매매 전략의 보조 자료를 제공합니다.

---

## 📄 주요 기능
1. **노드 연결**:
   - 블록체인 네트워크 노드와 연결하여 데이터를 실시간으로 수집.
2. **트랜잭션 데이터 수집**:
   - 특정 트랜잭션 해시를 통해 상세한 트랜잭션 정보를 가져옴.
3. **데이터 필터링 및 저장**:
   - 필요한 필드만 추출하여 데이터베이스에 저장.
4. **로그 관리**:
   - 수집 성공 및 오류 발생 시 이벤트 로깅.

---

## 📁 디렉터리 구조
```plaintext
data/
├── __init__.py
├── arbitrage_collector.py
├── collector.py
├── data_storage.py
├── logger.py
├── onchain_collector.py         # 온체인 데이터를 수집하는 모듈
├── preprocessor.py
└── real_time_collector.py
```

### 🔍 주요 함수 설계
1️⃣ `connect_to_node(node_url: str) -> object`
- **설명**: 특정 블록체인 네트워크 노드에 연결.
- **입력**:
  - `node_url` (str): 블록체인 노드 URL.
- **출력**:
  - 연결 객체 또는 예외 발생 시 오류 메시지.
- **예제 코드**:
  ```python
  def connect_to_node(node_url: str) -> object:
    try:
        # 노드 연결 시도
        connection = BlockchainNode(node_url)
        logger.info(f"Connected to node: {node_url}")
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to node: {e}")
        raise
2️⃣ `fetch_onchain_data(transaction_hash: str) -> dict`
- **설명**: 특정 트랜잭션 해시로부터 데이터를 수집.
- **입력**:
  - `transaction_hash` (str): 블록체인 트랜잭션 해시.
- **출력**:
  - 트랜잭션 데이터 (dict).
- **예제 코드**:
  ```python
  def fetch_onchain_data(transaction_hash: str) -> dict:
    try:
        # 트랜잭션 데이터 수집
        transaction_data = node.get_transaction(transaction_hash)
        logger.info(f"Fetched data for transaction: {transaction_hash}")
        return transaction_data
    except Exception as e:
        logger.error(f"Failed to fetch transaction data: {e}")
        return {}
3️⃣ `filter_transaction_data(raw_data: dict) -> dict`
- **설명**: 트랜잭션 데이터에서 필요한 필드만 추출.
- **입력**:
  - `raw_data` (dict): 원시 트랜잭션 데이터.
- **출력**:
  - 필터링된 데이터 (dict).
- **예제 코드**:
  ```python
  def filter_transaction_data(raw_data: dict) -> dict:
    filtered_data = {
        "hash": raw_data.get("hash"),
        "from": raw_data.get("from"),
        "to": raw_data.get("to"),
        "value": raw_data.get("value"),
        "timestamp": raw_data.get("timestamp"),
    }
    logger.info(f"Filtered transaction data: {filtered_data}")
    return filtered_data
4️⃣ `save_onchain_data(data: dict)`
- **설명**: 필터링된 데이터를 SQLite 데이터베이스에 저장.
- **입력**:
  - `data` (dict): 필터링된 트랜잭션 데이터.
- **출력**:
  - 없음.
- **예제 코드**:
  ```python
  def save_onchain_data(data: dict):
    try:
        db_connection = sqlite3.connect(DB_PATH)
        cursor = db_connection.cursor()
        cursor.execute("""
            INSERT INTO onchain_data (hash, from_address, to_address, value, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (data["hash"], data["from"], data["to"], data["value"], data["timestamp"]))
        db_connection.commit()
        logger.info(f"Saved onchain data to database: {data}")
    except Exception as e:
        logger.error(f"Failed to save onchain data: {e}")
    finally:
        db_connection.close()
```

### 🔗 통신 구조 및 의존성
- **통신 구조**:
  - 데이터 흐름:
    - `connect_to_node` → `fetch_onchain_data` → `filter_transaction_data` → `save_onchain_data`.
- **의존성**:
  - `sqlite3`: 데이터 저장.
  - `logger`: 수집 및 저장 과정 로깅.

---

## 📘 참고 문서 및 링크
- Docs/Plan/Phase1/module_data.md
- Docs/Plan/Phase1/logger.md
- Docs/Plan/Phase1/data_storage.md

