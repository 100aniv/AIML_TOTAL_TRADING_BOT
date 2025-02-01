# preprocessor.py
# Description and functionality placeholder.

import pandas as pd
import numpy as np
from typing import Optional, Union, List, Dict, Tuple
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from datetime import datetime, timedelta

from .logger import trading_logger

class DataPreprocessor:
    """
    데이터 전처리를 담당하는 클래스
    """
    
    def __init__(self):
        """
        전처리기 초기화
        """
        self.logger = trading_logger
        self.scalers = {}
        
    def handle_missing_data(
        self,
        data: pd.DataFrame,
        method: str = 'ffill',
        threshold: float = 0.5
    ) -> pd.DataFrame:
        """
        결측치를 처리합니다.
        
        Args:
            data (pd.DataFrame): 입력 데이터프레임
            method (str): 결측치 처리 방법 ('ffill', 'bfill', 'interpolate', 'drop')
            threshold (float): 결측치 비율 임계값 (이 비율 이상인 컬럼 제거)
            
        Returns:
            pd.DataFrame: 결측치가 처리된 데이터프레임
        """
        try:
            df = data.copy()
            
            # 결측치 비율 계산
            missing_ratio = df.isnull().sum() / len(df)
            cols_to_drop = missing_ratio[missing_ratio > threshold].index
            
            if not cols_to_drop.empty:
                df.drop(columns=cols_to_drop, inplace=True)
                self.logger.warning(
                    f"Dropped columns with high missing ratio: {list(cols_to_drop)}"
                )
            
            # 결측치 처리
            if method == 'ffill':
                df.fillna(method='ffill', inplace=True)
                df.fillna(method='bfill', inplace=True)  # 첫 부분의 NA 처리
            elif method == 'bfill':
                df.fillna(method='bfill', inplace=True)
                df.fillna(method='ffill', inplace=True)  # 마지막 부분의 NA 처리
            elif method == 'interpolate':
                df.interpolate(method='time', inplace=True)
                df.fillna(method='ffill', inplace=True)  # 양 끝단 처리
                df.fillna(method='bfill', inplace=True)
            elif method == 'drop':
                df.dropna(inplace=True)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error in handling missing data: {str(e)}")
            raise
            
    def remove_outliers(
        self,
        df: pd.DataFrame,
        column: str,
        threshold: float = 3.0
    ) -> pd.DataFrame:
        """
        이상치를 제거합니다.
        
        Args:
            df (pd.DataFrame): 입력 데이터프레임
            column (str): 이상치를 제거할 열 이름
            threshold (float): Z-score 임계값 (기본값: 3.0)
            
        Returns:
            pd.DataFrame: 이상치가 제거된 데이터프레임
        """
        try:
            df_copy = df.copy()
            z_scores = np.abs((df_copy[column] - df_copy[column].mean()) / df_copy[column].std())
            mask = z_scores < threshold
            removed_count = len(df_copy) - mask.sum()
            
            if removed_count > 0:
                self.logger.info(f"Removed {removed_count} outliers from {column}")
                return df_copy[mask].copy()
            
            return df_copy
            
        except Exception as e:
            self.logger.error(f"Error in removing outliers: {str(e)}")
            return df
            
    def normalize_data(
        self,
        df: pd.DataFrame,
        column: str,
        method: str = 'minmax'
    ) -> pd.DataFrame:
        """
        데이터를 정규화합니다.

        Args:
            df (pd.DataFrame): 입력 데이터프레임
            column (str): 정규화할 열 이름
            method (str): 정규화 방법 ('minmax' 또는 'standard')

        Returns:
            pd.DataFrame: 정규화된 데이터프레임
        """
        try:
            if method == 'minmax':
                scaler = MinMaxScaler()
            else:
                scaler = StandardScaler()
                
            df = df.copy()
            df[column] = scaler.fit_transform(df[[column]])
            return df
            
        except Exception as e:
            self.logger.error(f"Error in normalizing data: {str(e)}")
            return df
            
    def scale_data(
        self,
        data: pd.DataFrame,
        columns: List[str],
        method: str = 'minmax',
        feature_range: Tuple[float, float] = (0, 1)
    ) -> pd.DataFrame:
        """
        데이터를 정규화/스케일링합니다.
        
        Args:
            data (pd.DataFrame): 입력 데이터프레임
            columns (List[str]): 스케일링할 컬럼 목록
            method (str): 스케일링 방법 ('minmax', 'standard')
            feature_range (tuple): MinMaxScaler의 범위
            
        Returns:
            pd.DataFrame: 스케일링된 데이터프레임
        """
        try:
            df = data.copy()
            
            for column in columns:
                if method == 'minmax':
                    scaler = MinMaxScaler(feature_range=feature_range)
                elif method == 'standard':
                    scaler = StandardScaler()
                else:
                    raise ValueError(f"Unknown scaling method: {method}")
                
                # 스케일링 수행
                values = df[column].values.reshape(-1, 1)
                scaled_values = scaler.fit_transform(values)
                df[f"{column}_scaled"] = scaled_values
                
                # 스케일러 저장
                self.scalers[column] = scaler
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error in scaling data: {str(e)}")
            raise
            
    def create_technical_features(
        self,
        data: pd.DataFrame,
        windows: List[int] = [5, 10, 20, 60]
    ) -> pd.DataFrame:
        """
        기술적 지표 기반의 특징을 생성합니다.
        
        Args:
            data (pd.DataFrame): OHLCV 데이터프레임
            windows (List[int]): 이동평균 등의 기간 목록
            
        Returns:
            pd.DataFrame: 기술적 지표가 추가된 데이터프레임
        """
        try:
            df = data.copy()
            
            # 가격 변화율
            df['returns'] = df['close'].pct_change()
            df['log_returns'] = np.log1p(df['returns'])
            
            # 이동평균
            for window in windows:
                df[f'ma_{window}'] = df['close'].rolling(window=window).mean()
                df[f'vol_{window}'] = df['volume'].rolling(window=window).mean()
                
            # 변동성
            df['volatility'] = df['returns'].rolling(window=20).std()
            
            # 거래량 지표
            df['volume_change'] = df['volume'].pct_change()
            df['volume_ma_ratio'] = df['volume'] / df['volume'].rolling(window=20).mean()
            
            # 결측치 처리
            df = self.handle_missing_data(df)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error in creating technical features: {str(e)}")
            raise
            
    def prepare_data_for_training(
        self,
        data: pd.DataFrame,
        target_column: str = 'close',
        sequence_length: int = 60,
        prediction_horizon: int = 1,
        train_ratio: float = 0.8
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        모델 학습을 위한 데이터셋을 준비합니다.
        
        Args:
            data (pd.DataFrame): 전처리된 데이터프레임
            target_column (str): 예측 대상 컬럼
            sequence_length (int): 입력 시퀀스 길이
            prediction_horizon (int): 예측 기간
            train_ratio (float): 학습 데이터 비율
            
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        try:
            # 데이터 준비
            df = data.copy()
            
            # 시퀀스 데이터 생성
            X, y = [], []
            for i in range(len(df) - sequence_length - prediction_horizon + 1):
                X.append(df.iloc[i:(i + sequence_length)].values)
                y.append(df[target_column].iloc[i + sequence_length + prediction_horizon - 1])
                
            X = np.array(X)
            y = np.array(y)
            
            # 학습/테스트 분할
            train_size = int(len(X) * train_ratio)
            X_train = X[:train_size]
            X_test = X[train_size:]
            y_train = y[:train_size]
            y_test = y[train_size:]
            
            self.logger.info(
                f"Prepared training data: X_train: {X_train.shape}, "
                f"X_test: {X_test.shape}"
            )
            
            return X_train, X_test, y_train, y_test
            
        except Exception as e:
            self.logger.error(f"Error in preparing training data: {str(e)}")
            raise

# 사용 예시
if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    # 테스트 데이터 생성
    test_data = pd.DataFrame({
        'close': np.random.randn(100),
        'volume': np.random.randint(1000, 10000, 100)
    })
    processed_data = preprocessor.create_technical_features(test_data)
    print(processed_data.head())
