# 📁 Docs/Test/Phase1/Data_Module_Test.md

---

## 📌 목적
- `data` 모듈의 각 파일을 독립적으로 테스트하여 정확한 기능 수행을 확인합니다.
- 단위 테스트 완료 후 Git으로 버전 관리하여 작업 기록을 체계적으로 유지합니다.

---

## 📁 디렉터리 구조
```plaintext
Docs/
└── Test/
    └── Phase1/
        ├── Data_Module_Test.md
project/
├── data/
│   ├── __init__.py
│   ├── arbitrage_collector.py
│   ├── collector.py
│   ├── data_storage.py
│   ├── logger.py
│   ├── onchain_collector.py
│   ├── preprocessor.py
│   └── real_time_collector.py
└── tests/
    └── test_data_module.py  # 모든 단위 테스트를 포함한 파일
```
## 🔍 테스트 계획
## 1️⃣ 테스트 파일: test_data_module.py
목적:data 모듈의 모든 주요 기능 및 함수의 동작을 개별적으로 검증합니다.

## 2️⃣ 테스트 대상 모듈 및 주요 테스트 항목
## 1. arbitrage_collector.py
테스트 목표: 아비트라지 데이터를 정확히 수집하고 조건에 따라 알림을 전송하는지 확인.
테스트 시나리오:
유효한 거래소 목록 및 자산 심볼로 데이터 수집.
수집 실패 시 재시도 로직 동작 확인.
python ```
from data.arbitrage_collector import fetch_arbitrage_data, calculate_arbitrage_opportunity

def test_fetch_arbitrage_data():
    data = fetch_arbitrage_data(["Binance", "Upbit"], ["BTC/USDT"])
    assert len(data) > 0
    assert "Binance" in data and "Upbit" in data

def test_calculate_arbitrage_opportunity():
    data = [{"exchange": "Binance", "price": 30000}, {"exchange": "Upbit", "price": 30500}]
    result = calculate_arbitrage_opportunity(data)
    assert result["arbitrage"] == True
    assert result["profit"] > 0

## 2. collector.py
테스트 목표: API에서 데이터를 수집하고 적절히 반환.
테스트 시나리오:
API 키와 시크릿 키를 사용한 초기 연결.
특정 자산 심볼 및 시간 프레임으로 데이터 수집.
예제 코드:
python ```
from data.collector import initialize_connection, fetch_ohlcv_data

def test_initialize_connection():
    connection = initialize_connection("api_key", "secret_key")
    assert connection is not None

def test_fetch_ohlcv_data():
    data = fetch_ohlcv_data("BTC/USDT", "1h")
    assert data is not None
    assert "open" in data and "close" in data

## 3. data_storage.py
테스트 목표: 데이터베이스에 데이터를 올바르게 저장.
테스트 시나리오:
데이터베이스 초기화 및 테이블 생성.
중복 데이터 제거.
예제 코드:
python ```
from data.data_storage import initialize_database, store_data

def test_initialize_database():
    conn = initialize_database("./data/trading_bot.db")
    assert conn is not None

def test_store_data():
    sample_data = {"symbol": "BTC/USDT", "price": 30000}
    result = store_data("market_data", sample_data)
    assert result == True

## 4. logger.py
테스트 목표: 로그 기록 및 오류 로그를 정확히 출력.
테스트 시나리오:
로그 파일 생성.
오류 메시지 기록.
예제 코드:
python
from data.logger import configure_logger, log_error

def test_configure_logger():
    logger = configure_logger("test_log.log")
    assert logger is not None

def test_log_error():
    log_error("Test error message")
    # 로그 파일 확인 필요
🧪 테스트 실행 및 Git 업데이트 명령어

## 테스트 실행
bash ```
## 모든 테스트 실행
pytest tests/test_data_module.py --disable-warnings

## Git 업데이트
bash ```

# 변경 사항 확인
git status

# 변경 사항 스테이징
git add .

# 변경 사항 커밋
git commit -m "Phase 1: 데이터 모듈 단위 테스트 완료"

# 원격 저장소로 푸시
git push origin feature/phase1-data-tests

📘 참고 문서 및 링크
Docs/Plan/Phase1/Data_Module_Plan.md
Docs/Test/Phase1/Data_Module_Test.md

### 🔗 참고 파일 및 문서
- [Docs/Plan/Phase1/Data_Module_Plan.md](Docs/Plan/Phase1/Data_Module_plan.md)
- [Docs/Test/Phase1/Data_Module_test.md](Docs/Plan/Phase1/Data_Module_test.md)
