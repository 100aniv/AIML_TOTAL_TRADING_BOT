# 📁 Docs/Plan/Phase1/module/collector.md

---

## 📌 목적
- 거래소 데이터를 주기적으로 수집하여 데이터베이스에 저장할 수 있는 메인 모듈입니다.
- 다양한 거래소(API)와의 통신을 통해 OHLCV 데이터를 가져오고, 데이터 품질을 검증한 뒤 저장 단계로 넘깁니다.

---

## 🛠️ 주요 기능
1. **거래소 API 연결**
   - 거래소 인증키(API Key)를 사용하여 API 연결 초기화.
   - 지원 거래소: Binance, Upbit 등.
2. **데이터 수집**
   - 일정 주기로 OHLCV(Open, High, Low, Close, Volume) 데이터 수집.
   - 데이터 유효성 검증(결측값 및 이상치 처리).
3. **오류 처리**
   - API 호출 실패 시 재시도 및 오류 로그 기록.
   - 네트워크 이슈 또는 거래소 제한에 대한 예외 처리.

---

## 🧩 주요 함수

### 1️⃣ `initialize_connection(api_key: str, secret_key: str) -> object`
- **설명**: 거래소 API 인증키를 사용해 연결 초기화.
- **입력값**:
  - `api_key`: 거래소 API 키.
  - `secret_key`: 거래소 API 시크릿 키.
- **출력값**:
  - 연결된 API 객체.
- **세부 구현**:
  ```python
  import ccxt

  def initialize_connection(api_key: str, secret_key: str) -> object:
      """
      거래소 API 연결 초기화
      :param api_key: 거래소 API 키
      :param secret_key: 거래소 API 시크릿 키
      :return: ccxt 거래소 객체
      """
      try:
          exchange = ccxt.binance({
              'apiKey': api_key,
              'secret': secret_key
          })
          # 연결 테스트
          exchange.fetch_balance()
          print("API 연결 성공")
          return exchange
      except Exception as e:
          print(f"API 연결 실패: {e}")
          raise e
### 2️⃣ `fetch_ohlcv(exchange: object, symbol: str, timeframe: str) -> pd.DataFrame`
- **설명**: 특정 자산(Symbol)의 OHLCV 데이터를 요청.
- **입력값**:
  - `exchange`: 초기화된 거래소 API 객체.
  - `symbol`: 자산 심볼 (예: BTC/USDT).
  - `timeframe`: 데이터 간격 (예: 1m, 1h, 1d).
- **출력값**:
  - Pandas DataFrame 형태의 OHLCV 데이터.
- **세부 구현**:
  ```python
  import pandas as pd

def fetch_ohlcv(exchange: object, symbol: str, timeframe: str) -> pd.DataFrame:
    """
    OHLCV 데이터 수집
    :param exchange: ccxt 거래소 객체
    :param symbol: 거래 심볼 (예: BTC/USDT)
    :param timeframe: 시간 프레임 (예: 1m, 1h)
    :return: OHLCV 데이터프레임
    """
    try:
        raw_data = exchange.fetch_ohlcv(symbol, timeframe)
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame(raw_data, columns=columns)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        print(f"데이터 수집 성공: {len(df)} 개의 데이터")
        return df
    except Exception as e:
        print(f"데이터 수집 실패: {e}")
        raise e
3️⃣ `handle_api_error(exception: Exception) -> None`
- **설명**: API 호출 실패 시 예외를 처리하고 재시도 로직 실행.
- **입력값**:
  - `exception`: 발생한 예외 객체.
- **출력값**:
  - `None`.
- **세부 구현**:
  ```python
  import time

def handle_api_error(exception: Exception) -> None:
    """
    API 호출 오류 처리
    :param exception: 발생한 예외 객체
    """
    print(f"API 오류 발생: {exception}")
    print("5초 후 재시도...")
    time.sleep(5)  # 재시도 전에 대기 시간 추가
```

---

## 🔗 통신 구조 및 의존성
1️⃣ 통신 구조
- 입력: 사용자가 설정한 거래소와 자산 심볼.
- 출력:
수집된 데이터는 data_storage.py 모듈로 전달되어 데이터베이스에 저장.
흐름:
plaintext
collector.py → data_storage.py → preprocessor.py
2️⃣ 의존성
외부 라이브러리:
ccxt: 거래소 API 호출.
pandas: 데이터 처리 및 분석.
내부 모듈:
logger: 데이터 수집 이벤트 및 오류 로깅.
data_storage: 수집된 데이터를 데이터베이스에 저장.
### 📘 참고 문서
- Docs/Plan/Phase1/module/data_storage.md
- Docs/Plan/Phase1/module/logger.md
- Docs/Plan/Phase1/module/preprocessor.md
