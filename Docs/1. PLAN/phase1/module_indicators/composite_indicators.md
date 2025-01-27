# 📁 Docs/Plan/Phase1/module_indicators/composite_indicators.md

---

## 📌 목적
- **Composite Indicators** 모듈은 다양한 지표를 통합하여 종합적인 신호를 생성하고, 복잡한 시장 환경에서의 의사 결정을 지원합니다.
- 주요 개별 지표(Trend, Momentum, Volume 등)를 결합하여 단일 신호로 정리합니다.

---

## 🗂️ 디렉터리 구조
```plaintext
indicators/
├── __init__.py
├── composite_indicators.py
```

---

## ✨ 주요 기능

1️⃣ **다중 지표 결합**  
- 개별 지표의 결과를 통합하여 종합 점수를 계산.

2️⃣ **가중치 기반 신호 생성**  
- 사용자 정의 가중치를 사용하여 특정 지표의 중요도를 설정.

---

## 📄 주요 파일 설명

### 1️⃣ `composite_indicators.py`
#### 목적
- 개별 지표의 결과를 통합하여 종합 신호를 생성.

#### 주요 함수

```python
def calculate_composite_score(indicators, weights):
    """
    종합 점수 계산 함수
    :param indicators: 개별 지표 결과 (딕셔너리 형태)
    :param weights: 각 지표에 대한 가중치 (리스트 형태)
    :return: 종합 점수
    """
    weighted_scores = [indicators[key] * weight for key, weight in zip(indicators.keys(), weights)]
    return sum(weighted_scores)
```

```python
def generate_signal(composite_score, threshold):
    """
    종합 점수를 기반으로 매수/매도 신호 생성
    :param composite_score: 계산된 종합 점수
    :param threshold: 신호 생성 임계값
    :return: 매수/매도/중립 신호
    """
    if composite_score > threshold:
        return "Buy"
    elif composite_score < -threshold:
        return "Sell"
    else:
        return "Neutral"
```

#### 의존성
- Pandas: 데이터 처리 및 분석.

---

## 🔗 통신 구조 및 의존성

### 통신 구조
```plaintext
trend_indicator.py, momentum_indicator.py, volume_indicator.py → composite_indicators.py → generator.py
```

### 주요 의존성
1. **외부 라이브러리:**
   - Pandas: 데이터 처리 및 분석.
2. **내부 모듈:**
   - trend_indicator.py: 추세 지표 제공.
   - momentum_indicator.py: 모멘텀 지표 제공.
   - volume_indicator.py: 거래량 지표 제공.
   - generator.py: 신호 생성.

---

## 📑 테스트 계획
1️⃣ **단위 테스트**
- `calculate_composite_score`: 다양한 지표 및 가중치 조합에 대해 계산 검증.
- `generate_signal`: 다양한 종합 점수 및 임계값에 대해 신호 생성 검증.

2️⃣ **통합 테스트**
- 각 개별 지표 모듈의 결과를 입력으로 받아 종합 신호 생성 및 신호 정확성 검증.

---

## 📘 참고 문서 및 링크
- [Pandas Documentation](https://pandas.pydata.org/)
- [Docs/Plan/Phase1/module_indicators.md](Docs/Plan/Phase1/module_indicators.md)
- Docs/Plan/Phase1/module_data.md
- Docs/Plan/Phase1/module_indicators.md
- Docs/Plan/Phase1/module_signals.md
- Docs/Plan/Phase1/module_execution.md
- Docs/Plan/Phase1/module_uiux.md