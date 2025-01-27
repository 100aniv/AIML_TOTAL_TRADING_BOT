# 📁 execution/api/binance_api.md

---

## 📌 목적
**Binance API 모듈**은 Binance 거래소와 통합하여 주문 실행, 데이터 조회, 계정 상태 확인 등의 작업을 수행합니다.  
이 모듈은 거래소 API를 통해 실시간 트레이딩 데이터를 가져오고 매수/매도 주문을 실행합니다.

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
1️⃣ API 인증

Binance API 키와 시크릿 키를 사용하여 인증을 처리합니다.
2️⃣ 주문 실행

시장가 및 지정가 주문을 생성하고 실행합니다.
3️⃣ 데이터 조회

실시간 가격 데이터 및 주문 상태를 조회합니다.
4️⃣ 계정 상태

계정 자산 및 잔액 정보를 가져옵니다.
📄 주요 함수 설명
1️⃣ initialize_client()
목적
Binance API 클라이언트를 초기화합니다.

함수 설명
python
복사
편집
def initialize_client(api_key, api_secret):
    """
    Binance API 클라이언트 초기화
    :param api_key: Binance API 키
    :param api_secret: Binance 시크릿 키
    :return: Binance 클라이언트 객체
    """
    from binance.client import Client
    client = Client(api_key, api_secret)
    return client
2️⃣ get_market_price()
목적
지정된 거래 쌍의 현재 시장 가격을 가져옵니다.

함수 설명
python
복사
편집
def get_market_price(client, symbol):
    """
    시장 가격 조회
    :param client: Binance 클라이언트
    :param symbol: 거래 쌍 (예: BTCUSDT)
    :return: 현재 시장 가격
    """
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])
3️⃣ place_order()
목적
매수 또는 매도 주문을 실행합니다.

함수 설명
python
복사
편집
def place_order(client, symbol, side, quantity, order_type='MARKET', price=None):
    """
    주문 실행
    :param client: Binance 클라이언트
    :param symbol: 거래 쌍 (예: BTCUSDT)
    :param side: 매수 또는 매도 ('BUY' 또는 'SELL')
    :param quantity: 주문 수량
    :param order_type: 주문 유형 ('MARKET' 또는 'LIMIT')
    :param price: 지정가 주문의 가격
    :return: 주문 결과
    """
    if order_type == 'MARKET':
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
    elif order_type == 'LIMIT' and price is not None:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=str(price)
        )
    return order
4️⃣ get_account_balance()
목적
계정의 잔액 및 자산 상태를 조회합니다.

함수 설명
python
복사
편집
def get_account_balance(client):
    """
    계정 잔액 조회
    :param client: Binance 클라이언트
    :return: 계정 잔액 정보
    """
    account_info = client.get_account()
    balances = account_info['balances']
    return {balance['asset']: float(balance['free']) for balance in balances if float(balance['free']) > 0}
🔗 통신 구조 및 의존성
통신 구조
plaintext
복사
편집
signals/generator.py → execution/api/binance_api.py → execution/order_manager.py
주요 의존성
외부 라이브러리:
binance: Binance API 호출.
ccxt: 다른 거래소와의 API 통합.
내부 모듈:
order_manager.py: 주문 생성 및 상태 전달.
logger.py: API 호출 및 주문 상태 로깅.
📅 개발 일정
1️⃣ 설계 및 검토 (1일)

Binance API 엔드포인트 정의.
2️⃣ 기능 개발 (2일)

API 인증, 주문 실행, 데이터 조회 기능 구현.
3️⃣ 테스트 및 통합 (1일)

실시간 API 호출 및 응답 테스트.
📑 테스트 계획
1️⃣ 유닛 테스트

각 함수의 입력 및 출력 검증.
2️⃣ 통합 테스트

주문 생성 후 주문 상태 확인.
3️⃣ 시스템 테스트

실시간 시장 데이터를 기반으로 주문 실행.
📘 참고 문서 및 링크
Binance API Documentation
Docs/Plan/Phase1/module_execution.md