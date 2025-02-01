# 📁 Indicators 모듈 테스트 계획

---

## 📌 목적
- `indicators` 모듈의 각 파일을 독립적으로 테스트하여 정확한 기능 수행을 확인합니다.
- 모든 지표의 계산 정확성과 성능을 검증합니다.
- 실제 트레이딩에 사용 가능한 수준의 안정성을 확보합니다.

---

## 📁 디렉터리 구조
```plaintext
tests/
└── phase1/
    └── module_indicators/
        ├── TEST_PLAN.md
        ├── test_trend_indicator.py
        ├── test_momentum_indicator.py
        ├── test_volume_indicator.py
        ├── test_volatility_indicator.py
        ├── test_sentiment_indicator.py
        ├── test_onchain_indicator.py
        ├── test_composite_indicator.py
        ├── test_arbitrage_features.py
        └── test_feature_generator.py
```

---

## 🔍 테스트 계획

### 1️⃣ 공통 테스트 항목

#### 1. 클래스 초기화 테스트
```python
def test_initialization():
    """클래스 초기화 테스트"""
    # 1) 정상 데이터로 초기화
    indicator = Indicator(valid_data)
    assert indicator is not None
    
    # 2) 잘못된 데이터로 초기화
    with pytest.raises(ValueError):
        Indicator(invalid_data)
    
    # 3) 필수 컬럼 검증
    assert all(col in indicator.data.columns 
              for col in ['open', 'high', 'low', 'close', 'volume'])
```

#### 2. 데이터 유효성 검증
```python
def test_data_validation():
    """데이터 유효성 검증"""
    # 1) 데이터 형식 검증
    assert isinstance(indicator.data, pd.DataFrame)
    
    # 2) 결측치 처리
    data_with_nan = add_nan_to_data(valid_data)
    result = indicator.calculate(data_with_nan)
    assert not result.isnull().any()
    
    # 3) 데이터 타입 검증
    assert indicator.data.dtypes['close'] == np.float64
```

#### 3. 성능 테스트
```python
def test_performance():
    """성능 테스트"""
    # 1) 실행 시간 측정
    start_time = time.time()
    result = indicator.calculate()
    assert time.time() - start_time < 0.05  # 50ms 이내
    
    # 2) 메모리 사용량 확인
    memory_usage = indicator.data.memory_usage().sum()
    assert memory_usage < 1e6  # 1MB 이내
    
    # 3) 대용량 데이터 처리
    large_data = generate_large_dataset()
    assert indicator.calculate(large_data) is not None
```

### 2️⃣ 파일별 특수 테스트 항목

#### 1. test_trend_indicator.py
```python
class TestTrendIndicator:
    """추세 지표 테스트"""
    
    # 기본 이동평균선 테스트
    def test_sma_calculation(self):
        """SMA 계산 정확성 테스트"""
        # 1) 기본 계산
        # 2) 크로스오버 감지
        # 3) 추세 방향 판별
    
    # 지수 이동평균선 테스트
    def test_ema_calculation(self):
        """EMA 계산 정확성 테스트"""
        # 1) 가중치 계산
        # 2) 실시간 업데이트
        # 3) 반응 속도 검증
    
    # MACD 테스트
    def test_macd_calculation(self):
        """MACD 신호 테스트"""
        # 1) 시그널 라인 교차
        # 2) 히스토그램 변화
        # 3) 다이버전스 감지
    
    # Ichimoku Cloud 테스트
    def test_ichimoku_calculation(self):
        """Ichimoku Cloud 계산 테스트"""
        # 1) 5개 라인 계산
        # 2) 구름 형성 확인
        # 3) 미래/과거 데이터 처리
    
    # Parabolic SAR 테스트
    def test_parabolic_sar_calculation(self):
        """Parabolic SAR 계산 테스트"""
        # 1) 반전점 위치
        # 2) 가격 범위 검증
        # 3) 가속 계수 적용
    
    # ADX 테스트
    def test_adx_calculation(self):
        """ADX 계산 테스트"""
        # 1) 0-100 범위 확인
        # 2) 추세 강도 측정
        # 3) DI+/DI- 관계
    
    # Hull MA 테스트
    def test_hma_calculation(self):
        """Hull MA 계산 테스트"""
        # 1) 지연 감소 확인
        # 2) 가중치 적용
        # 3) 노이즈 감소
    
    # DEMA/TEMA 테스트
    def test_dema_tema_calculation(self):
        """DEMA/TEMA 계산 테스트"""
        # 1) 이중/삼중 지수 처리
        # 2) 지연 감소 확인
        # 3) 오버슈트 검증
    
    # 추세 강도/전환점 테스트
    def test_trend_analysis(self):
        """추세 분석 테스트"""
        # 1) 강도 측정
        # 2) 전환점 감지
        # 3) 신뢰도 평가
```

#### 테스트 데이터 요구사항
1. 기본 시장 데이터
   - 일봉 OHLCV 데이터
   - 최소 1년치 데이터
   - 다양한 시장 상황 포함

2. 특수 테스트 데이터
   - 강한 상승/하락 추세
   - 횡보 구간
   - 갭 포함 데이터
   - 극단적 변동성 구간

#### 성공 기준
1. 정확성
   - 모든 지표 계산이 참조 구현과 일치
   - 오차 범위 < 0.0001
   - 엣지 케이스 정상 처리

2. 성능
   - 단일 지표 계산 < 50ms
   - 전체 지표 계산 < 500ms
   - 메모리 사용 최적화

3. 안정성
   - 예외 상황 적절한 처리
   - 실시간 업데이트 지원
   - 메모리 누수 없음

#### 2. test_momentum_indicator.py
```python
class TestMomentumIndicator:
    """모멘텀 지표 테스트"""
    
    # RSI 테스트
    def test_rsi_calculation(self):
        """RSI 계산 테스트"""
        # 1) 기본 RSI 계산
        # 2) 과매수/과매도 구간 식별
        # 3) 다이버전스 패턴 감지
    
    # Stochastic 테스트
    def test_stochastic_calculation(self):
        """Stochastic 계산 테스트"""
        # 1) %K, %D 계산
        # 2) Slow/Fast 스토캐스틱
        # 3) 신호선 교차 감지
    
    # Williams %R 테스트
    def test_williams_r_calculation(self):
        """Williams %R 계산 테스트"""
        # 1) -100~0 범위 확인
        # 2) 과매수/과매도 구간
        # 3) 반전 신호 감지
    
    # CCI 테스트
    def test_cci_calculation(self):
        """CCI 계산 테스트"""
        # 1) 표준편차 기반 계산
        # 2) 과매수/과매도 레벨
        # 3) 트렌드 강도 측정
    
    # ROC 테스트
    def test_roc_calculation(self):
        """Rate of Change 계산 테스트"""
        # 1) 변화율 계산
        # 2) 모멘텀 강도 측정
        # 3) 발산/수렴 패턴
```

#### 3. test_volume_indicator.py
```python
class TestVolumeIndicator:
    """거래량 지표 테스트"""
    
    # OBV 테스트
    def test_obv_calculation(self):
        """OBV 계산 테스트"""
        # 1) 누적 거래량 계산
        # 2) 가격-거래량 관계
        # 3) 다이버전스 감지
    
    # VWAP 테스트
    def test_vwap_calculation(self):
        """VWAP 계산 테스트"""
        # 1) 거래량 가중 가격
        # 2) 일중 VWAP 리셋
        # 3) 지지/저항 레벨
    
    # Force Index 테스트
    def test_force_index(self):
        """Force Index 계산 테스트"""
        # 1) 거래량-가격 영향력
        # 2) 추세 강도 측정
        # 3) 돌파 신호 감지
```

#### 4. test_volatility_indicator.py
```python
class TestVolatilityIndicator:
    """변동성 지표 테스트"""
    
    # Bollinger Bands 테스트
    def test_bollinger_bands(self):
        """볼린저 밴드 계산 테스트"""
        # 1) 표준편차 기반 밴드
        # 2) 스퀴즈 감지
        # 3) 밴드폭 계산
    
    # ATR 테스트
    def test_atr_calculation(self):
        """ATR 계산 테스트"""
        # 1) TR 계산
        # 2) 평균 실제 범위
        # 3) 변동성 확장/수축
```

#### 5. test_sentiment_indicator.py
```python
class TestSentimentIndicator:
    """감성 지표 테스트"""
    
    # Fear & Greed 테스트
    def test_fear_greed_index(self):
        """공포탐욕지수 계산 테스트"""
        # 1) 복합 지표 계산
        # 2) 극단치 감지
        # 3) 시장 심리 평가
    
    # Social Sentiment 테스트
    def test_social_sentiment(self):
        """소셜 감성 분석 테스트"""
        # 1) 텍스트 감성 분석
        # 2) 실시간 데이터 처리
        # 3) 감성 점수 집계
```

#### 테스트 데이터 요구사항
1. 기본 시장 데이터
   - 일봉 OHLCV 데이터
   - 최소 1년치 데이터
   - 다양한 시장 상황 포함

2. 특수 테스트 데이터
   - 강한 상승/하락 추세
   - 횡보 구간
   - 갭 포함 데이터
   - 극단적 변동성 구간

#### 성공 기준
1. 정확성
   - 모든 지표 계산이 참조 구현과 일치
   - 오차 범위 < 0.0001
   - 엣지 케이스 정상 처리

2. 성능
   - 단일 지표 계산 < 50ms
   - 전체 지표 계산 < 500ms
   - 메모리 사용 최적화

3. 안정성
   - 예외 상황 적절한 처리
   - 실시간 업데이트 지원
   - 메모리 누수 없음

#### 4. test_arbitrage_features.py
```python
class TestArbitrageFeatures:
    """차익거래 기능 테스트"""
    
    def test_price_spread_detection(self):
        """가격차 감지 테스트"""
        # 1) 거래소간 가격차
        # 2) 수수료 고려
        # 3) 실행 가능성
    
    def test_arbitrage_opportunity(self):
        """차익기회 분석 테스트"""
        # 1) 최소 수익률
        # 2) 실시간 감지
        # 3) 위험 평가
```

[나머지 파일별 테스트 클래스 및 메서드...]

### 3️⃣ 통합 테스트
```python
class TestIndicatorIntegration:
    """지표 통합 테스트"""
    
    def test_combined_signals(self):
        """통합 신호 테스트"""
        # 1) 다중 지표 조합
        # 2) 신호 우선순위
        # 3) 충돌 해결
    
    def test_realtime_processing(self):
        """실시간 처리 테스트"""
        # 1) 스트리밍 데이터 처리
        # 2) 성능 모니터링
        # 3) 메모리 관리
```

---

## 🧪 테스트 실행 방법

### 1. 개별 파일 테스트
```bash
# 특정 지표 파일 테스트
pytest tests/phase1/module_indicators/test_trend_indicator.py -v

# 특정 테스트 함수 실행
pytest tests/phase1/module_indicators/test_trend_indicator.py::test_sma -v
```

### 2. 전체 테스트 실행
```bash
# 모든 지표 테스트
pytest tests/phase1/module_indicators/ -v

# 커버리지 리포트 생성
pytest tests/phase1/module_indicators/ --cov=indicators --cov-report=html
```

---

## ✅ 테스트 성공 기준

### 1. 기능적 요구사항
- 모든 지표의 계산 결과가 참조 구현과 일치
- 실시간 데이터 처리 지원
- 모든 엣지 케이스 정상 처리

### 2. 성능 요구사항
- 단일 지표 계산: < 50ms
- 전체 지표 계산: < 500ms
- 메모리 사용: 입력 데이터의 2배 이내

### 3. 신뢰성 요구사항
- 테스트 커버리지 90% 이상
- 모든 예외 상황 적절히 처리
- 메모리 누수 없음

---

## 📊 테스트 데이터셋

### 1. 기본 테스트 데이터
- 정상 시장 상황 데이터
- 다양한 시간프레임 데이터
- 다양한 자산 클래스 데이터

### 2. 특수 테스트 데이터
- 극단적 변동성 데이터
- 갭 포함 데이터
- 이상치 포함 데이터
- 결측치 포함 데이터

---

## 📝 테스트 결과 보고
- 테스트 성공/실패 여부
- 성능 측정 결과
- 커버리지 리포트
- 발견된 이슈 목록
- 개선 권장사항

---

## 🔄 다음 단계
1. CI/CD 파이프라인 통합
2. 자동화된 성능 모니터링
3. 실시간 테스트 환경 구축
4. 스트레스 테스트 추가 