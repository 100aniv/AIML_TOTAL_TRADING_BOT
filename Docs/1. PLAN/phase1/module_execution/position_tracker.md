# 📁 execution/position_tracker.md

---

## 📌 목적
**Position Tracker**는 실행된 매수 및 매도 주문을 기반으로 포지션 상태를 실시간으로 추적하고 관리하는 모듈입니다.  
포지션 정보는 수익/손실 분석 및 리스크 관리를 위해 사용됩니다.

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
1️⃣ 포지션 상태 관리

각 거래 쌍의 포지션(수량, 평균 매수가 등)을 실시간으로 업데이트.
2️⃣ 수익/손실 계산

포지션 데이터를 기반으로 실현 손익(PnL) 및 미실현 손익을 계산.
3️⃣ 데이터 통합

주문 상태와 거래소 데이터를 통합하여 포지션 정보를 업데이트.
📄 주요 함수 설명
1️⃣ update_position()
목적
새로운 주문 데이터에 따라 포지션 상태를 업데이트합니다.

함수 설명
python
복사
편집
def update_position(symbol, quantity, price):
    """
    포지션 상태 업데이트 함수
    :param symbol: 거래 쌍 (예: BTC/USDT)
    :param quantity: 주문 수량
    :param price: 체결 가격
    :return: 업데이트된 포지션
    """
    position = {
        "symbol": symbol,
        "quantity": quantity,
        "price": price
    }
    print(f"Updated Position: {position}")
    return position
2️⃣ calculate_pnl()
목적
포지션 데이터를 기반으로 수익/손실을 계산합니다.

함수 설명
python
복사
편집
def calculate_pnl(position, current_price):
    """
    수익/손실(PnL) 계산 함수
    :param position: 포지션 데이터
    :param current_price: 현재 시장 가격
    :return: 수익/손실 값
    """
    pnl = (current_price - position['price']) * position['quantity']
    return pnl
3️⃣ get_position_summary()
목적
현재 포지션 상태를 요약하여 반환합니다.

함수 설명
python
복사
편집
def get_position_summary(positions):
    """
    포지션 요약 반환 함수
    :param positions: 전체 포지션 데이터
    :return: 요약 정보 (총 수익/손실 등)
    """
    summary = {
        "total_pnl": sum([calculate_pnl(pos, pos['current_price']) for pos in positions]),
        "positions_count": len(positions)
    }
    return summary
🔗 통신 구조 및 의존성
통신 구조
plaintext
복사
편집
execution/order_manager.py → execution/position_tracker.py → execution/risk_manager.py
주요 의존성
외부 라이브러리:
ccxt: 거래소 API 호출.
pandas: 데이터 관리 및 처리.
내부 모듈:
api/binance_api.py: Binance 거래소 데이터 통합.
api/upbit_api.py: Upbit 거래소 데이터 통합.
execution/order_manager.py: 주문 상태 관리.
📅 개발 일정
1️⃣ 설계 및 구현 (3일)

포지션 상태 추적 설계.
손익 계산 로직 설계.
2️⃣ 기능 개발 (4일)

포지션 상태 업데이트 함수 구현.
수익/손실 계산 로직 개발.
3️⃣ 통합 및 테스트 (3일)

거래소 API와 통합 테스트.
실시간 데이터 기반 포지션 업데이트 검증.
📑 테스트 계획
1️⃣ 유닛 테스트

포지션 업데이트 함수의 정확성 검증.
수익/손실 계산 로직의 정확성 테스트.
2️⃣ 통합 테스트

주문 관리 모듈과 통합하여 포지션 상태 관리 검증.
3️⃣ 시스템 테스트

실시간 시장 데이터 기반 포지션 업데이트와 손익 계산 검증.
📘 참고 문서 및 링크
Binance API Documentation
CCXT Documentation
Docs/Plan/Phase1/module_execution.md