# 📁 Docs/Plan/Phase1/module_data_init.md

---

## 📌 목적
- `data` 모듈을 패키지로 인식하게 하고, 공용 함수와 클래스를 초기화합니다.
- 다른 모듈에서 `data` 패키지를 효율적으로 사용할 수 있도록 설정합니다.

---

## 📄 주요 역할
1. `data` 모듈 내의 주요 클래스 및 함수 초기화.
2. 다른 모듈에서 사용할 수 있도록 데이터베이스 경로, 공용 상수 및 유틸리티 로드.
3. 환경 변수 설정 및 초기화.

---

## ✨ 주요 함수 및 구현 초안

### 1️⃣ load_environment()
**목적**: `.env` 파일에서 환경 변수를 로드하여 설정.

```python
from dotenv import load_dotenv
import os
```
def load_environment():
    """
    환경 변수를 로드하고 설정하는 함수.
    """
    load_dotenv()
    db_path = os.getenv("DB_PATH")
    api_key = os.getenv("BINANCE_API_KEY")
    secret_key = os.getenv("BINANCE_SECRET_KEY")

    if not db_path or not api_key or not secret_key:
        raise EnvironmentError("환경 변수가 제대로 설정되지 않았습니다.")

### 2️⃣ initialize_logger()
목적: logger.py에서 정의된 로거를 초기화.

'''python
from .logger import configure_logger
'''
def initialize_logger():
    """
    로깅 초기화 설정.
    """
    configure_logger(log_file="./logs/system.log")
### 3️⃣ import_data_modules()
목적: data 모듈의 주요 클래스 및 함수 초기화.
from .collector import fetch_ohlcv_data
from .arbitrage_collector import fetch_arbitrage_data
from .data_storage import initialize_database, store_data
from .preprocessor import remove_outliers, scale_data
from .real_time_collector import connect_to_websocket, process_real_time_data

### 📄 통신 구조 및 의존성

### 1️⃣ 통신 구조
__init__.py는 다른 모듈에서 data 패키지를 호출할 때 자동으로 실행되며, data 내부의 주요 함수 및 클래스를 초기화합니다.
환경 변수는 .env 파일을 통해 로드되며, 모든 모듈에서 공유됩니다.

### 2️⃣ 의존성
dotenv: 환경 변수 로드.
os: 시스템 환경 변수 접근.
logger: 로그 관리.

### 🔗 참고 파일 및 문서
- [Docs/Plan/Phase1/module_data.md](Docs/Plan/Phase1/module_data.md)
- [Docs/Plan/Phase1/module_data_logger.md](Docs/Plan/Phase1/module_data_logger.md)
- [Docs/Plan/Phase1/module_data_collector.md](Docs/Plan/Phase1/module_data_collector.md)
