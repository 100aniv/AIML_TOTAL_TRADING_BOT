## 📁 Docs/Plan/Phase2/README.md

### 📌 Phase 2: AI/ML 기반 신호 생성

### 📌 목적

- 머신러닝 기반으로 고도화된 매수/매도 신호를 생성.
데이터 전처리와 피처 엔지니어링을 통해 고품질 학습 데이터를 생성.
모델 학습 및 평가로 신호의 신뢰도를 향상.
## 📂 디렉터리 구조
```plaintext
project/
├── data/                             # 데이터 수집 및 처리
│   ├── preprocessor.py               # 데이터 전처리
│   ├── data_storage.py               # 데이터 저장
│   ├── logger.py                     # 데이터 로깅
├── models/                           # AI/ML 학습 및 신호 생성
│   ├── trainer.py                    # 모델 학습
│   ├── inference.py                  # 신호 추론
│   ├── evaluators.py                 # 모델 평가
│   ├── arbitrage_trainer.py          # 아비트라지 모델 학습
│   ├── rl_trainer.py                 # 강화 학습 모델 학습
│   └── model_storage.py              # 모델 저장 및 로드
├── signals/                          # 신호 생성 및 리스크 관리
│   ├── generator.py                  # 신호 생성
│   ├── filters.py                    # 신호 필터링
│   └── risk_management.py            # 리스크 관리
```

### 🛠️ 주요 기능 및 모듈

#### 1️⃣ **데이터 처리 (data/preprocessor.py)**

- 데이터 정규화 및 이상치 제거.
- AI 학습을 위한 피처 생성.

#### 2️⃣ **AI 모델 학습 (models/trainer.py)**

- AI/ML 모델 학습 파이프라인 구성.
- 학습 결과 저장 및 평가.

#### 3️⃣ **신호 생성 (signals/generator.py)**

- 학습된 모델을 기반으로 매매 신호 생성.
- 실시간 데이터와 통합.

### 🛠️ 주요 모듈과 함수

#### 1️⃣ **Data 모듈**

(1) **preprocessor.py**
기능: 결측치 제거, 이상치 처리, 데이터 정규화.
주요 함수:
```python
def clean_data(data):
    """
    결측치 제거 및 클리닝
    :param data: 입력 데이터 (DataFrame)
    :return: 클리닝된 데이터
    """
    return data.dropna()

def normalize_data(data):
    """
    데이터 정규화
    :param data: 입력 데이터 (DataFrame)
    :return: 정규화된 데이터
    """
    return (data - data.mean()) / data.std()

(2) **feature_generator.py**
기능: 기술적 지표 기반으로 피처 생성.
주요 함수:
```python
def generate_features(data):
    """
    기술적 지표를 기반으로 피처 생성
    :param data: 입력 데이터
    :return: 피처가 추가된 데이터
    """
    data['MA'] = data['close'].rolling(window=14).mean()
    data['RSI'] = calculate_rsi(data['close'])
    return data

#### 2️⃣ **Models 모듈**

(1) **trainer.py**
기능: 학습 데이터로 머신러닝 모델 학습.
주요 함수:
```python
def train_model(features, labels):
    """
    모델 학습
    :param features: 학습 데이터
    :param labels: 레이블
    :return: 학습된 모델
    """
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()
    model.fit(features, labels)
    return model
(2) **evaluators.py**
기능: 모델 성능 평가.
주요 함수:
```python
def evaluate_model(model, test_features, test_labels):
    """
    모델 성능 평가
    :param model: 학습된 모델
    :param test_features: 테스트 피처
    :param test_labels: 테스트 레이블
    :return: 평가 결과
    """
    from sklearn.metrics import classification_report
    predictions = model.predict(test_features)
    return classification_report(test_labels, predictions)
(3) **inference.py**
기능: 학습된 모델로 신호 생성.
주요 함수:
```python
def generate_signals(model, features):
    """
    신호 생성
    :param model: 학습된 모델
    :param features: 입력 피처
    :return: 신호 데이터
    """
    return model.predict(features)
(4) **model_storage.py**
기능: 학습된 모델 저장 및 로드.
주요 함수:
```python
def save_model(model, path):
    """
    학습된 모델 저장
    :param model: 학습된 모델
    :param path: 저장 경로
    """
    import joblib
    joblib.dump(model, path)

def load_model(path):
    """
    저장된 모델 로드
    :param path: 모델 저장 경로
    :return: 로드된 모델
    """
    import joblib
    return joblib.load(path)

#### 🔗 통신 구조 및 의존성

1️⃣ 통신 구조
데이터 흐름:
```plaintext
preprocessor.py → feature_generator.py → trainer.py → inference.py
```
2️⃣ 의존성
1. 외부 라이브러리:
scikit-learn: 모델 학습 및 평가.
pandas: 데이터 처리.
2. 내부 모듈:
logger: 로깅 모듈.

#### 📅 개발 일정
1. 설계 및 검토
- 데이터 전처리 및 피처 설계: 3일
- 모델 학습 및 신호 생성 설계: 3일
2. 개발 및 테스트
데이터 모듈 구현: 5일
모델 학습 및 평가 구현: 5일
신호 생성 구현: 5일
3. 통합 및 프로토타입 테스트
데이터 → 피처 생성 → 모델 학습 → 신호 생성 테스트: 5일
📑 테스트 계획
1. 유닛 테스트
데이터 전처리, 피처 생성, 모델 학습 및 평가 개별 테스트.
2. 통합 테스트
데이터 모듈 → 모델 학습 → 신호 생성의 전체 흐름 검증.
3. 성능 테스트
과거 데이터 1년 분량으로 학습 및 신호 생성 성능 확인.
