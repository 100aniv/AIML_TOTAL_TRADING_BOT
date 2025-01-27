# error_handler.py

# 목적:
# 매매 실행 중 발생하는 에러를 처리하고 복구하며, 시스템 안정성을 유지.
# Telegram 알림을 통해 주요 에러 상황을 관리자에게 실시간으로 전달.

# 목표:
# 1. 시스템 장애를 최소화하여 매매 연속성을 유지.
# 2. 에러 발생 시 빠르게 복구하거나 관리자에게 경고를 전송.
# 3. Telegram 알림으로 관리자와의 실시간 커뮤니케이션 강화.

# 구현해야 할 기능:
# 1. 주문 실패 시 자동 재시도:
#    - 주문 실패 시 재시도 횟수를 설정하고 재시도 후에도 실패할 경우 복구 절차 실행.
#    - Telegram으로 주문 실패 알림 전송 (실패 이유, 주문 ID 등 포함).
# 2. API 연결 실패 처리:
#    - API 호출 실패 시 백오프(backoff) 전략 적용.
#    - 연결 복구 시도 후 실패 시 Telegram으로 관리자에게 알림 전송.
#    - 알림 내용: API 이름, 에러 메시지, 재시도 횟수.
# 3. 네트워크 장애 복구 로직 구현:
#    - 네트워크 연결이 끊길 경우 자동 복구 로직 수행.
#    - 복구 실패 시 Telegram으로 관리자에게 경고 메시지 전송.
# 4. 거래소별 에러 코드 처리 및 메시지 로깅:
#    - 각 거래소에서 반환하는 에러 코드를 식별하고 적절히 처리.
#    - 에러 메시지를 로깅하고 Telegram으로 관리자에게 전송.
# 5. 복구 실패 시 관리자에게 알림 전송:
#    - 복구 절차 실패 시 Telegram으로 긴급 알림 전송.
#    - 알림 내용: 에러 유형, 발생 위치, 복구 시도 기록.
# 6. 오류 발생 시 안전한 종료 또는 재시작 기능:
#    - 시스템 상태를 저장하고 안전하게 종료 또는 재시작.
#    - 종료/재시작 이벤트 발생 시 Telegram 알림 전송 (시스템 상태 포함).