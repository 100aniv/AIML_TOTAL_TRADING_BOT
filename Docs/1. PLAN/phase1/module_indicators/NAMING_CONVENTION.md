# Indicators 모듈 네이밍 및 구조 컨벤션

## 1. 기본 원칙
- 모든 함수명은 명확하고 설명적이어야 함
- 일관된 네이밍 패턴 사용
- 약어 사용 최소화

## 2. 함수 네이밍 규칙
- calculate_ 접두사 제거
- 동사_명사 형태 권장
- 예시:
  - calculate_rsi() -> rsi()
  - calculate_macd() -> macd()
  - calculate_bollinger_bands() -> bollinger_bands()

## 3. 클래스 구조 표준화
### 기본 구조
```python
class BaseIndicator:
    def __init__(self, data: Optional[pd.DataFrame] = None)
    def _validate_data(self) -> None
    def set_data(self, data: pd.DataFrame) -> None
    def calculate_all(self, periods: List[int]) -> pd.DataFrame
```

### 책임 분리
- indicators/: 순수 지표 계산만 담당
- signals/: 지표 기반 신호 생성 담당

## 4. 문서화 규칙
### Docstring 형식
```python
def function_name():
    """함수 설명
    
    Args:
        param1: 설명
        
    Returns:
        반환값 설명
        
    Note:
        추가 설명
    """
```

## 5. 모듈별 역할
- momentum_indicator.py: RSI, Stochastic 등 모멘텀 지표
- trend_indicator.py: MA, MACD 등 추세 지표
- volume_indicator.py: OBV, Volume Profile 등 거래량 지표
- onchain_indicator.py: NVT, MVRV 등 온체인 지표
- composite_indicator.py: 여러 지표의 조합

## 6. 구현 방향성
1. 지표 계산 책임 분리
   - 순수 계산 로직만 포함
   - 신호 생성 로직은 signals 모듈로 이동

2. 클래스 구조 통일
   - 모든 지표 클래스가 동일한 인터페이스 제공
   - 확장성과 유지보수성 고려

3. 데이터 검증 강화
   - 필수 컬럼 확인
   - 데이터 타입 검증
   - 무결성 검사

4. 성능 최적화
   - 벡터화 연산 활용
   - 캐싱 메커니즘 고려
   - 계산 효율성 개선

## 7. 코드 품질 기준
- 모든 함수에 타입 힌트 포함
- 테스트 코드 필수
- 일관된 들여쓰기와 포맷팅
- 명확한 에러 메시지

# 명명 규칙 및 코드 스타일 가이드

## 1. 파일 상단 주석 형식
```python
'''
N. 지표 분류명 (영문명)

정의
해당 지표군이 무엇인지 간단히 설명합니다.

목적
• 첫번째 목적
• 두번째 목적
• ...

지표 목록 (개수)
1. 지표명: 간단한 설명
2. 지표명: 간단한 설명
...

[날짜] 함수명 패턴 표준화
기존 함수명 -> 변경된 함수명:
- calculate_xxx -> xxx
- ...
'''
```

## 2. 함수 주석 형식
```python
#N. 지표명: 간단한 설명
def function_name(param1: type, param2: type) -> return_type:
    """
    함수 설명
    :param param1: 파라미터 설명 (타입)
    :param param2: 파라미터 설명 (타입)
    :return: 반환값 설명 (타입)
    """
```

## 3. 클래스 주석 형식
```python
class ClassName:
    """클래스 설명"""
    
    def __init__(self, param: type):
        """
        초기화 함수 설명
        :param param: 파라미터 설명
        """
```

# 지표 함수 명명 규칙 (Indicator Function Naming Convention)

## 1. 기본 원칙
- 명확성 (Clarity)
- 일관성 (Consistency)
- 간결성 (Conciseness)
- 확장성 (Extensibility)

## 2. 카테고리별 명명 규칙

### 2.1 기본 지표 함수 (Base Indicators)
- 단순 명사형 또는 약어 사용
- 업계 표준 약어는 그대로 사용 (RSI, MACD 등)

```python
# 올바른 예시
sma()          # Simple Moving Average
rsi()          # Relative Strength Index
macd()         # Moving Average Convergence Divergence
obv()          # On Balance Volume
```

### 2.2 비율/지수 함수 (Ratios & Indices)
- _ratio, _index 접미사 사용
- 업계 표준 용어는 유지

```python
# 올바른 예시
nvt_ratio()          # Network Value to Transactions Ratio
mvrv_ratio()         # Market Value to Realized Value Ratio
fear_greed_index()   # Fear and Greed Index
```

### 2.3 특징 생성 함수 (Feature Generation)
- generate_ 접두어 사용
- 명확한 출력 설명

```python
# 올바른 예시
generate_technical()     # 기술적 특징 생성
generate_price()        # 가격 관련 특징 생성
generate_volume()       # 거래량 특징 생성
```

### 2.4 분석 함수 (Analysis)
- analyze_ 접두어 사용
- 분석 대상을 명확히 표현

```python
# 올바른 예시
analyze_trend()         # 추세 분석
analyze_pattern()       # 패턴 분석
analyze_volatility()    # 변동성 분석
```

### 2.5 복합 지표 함수 (Composite Indicators)
- composite_ 접두어 사용
- 결합되는 주요 지표 명시

```python
# 올바른 예시
composite_trend()       # 추세 복합 지표
composite_momentum()    # 모멘텀 복합 지표
```

## 3. 파라미터 명명 규칙

### 3.1 기본 파라미터
- data: 기본 입력 데이터
- period: 계산 기간
- window: 이동창 크기
- threshold: 임계값

### 3.2 특수 파라미터
- high, low, close: 가격 데이터
- volume: 거래량 데이터
- weights: 가중치 값

## 4. 반환값 명명 규칙
- 단일 값: indicator_name
- 복수 값: indicator_name_type (예: macd_signal, macd_histogram)

## 5. 확장성 고려사항
- AI/ML 파이프라인과의 통합 용이성
- 실시간 처리 지원
- 새로운 지표 추가 용이성

## 6. 예시 코드 구조
```python
def rsi(data: pd.Series, period: int = 14) -> pd.Series:
    """상대강도지수(RSI) 계산"""
    
def macd(data: pd.Series, 
         fast_period: int = 12, 
         slow_period: int = 26, 
         signal_period: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """MACD 계산"""

def generate_technical(data: pd.DataFrame) -> pd.DataFrame:
    """기술적 특징 생성"""
``` 