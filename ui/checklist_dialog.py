"""
Checklist Dialog for pre-test verification.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QCheckBox, QPushButton, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt

from ui.styles.main_styles import DIALOG_STYLESHEET


CHECKLIST_ITEMS = [
    "Set laptop Power mode to \"Balance\" (on Mac, do not turn on High Performance Mode)",
    "Set laptop's screen brightness to 75% (on Mac, you can ask Siri \"Set screen brightness to 75%\" for an accurate setting). Leave all refresh rate at default config.",
    "Turn off auto turn off screen on battery power",
    "Connect your laptop to Wifi network, turn on Bluetooth",
    "Leave battery saver mode on if your laptop have it, set battery saver on at 30% (30% is the default settings for Windows in recent updates)",
    "Turn \"lower screen brightness on low battery\" off",
    "Turn off any battery settings such as auto dim / lock screen when user is away... (on some new Windows laptops)",
    "Turn the volume to 0%",
    "Charge your laptop to 100% battery",
]


class ChecklistDialog(QDialog):
    """Dialog showing pre-test checklist."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checkboxes = []
        self._setup_ui()
        self.setStyleSheet(DIALOG_STYLESHEET)
    
    def _setup_ui(self):
        """Setup the dialog UI."""
        self.setWindowTitle("Test Checklist")
        self.setMinimumSize(550, 450)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("Before you run any test, check all boxes")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Use this checklist to make sure all tests are consistent")
        subtitle.setObjectName("dialogSubtitle")
        layout.addWidget(subtitle)
        
        # Scroll area for checklist
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("checklistScroll")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(12)
        
        # Add checklist items
        for item in CHECKLIST_ITEMS:
            checkbox = QCheckBox(item)
            checkbox.setObjectName("checklistItem")
            self.checkboxes.append(checkbox)
            scroll_layout.addWidget(checkbox)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area, stretch=1)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.check_all_button = QPushButton("Check All")
        self.check_all_button.setObjectName("secondaryButton")
        self.check_all_button.clicked.connect(self._check_all)
        
        self.close_button = QPushButton("Close")
        self.close_button.setObjectName("primaryButton")
        self.close_button.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(self.check_all_button)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
    
    def _check_all(self):
        """Check all checkboxes."""
        all_checked = all(cb.isChecked() for cb in self.checkboxes)
        for checkbox in self.checkboxes:
            checkbox.setChecked(not all_checked)
        
        # Update button text
        if not all_checked:
            self.check_all_button.setText("Uncheck All")
        else:
            self.check_all_button.setText("Check All")
