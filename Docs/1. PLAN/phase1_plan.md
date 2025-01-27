## 📁 Docs/Plan/Phase1/README.md

### 📌 Phase 1: 기본 시스템 구축

### 📌 목적
- 거래소 데이터를 수집하고, 기본적인 기술적 지표를 계산하며, 간단한 매매 신호를 생성 및 실행.
- 데이터 기반의 프로토타입 트레이딩 시스템을 구축하여 전체 시스템 개발의 기초를 마련.

### 📂 디렉터리 구조
```plaintext
Docs/
└── Plan/
    └── Phase1/
        ├── README.md
project/
├── data/
│   ├── collector.py           # 거래소 데이터 수집
│   ├── real_time_collector.py # 실시간 데이터 수집
│   ├── data_storage.py        # 데이터 저장
│   ├── preprocessor.py        # 데이터 전처리
│   ├── logger.py              # 데이터 로깅
│   └── arbitrage_collector.py # 아비트라지 데이터 수집
├── indicators/
│   ├── trend_indicator.py     # 이동평균선 계산
│   ├── momentum_indicator.py  # RSI 계산
├── signals/
│   ├── generator.py           # 신호 생성
│   ├── filters.py             # 신호 필터링
│   ├── risk_management.py     # 리스크 관리
├── execution/
│   ├── order_manager.py       # 매수/매도 주문 실행
```

### 🛠️ 주요 모듈과 함수
1️⃣ **Data 모듈**
(1) collector.py
기능: 거래소 API(CCXT 등)를 통해 과거 데이터를 수집.
주요 함수:
```python
def fetch_historical_data(exchange_name, symbol, timeframe, since):
    """
    거래소에서 과거 데이터를 수집.
    :param exchange_name: 거래소 이름
    :param symbol: 거래 심볼
    :param timeframe: 시간 간격
    :param since: 데이터 시작 시간
    :return: 수집된 OHLCV 데이터
    """
    exchange = getattr(ccxt, exchange_name.lower())()
    return exchange.fetch_ohlcv(symbol, timeframe, since)
(2) data_storage.py
기능: 수집된 데이터를 SQLite 데이터베이스에 저장.
주요 함수:
```python
def store_data(conn, table_name, data):
    """
    데이터를 데이터베이스에 저장.
    :param conn: SQLite 연결 객체
    :param table_name: 저장할 테이블 이름
    :param data: 저장할 데이터 (Pandas DataFrame)
    """
    data.to_sql(table_name, conn, if_exists='append', index=False)
(3) preprocessor.py
기능: 결측치 처리, 이상치 제거, 데이터 정규화.
주요 함수:
```python
def preprocess_data(data):
    """
    데이터 전처리 함수
    :param data: 입력 데이터 (Pandas DataFrame)
    :return: 전처리된 데이터
    """
    data = data.dropna()
    data['zscore'] = (data['close'] - data['close'].mean()) / data['close'].std()
    return data
2️⃣ Indicators 모듈
(1) trend_indicator.py
기능: 이동평균선(MA) 계산.
주요 함수:
```python
def calculate_ma(data, window):
    """
    이동평균선 계산 함수
    :param data: 입력 데이터
    :param window: 이동평균 창 크기
    :return: 이동평균선
    """
    return data['close'].rolling(window=window).mean()
(2) momentum_indicator.py
기능: RSI 계산.
주요 함수:
```python
def calculate_rsi(data, period=14):
    """
    RSI 계산 함수
    :param data: 입력 데이터
    :param period: RSI 계산 기간
    :return: RSI 값
    """
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
3️⃣ Signals 모듈
(1) generator.py
기능: 이동평균선 교차 또는 RSI 기반으로 신호 생성.
주요 함수:
```python
def generate_signals(data):
    """
    매수/매도 신호 생성
    :param data: 입력 데이터
    :return: 신호가 포함된 데이터
    """
    data['signal'] = 0
    data.loc[data['MA_short'] > data['MA_long'], 'signal'] = 1
    data.loc[data['MA_short'] < data['MA_long'], 'signal'] = -1
    return data
🔗 통신 구조 및 의존성
1️⃣ 통신 구조
데이터 흐름:
```plaintext
collector.py → data_storage.py → preprocessor.py → indicators/ → signals/ → execution/
```
2️⃣ 의존성
외부 라이브러리:
ccxt: 거래소 API 호출.
sqlite3: 데이터베이스 저장.
pandas: 데이터프레임 처리.
내부 모듈:
logger: 이벤트 기록.

### 📅 개발 일정
1. **설계 및 검토**
데이터 모듈 설계: 5일
지표 및 신호 모듈 설계: 5일
매매 실행 모듈 설계: 5일
2. **개발 및 테스트**
데이터 모듈 구현 및 테스트: 7일
신호 모듈 구현 및 테스트: 7일
매매 실행 모듈 구현 및 테스트: 7일
3. 통합 및 프로토타입 테스트
데이터 → 지표 → 신호 → 실행 통합 테스트: 5일

### 📑 테스트 계획
1. **유닛 테스트**
각 모듈의 주요 기능을 개별적으로 검증.
예: /data/collector.py의 fetch_historical_data 테스트.
2. **통합 테스트**
데이터 수집 → 지표 계산 → 신호 생성 → 매매 실행의 전체 흐름 검증.
3. **성능 테스트**
과거 데이터 1년 분량으로 시스템 처리 성능 확인.
