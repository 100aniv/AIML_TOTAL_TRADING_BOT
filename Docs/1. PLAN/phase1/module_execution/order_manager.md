📁 execution/order_manager.md
📌 목적
Order Manager는 매수 및 매도 주문을 생성하고 관리하는 모듈입니다.
거래소 API를 활용하여 주문 상태를 실시간으로 추적하며, 주문 실행 및 취소 기능을 제공합니다.
📁 디렉터리 구조
plaintext
복사
편집
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
1️⃣ 주문 생성

매수 및 매도 주문을 생성하고 거래소 API를 통해 실행합니다.
2️⃣ 주문 상태 관리

주문 실행 후 거래소에서의 상태(성공, 실패, 대기)를 추적합니다.
3️⃣ 주문 취소

특정 조건에 따라 주문을 취소하거나 수정합니다.
📄 주요 함수 설명
1️⃣ create_order()
목적
매수 및 매도 주문을 생성합니다.
함수 설명
python
복사
편집
def create_order(symbol, quantity, order_type, price=None):
    """
    주문 생성 함수
    :param symbol: 거래 쌍 (예: BTC/USDT)
    :param quantity: 주문 수량
    :param order_type: 주문 유형 (시장가, 지정가 등)
    :param price: 지정가 주문일 경우 가격
    :return: 주문 결과
    """
    order = {
        "symbol": symbol,
        "quantity": quantity,
        "order_type": order_type,
        "price": price
    }
    # API 호출 로직 추가
    return order
2️⃣ track_order_status()
목적
주문 실행 후 상태를 확인하고 추적합니다.
함수 설명
python
복사
편집
def track_order_status(order_id, api_client):
    """
    주문 상태 추적 함수
    :param order_id: 주문 ID
    :param api_client: 거래소 API 클라이언트
    :return: 주문 상태
    """
    status = api_client.get_order_status(order_id)
    return status
3️⃣ cancel_order()
목적
특정 조건에 따라 주문을 취소합니다.
함수 설명
python
복사
편집
def cancel_order(order_id, api_client):
    """
    주문 취소 함수
    :param order_id: 주문 ID
    :param api_client: 거래소 API 클라이언트
    :return: 취소 결과
    """
    result = api_client.cancel_order(order_id)
    return result
🔗 통신 구조 및 의존성
통신 구조
plaintext
복사
편집
signals/generator.py → execution/order_manager.py → execution/position_tracker.py
주요 의존성
외부 라이브러리
ccxt: 거래소 API 호출.
requests: API 통신.
내부 모듈
api/binance_api.py: Binance 거래소 통합 API.
api/upbit_api.py: Upbit 거래소 통합 API.
logger.py: 주문 상태 로깅.
📘 참고 문서 및 링크
Binance API Documentation
Upbit API Documentation