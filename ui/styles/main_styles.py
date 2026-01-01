"""
Application stylesheet for the Battery Test UI.
"""

MAIN_STYLESHEET = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
    }
    
    QLabel {
        color: #e8e8e8;
        font-size: 14px;
    }
    
    QLabel#header {
        color: #ffffff;
        font-size: 28px;
        font-weight: bold;
        padding: 10px 0;
    }
    
    QLabel#timerLabel {
        color: #00ff88;
        font-size: 56px;
        font-weight: bold;
        font-family: 'SF Mono', 'Menlo', monospace;
        padding: 20px;
    }
    
    QLabel#batteryText {
        color: #aaa;
        font-size: 16px;
    }
    
    QLabel#batteryLabel {
        color: #ffd700;
        font-size: 20px;
        font-weight: bold;
    }
    
    QLabel#statusLabel {
        color: #888;
        font-size: 14px;
        font-weight: 500;
    }
    
    QFrame#timerFrame, QFrame#logFrame {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
    }
    
    QLabel#sectionTitle {
        color: #aaa;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    QPushButton {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: #e8e8e8;
        font-size: 15px;
        font-weight: 600;
        padding: 14px 28px;
        min-width: 120px;
    }
    
    QPushButton:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    QPushButton:pressed {
        background: rgba(255, 255, 255, 0.2);
    }
    
    QPushButton:disabled {
        background: rgba(255, 255, 255, 0.03);
        border-color: rgba(255, 255, 255, 0.05);
        color: #555;
    }
    
    QPushButton#startButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #00c853, stop:1 #00e676);
        border: none;
        color: #fff;
    }
    
    QPushButton#startButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #00e676, stop:1 #69f0ae);
    }
    
    QPushButton#startButton:disabled {
        background: #2a3a2a;
        color: #555;
    }
    
    QPushButton#pauseButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #ff9800, stop:1 #ffb74d);
        border: none;
        color: #fff;
    }
    
    QPushButton#pauseButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #ffb74d, stop:1 #ffc947);
    }
    
    QPushButton#pauseButton:disabled {
        background: #3a3a2a;
        color: #555;
    }
    
    QPushButton#stopButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #f44336, stop:1 #ef5350);
        border: none;
        color: #fff;
    }
    
    QPushButton#stopButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #ef5350, stop:1 #e57373);
    }
    
    QPushButton#stopButton:disabled {
        background: #3a2a2a;
        color: #555;
    }
    
    QPushButton#clearButton {
        padding: 8px 16px;
        min-width: 80px;
        font-size: 12px;
    }
    
    QPushButton#checklistButton {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: #e8e8e8;
        font-size: 13px;
        font-weight: 500;
        padding: 10px 20px;
        min-width: 100px;
    }
    
    QPushButton#checklistButton:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    QCheckBox#optionCheckbox {
        color: #ffffff;
    }
    
    QTextEdit#logText {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #00ff88;
        font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
        font-size: 12px;
        padding: 12px;
    }
"""

DIALOG_STYLESHEET = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
    }
    
    QLabel#dialogTitle {
        color: #ffffff;
        font-size: 20px;
        font-weight: bold;
    }
    
    QLabel#dialogSubtitle {
        color: #aaa;
        font-size: 14px;
    }
    
    QPushButton#primaryButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #00c853, stop:1 #00e676);
        border: none;
        border-radius: 8px;
        color: #fff;
        font-size: 14px;
        font-weight: 600;
        padding: 12px 24px;
        min-width: 100px;
    }
    
    QPushButton#primaryButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #00e676, stop:1 #69f0ae);
    }
    
    QPushButton#secondaryButton {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: #e8e8e8;
        font-size: 14px;
        font-weight: 600;
        padding: 12px 24px;
        min-width: 100px;
    }
    
    QPushButton#secondaryButton:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
    }
"""
