📁 execution/api/upbit_api.md
📌 목적
Upbit API 모듈은 Upbit 거래소와의 통신을 처리하며, 주문 생성, 주문 조회, 잔고 확인 등 주요 기능을 제공합니다.
Upbit의 RESTful API를 활용하여 트레이딩 관련 데이터를 실시간으로 관리합니다.
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

Upbit의 RESTful API를 통해 매수/매도 주문 생성.
2️⃣ 주문 조회

특정 주문의 상태를 확인하고, 성공 여부를 반환.
3️⃣ 잔고 조회

계좌 내 보유 자산 및 잔고 확인.
📄 주요 함수 설명
1️⃣ place_order()
목적
Upbit에서 매수/매도 주문을 생성합니다.
함수 설명
python
복사
편집
def place_order(api_key, secret_key, market, side, volume, price=None):
    """
    Upbit 주문 생성 함수
    :param api_key: Upbit API 키
    :param secret_key: Upbit 시크릿 키
    :param market: 거래 시장 (예: KRW-BTC)
    :param side: 매수/매도 ("bid"/"ask")
    :param volume: 주문 수량
    :param price: 지정가 주문일 경우 가격 (시장가 주문 시 None)
    :return: 주문 결과
    """
    import jwt
    import requests
    import uuid
    import hashlib
    from urllib.parse import urlencode

    query = {
        'market': market,
        'side': side,
        'volume': volume,
        'price': price,
        'ord_type': 'limit' if price else 'market',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': api_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
    jwt_token = jwt.encode(payload, secret_key)
    authorization = f'Bearer {jwt_token}'

    headers = {'Authorization': authorization}
    response = requests.post('https://api.upbit.com/v1/orders', params=query, headers=headers)
    return response.json()
2️⃣ get_order_status()
목적
특정 주문의 상태를 조회합니다.
함수 설명
python
복사
편집
def get_order_status(api_key, secret_key, uuid):
    """
    주문 상태 조회 함수
    :param api_key: Upbit API 키
    :param secret_key: Upbit 시크릿 키
    :param uuid: 주문 UUID
    :return: 주문 상태
    """
    import jwt
    import requests
    import uuid as uuid_gen

    payload = {
        'access_key': api_key,
        'nonce': str(uuid_gen.uuid4()),
    }
    jwt_token = jwt.encode(payload, secret_key)
    authorization = f'Bearer {jwt_token}'

    headers = {'Authorization': authorization}
    response = requests.get(f'https://api.upbit.com/v1/order?uuid={uuid}', headers=headers)
    return response.json()
3️⃣ get_balance()
목적
계좌 내 잔고 및 보유 자산 정보를 조회합니다.
함수 설명
python
복사
편집
def get_balance(api_key, secret_key):
    """
    잔고 조회 함수
    :param api_key: Upbit API 키
    :param secret_key: Upbit 시크릿 키
    :return: 잔고 정보
    """
    import jwt
    import requests
    import uuid

    payload = {
        'access_key': api_key,
        'nonce': str(uuid.uuid4()),
    }
    jwt_token = jwt.encode(payload, secret_key)
    authorization = f'Bearer {jwt_token}'

    headers = {'Authorization': authorization}
    response = requests.get('https://api.upbit.com/v1/accounts', headers=headers)
    return response.json()
🔗 통신 구조 및 의존성
통신 구조
plaintext
    복사
편집    
execution/api/upbit_api.py → execution/order_manager.py
주요 의존성
1. 외부 라이브러리
- requests: HTTP 요청.
- jwt: 토큰 생성 및 인증.
- uuid: 고유 식별자 생성.
- hashlib: 해시 생성.
2. 내부 모듈
- order_manager.py: 주문 실행 호출.

## 📘 참고 문서 및 링크
1. 외부 라이브러리
- Upbit API Documentation
2. 내부 모듈
- Docs/Plan/Phase1/module_data.md
- Docs/Plan/Phase1/module_indicators.md
- Docs/Plan/Phase1/module_signals.md
- Docs/Plan/Phase1/module_execution.md
- Docs/Plan/Phase1/module_uiux.md