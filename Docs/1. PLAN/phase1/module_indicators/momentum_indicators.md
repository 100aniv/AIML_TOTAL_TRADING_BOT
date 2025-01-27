# 📁 Docs/Plan/Phase1/module_indicators/momentum_indicator.md

---

## 📌 목적
- **Momentum Indicator** 모듈은 시장의 가격 변화 속도를 측정하여 매수 및 매도 시점을 분석합니다.
- RSI, Stochastic Oscillator 등의 모멘텀 기반 지표를 계산합니다.

---

## 🗂️ 디렉터리 구조
```plaintext
indicators/
├── __init__.py
├── momentum_indicator.py
```

---

## ✨ 주요 기능

1️⃣ **RSI 계산**  
- 상대 강도 지수를 계산하여 과매수 및 과매도 상태를 탐지.

2️⃣ **Stochastic Oscillator 계산**  
- 현재 가격이 최근 범위에서 차지하는 위치를 측정.

---

## 📄 주요 파일 설명

### 1️⃣ `momentum_indicator.py`
#### 목적
- 모멘텀 지표 계산 및 분석.

#### 주요 함수

```python
def calculate_rsi(data, window):
    """
    RSI (Relative Strength Index) 계산 함수
    :param data: 입력 데이터 (리스트 또는 Pandas Series)
    :param window: RSI 계산 창 크기
    :return: RSI 값
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
```

```python
def calculate_stochastic(data, high, low, window):
    """
    Stochastic Oscillator 계산 함수
    :param data: 현재 종가 데이터
    :param high: 고가 데이터
    :param low: 저가 데이터
    :param window: 계산 창 크기
    :return: Stochastic Oscillator 값
    """
    k_percent = (data - low.rolling(window=window).min()) / (high.rolling(window=window).max() - low.rolling(window=window).min()) * 100
    return k_percent
```

#### 의존성
- Pandas: 데이터 처리 및 분석.

---

## 🔗 통신 구조 및 의존성

### 통신 구조
```plaintext
collector.py → momentum_indicator.py → generator.py
```

### 주요 의존성
1. **외부 라이브러리:**
   - Pandas: 데이터 처리 및 모멘텀 지표 계산.
2. **내부 모듈:**
   - collector.py: 데이터 수집.
   - generator.py: 신호 생성.

---

## 📑 테스트 계획
1️⃣ **단위 테스트**
- `calculate_rsi`: 다양한 창 크기에 대해 RSI 계산 검증.
- `calculate_stochastic`: 다양한 데이터 입력에 대해 Stochastic Oscillator 계산 검증.

2️⃣ **통합 테스트**
- `collector.py`에서 수집한 데이터를 입력으로 받아 지표 계산 및 신호 생성 검증.

---

## 📘 참고 문서 및 링크
- [Pandas Documentation](https://pandas.pydata.org/)
- [Docs/Plan/Phase1/module_indicators.md](Docs/Plan/Phase1/module_indicators.md)
- [Docs/Plan/Phase1/module_data/collector.md](Docs/Plan/Phase1/module_data/collector.md)