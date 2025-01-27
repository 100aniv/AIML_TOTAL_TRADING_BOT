# 📁 Docs/Plan/Phase1/module/logger.md

---

## 📌 목적
- 데이터 수집 및 저장, 전처리 과정에서 발생하는 주요 이벤트 및 오류를 기록하기 위해 설계된 로깅 모듈입니다.
- 모든 로그는 지정된 포맷에 따라 콘솔 및 파일로 출력되며, 시스템 디버깅 및 문제 해결에 활용됩니다.

---

## 📁 주요 기능
1. **로그 설정 초기화**
   - 로그 파일 경로 및 로그 포맷 지정.
   - 로깅 레벨(Info, Warning, Error 등) 설정.
2. **이벤트 로깅**
   - 주요 이벤트 및 프로세스 상태를 기록.
3. **오류 로깅**
   - 발생한 예외와 관련된 상세 정보를 기록.
4. **외부 알림 연동**
   - 주요 오류 발생 시 텔레그램 알림 발송 기능(선택적 구현).

---

## 🧩 주요 함수

### 1️⃣ `configure_logger(log_file: str) -> logging.Logger`
- **설명**: 로그 설정을 초기화하고 로거 객체를 반환합니다.
- **입력값**:
  - `log_file`: 로그 파일 경로.
- **출력값**:
  - 초기화된 로거 객체.
- **세부 구현**:
  ```python
  import logging

  def configure_logger(log_file: str) -> logging.Logger:
      """
      로거 초기화 및 설정
      :param log_file: 로그 파일 경로
      :return: 초기화된 로거 객체
      """
      logger = logging.getLogger('trading_bot_logger')
      logger.setLevel(logging.DEBUG)

      # 콘솔 핸들러
      console_handler = logging.StreamHandler()
      console_handler.setLevel(logging.INFO)

      # 파일 핸들러
      file_handler = logging.FileHandler(log_file)
      file_handler.setLevel(logging.DEBUG)

      # 포맷 설정
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      console_handler.setFormatter(formatter)
      file_handler.setFormatter(formatter)

      # 핸들러 추가
      logger.addHandler(console_handler)
      logger.addHandler(file_handler)

      return logger
  ```

### 2️⃣ `log_event(logger: logging.Logger, event_type: str, message: str) -> None`
- **설명**: 특정 이벤트를 기록합니다.
- **입력값**:
  - `logger`: 로거 객체.
  - `event_type`: 이벤트 타입(예: INFO, WARNING, ERROR).
  - `message`: 기록할 메시지.
- **출력값**:
  - `None`.
- **세부 구현**:
  ```python
    def log_event(logger: logging.Logger, event_type: str, message: str) -> None:
    """
    이벤트 로깅
    :param logger: 로거 객체
    :param event_type: 이벤트 타입
    :param message: 로그 메시지
    """
    if event_type == "INFO":
        logger.info(message)
    elif event_type == "WARNING":
        logger.warning(message)
    elif event_type == "ERROR":
        logger.error(message)
  ```

### 3️⃣ `log_error(logger: logging.Logger, error_message: str) -> None`
- **설명**: 발생한 오류를 기록합니다.
- **입력값**:
  - `logger`: 로거 객체.
  - `error_message`: 오류 메시지.
- **출력값**:
  - `None`
- **세부 구현**:
  ```python
  def log_error(logger: logging.Logger, error_message: str) -> None:
    """
    오류 로깅
    :param logger: 로거 객체
    :param error_message: 오류 메시지
    """
    logger.error(f"Error occurred: {error_message}")

### 4️⃣ `send_telegram_alert(message: str, bot_token: str, chat_id: str) -> None`
- **설명**: 텔레그램 알림을 발송합니다.
- **입력값**:
  - `message`: 발송할 메시지.
  - `bot_token`: 텔레그램 봇 토큰.
  - `chat_id`: 텔레그램 채널 ID.
- **출력값**:
  - `None`.
- **세부 구현**:
  ```python
  import requests

def send_telegram_alert(message: str, bot_token: str, chat_id: str) -> None:
    """
    텔레그램 알림 전송
    :param message: 발송할 메시지
    :param bot_token: 텔레그램 봇 토큰
    :param chat_id: 텔레그램 채널 ID
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=data)
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram alert: {e}")
  ```

### 🔗 통신 구조 및 의존성
1️⃣ 통신 구조
- 입력:
  - 모든 모듈에서 발생한 로그 및 오류 데이터를 입력받아 기록.
- 출력:
로깅 메시지는 콘솔 및 파일에 기록.
  - 주요 오류는 텔레그램 알림으로 전송(선택적).
- 흐름:
  - `collector.py` → `logger.py`
  - `data_storage.py` → `logger.py`
  - `preprocessor.py` → `logger.py`
2️⃣ 의존성
- 외부 라이브러리:
  - `logging`: 기본 로깅 구현.
  - `requests`: 텔레그램 알림 전송.
- 내부 모듈:
  - 모든 주요 모듈에서 의존하여 로깅 메시지를 기록.

### 📘 참고 문서
- `Docs/Plan/Phase1/module/collector.md`
- `Docs/Plan/Phase1/module/data_storage.md`
- `Docs/Plan/Phase1/module/preprocessor.md`
