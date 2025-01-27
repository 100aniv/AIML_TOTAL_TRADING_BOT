# 📁 execution/error_handler.md

---

## 📌 목적
**Error Handler**는 매매 실행 중 발생하는 다양한 오류를 감지하고 복구하기 위한 모듈입니다.  
네트워크 장애, 주문 실패, API 호출 오류 등의 문제를 자동으로 처리하며, 시스템 안정성을 보장합니다.

---

## 📁 디렉터리 구조
```plaintext
execution/
├── __init__.py              # 모듈 초기화 파일
├── api/                     # 거래소 API 통합
│   ├── binance_api.py       # Binance API 통합
│   ├── upbit_api.py         # Upbit API 통합
├── order_manager.py         # 주문 생성 및 관리
├── position_tracker.py      # 포지션 추적 및 상태 관리
├── risk_manager.py          # 리스크 관리
└── error_handler.py         # 장애 복구 및 에러 처리
✨ 주요 기능
1️⃣ 오류 감지

네트워크 장애, API 호출 실패 등의 다양한 오류를 감지합니다.
2️⃣ 장애 복구

감지된 오류를 분석하고 복구 작업을 수행합니다.
3️⃣ 로깅

오류 발생 원인과 복구 과정을 기록하여 문제 해결의 근거를 제공합니다.
📄 주요 함수 설명
1️⃣ handle_error()
목적
주어진 오류 코드를 기반으로 적절한 복구 작업을 수행합니다.

함수 설명
python
복사
편집
def handle_error(error_code, context=None):
    """
    장애 처리 함수
    :param error_code: 에러 코드
    :param context: 에러 발생 상황
    :return: 복구 상태
    """
    print(f"Error occurred: {error_code}, Context: {context}")
    if error_code == "NETWORK_ERROR":
        recover_network()
    elif error_code == "ORDER_FAILED":
        retry_order(context)
    else:
        log_error(error_code, context)
    return "Handled"
2️⃣ recover_network()
목적
네트워크 장애를 복구합니다.

함수 설명
python
복사
편집
def recover_network():
    """
    네트워크 장애 복구 함수
    :return: 복구 상태
    """
    print("Attempting to recover network...")
    # 네트워크 복구 로직 추가
    return "Network Recovered"
3️⃣ retry_order()
목적
주문 실패 시 재시도를 수행합니다.

함수 설명
python
복사
편집
def retry_order(order_context):
    """
    주문 재시도 함수
    :param order_context: 실패한 주문 정보
    :return: 재시도 결과
    """
    print(f"Retrying order: {order_context}")
    # 주문 재시도 로직 추가
    return "Order Retried"
4️⃣ log_error()
목적
발생한 오류를 기록합니다.

함수 설명
python
복사
편집
def log_error(error_code, context):
    """
    오류 로깅 함수
    :param error_code: 에러 코드
    :param context: 에러 발생 상황
    """
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"Error Code: {error_code}, Context: {context}\n")
    print(f"Error logged: {error_code}")
🔗 통신 구조 및 의존성
통신 구조
plaintext
복사
편집
execution/order_manager.py → execution/error_handler.py
주요 의존성
외부 라이브러리:
requests: 네트워크 상태 확인 및 API 호출.
time: 재시도 딜레이 추가.
내부 모듈:
order_manager.py: 주문 관련 오류 정보 전달.
logger.py: 오류 로깅.
📅 개발 일정
1️⃣ 설계 및 검토 (1일)

장애 복구 로직 및 오류 유형 정의.
2️⃣ 기능 개발 (2일)

네트워크 복구, 주문 재시도, 오류 로깅 기능 구현.
3️⃣ 테스트 및 통합 (1일)

주문 관리 및 리스크 관리 모듈과의 통합 테스트.
📑 테스트 계획
1️⃣ 유닛 테스트

장애 복구 및 재시도 함수의 동작 검증.
2️⃣ 통합 테스트

주문 관리와의 통합 검증.
3️⃣ 시스템 테스트

실시간 장애 상황에서 복구 로직의 반응 시간 및 성공률 검증.

## 📘 참고 문서 및 링크
1. 외부 라이브러리
- Binance API Documentation
- Upbit API Documentation
2. 내부 모듈
- Docs/Plan/Phase1/module_execution.md
- Docs/Plan/Phase1/module_data.md
- Docs/Plan/Phase1/module_indicators.md
- Docs/Plan/Phase1/module_signals.md
- Docs/Plan/Phase1/module_uiux.md