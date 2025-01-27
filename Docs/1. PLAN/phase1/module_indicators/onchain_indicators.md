# 📁 Docs/Plan/Phase1/module_indicators/onchain_indicators.md

---

## 📌 목적
- **On-Chain Indicators** 모듈은 블록체인 데이터를 분석하여 시장 심리와 네트워크 활동을 기반으로 신호를 생성합니다.
- NVT Ratio, Active Addresses 등의 온체인 지표를 계산합니다.

---

## 🗂️ 디렉터리 구조
```plaintext
indicators/
├── __init__.py
├── onchain_indicators.py
```

---

## ✨ 주요 기능

1️⃣ **NVT Ratio 계산**  
- 시가총액 대비 거래량 비율을 계산하여 네트워크 가치 평가.

2️⃣ **Active Addresses 분석**  
- 활성 주소 수를 기반으로 시장 참여도 분석.

---

## 📄 주요 파일 설명

### 1️⃣ `onchain_indicators.py`
#### 목적
- 온체인 데이터를 활용한 지표 계산 및 분석.

#### 주요 함수

```python
def calculate_nvt_ratio(market_cap, transaction_volume):
    """
    NVT Ratio 계산 함수
    :param market_cap: 시가총액 데이터
    :param transaction_volume: 거래량 데이터
    :return: NVT Ratio 값
    """
    return market_cap / transaction_volume
```

```python
def calculate_active_addresses(data):
    """
    활성 주소 수 계산 함수
    :param data: 온체인 주소 데이터
    :return: 활성 주소 수
    """
    return data[data['transactions'] > 0].count()
```

#### 의존성
- Pandas: 데이터 처리 및 분석.

---

## 🔗 통신 구조 및 의존성

### 통신 구조
```plaintext
onchain_collector.py → onchain_indicators.py → generator.py
```

### 주요 의존성
1. **외부 라이브러리:**
   - Pandas: 데이터 처리 및 온체인 지표 계산.
2. **내부 모듈:**
   - onchain_collector.py: 온체인 데이터 수집.
   - generator.py: 신호 생성.

---

## 📑 테스트 계획
1️⃣ **단위 테스트**
- `calculate_nvt_ratio`: 다양한 시가총액 및 거래량 데이터에 대해 NVT Ratio 계산 검증.
- `calculate_active_addresses`: 다양한 온체인 데이터에 대해 활성 주소 수 계산 검증.

2️⃣ **통합 테스트**
- `onchain_collector.py`에서 수집한 데이터를 입력으로 받아 지표 계산 및 신호 생성 검증.

---

## 📘 참고 문서 및 링크
- [Pandas Documentation](https://pandas.pydata.org/)
- [Docs/Plan/Phase1/module_indicators.md](Docs/Plan/Phase1/module_indicators.md)
- Docs/Plan/Phase1/module_data.md
- Docs/Plan/Phase1/module_indicators.md
- Docs/Plan/Phase1/module_signals.md
- Docs/Plan/Phase1/module_execution.md
- Docs/Plan/Phase1/module_uiux.md