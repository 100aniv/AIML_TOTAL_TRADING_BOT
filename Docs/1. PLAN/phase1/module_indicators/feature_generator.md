# 📁 Docs/Plan/Phase1/module_indicators/feature_generator.md

---

## 📌 목적
- **Feature Generator** 모듈은 AI/ML 학습을 위한 고유한 특징 데이터를 생성하여 모델의 성능을 최적화합니다.
- 다양한 지표와 원천 데이터를 변환하여 학습 가능한 형식으로 제공합니다.

---

## 🗂️ 디렉터리 구조
```plaintext
indicators/
├── __init__.py
├── feature_generator.py
```

---

## ✨ 주요 기능

1️⃣ **특징 데이터 생성**  
- 가격, 거래량, 지표 데이터를 조합하여 새로운 특징을 생성.

2️⃣ **특징 스케일링 및 정규화**  
- 데이터의 범위를 조정하여 학습 모델의 수렴 속도를 향상.

---

## 📄 주요 파일 설명

### 1️⃣ `feature_generator.py`
#### 목적
- AI/ML 학습에 적합한 특징 데이터를 생성 및 전처리.

#### 주요 함수

```python
def generate_features(data, indicators):
    """
    학습 특징 데이터 생성 함수
    :param data: 원천 데이터 (가격, 거래량 등)
    :param indicators: 지표 데이터 (딕셔너리 형태)
    :return: 학습 특징 데이터 (DataFrame)
    """
    features = data.copy()
    for key, values in indicators.items():
        features[key] = values
    return features
```

```python
def normalize_features(features):
    """
    특징 데이터 정규화 함수
    :param features: 학습 특징 데이터 (DataFrame)
    :return: 정규화된 특징 데이터
    """
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    normalized = scaler.fit_transform(features)
    return normalized
```

#### 의존성
- Pandas: 데이터 처리 및 분석.
- Scikit-learn: 데이터 정규화 및 전처리.

---

## 🔗 통신 구조 및 의존성

### 통신 구조
```plaintext
trend_indicator.py, momentum_indicator.py, volume_indicator.py → feature_generator.py → trainer.py
```

### 주요 의존성
1. **외부 라이브러리:**
   - Pandas: 데이터 처리 및 특징 생성.
   - Scikit-learn: 특징 스케일링 및 정규화.
2. **내부 모듈:**
   - trend_indicator.py: 추세 지표 데이터.
   - momentum_indicator.py: 모멘텀 지표 데이터.
   - volume_indicator.py: 거래량 지표 데이터.

---

## 📑 테스트 계획
1️⃣ **단위 테스트**
- `generate_features`: 다양한 데이터와 지표 입력에 대해 특징 생성 검증.
- `normalize_features`: 다양한 데이터 세트에 대해 정규화 검증.

2️⃣ **통합 테스트**
- 개별 지표 모듈의 출력을 입력으로 받아 특징 생성 및 정규화 검증.

---

## 📘 참고 문서 및 링크
- [Pandas Documentation](https://pandas.pydata.org/)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Docs/Plan/Phase1/module_indicators.md](Docs/Plan/Phase1/module_indicators.md)
- Docs/Plan/Phase1/module_data.md
- Docs/Plan/Phase1/module_indicators.md
- Docs/Plan/Phase1/module_signals.md
- Docs/Plan/Phase1/module_execution.md
- Docs/Plan/Phase1/module_uiux.md