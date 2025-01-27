# 📁 Docs/Plan/Phase1/module_indicators/volume_indicator.md

---

## 📌 목적
- **Volume Indicator** 모듈은 거래량 데이터를 분석하여 시장의 강도를 평가하고 주요 트레이딩 기회를 탐지합니다.
- OBV, Volume Weighted Average Price (VWAP) 등의 거래량 기반 지표를 계산합니다.

---

## 🗂️ 디렉터리 구조
```plaintext
indicators/
├── __init__.py
├── volume_indicator.py
```

---

## ✨ 주요 기능

1️⃣ **OBV 계산**  
- On-Balance Volume을 계산하여 거래량 기반 추세를 확인.

2️⃣ **VWAP 계산**  
- 특정 기간 동안의 거래량 가중 평균 가격을 계산하여 가격의 공정성을 평가.

---

## 📄 주요 파일 설명

### 1️⃣ `volume_indicator.py`
#### 목적
- 거래량 지표 계산 및 분석.

#### 주요 함수

```python
def calculate_obv(data):
    """
    OBV (On-Balance Volume) 계산 함수
    :param data: 입력 데이터 (DataFrame, 종가 및 거래량 포함)
    :return: OBV 값
    """
    obv = [0]
    for i in range(1, len(data)):
        if data['close'][i] > data['close'][i-1]:
            obv.append(obv[-1] + data['volume'][i])
        elif data['close'][i] < data['close'][i-1]:
            obv.append(obv[-1] - data['volume'][i])
        else:
            obv.append(obv[-1])
    return obv
```

```python
def calculate_vwap(price, volume):
    """
    VWAP (Volume Weighted Average Price) 계산 함수
    :param price: 가격 데이터
    :param volume: 거래량 데이터
    :return: VWAP 값
    """
    cumulative_vp = (price * volume).cumsum()
    cumulative_volume = volume.cumsum()
    return cumulative_vp / cumulative_volume
```

#### 의존성
- Pandas: 데이터 처리 및 분석.

---

## 🔗 통신 구조 및 의존성

### 통신 구조
```plaintext
collector.py → volume_indicator.py → generator.py
```

### 주요 의존성
1. **외부 라이브러리:**
   - Pandas: 데이터 처리 및 거래량 지표 계산.
2. **내부 모듈:**
   - collector.py: 데이터 수집.
   - generator.py: 신호 생성.

---

## 📑 테스트 계획
1️⃣ **단위 테스트**
- `calculate_obv`: 다양한 데이터 세트에 대해 OBV 계산 검증.
- `calculate_vwap`: 다양한 데이터 세트에 대해 VWAP 계산 검증.

2️⃣ **통합 테스트**
- `collector.py`에서 수집한 데이터를 입력으로 받아 지표 계산 및 신호 생성 검증.

---

## 📘 참고 문서 및 링크
- [Pandas Documentation](https://pandas.pydata.org/)
- [Docs/Plan/Phase1/module_indicators.md](Docs/Plan/Phase1/module_indicators.md)
- [Docs/Plan/Phase1/module_data.md](Docs/Plan/Phase1/module_data.md)
- [Docs/Plan/Phase1/module_signals.md](Docs/Plan/Phase1/module_signals.md)
- [Docs/Plan/Phase1/module_execution.md](Docs/Plan/Phase1/module_execution.md)
- [Docs/Plan/Phase1/module_uiux.md](Docs/Plan/Phase1/module_uiux.md)s