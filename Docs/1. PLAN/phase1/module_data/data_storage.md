# 📁 Docs/Plan/Phase1/module/data_storage.md

---

## 📌 목적
- 수집된 데이터를 SQLite 데이터베이스에 저장하고 관리하는 역할을 담당합니다.
- 데이터베이스 초기화, 데이터 삽입, 중복 제거 및 최적화 기능을 제공합니다.

---

## 🛠️ 주요 기능
1. **데이터베이스 초기화**
   - 데이터베이스 파일 생성 및 테이블 스키마 정의.
   - 데이터 저장소 준비.
2. **데이터 저장**
   - 수집된 데이터를 효율적으로 저장.
   - 중복 데이터 검증 및 제거.
3. **데이터베이스 관리**
   - 데이터 백업 및 복구를 지원.
   - 오래된 데이터 삭제 및 정리.

---

## 🧩 주요 함수

### 1️⃣ `initialize_database(db_path: str) -> sqlite3.Connection`
- **설명**: 데이터베이스 파일을 초기화하고 필요한 테이블을 생성.
- **입력값**:
  - `db_path`: 데이터베이스 파일 경로.
- **출력값**:
  - 데이터베이스 연결 객체.
- **세부 구현**:
  ```python
  import sqlite3

  def initialize_database(db_path: str) -> sqlite3.Connection:
      """
      데이터베이스 초기화 및 테이블 생성
      :param db_path: 데이터베이스 파일 경로
      :return: SQLite 연결 객체
      """
      try:
          conn = sqlite3.connect(db_path)
          cursor = conn.cursor()
          # 테이블 생성
          cursor.execute("""
          CREATE TABLE IF NOT EXISTS ohlcv (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              timestamp TEXT NOT NULL,
              symbol TEXT NOT NULL,
              open REAL NOT NULL,
              high REAL NOT NULL,
              low REAL NOT NULL,
              close REAL NOT NULL,
              volume REAL NOT NULL,
              UNIQUE(timestamp, symbol)
          )
          """)
          conn.commit()
          print("데이터베이스 초기화 성공")
          return conn
      except Exception as e:
          print(f"데이터베이스 초기화 실패: {e}")
          raise e
  ```

### 2️⃣ `store_data(conn: sqlite3.Connection, table_name: str, data: pd.DataFrame) -> None`
- **설명**: Pandas 데이터프레임을 지정된 테이블에 저장.
- **입력값**:
  - `conn`: SQLite 연결 객체.
  - `table_name`: 저장할 테이블 이름.
  - `data`: 저장할 데이터 (Pandas DataFrame).
- **출력값**:
  - `None`.
- **세부 구현**:
  ```python
  import pandas as pd

    def store_data(conn: sqlite3.Connection, table_name: str, data: pd.DataFrame) -> None:
    """
    데이터 저장
    :param conn: SQLite 연결 객체
    :param table_name: 저장할 테이블 이름
    :param data: Pandas DataFrame 형태의 데이터
    """
    try:
        data.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"{len(data)} 개의 데이터가 {table_name} 테이블에 저장됨")
    except Exception as e:
        print(f"데이터 저장 실패: {e}")
        raise e
  ```

### 3️⃣ `remove_old_data(conn: sqlite3.Connection, table_name: str, date_threshold: str) -> None`
- **설명**: 특정 날짜 이전의 데이터를 삭제하여 데이터베이스를 정리.
- **입력값**:
  - `conn`: SQLite 연결 객체.
  - `table_name`: 삭제할 데이터가 있는 테이블 이름.
  - `date_threshold`: 삭제 기준 날짜 (ISO 형식).
- **출력값**:
  - `None`.
- **세부 구현**:
  ```python
  def remove_old_data(conn: sqlite3.Connection, table_name: str, date_threshold: str) -> None:
      """
    오래된 데이터 삭제
    :param conn: SQLite 연결 객체
    :param table_name: 테이블 이름
    :param date_threshold: 삭제 기준 날짜
    """
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE timestamp < ?", (date_threshold,))
        conn.commit()
        print(f"{table_name} 테이블에서 {date_threshold} 이전의 데이터 삭제 완료")
    except Exception as e:
        print(f"오래된 데이터 삭제 실패: {e}")
        raise e

---

## 🔗 통신 구조 및 의존성
1️⃣ 통신 구조
- 입력:
  - collector.py에서 수집한 데이터를 저장.
- 출력:
preprocessor.py에서 정제된 데이터 요청.
흐름:
plaintext
collector.py → data_storage.py → preprocessor.py
### 2️⃣ 의존성
- 외부 라이브러리:
  - sqlite3: 데이터베이스 연결 및 조작.
  - pandas: 데이터 저장 및 조작.
- 내부 모듈:
  - logger: 데이터 저장 이벤트 및 오류 로깅.

## 📘 참고 문서
- Docs/Plan/Phase1/module/collector.md
- Docs/Plan/Phase1/module/preprocessor.md
