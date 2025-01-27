# 📁 Docs/Plan/Phase1/module_signal/generator.md

---

## 📌 목적
- `generator.py`는 Signal 모듈의 핵심 파일로, AI/ML 모델 및 기술적 지표 데이터를 기반으로 매수 및 매도 신호를 생성합니다.
- 이 모듈은 간단한 규칙 기반 신호부터 복합 신호 생성까지 다양한 기능을 포함하며, 트레이딩의 주요 의사결정을 지원합니다.

---

## 📄 주요 기능
1️⃣ **기본 신호 생성 규칙**
   - 기술적 지표 데이터를 활용한 규칙 기반 신호 생성.
   - 이동평균선, RSI, MACD 등의 지표 활용.

2️⃣ **복합 신호 생성 로직 구현**
   - 다중 신호를 결합하여 강력한 매수/매도 신호를 생성.
   - 사용자 정의 신호 생성 로직 지원.

3️⃣ **신호 강도 계산**
   - 각 신호의 강도를 수치화하여 의사결정에 활용.

---

## 📁 디렉터리 구조
```plaintext
project/
├── signals/
│   ├── __init__.py
│   ├── generator.py                  # 신호 생성 모듈
│   ├── filters.py
│   ├── optimizer.py
│   ├── arbitrage_signals.py
│   └── risk_management.py
Docs/
└── Plan/
    └── Phase1/
        └── module_signal/
            ├── generator.md
            ├── filters.md
            ├── optimizer.md
            ├── arbitrage_signals.md
            ├── risk_management.md
```

---

### 🔍 주요 함수 설계
1️⃣ `generate_signal(data: pd.DataFrame, model: object) -> dict`
- **설명**: 입력 데이터와 ML 모델을 사용하여 매수/매도 신호를 생성합니다.
- **입력**:
  - `data` (pd.DataFrame): 지표 데이터 (예: 이동 평균, RSI).
  - `model` (object): 훈련된 머신러닝 모델.
- **출력**:
  - `dict`: 매수/매도 신호 및 신호 강도.
- **예제 코드**:
```python
from sklearn.ensemble import RandomForestClassifier

def generate_signal(data: pd.DataFrame, model: RandomForestClassifier) -> dict:
    features = data[['moving_avg', 'rsi', 'macd']]
    predictions = model.predict(features)
    signal_strength = model.predict_proba(features)[:, 1]
    return {
        'signals': predictions,
        'strength': signal_strength
    }
```

2️⃣ `combine_signals(signals: list, weights: list) -> list`
- **설명**: 여러 신호를 가중 평균으로 결합하여 복합 신호를 생성합니다.
- **입력**:
  - `signals` (list): 신호 리스트 (예: [1, 0, 1]).
  - `weights` (list): 각 신호에 대한 가중치.
- **출력**:
  - `list`: 결합된 신호 리스트.
- **예제 코드**:
```python
import numpy as np

def combine_signals(signals: list, weights: list) -> list:
    weighted_signals = np.average(signals, axis=0, weights=weights)
    return [1 if s > 0.5 else 0 for s in weighted_signals]
```

3️⃣ `calculate_signal_strength(signal: list) -> float`
- **설명**: 생성된 신호의 강도를 계산하여 수치화합니다.
- **입력**:
  - `signal` (list): 신호 리스트 (예: [1, 0, 1]).
- **출력**:
  - `float`: 신호 강도 (0 ~ 1).
- **예제 코드**:
```python
def calculate_signal_strength(signal: list) -> float:
    return sum(signal) / len(signal)
```

---

## 🔗 통신 구조 및 데이터 흐름
- **데이터 흐름**:
  - 입력: 데이터 모듈(`data/preprocessor.py`)에서 전처리된 데이터를 입력받음.
  - 처리: AI/ML 모델(`models/inference.py`)과 결합하여 신호 생성.
  - 출력: 필터링(`signals/filters.py`) 및 최적화(`signals/optimizer.py`) 모듈로 전달.

---

## 📑 테스트 계획
1️⃣ **유닛 테스트**:
   - 개별 함수(`generate_signal`, `combine_signals`, `calculate_signal_strength`)의 동작 검증.
   - 다양한 입력값(결측치, 잘못된 형식 등)에 대한 예외 처리 검증.

2️⃣ **통합 테스트**:
   - 데이터 모듈(`data/preprocessor.py`)과의 입력/출력 연동 테스트.
   - 최적화 및 필터링 모듈과의 데이터 흐름 검증.

3️⃣ **성능 테스트**:
   - 대량의 데이터 처리 속도와 신호 생성 정확도 측정.

---

## 📘 참고 문서 및 링크
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [NumPy Documentation](https://numpy.org/)
- Docs/Plan/Phase1/module_data.md

