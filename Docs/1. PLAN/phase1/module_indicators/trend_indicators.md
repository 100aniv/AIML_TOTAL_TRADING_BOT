# 📁 Docs/Plan/Phase1/Indicators/trend_indicator.md

---

## 📌 목적
- **trend_indicator.py** 파일은 시장 추세를 분석하고 트레이딩 신호의 기초로 사용할 지표를 계산합니다.
- 주요 추세 지표를 활용하여 상승, 하락 또는 횡보 상태를 탐지합니다.

---

## 📁 디렉터리 구조
```plaintext
indicators/
├── __init__.py           # 모듈 초기화 파일
├── trend_indicator.py    # 추세 지표
├── momentum_indicator.py # 모멘텀 지표
├── volume_indicator.py   # 거래량 지표
├── volatility_indicator.py # 변동성 지표
├── onchain_indicators.py # 온체인 지표
├── sentiment_indicators.py # 감정 지표
└── feature_generator.py  # 피처 생성
```

---

## ✨ 주요 기능

1️⃣ **이동 평균(MA)**
- 단기 및 장기 이동 평균을 계산하여 추세를 확인.

2️⃣ **MACD (이동 평균 수렴 발산)**
- 두 이동 평균 간의 차이를 계산하여 추세 강도를 평가.

3️⃣ **ADX (Average Directional Index)**
- 시장 추세 강도를 측정하여 트레이딩 신호 생성.

---

## 📄 주요 파일 설명

### 1️⃣ trend_indicator.py
#### 목적
- 다양한 추세 지표를 계산하여 시장 상태를 분석.

#### 주요 함수

##### (1) `calculate_moving_average`
- 이동 평균을 계산하여 상승/하락 추세를 탐지.

```python
def calculate_moving_average(data, window):
    """
    이동 평균 계산 함수
    :param data: 가격 데이터 (리스트 또는 Pandas Series)
    :param window: 이동 평균 기간
    :return: 이동 평균 값 (리스트 또는 Pandas Series)
    """
    return data.rolling(window=window).mean()
```

##### (2) `calculate_macd`
- 이동 평균 간의 차이를 계산하여 추세 강도를 평가.

```python
def calculate_macd(data, short_window, long_window):
    """
    MACD 계산 함수
    :param data: 가격 데이터
    :param short_window: 단기 이동 평균 기간
    :param long_window: 장기 이동 평균 기간
    :return: MACD 값 (Pandas Series)
    """
    short_ma = data.rolling(window=short_window).mean()
    long_ma = data.rolling(window=long_window).mean()
    return short_ma - long_ma
```

##### (3) `calculate_adx`
- 시장 추세 강도를 평가하는 ADX를 계산.

```python
def calculate_adx(high, low, close, window):
    """
    ADX 계산 함수
    :param high: 고가 데이터
    :param low: 저가 데이터
    :param close: 종가 데이터
    :param window: ADX 계산 기간
    :return: ADX 값 (Pandas Series)
    """
    # True Range 계산
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # Directional Movement 계산
    plus_dm = high.diff().clip(lower=0)
    minus_dm = -low.diff().clip(upper=0)

    # ADX 계산
    atr = true_range.rolling(window=window).mean()
    adx = (plus_dm / atr).rolling(window=window).mean()
    return adx
```

---

## 🔗 통신 구조 및 의존성

### 통신 구조
```plaintext
data/preprocessor.py → indicators/trend_indicator.py → signals/generator.py
```

### 주요 의존성
1. **외부 라이브러리:**
   - Pandas: 데이터 처리.
   - NumPy: 수학적 계산.
2. **내부 모듈:**
   - data/preprocessor.py: 전처리된 데이터 입력.
   - signals/generator.py: 계산된 추세 지표를 신호 생성에 활용.

---

## 📑 테스트 계획

### 1. 유닛 테스트
- `calculate_moving_average`가 올바른 이동 평균 값을 계산하는지 확인.
- `calculate_macd`가 정확한 MACD 값을 반환하는지 테스트.
- `calculate_adx`가 추세 강도를 올바르게 평가하는지 검증.

### 2. 통합 테스트
- data/preprocessor.py → indicators/trend_indicator.py → signals/generator.py의 데이터 흐름 검증.

---

## 📘 참고 문서 및 링크
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/)
- Docs/Plan/Phase1/module_data.md
- Docs/Plan/Phase1/module_indicators.md
- Docs/Plan/Phase1/module_signals.md
- Docs/Plan/Phase1/module_execution.md
- Docs/Plan/Phase1/module_uiux.md
- Docs/Plan/Phase1/module_logger.md
- Docs/Plan/Phase1/module_data_storage.md