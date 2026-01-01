"""
Background worker for running battery tests.
"""
import time
import logging
import pyautogui
from PyQt6.QtCore import QObject, pyqtSignal

from utils.battery_utils import get_battery_level
from test_cases.office_test import run_office_test
from test_cases.browser_test import run_browser_test
from test_cases.youtube_test import run_youtube_test


class BatteryTestWorker(QObject):
    """Worker thread for running battery tests."""
    
    log_message = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, no_youtube='0'):
        super().__init__()
        self.no_youtube = no_youtube
        self._is_running = False
        self._is_paused = False
    
    def run(self):
        """Run the battery test loop."""
        # Disable pyautogui failsafe
        pyautogui.FAILSAFE = False
        
        self._is_running = True
        
        if self.no_youtube == '1':
            self.log_message.emit("📺 YouTube test is disabled")
        else:
            self.log_message.emit("📺 YouTube test is enabled")
        
        logging.info('====================== Starting new test... ====================')
        get_battery_level()
        
        try:
            while self._is_running:
                # Check for pause
                while self._is_paused and self._is_running:
                    time.sleep(0.5)
                
                if not self._is_running:
                    break
                
                # Run browser test
                self.log_message.emit("🌐 Running browser test...")
                logging.info("Starting browser test")
                run_browser_test()
                
                if not self._is_running:
                    break
                
                # Check for pause
                while self._is_paused and self._is_running:
                    time.sleep(0.5)
                
                if not self._is_running:
                    break
                
                # Run office test
                self.log_message.emit("📄 Running office test...")
                logging.info("Starting office test")
                run_office_test()
                
                if not self._is_running:
                    break
                
                # Check for pause
                while self._is_paused and self._is_running:
                    time.sleep(0.5)
                
                if not self._is_running:
                    break
                
                # Run YouTube test if enabled
                if str(self.no_youtube) != '1':
                    self.log_message.emit("📺 Running YouTube test...")
                    logging.info("Starting YouTube test")
                    run_youtube_test()
                
                if not self._is_running:
                    break
                
                get_battery_level()
                self.log_message.emit("🔄 Completed one test cycle, starting next...")
                
        except Exception as e:
            self.log_message.emit(f"❌ Error: {str(e)}")
            logging.error(f"Error during test: {str(e)}")
        
        self.finished.emit()
    
    def pause(self):
        """Pause the test."""
        self._is_paused = True
    
    def resume(self):
        """Resume the test."""
        self._is_paused = False
    
    def stop(self):
        """Stop the test."""
        self._is_running = False
        self._is_paused = False
