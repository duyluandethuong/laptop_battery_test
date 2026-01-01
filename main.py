#!/usr/bin/env python3
"""
Laptop Battery Test - PyQt6 Application Entry Point
"""
import sys
import os
import logging
import traceback

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.main_window import MainWindow


def get_log_path():
    """Get a writable path for the log file."""
    # When bundled, use the user's home directory
    if getattr(sys, 'frozen', False):
        # Running as bundled app
<<<<<<< HEAD
        log_dir = os.path.expanduser('~/Library/Logs/LaptopBatteryTest')
=======
        if sys.platform == 'darwin':
            # macOS
            log_dir = os.path.expanduser('~/Library/Logs/LaptopBatteryTest')
        elif sys.platform == 'win32':
            # Windows
            log_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'LaptopBatteryTest', 'Logs')
        else:
            # Linux/Other
            log_dir = os.path.expanduser('~/.local/share/LaptopBatteryTest/logs')
        
>>>>>>> f40e228 (Update laptop battery test application)
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, 'logfilename.log')
    else:
        # Running from source
        return 'logfilename.log'


def setup_logging():
    """Setup logging configuration."""
    log_path = get_log_path()
    logging.basicConfig(
        filename=log_path,
        encoding='utf-8',
        level=logging.INFO,
        format='%(asctime)s | %(message)s'
    )
    logging.info(f"Log file location: {log_path}")


def main():
    """Main entry point."""
    try:
        setup_logging()
        
        app = QApplication(sys.argv)
        
        # Set application metadata
        app.setApplicationName("Laptop Battery Test")
        app.setApplicationVersion("1.0.0")
        
        # Set default font
        font = QFont("SF Pro Display", 12)
        font.setStyleHint(QFont.StyleHint.SansSerif)
        app.setFont(font)
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
        
    except Exception as e:
        # Show error dialog if app fails to start
        error_msg = f"Failed to start application:\n\n{str(e)}\n\n{traceback.format_exc()}"
        logging.error(error_msg)
        
        # Try to show a message box
        try:
            app = QApplication.instance() or QApplication(sys.argv)
            QMessageBox.critical(None, "Startup Error", error_msg)
        except:
            print(error_msg, file=sys.stderr)
        
        sys.exit(1)


if __name__ == "__main__":
    main()
