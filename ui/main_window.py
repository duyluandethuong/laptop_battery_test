"""
Main Window for Battery Test Application
"""
import sys
import os
import re
import logging
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFrame, QCheckBox,
    QLineEdit, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QColor, QPalette, QTextCursor

from ui.worker import BatteryTestWorker
from ui.checklist_dialog import ChecklistDialog
from ui.styles.main_styles import MAIN_STYLESHEET


class LogHandler(logging.Handler):
    """Custom logging handler that emits signals for the UI."""
    
    def __init__(self, signal):
        super().__init__()
        self.signal = signal
        self.setFormatter(logging.Formatter('%(asctime)s | %(message)s'))
    
    def emit(self, record):
        msg = self.format(record)
        self.signal.emit(msg)


class ElapsedTimeFilter(logging.Filter):
    """Filter to inject elapsed time into log records."""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
    
    def filter(self, record):
        if hasattr(self.main_window, 'elapsed_seconds'):
            s = self.main_window.elapsed_seconds
            h, r = divmod(s, 3600)
            m, s = divmod(r, 60)
            record.elapsed = f"[{h:02d}:{m:02d}:{s:02d}]"
        else:
            record.elapsed = "[00:00:00]"
        return True


class MainWindow(QMainWindow):
    """Main application window."""
    
    log_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.worker_thread = None
        self.start_time = None
        self.elapsed_seconds = 0
        self.is_paused = False
        
        # Default log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_path = os.path.join(os.path.expanduser('~'), f'battery_test_{timestamp}.log')
        
        self._setup_ui()
        self._setup_timer()
        self._setup_logging()
        self._apply_styles()
    
    def _setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("Laptop Battery Test")
        self.resize(1024, 768)
        self.setMinimumSize(700, 550)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)
        
        # Header
        header_label = QLabel("Laptop Battery Test")
        header_label.setObjectName("header")
        main_layout.addWidget(header_label)
        
        # Timer section
        timer_frame = QFrame()
        timer_frame.setObjectName("timerFrame")
        timer_layout = QVBoxLayout(timer_frame)
        timer_layout.setContentsMargins(16, 16, 16, 16)
        
        timer_title = QLabel("Elapsed Time")
        timer_title.setObjectName("sectionTitle")
        timer_layout.addWidget(timer_title)
        
        self.timer_label = QLabel("00:00:00")
        self.timer_label.setObjectName("timerLabel")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.timer_label)
        
        # Battery level indicator
        battery_layout = QHBoxLayout()
        battery_text = QLabel("Battery:")
        battery_text.setObjectName("batteryText")
        self.battery_label = QLabel("---%")
        self.battery_label.setObjectName("batteryLabel")
        battery_layout.addStretch()
        battery_layout.addWidget(battery_text)
        battery_layout.addWidget(self.battery_label)
        battery_layout.addStretch()
        timer_layout.addLayout(battery_layout)
        
        main_layout.addWidget(timer_frame)
        
        # Options section
        options_layout = QHBoxLayout()
        self.youtube_checkbox = QCheckBox("Enable YouTube Test")
        self.youtube_checkbox.setChecked(True)
        self.youtube_checkbox.setObjectName("optionCheckbox")
        options_layout.addWidget(self.youtube_checkbox)
        options_layout.addStretch()
        
        # Test Office button
        test_office_button = QPushButton("Test Office")
        test_office_button.setObjectName("checklistButton")
        test_office_button.clicked.connect(self._test_office)
        options_layout.addWidget(test_office_button)
        
        # Test Checklist button
        checklist_button = QPushButton("Test Checklist")
        checklist_button.setObjectName("checklistButton")
        checklist_button.clicked.connect(self._show_checklist)
        options_layout.addWidget(checklist_button)
        
        main_layout.addLayout(options_layout)
        
        # Log location section
        log_location_layout = QHBoxLayout()
        log_location_label = QLabel("Log file:")
        log_location_label.setObjectName("logLocationLabel")
        log_location_layout.addWidget(log_location_label)
        
        self.log_path_edit = QLineEdit(self.log_path)
        self.log_path_edit.setObjectName("logPathEdit")
        self.log_path_edit.setReadOnly(True)
        log_location_layout.addWidget(self.log_path_edit, stretch=1)
        
        browse_button = QPushButton("Browse")
        browse_button.setObjectName("browseButton")
        browse_button.clicked.connect(self._browse_log_location)
        log_location_layout.addWidget(browse_button)
        
        main_layout.addLayout(log_location_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.start_button = QPushButton("▶ Start")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self._on_start)
        
        self.pause_button = QPushButton("⏸ Pause")
        self.pause_button.setObjectName("pauseButton")
        self.pause_button.clicked.connect(self._on_pause)
        self.pause_button.setEnabled(False)
        
        self.stop_button = QPushButton("⏹ Stop")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self._on_stop)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        
        main_layout.addLayout(button_layout)
        
        # Status indicator
        status_layout = QHBoxLayout()
        status_text = QLabel("Status:")
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        status_layout.addWidget(status_text)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        main_layout.addLayout(status_layout)
        
        # Log section
        log_frame = QFrame()
        log_frame.setObjectName("logFrame")
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(16, 16, 16, 16)
        
        # Log title and clear button on same row
        log_header_layout = QHBoxLayout()
        log_title = QLabel("Log")
        log_title.setObjectName("sectionTitle")
        log_header_layout.addWidget(log_title)
        log_header_layout.addStretch()
        
        clear_button = QPushButton("Clear Log")
        clear_button.setObjectName("clearButton")
        clear_button.clicked.connect(self._clear_log)
        log_header_layout.addWidget(clear_button)
        
        log_layout.addLayout(log_header_layout)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setObjectName("logText")
        self.log_text.setMinimumHeight(180)
        log_layout.addWidget(self.log_text)
        
        main_layout.addWidget(log_frame, stretch=1)
    
    def _setup_timer(self):
        """Setup the elapsed time timer."""
        self.elapsed_timer = QTimer()
        self.elapsed_timer.timeout.connect(self._update_elapsed_time)
        
        # Battery check timer
        self.battery_timer = QTimer()
        self.battery_timer.timeout.connect(self._update_battery)
        self.battery_timer.start(5000)  # Check every 5 seconds
        self._update_battery()  # Initial check
    
    def _setup_logging(self):
        """Setup logging to capture logs in the UI."""
        self.log_signal.connect(self._append_log)
        self.log_handler = LogHandler(self.log_signal)
        
        # Add filter to inject elapsed time
        self.log_handler.addFilter(ElapsedTimeFilter(self))
        self.log_handler.setFormatter(logging.Formatter('%(elapsed)s %(asctime)s | %(message)s'))
        
        # Get root logger and add our handler
        root_logger = logging.getLogger()
        root_logger.addHandler(self.log_handler)
        root_logger.setLevel(logging.INFO)
    
    def _apply_styles(self):
        """Apply stylesheet to the application."""
        self.setStyleSheet(MAIN_STYLESHEET)
    
    def _show_checklist(self):
        """Show the pre-test checklist dialog."""
        dialog = ChecklistDialog(self)
        dialog.exec()
    
    def _test_office(self):
        """Run the office test to verify Office files open correctly."""
        from test_cases.office_test import run_office_test
        self._append_log("📄 Running Office test...")
        try:
            run_office_test()
            self._append_log("✅ Office test completed")
        except Exception as e:
            self._append_log(f"❌ Office test failed: {str(e)}")
    
    def _browse_log_location(self):
        """Open file dialog to select log file location."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select Log File Location",
            self.log_path,
            "Log Files (*.log);;All Files (*)"
        )
        if file_path:
            self.log_path = file_path
            self.log_path_edit.setText(file_path)
            self._append_log(f"📁 Log location changed to: {file_path}")
    
    def _is_worker_running(self):
        """Check if worker thread is actually running."""
        return self.worker_thread is not None and self.worker_thread.isRunning()
    
    def _on_start(self):
        """Handle start button click."""
        if self._is_worker_running():
            self._append_log("⚠️ Waiting for previous test to finish cleanup...")
            return

        if self.is_paused:
            # Resume
            self._resume_test()
            return
        
        # Start new test
        self.start_time = datetime.now()
        self.elapsed_seconds = 0
        self.timer_label.setText("00:00:00")
        
        # Configure file logging with selected path
        file_handler = logging.FileHandler(self.log_path, encoding='utf-8')
        file_handler.addFilter(ElapsedTimeFilter(self))
        file_handler.setFormatter(logging.Formatter('%(elapsed)s %(asctime)s | %(message)s'))
        logging.getLogger().addHandler(file_handler)
        
        # Update UI state
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.youtube_checkbox.setEnabled(False)
        self._set_status("Running", "#00ff88")
        
        # Start elapsed timer
        self.elapsed_timer.start(1000)
        
        # Start worker thread
        no_youtube = '0' if self.youtube_checkbox.isChecked() else '1'
        self.worker_thread = QThread()
        self.worker = BatteryTestWorker(no_youtube)
        self.worker.moveToThread(self.worker_thread)
        
        self.worker.log_message.connect(self._append_log)
        self.worker.finished.connect(self._on_worker_finished)
        self.worker_thread.started.connect(self.worker.run)
        
        self.worker_thread.start()
        
        self._append_log(f"🚀 Test started! Logging to: {self.log_path}")
    
    def _on_pause(self):
        """Handle pause button click."""
        if not self.is_paused:
            # Pause
            self.is_paused = True
            self.elapsed_timer.stop()
            if self.worker:
                self.worker.pause()
            self.pause_button.setText("▶ Resume")
            self.start_button.setEnabled(False)
            self._set_status("Paused", "#ffd700")
            self._append_log("⏸ Test paused")
        else:
            self._resume_test()
    
    def _resume_test(self):
        """Resume the paused test."""
        self.is_paused = False
        self.elapsed_timer.start(1000)
        if self.worker:
            self.worker.resume()
        self.pause_button.setText("⏸ Pause")
        self._set_status("Running", "#00ff88")
        self._append_log("▶ Test resumed")
    
    def _on_stop(self):
        """Handle stop button click."""
        self._append_log("⏹ Stopping test (waiting for current task)...")
        self.elapsed_timer.stop()
        
        if self.worker:
            self.worker.stop()
            
        self.stop_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self._set_status("Stopping...", "#ff9800")
    
    def _cleanup_test(self):
        """Clean up thread and reset UI."""
        self.elapsed_timer.stop()
        
        # Cleanup thread safe
        if self.worker_thread:
            if self.worker_thread.isRunning():
                self.worker_thread.quit()
                self.worker_thread.wait(2000) # Wait up to 2s
            self.worker_thread = None
        
        self.worker = None
        self.is_paused = False
        
        # Reset UI state
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.pause_button.setText("⏸ Pause")
        self.stop_button.setEnabled(False)
        self.youtube_checkbox.setEnabled(True)
        self._set_status("Stopped", "#f44336")

    def _on_worker_finished(self):
        """Handle worker thread completion."""
        self._cleanup_test()
        self._append_log("✅ Test finished")
        
    def _stop_test(self):
        """Legacy method needed for closeEvent - force stop."""
        self.elapsed_timer.stop()
        if self.worker:
            self.worker.stop()
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait(1000)
        self._cleanup_test()
    
    def _update_elapsed_time(self):
        """Update the elapsed time display."""
        self.elapsed_seconds += 1
        hours = self.elapsed_seconds // 3600
        minutes = (self.elapsed_seconds % 3600) // 60
        seconds = self.elapsed_seconds % 60
        self.timer_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def _update_battery(self):
        """Update the battery level display."""
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                self.battery_label.setText(f"{percent:.0f}%")
                
                # Color based on level
                if percent > 50:
                    color = "#00ff88"
                elif percent > 20:
                    color = "#ffd700"
                else:
                    color = "#f44336"
                self.battery_label.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold;")
            else:
                self.battery_label.setText("N/A")
        except Exception:
            self.battery_label.setText("N/A")
    
    def _set_status(self, text, color):
        """Set the status label text and color."""
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: 500;")
    
    def _append_log(self, message):
        """Append a message to the log."""
        # Check if message already starts with elapsed time format [HH:MM:SS]
        if not re.match(r'^\[\d{2}:\d{2}:\d{2}\]', message):
            # Calculate current elapsed time string
            hours = self.elapsed_seconds // 3600
            minutes = (self.elapsed_seconds % 3600) // 60
            seconds = self.elapsed_seconds % 60
            elapsed_str = f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"
            message = f"{elapsed_str} {message}"
        
        self.log_text.append(message)
        # Auto-scroll to bottom
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_text.setTextCursor(cursor)
    
    def _clear_log(self):
        """Clear the log text."""
        self.log_text.clear()
    
    def closeEvent(self, event):
        """Handle window close event."""
        self._stop_test()
        super().closeEvent(event)
