"""
파일명: logger.py
목적: 데이터 수집 및 처리 과정의 로깅 시스템 구현
주요 기능:
1. 로그 설정 초기화 및 관리
2. 이벤트 및 오류 로깅
3. 텔레그램 알림 발송
4. 로그 레벨별 처리
"""

import logging
import requests
from pathlib import Path
from typing import Optional
from datetime import datetime
import yaml
import os

class TradingLogger:
    """
    트레이딩 시스템의 로깅을 담당하는 클래스
    """
    
    def __init__(self, name: str = 'trading_bot'):
        """
        로거 초기화
        
        Args:
            name (str): 로거 이름
        """
        self.logger = logging.getLogger(name)
        self._load_config()
        self._setup_handlers()
        
    def _load_config(self) -> None:
        """
        로그 설정 파일을 로드합니다.
        """
        config_path = Path(__file__).parent.parent / 'log_config.yaml'
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.telegram_token = config.get('telegram', {}).get('token')
                self.telegram_chat_id = config.get('telegram', {}).get('chat_id')
                self.log_level = config.get('log_level', 'INFO')
        else:
            self.log_level = os.getenv('LOG_LEVEL', 'INFO')
            self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
            self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    def _setup_handlers(self) -> None:
        """
        로그 핸들러를 설정합니다.
        """
        self.logger.setLevel(getattr(logging, self.log_level))
        
        # 기존 핸들러 제거
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            
        # 파일 핸들러 설정
        log_dir = Path(__file__).parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        # 일자별 로그 파일 생성
        current_date = datetime.now().strftime('%Y%m%d')
        file_handler = logging.FileHandler(
            log_dir / f'trading_bot_{current_date}.log',
            encoding='utf-8'
        )
        
        # 포맷터 설정
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s %(module)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def send_telegram_alert(self, message: str, level: str = 'INFO') -> None:
        """
        텔레그램으로 알림을 발송합니다.
        
        Args:
            message (str): 발송할 메시지
            level (str): 로그 레벨 (INFO, WARNING, ERROR, CRITICAL)
        """
        if not (self.telegram_token and self.telegram_chat_id):
            self.logger.warning("Telegram credentials not configured")
            return
            
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            emoji = {
                'INFO': 'ℹ️',
                'WARNING': '⚠️',
                'ERROR': '❌',
                'CRITICAL': '🚨'
            }
            formatted_message = f"{emoji.get(level, 'ℹ️')} {level}\n{message}"
            
            response = requests.post(url, data={
                'chat_id': self.telegram_chat_id,
                'text': formatted_message
            })
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Failed to send Telegram alert: {str(e)}")

    def debug(self, message: str) -> None:
        """디버그 레벨 로그를 기록합니다."""
        self.logger.debug(message)

    def info(self, message: str, notify: bool = False) -> None:
        """
        정보 레벨 로그를 기록합니다.
        
        Args:
            message (str): 로그 메시지
            notify (bool): 텔레그램 알림 발송 여부
        """
        self.logger.info(message)
        if notify:
            self.send_telegram_alert(message, 'INFO')

    def warning(self, message: str, notify: bool = True) -> None:
        """
        경고 레벨 로그를 기록합니다.
        
        Args:
            message (str): 로그 메시지
            notify (bool): 텔레그램 알림 발송 여부
        """
        self.logger.warning(message)
        if notify:
            self.send_telegram_alert(message, 'WARNING')

    def error(self, message: str, notify: bool = True) -> None:
        """
        에러 레벨 로그를 기록합니다.
        
        Args:
            message (str): 로그 메시지
            notify (bool): 텔레그램 알림 발송 여부
        """
        self.logger.error(message)
        if notify:
            self.send_telegram_alert(message, 'ERROR')

    def critical(self, message: str, notify: bool = True) -> None:
        """
        치명적 에러 레벨 로그를 기록합니다.
        
        Args:
            message (str): 로그 메시지
            notify (bool): 텔레그램 알림 발송 여부
        """
        self.logger.critical(message)
        if notify:
            self.send_telegram_alert(message, 'CRITICAL')

# 전역 로거 인스턴스 생성
trading_logger = TradingLogger()
