import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from password_checker import PasswordChecker
from app_logic import PasswordAppLogic

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join("ui", "main_page.ui"), self)
        self.setWindowTitle("Passwerify - Check Password")
        self.pushButton.clicked.connect(self.on_verify_clicked)
        self.label_error.setVisible(False)
        self.app_logic = PasswordAppLogic()
        self.last_password = ""
        
    def on_verify_clicked(self):
        password = self.textedit_password_value.toPlainText().strip()
        self.last_password = password
        success, message = self.app_logic.check_password_input(password)
        
        if not success:
            self.show_error(message)
            return
            
        self.label_error.setVisible(False)
        self.result_window = ResultWindow(password, self.app_logic, self)
        self.result_window.show()
        self.hide()
        
    def clear_password_field(self):
        self.textedit_password_value.clear()
        self.label_error.setVisible(False)
        
    def set_password_to_edit(self, password):
        self.textedit_password_value.setText(password)
        self.label_error.setVisible(False)
        
    def show_error(self, message):
        self.label_error.setText(message)
        self.label_error.setVisible(True)
        
    def closeEvent(self, event):
        QApplication.quit()

class ResultWindow(QMainWindow):
    def __init__(self, password, app_logic, main_window):
        super().__init__()
        uic.loadUi(os.path.join("ui", "verify_page.ui"), self)
        self.setWindowTitle("Passwerify - Results")
        self.password = password
        self.app_logic = app_logic
        self.main_window = main_window
        self.setup_ui()
        self.label_password_value.setText(self.password)
        self.analyze_password()
        
    def setup_ui(self):
        self.label_error.setVisible(False)
        self.apply_textedit_styles()
        self.button_new_password.clicked.connect(self.on_new_password_clicked)
        self.button_fix_password.clicked.connect(self.on_fix_password_clicked)
        
    def apply_textedit_styles(self):
        good_style = """
            QTextEdit {
                font: 15pt "Segoe Print";
                color: rgb(0, 170, 0);
                background: transparent;
                border: none;
            }
        """
        
        bad_style = """
            QTextEdit {
                font: 15pt "Segoe Print";
                color: rgb(170, 0, 0);
                background: transparent;
                border: none;
            }
        """
        
        self.textedit_good_moments.setStyleSheet(good_style)
        self.textedit_bad_moments.setStyleSheet(bad_style)
        
        good_font = QFont("Segoe Print", 15)
        self.textedit_good_moments.setFont(good_font)
        self.textedit_bad_moments.setFont(QFont("Segoe Print", 15))
        
        self.textedit_good_moments.setReadOnly(True)
        self.textedit_bad_moments.setReadOnly(True)
        self.textedit_good_moments.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textedit_bad_moments.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    
    def on_new_password_clicked(self):
        self.main_window.clear_password_field()
        self.main_window.show()
        self.hide()
        
    def on_fix_password_clicked(self):
        self.main_window.set_password_to_edit(self.password)
        self.main_window.show()
        self.hide()
        
    def analyze_password(self):
        try:
            result = self.app_logic.analyze_password(self.password)
            self.update_ui_with_results(result)
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
            
    def update_ui_with_results(self, result):
        self.label_security_value.setText(result['security_level'])
        
        if result['good_moments']:
            good_text = "\n\n".join([f"✓ {item}" for item in result['good_moments']])
            self.textedit_good_moments.setPlainText(good_text)
        else:
            self.textedit_good_moments.setPlainText("No good points found")
            
        if result['bad_moments']:
            bad_text = "\n\n".join([f"✗ {item}" for item in result['bad_moments']])
            self.textedit_bad_moments.setPlainText(bad_text)
        else:
            self.textedit_bad_moments.setPlainText("No issues found!")
            
        self.display_grade_image(result['grade'])
        self.set_security_level_color(result['security_level'])
        
    def display_grade_image(self, grade):
        image_path = os.path.join("images", f"{grade.lower()}grade.png")
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(
                self.label_grade_image.width(),
                self.label_grade_image.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_grade_image.setPixmap(pixmap)
        else:
            self.label_grade_image.setText(grade)
            self.label_grade_image.setStyleSheet("""
                font-size: 48px;
                font-weight: bold;
                color: #2c3e50;
                border: 3px solid #2c3e50;
                border-radius: 50px;
            """)
            
    def set_security_level_color(self, security_level):
        colors = {
            "Very Low": "color: #e74c3c;",
            "Low": "color: #e67e22;",
            "Mid": "color: #f39c12;",
            "High": "color: #2ecc71;",
            "Very High": "color: #27ae60;",
        }
        
        style = colors.get(security_level, "")
        new_style = f"font: 75 18pt 'MS Sans Serif'; {style}"
        self.label_security_value.setStyleSheet(new_style)
        
    def show_error(self, message):
        self.label_error.setText(message)
        self.label_error.setVisible(True)
        
    def closeEvent(self, event):
        if self.main_window:
            self.main_window.show()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()