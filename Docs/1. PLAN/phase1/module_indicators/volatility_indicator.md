# 📁 Docs/Plan/Phase1/module_indicators/volatility_indicator.md

---

## 📌 목적
- **Volatility Indicator** 모듈은 시장 변동성을 분석하여 리스크 및 잠재적인 트레이딩 기회를 탐지합니다.
- Bollinger Bands, ATR (Average True Range) 등의 변동성 기반 지표를 계산합니다.

---

## 🗂️ 디렉터리 구조
```plaintext
indicators/
├── __init__.py
├── volatility_indicator.py
```

---

## ✨ 주요 기능

1️⃣ **Bollinger Bands 계산**  
- 가격 변동성에 따라 상한선 및 하한선을 계산하여 매수/매도 신호를 제공.

2️⃣ **ATR 계산**  
- 평균 실제 범위를 계산하여 시장 변동성을 측정.

---

## 📄 주요 파일 설명

### 1️⃣ `volatility_indicator.py`
#### 목적
- 변동성 지표 계산 및 분석.

#### 주요 함수

```python
def calculate_bollinger_bands(data, window, num_std_dev):
    """
    Bollinger Bands 계산 함수
    :param data: 가격 데이터
    :param window: 이동 평균 창 크기
    :param num_std_dev: 표준 편차의 배수
    :return: (상한선, 중간선, 하한선)
    """
    mean = data.rolling(window=window).mean()
    std_dev = data.rolling(window=window).std()
    upper_band = mean + (std_dev * num_std_dev)
    lower_band = mean - (std_dev * num_std_dev)
    return upper_band, mean, lower_band
```

```python
def calculate_atr(high, low, close, window):
    """
    ATR (Average True Range) 계산 함수
    :param high: 고가 데이터
    :param low: 저가 데이터
    :param close: 종가 데이터
    :param window: ATR 계산 창 크기
    :return: ATR 값
    """
    tr = pd.concat([
        high - low,
        abs(high - close.shift(1)),
        abs(low - close.shift(1))
    ], axis=1).max(axis=1)
    atr = tr.rolling(window=window).mean()
    return atr
```

#### 의존성
- Pandas: 데이터 처리 및 분석.

---

## 🔗 통신 구조 및 의존성

### 통신 구조
```plaintext
collector.py → volatility_indicator.py → generator.py
```

### 주요 의존성
1. **외부 라이브러리:**
   - Pandas: 데이터 처리 및 변동성 지표 계산.
2. **내부 모듈:**
   - collector.py: 데이터 수집.
   - generator.py: 신호 생성.

---

## 📑 테스트 계획
1️⃣ **단위 테스트**
- `calculate_bollinger_bands`: 다양한 표준 편차 배수와 창 크기에 대해 계산 검증.
- `calculate_atr`: 다양한 데이터 세트에 대해 ATR 계산 검증.

2️⃣ **통합 테스트**
- `collector.py`에서 수집한 데이터를 입력으로 받아 지표 계산 및 신호 생성 검증.

---

## 📘 참고 문서 및 링크
- [Pandas Documentation](https://pandas.pydata.org/)
- [Docs/Plan/Phase1/module_indicators.md](Docs/Plan/Phase1/module_indicators.md)
- Docs/Plan/Phase1/module_data.md
- Docs/Plan/Phase1/module_indicators.md
- Docs/Plan/Phase1/module_signals.md
- Docs/Plan/Phase1/module_execution.md
- Docs/Plan/Phase1/module_uiux.md