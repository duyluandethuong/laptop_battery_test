#!/usr/bin/env python3
"""
Laptop Battery Test - PyQt6 Application Entry Point
"""
import sys
import logging

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.main_window import MainWindow


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        filename='logfilename.log',
        encoding='utf-8',
        level=logging.INFO,
        format='%(asctime)s | %(message)s'
    )


def main():
    """Main entry point."""
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


if __name__ == "__main__":
    main()
