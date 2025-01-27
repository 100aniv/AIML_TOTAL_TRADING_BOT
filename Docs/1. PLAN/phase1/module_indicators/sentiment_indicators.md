# 📁 Docs/Plan/Phase1/module_indicators/sentiment_indicators.md

---

## 📌 목적
- **Sentiment Indicators** 모듈은 시장의 심리적 상태를 분석하여 투자자 감정 기반의 신호를 생성합니다.
- 소셜 미디어 데이터, 뉴스 헤드라인, Google Trends 등을 활용하여 시장의 감정 지표를 제공합니다.

---

## 🗂️ 디렉터리 구조
```plaintext
indicators/
├── __init__.py
├── sentiment_indicators.py
```

---

## ✨ 주요 기능

1️⃣ **소셜 미디어 감정 분석**  
- 트윗, Reddit 포스트 등에서 긍정적/부정적 감정을 분석.

2️⃣ **뉴스 기반 감정 점수 계산**  
- 뉴스 헤드라인에서 긍정적, 부정적 키워드를 추출하여 점수를 계산.

---

## 📄 주요 파일 설명

### 1️⃣ `sentiment_indicators.py`
#### 목적
- 시장 감정 데이터를 활용한 지표 계산 및 분석.

#### 주요 함수

```python
def analyze_social_media(data):
    """
    소셜 미디어 데이터 감정 분석
    :param data: 소셜 미디어 텍스트 데이터
    :return: 감정 점수 (긍정/부정 비율)
    """
    from textblob import TextBlob
    sentiment_scores = data.apply(lambda x: TextBlob(x).sentiment.polarity)
    return sentiment_scores.mean()
```

```python
def analyze_news_headlines(headlines):
    """
    뉴스 헤드라인 기반 감정 점수 계산
    :param headlines: 뉴스 헤드라인 리스트
    :return: 감정 점수 (긍정/부정 비율)
    """
    positive_words = ["profit", "growth", "bullish"]
    negative_words = ["loss", "decline", "bearish"]
    positive_score = sum(any(word in headline for word in positive_words) for headline in headlines)
    negative_score = sum(any(word in headline for word in negative_words) for headline in headlines)
    return (positive_score - negative_score) / len(headlines)
```

#### 의존성
- TextBlob: 감정 분석.
- Pandas: 데이터 처리 및 분석.

---

## 🔗 통신 구조 및 의존성

### 통신 구조
```plaintext
collector.py → sentiment_indicators.py → generator.py
```

### 주요 의존성
1. **외부 라이브러리:**
   - TextBlob: 감정 분석.
   - Pandas: 데이터 처리.
2. **내부 모듈:**
   - collector.py: 소셜 미디어 및 뉴스 데이터 수집.
   - generator.py: 신호 생성.

---

## 📑 테스트 계획
1️⃣ **단위 테스트**
- `analyze_social_media`: 다양한 소셜 미디어 데이터에 대해 감정 점수 계산 검증.
- `analyze_news_headlines`: 다양한 뉴스 헤드라인 데이터에 대해 점수 계산 검증.

2️⃣ **통합 테스트**
- `collector.py`에서 수집한 데이터를 입력으로 받아 지표 계산 및 신호 생성 검증.

---

## 📘 참고 문서 및 링크
- [TextBlob Documentation](https://textblob.readthedocs.io/en/dev/)
- [Docs/Plan/Phase1/module_indicators.md](Docs/Plan/Phase1/module_indicators.md)
- Docs/Plan/Phase1/module_data.md
- Docs/Plan/Phase1/module_indicators.md
- Docs/Plan/Phase1/module_signals.md
- Docs/Plan/Phase1/module_execution.md
- Docs/Plan/Phase1/module_uiux.md