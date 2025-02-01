# 📁 Docs/Plan/Phase1/README.md

---

## Phase 1: 데이터 수집 및 초기 모듈 개발

---

### 📌 목적
Phase 1의 주요 목적은 데이터 수집과 저장을 담당하는 초기 모듈을 설계 및 구현하여 프로젝트의 기본 토대를 구축하는 것입니다.

---

###  📁 디렉터리 구조
```plaintext
Docs/
└── Plan/
    └── Phase1/
        ├── README.md
        ├── 개발 계획.md
        └── module/
            ├── 데이터 수집 모듈 개발 계획.md
            ├── 데이터 저장 모듈 개발 계획.md
            └── 데이터 전처리 모듈 개발 계획.md
project/
├── data/
│   ├── __init__.py
│   ├── collector.py
│   ├── real_time_collector.py
│   ├── data_storage.py
│   ├── preprocessor.py
│   └── logger.py
└── main.py

---

### 🗂️ 개발 모듈 및 주요 기능
1️⃣ 데이터 수집 모듈
파일 위치: project/data/collector.py, project/data/real_time_collector.py
주요 기능:
거래소 API(CCXT)를 통해 OHLCV 데이터(Open, High, Low, Close, Volume) 수집.
실시간 데이터 수집 지원.
네트워크 오류 및 API 호출 실패 시 재시도 로직 구현.
2️⃣ 데이터 저장 모듈
파일 위치: project/data/data_storage.py
주요 기능:
SQLite 데이터베이스 초기화 및 테이블 생성.
중복 데이터 처리 및 효율적인 데이터 저장 로직.
데이터베이스와의 비동기 연결 구현(필요 시).
3️⃣ 데이터 전처리 모듈
파일 위치: project/data/preprocessor.py
주요 기능:
결측치 처리(예: 평균값 대체, 제거 등).
이상치 제거 및 정규화 작업.
주요 트레이딩 지표(예: 이동평균, RSI 등) 계산.
4️⃣ 로깅 모듈
파일 위치: project/data/logger.py
주요 기능:
데이터 수집 및 저장 작업의 로그 기록.
에러 및 성공 메시지를 파일 또는 콘솔로 출력.

---

### 📑 개발 단계 및 일정
1️⃣ 단계 1: 설계

각 모듈의 기능 정의 및 디렉터리 구조 확정.
설계 초안을 검토 후 승인.
2️⃣ 단계 2: 구현

각 모듈별로 독립적으로 개발 진행.
유닛 테스트 및 초기 디버깅.
3️⃣ 단계 3: 통합

모듈 간 통합 테스트 진행.
데이터 수집 → 데이터 저장 → 전처리로 이어지는 데이터 파이프라인 구축.
4️⃣ 단계 4: 검증

실제 거래소 데이터를 사용한 기능 테스트.
테스트 결과를 바탕으로 최종 디버깅 및 성능 최적화.

---

### 📑 환경 설정
Python 패키지 설치
# 주요 패키지 설치(Powershell)
pip install ccxt pandas numpy sqlite3
환경 변수 설정
데이터베이스 경로와 API 키 설정을 위한 .env 파일 생성:
# .env 파일 예시
DB_PATH=./data/trading_bot.db
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key

---

### 🔗 통신 구조 및 의존성
1️⃣ 통신 구조
데이터 수집 모듈 → 데이터 저장 모듈(SQLite)에 데이터를 저장.
데이터 전처리 모듈 → 저장된 데이터를 불러와 클린닝 작업 수행.
2️⃣ 의존성
ccxt: 거래소 API 통합.
sqlite3: 데이터 저장.
dotenv: 환경 변수 로드.
pandas: 데이터 전처리.
numpy: 데이터 전처리.

---

###📘 참고 문서 및 링크
CCXT Documentation
SQLite Documentation
Pandas Documentation
NumPy Documentation