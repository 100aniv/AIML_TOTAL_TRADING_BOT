"""
Logger 모듈 테스트
목적: data/logger.py의 구현된 기능 테스트
"""

import os
import pytest
from data.logger import trading_logger

class TestLogger:
    def test_file_logging(self):
        """로그 파일 생성 및 기록 테스트"""
        log_file = "logs/trading_bot.log"
        
        # 로그 기록
        test_msg = "Test log message"
        trading_logger.info(test_msg)
        
        # 파일 생성 확인
        assert os.path.exists(log_file)
        
        # 로그 내용 확인
        with open(log_file, 'r') as f:
            log_content = f.read()
            assert test_msg in log_content

    def test_log_levels(self):
        """로그 레벨별 기록 테스트"""
        # 각 레벨별 로그 기록
        trading_logger.debug("Debug message")
        trading_logger.info("Info message")
        trading_logger.warning("Warning message")
        trading_logger.error("Error message")
        
        # 로그 파일에서 각 레벨 메시지 확인
        with open("logs/trading_bot.log", 'r') as f:
            log_content = f.read()
            assert "INFO" in log_content
            assert "WARNING" in log_content
            assert "ERROR" in log_content

    def test_telegram_notification(self):
        """텔레그램 알림 기능 테스트"""
        # 텔레그램 자격증명이 설정된 경우에만 테스트
        if os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_CHAT_ID'):
            trading_logger.error("Test telegram notification", notify=True)
            # 실제 전송은 어려우므로 예외가 발생하지 않는지만 확인
            assert True
        else:
            pytest.skip("Telegram credentials not configured")

    def test_custom_format(self):
        """로그 포맷 테스트"""
        test_msg = "Test format message"
        trading_logger.info(test_msg)
        
        with open("logs/trading_bot.log", 'r') as f:
            last_line = f.readlines()[-1]
            # 날짜, 시간, 로그 레벨, 메시지 포맷 확인
            assert "[INFO]" in last_line
            assert test_msg in last_line 