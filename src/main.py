import sys
from ui.main_window import SteelStrengthPredictor
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = SteelStrengthPredictor()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()