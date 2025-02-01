# strategy_manager_dashboard.py
# 목적:
# - 여러 전략(모멘텀, 아비트라지, 스캘핑, 패턴 인식 등)의 상태를 실시간으로 모니터링하고, 통합 제어.
# 목표:
# - 모든 전략의 요약 성과와 현재 상태를 한 화면에서 확인.
# 구현해야 할 기능:
# 1. 전략 요약 섹션:
#    - 각 전략별 활성화 상태, 누적 수익, 성공률, 현재 거래 상태를 요약.
# 2. 전략 선택 및 제어:
#    - 사용자가 활성화/비활성화할 전략 선택.
#    - 전략별 상세 설정(리스크 관리, 목표 수익률 등) 관리.
# 3. 실시간 업데이트:
#    - 각 전략의 상태와 성과를 실시간으로 반영.
# 4. 성과 분석:
#    - 전체 포트폴리오 성과(총 수익, 평균 수익률, 리스크 등)를 요약.
# 5. 경고 시스템:
#    - 모든 전략의 주요 경고를 집계하여 사용자에게 표시.
