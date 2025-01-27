# 📁 Docs/Plan/Phase1/Signals/filters.md

---

## 📌 목적
- **filters.py** 파일은 생성된 신호를 필터링하여 신뢰도가 높은 신호만 남기는 기능을 제공합니다.
- 다양한 조건 기반 필터를 통해 트레이딩 전략의 성능을 향상시킵니다.

---

## 📁 디렉터리 구조
```plaintext
signals/
├── __init__.py           # 모듈 초기화 파일
├── generator.py          # 신호 생성
├── filters.py            # 신호 필터링
├── arbitrage_signals.py  # 아비트라지 신호
├── risk_management.py    # 리스크 관리
└── optimizer.py          # 전략 최적화
```

---

## ✨ 주요 기능

1️⃣ **볼륨 기반 필터**
- 특정 거래량 이상의 데이터만 포함.

2️⃣ **변동성 필터**
- 특정 변동성 범위 내의 데이터만 포함.

3️⃣ **감정 필터**
- 시장 감정 지표에 따라 신호를 필터링.

---

## 📄 주요 파일 설명

### 1️⃣ filters.py
#### 목적
- 신호 데이터를 다양한 기준에 따라 필터링.

#### 주요 함수

##### (1) `volume_filter`
- 거래량이 특정 임계값 이상인 데이터만 필터링.

```python
def volume_filter(data, min_volume):
    """
    거래량 필터 함수
    :param data: 입력 데이터 (DataFrame)
    :param min_volume: 최소 거래량
    :return: 필터링된 데이터
    """
    return data[data['volume'] >= min_volume]
```

##### (2) `volatility_filter`
- 변동성이 특정 범위 내에 있는 데이터만 필터링.

```python
def volatility_filter(data, min_volatility, max_volatility):
    """
    변동성 필터 함수
    :param data: 입력 데이터 (DataFrame)
    :param min_volatility: 최소 변동성
    :param max_volatility: 최대 변동성
    :return: 필터링된 데이터
    """
    return data[(data['volatility'] >= min_volatility) & (data['volatility'] <= max_volatility)]
```

##### (3) `sentiment_filter`
- 감정 지표에 따라 신호를 필터링.

```python
def sentiment_filter(data, sentiment_score):
    """
    감정 필터 함수
    :param data: 입력 데이터 (DataFrame)
    :param sentiment_score: 감정 점수 기준
    :return: 필터링된 데이터
    """
    return data[data['sentiment'] >= sentiment_score]
```

---

## 🔗 통신 구조 및 의존성

### 통신 구조
```plaintext
generator.py → filters.py → optimizer.py → execution/
```

### 주요 의존성
1. **외부 라이브러리:**
   - Pandas: 데이터 필터링 및 처리.
   - NumPy: 수학적 계산.
2. **내부 모듈:**
   - signals/generator.py: 생성된 신호 데이터를 필터링.

---

## 📑 테스트 계획

### 1. 유닛 테스트
- 각 필터 함수가 올바른 조건으로 데이터를 필터링하는지 확인.
  - 예: `volume_filter`가 거래량이 100 이상인 데이터만 반환하는지 테스트.

### 2. 통합 테스트
- generator.py → filters.py → optimizer.py의 데이터 흐름 검증.

---

## 📘 참고 문서 및 링크
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/)
