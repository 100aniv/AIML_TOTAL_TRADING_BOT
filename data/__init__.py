"""
파일명: __init__.py
목적: data 모듈의 초기화 및 공통 기능 제공
주요 기능:
1. 환경 변수 로드 및 설정
2. 로깅 시스템 초기화
3. 공용 함수 및 클래스 제공
4. 모듈 간 의존성 관리
"""

from dotenv import load_dotenv
import os
import logging
from pathlib import Path

# 모듈에서 공개할 함수/클래스 목록
__all__ = [
    'load_environment',
    'initialize_logger',
    'get_project_root'
]

def get_project_root() -> Path:
    """
    프로젝트 루트 경로를 반환합니다.

    Returns:
        Path: 프로젝트 루트 디렉토리 경로
    """
    return Path(__file__).parent.parent

def load_environment() -> dict:
    """
    환경 변수를 로드하고 설정합니다.
    
    Returns:
        dict: 로드된 환경 변수 딕셔너리

    Raises:
        EnvironmentError: 필수 환경 변수가 없는 경우
    """
    load_dotenv()
    
    required_vars = {
        'DB_PATH': os.getenv('DB_PATH'),
        'BINANCE_API_KEY': os.getenv('BINANCE_API_KEY'),
        'BINANCE_SECRET_KEY': os.getenv('BINANCE_SECRET_KEY')
    }

    # 필수 환경 변수 검증
    missing_vars = [key for key, value in required_vars.items() if not value]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return required_vars

def initialize_logger() -> logging.Logger:
    """
    로깅 시스템을 초기화합니다.
    
    Returns:
        logging.Logger: 설정된 로거 객체

    Note:
        로그 레벨: DEBUG, INFO, WARNING, ERROR, CRITICAL
        로그 포맷: [시간] {로그레벨} {모듈명}: {메시지}
    """
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.DEBUG)

    # 파일 핸들러 설정
    log_dir = get_project_root() / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(log_dir / 'system.log')
    file_handler.setLevel(logging.DEBUG)
    
    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 로그 포맷 설정
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# 모듈 초기화 시 자동 실행
try:
    env_vars = load_environment()
    logger = initialize_logger()
    logger.info("Data module initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize data module: {str(e)}")
    raise
