# 📁 Docs/Plan/Phase1/module/preprocessor.md

---

## 📌 목적
- 수집된 데이터를 전처리하여 분석 및 모델 학습에 적합한 형식으로 변환합니다.
- 결측치 처리, 이상치 제거, 데이터 정규화 등의 작업을 수행하여 데이터 품질을 보장합니다.

---

## 📁 디렉터리 구조
```plaintext
data/
├── __init__.py
├── arbitrage_collector.py
├── collector.py
├── data_storage.py
├── logger.py
├── onchain_collector.py
├── preprocessor.py            # 데이터 전처리를 수행하는 모듈
└── real_time_collector.py
```

---

## 📄 주요 기능
1. **결측치 처리**
   - 수집된 데이터에서 결측치를 확인하고 적절한 방식으로 처리.
2. **이상치 제거**
   - 통계적 기준 또는 특정 조건에 따라 이상치를 제거.
3. **데이터 정규화**
   - 특정 범위로 데이터를 스케일링하여 분석 및 모델 학습에 최적화.
4. **파생 변수 생성**
   - 데이터에 새로운 정보를 추가하기 위해 유용한 파생 변수를 생성.

---

## 🧩 주요 함수

### 1️⃣ `handle_missing_data(data: pd.DataFrame, method: str = "mean") -> pd.DataFrame`
- **설명**: 결측치를 처리합니다.
- **입력**:
data (pd.DataFrame): 원본 데이터프레임.
method (str): 결측치 처리 방법 ("mean", "median", "drop").
- **출력**:
  - 결측치가 처리된 데이터프레임.
- **예제 코드**:
  ```python
  def handle_missing_data(data: pd.DataFrame, method: str = "mean") -> pd.DataFrame:
      if method == "mean":
          return data.fillna(data.mean())
      elif method == "median":
        return data.fillna(data.median())
    elif method == "drop":
        return data.dropna()
    else:
        raise ValueError(f"Unknown method: {method}")

### 2️⃣ `remove_outliers(data: pd.DataFrame, columns: list) -> pd.DataFrame`
- **설명**: 지정된 컬럼에서 이상치를 제거합니다.
- **입력**:
  - `data` (pd.DataFrame): 원본 데이터프레임.
columns (list): 이상치를 제거할 컬럼 리스트.
- **출력**:
  - 이상치가 제거된 데이터프레임.
- **예제 코드**:
  ```python
  def remove_outliers(data: pd.DataFrame, columns: list) -> pd.DataFrame:
    for column in columns:
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    return data

### 3️⃣ `normalize_data(data: pd.DataFrame, columns: list, method: str = "minmax") -> pd.DataFrame`
- **설명**: 지정된 컬럼을 정규화합니다.
- **입력**:
  - `data` (pd.DataFrame): 원본 데이터프레임.
  - `columns` (list): 정규화할 컬럼 리스트.
  - `method` (str): 정규화 방법 ("minmax", "zscore").
- **출력**:
  - 정규화된 데이터프레임.
- **예제 코드**:
  ```python
    def normalize_data(data: pd.DataFrame, columns: list, method: str = "minmax") -> pd.DataFrame:
    if method == "minmax":
        for column in columns:
            data[column] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())
    elif method == "zscore":
        for column in columns:
            data[column] = (data[column] - data[column].mean()) / data[column].std()
    else:
        raise ValueError(f"Unknown normalization method: {method}")
    return data

### 4️⃣ `generate_features(data: pd.DataFrame) -> pd.DataFrame`
- **설명**: 데이터에서 새로운 파생 변수를 생성합니다.
- **입력**:
  - `data` (pd.DataFrame): 원본 데이터프레임.
- **출력**:
  - 파생 변수가 추가된 데이터프레임.
- **예제 코드**:
  ```python
  def generate_features(data: pd.DataFrame) -> pd.DataFrame:
    data["price_diff"] = data["high"] - data["low"]
    data["volume_change"] = data["volume"].diff()
    return data

---

## 🔗 통신 구조 및 의존성
- **통신 구조**:
  - `collector.py` → `data_storage.py` → `preprocessor.py` → 모델 학습 모듈.
- **의존성**:
  - `pandas`: 데이터 처리.
  - `numpy` : 수치 계산.
  - `sqlite3`: 데이터 로드.

---

## 📘 참고 문서 및 링크
- `Docs/Plan/Phase1/module_data.md`
- `Docs/Plan/Phase1/data_storage.md`
- `Docs/Plan/Phase1/logger.md`
