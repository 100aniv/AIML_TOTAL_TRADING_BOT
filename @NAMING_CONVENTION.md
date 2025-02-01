# 네이밍 컨벤션 및 코드 스타일 가이드

## 클래스 메서드 구조

### 1. 기본 구조 (모든 Indicator 클래스 공통)
```python
class BaseIndicator:
    def __init__(self, data: Optional[pd.DataFrame] = None)
    def _validate_data(self) -> None
    def set_data(self, data: pd.DataFrame) -> None
    def calculate_all(self, periods: List[int] = [7, 14, 30]) -> pd.DataFrame
```

### 2. 지표별 추가 메서드

#### 개별 지표 호출이 필요한 클래스
- VolumeIndicator
- TrendIndicator
- OnchainIndicator
- CompositeIndicator  # 복합 지표는 개별 호출 필요
```python
def get_indicator(self, indicator_name: str, **kwargs) -> pd.Series
```

#### 통합 계산이 효율적인 클래스
- MomentumIndicator
- VolatilityIndicator
- SentimentIndicator
```python
# 기본 구조만 사용 (추가 메서드 없음)
```

#### 특수 목적 클래스
- ArbitrageFeature
```python
def calculate_features(self, **kwargs) -> pd.DataFrame  # 차익거래 특징 계산
def get_feature(self, feature_name: str, **kwargs) -> pd.Series  # 개별 특징 계산
```

- FeatureGenerator
```python
def generate_features(self, **kwargs) -> pd.DataFrame  # ML 학습용 특징 생성
def get_feature(self, feature_name: str, **kwargs) -> pd.Series  # 개별 특징 계산
def transform(self, data: pd.DataFrame) -> pd.DataFrame  # 데이터 변환
```

### 3. 메서드 구현 기준
- 지표의 특성과 사용 패턴에 따라 필요한 메서드만 구현
- 개별 호출 필요성이 높은 지표는 get_indicator 메서드 포함
- 세트로 사용되는 지표는 calculate_all 메서드만 사용
- 모든 클래스는 기본 구조 준수
- 특수 목적 클래스는 목적에 맞는 추가 메서드 구현 가능 