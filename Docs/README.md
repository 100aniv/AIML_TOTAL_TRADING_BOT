# 프로젝트 개발 계획서

## 프로젝트 개요
AI/ML 기반 자동화 트레이딩 시스템 프로젝트입니다.  
이 시스템은 거래소 데이터를 기반으로 AI와 머신러닝을 활용하여 매매 신호를 생성하고,  
다양한 전략(아비트라지, 스켈핑 등)을 통해 트레이딩을 수행합니다.

주요 목표는 다음과 같습니다:
1. **데이터 수집 및 처리**: 거래소 API 및 온체인 데이터를 실시간으로 수집 및 전처리.
2. **AI/ML 신호 생성**: 머신러닝과 딥러닝을 활용하여 고도화된 신호 생성.
3. **전략 기반 트레이딩 실행**: 사용자 맞춤형 및 AI 기반 전략 실행.
4. **실시간 대시보드 제공**: 사용자가 결과를 시각적으로 확인할 수 있는 대시보드 구현.
5. **통합 및 자동화**: 지속적 학습 파이프라인과 완전 자동화 시스템 구축.

---

## 최종 디렉터리 구조
아래는 최종적으로 설계된 디렉터리 구조입니다.  
모듈화된 구조로, 각 디렉터리는 관련된 기능별로 나뉩니다.

```
project/
├── data/                             # 데이터 수집 및 처리
│   ├── __init__.py
│   ├── collector.py                  # 거래소 데이터 수집
│   ├── real_time_collector.py        # 실시간 데이터 수집
│   ├── arbitrage_collector.py        # 실시간 데이터 수집
│   ├── preprocessor.py               # 데이터 전처리
│   ├── data_storage.py               # 데이터 저장
│   ├── logger.py                     # 데이터 로깅
│   └── onchain_collector.py          # 온체인 데이터 수집
├── indicators/                       # 지표 계산
│   ├── __init__.py
│   ├── trend_indicator.py               # 추세 지표
│   ├── momentum_indicator.py       # 모멘텀 지표
│   ├── volume_indicator.py            # 거래량 지표
│   ├── volatility_inidicator.py          # 변동성 지표
│   ├── onchain_indicators.py          # 온체인 지표
│   ├── sentiment_indicators.py        # 감정 지표
│   ├── composite_indicators.py        # 복합 지표
│   ├── arbitrage_features.py           # 아비트라지 지표
│   └── feature_generator.py           # AI/ML 학습용 피처 생성
├── models/                           # AI/ML 학습 및 신호 생성
│   ├── __init__.py
│   ├── trainer.py                      # 머신러닝/딥러닝 모델 학습
│   ├── inference.py                  # 신호 예측
│   ├── evaluators.py                 # 모델 성능 평가
│   ├── arbitrage_trainer.py         # 아비트라지 모델 학습
│   ├── rl_trainer.py                   # 강화학습 모델 학습
│   ├── auto_update.py               # 지속적 학습
│   └── model_storage.py             # 모델 저장 및 불러오기
├── signals/                          # 신호 생성 및 리스크 관리
│   ├── __init__.py
│   ├── generator.py                  # 신호 생성
│   ├── filters.py                    # 신호 필터링
│   ├── arbitrage_signals.py                    # 신호 필터링
│   ├── risk_management.py            # 리스크 관리
│   └── optimizer.py                  # 전략 최적화
├── execution/                        # 매매 실행
│   ├── __init__.py
│   ├── api/                          # 거래소 API 통합
│   │   ├── __init__.py
│   │   ├── binance_api.py               # Binance API
│   │   └── other_exchange_api.py     # 기타 거래소 API
│   ├── arbitrage_executor.py            # 아비트라지 주문 관리
│   ├── order_manager.py                # 매수/매도 주문 관리
│   ├── position_tracker.py               # 포지션 상태 추적
│   └── error_handler.py                  # 장애 복구
├── uiux/                             # UI/UX 모듈
│   ├── __init__.py
│   ├── dashboard.py                      	# 실시간 대시보드
│   ├── arbitrage_dashboard.py          	# 아비트라지 대시보드
│   ├── saclping_dashboard.py	          	# 스캘핑 대시보드
│   ├── mean_reversion_dashboard.py      # mean_reversion 대시보드
│   ├── momentum_dashboard.py	          # 모멘텀 대시보드
│   ├── grid_dashboard.py	          		# 그리드 대시보드
│   ├── volume_weighted_dashboard.py	# 볼륨 weighted 대시보드
│   ├── paris_trading_dashboard.py	     # paris tradng 대시보드
│   ├── strategy_manager_dashboard.py   	# 전략 선택 대시보드
│   ├── api_connector.py              		# 백엔드와 UI 연결
│   ├── charts.py                     			# 데이터 시각화
│   ├── forms.py                      			# 사용자 입력 처리
│   ├── layouts.py                    			# 대시보드 레이아웃
│   ├── api_connector.py              		# 백엔드와 UI 연결
│   └── server.py                     		# 대시보드 실행
├── utils/                            # 공통 유틸리티
│   ├── __init__.py
│   ├── config.py                     # 설정 파일
│   ├── helpers.py                    # 공통 함수
│   ├── logger.py                     # 로깅 모듈
│   ├── telegram_alerts.py          # 텔레그램 알람
│   ├── dashboard_utilss.py         # 대시보드 설정
│   └── gpu_utils.py                  # GPU 가속 유틸리티
├── ci_cd/                            # CI/CD 관련 파일
│   ├── github_actions/               # GitHub Actions 워크플로우
│   ├── docker/                       # Docker 관련 파일
│   ├── kubernetes/                   # Kubernetes 배포 파일
│   └── ...
├── test/                            # 모듈 테스트
│   ├── __init__.py
│   ├── test_indicators.py      		#indicators 모듈 테스트
│   ├── test_data.py                  # data 모듈 테스트
│   ├── test_models.py              # 모델 모듈 테스트
│   ├── test_signals.py               # 시그널 모듈 테스트
│   ├── test_execution.py          # 실행 모듈 테스트
│   ├── test_uiux.py         	   # uiux 모듈 테스트
│   └── test_utils.py                 # util 모듈 테스트
├── requirements.txt                  # Python 패키지 설치 파일
├── environment.yml                   # 아나콘다 환경 설정 파일
├── main.py                           # 프로그램 실행 진입점
```

---

## 단계별 개발 로드맵
프로젝트는 총 5단계(Phase)로 나뉘며, 각 단계에서 프로토타입을 점진적으로 완성합니다.

### 1단계: 기본 시스템 구축
- **목표**: 거래소 데이터 수집, 간단한 지표 계산, 기본 매매 로직 구현.
- **주요 작업**:
  1. 데이터 수집 모듈 개발.
  2. 이동평균선(MA), MACD 등의 기본 지표 계산.
  3. 간단한 매매 전략(예: 아비트라지) 구현.

### 2단계: AI/ML 기반 신호 생성
- **목표**: 머신러닝을 활용한 매매 신호 생성.
- **주요 작업**:
  1. 피처 엔지니어링 및 데이터 전처리.
  2. 머신러닝 모델 학습 및 신호 생성 모듈 구현.
  3. 모델 성능 평가 및 백테스트.

### 3단계: 실시간 트레이딩
- **목표**: 실시간 데이터 처리 및 매매 실행.
- **주요 작업**:
  1. 실시간 데이터 수집 모듈 개발.
  2. 실시간 신호 생성 및 매매 실행.
  3. 리스크 관리 및 주문 최적화.

### 4단계: 고급 AI/ML 도입
- **목표**: 강화학습 및 딥러닝을 활용한 고급 트레이딩 시스템 구축.
- **주요 작업**:
  1. LSTM/GRU 기반 모델 구현.
  2. 강화학습(PPO/DDPG) 적용 및 학습.
  3. GPU 최적화 및 병렬 처리.

### 5단계: 완전 자동화 및 통합
- **목표**: 모든 모듈의 통합 및 자동화.
- **주요 작업**:
  1. 지속적 학습 파이프라인 구축.
  2. 통합 테스트 및 배포.
  3. 실시간 대시보드 완성.

---

검토 후 **다음 문서(개발 환경.md)**를 작성하겠습니다. 필요한 수정사항이 있다면 알려주세요! 😊
