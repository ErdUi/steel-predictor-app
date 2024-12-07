from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QComboBox, QPushButton, 
                           QTextEdit, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from model.predictor import SteelPredictor
import numpy as np

class SteelStrengthPredictor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steel Strength Predictor")
        self.setMinimumSize(800, 600)
        self.predictor = SteelPredictor()
        self.setup_ui()

    def setup_ui(self):
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create input section
        input_group = QWidget()
        input_layout = QGridLayout(input_group)
        
        # Input fields
        self.inputs = {}
        parameters = {
            'QC_Re': 'Certificate yield strength',
            'QC_Rm': 'Certificate tensile strength',
            'QC_A': 'Certificate Elongation',
            'Dimension': 'Thickness in mm'
        }
        
        row = 0
        for name, description in parameters.items():
            label = QLabel(f"{name}:")
            input_field = QLineEdit()
            input_field.setPlaceholderText(description)
            self.inputs[name] = input_field
            input_layout.addWidget(label, row, 0)
            input_layout.addWidget(input_field, row, 1)
            row += 1
        
        # Manufacturer dropdown
        label = QLabel("Manufacturer:")
        self.manufacturer_combo = QComboBox()
        self.manufacturer_combo.addItems([
            "Select manufacturer...",
            "Manufacturer A",
            "Manufacturer B",
            "Manufacturer C"
        ])
        input_layout.addWidget(label, row, 0)
        input_layout.addWidget(self.manufacturer_combo, row, 1)
        
        # Grade selection
        row += 1
        label = QLabel("Grade:")
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(["S355", "S690"])
        input_layout.addWidget(label, row, 0)
        input_layout.addWidget(self.grade_combo, row, 1)
        
        layout.addWidget(input_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.predict_button = QPushButton("Predict")
        self.predict_button.clicked.connect(self.predict)
        self.train_button = QPushButton("Train Model")
        self.train_button.clicked.connect(self.train_model)
        button_layout.addWidget(self.train_button)
        button_layout.addWidget(self.predict_button)
        layout.addLayout(button_layout)
        
        # Results area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)

    def get_min_yield_strength(self, thickness, grade):
        """Determine minimum required yield strength based on thickness and grade."""
        if grade == 'S355':
            if thickness <= 16:
                return 355
            elif thickness <= 40:
                return 345
            elif thickness <= 63:
                return 335
            elif thickness <= 80:
                return 325
            elif thickness <= 100:
                return 315
            elif thickness <= 150:
                return 295
            elif thickness <= 200:
                return 285
            elif thickness <= 250:
                return 275
            elif thickness <= 400:
                return 265
            else:
                return None
        elif grade == 'S690':
            if thickness <= 50:
                return 690
            elif thickness <= 100:
                return 650
            elif thickness <= 150:
                return 630
            else:
                return 630
        return None

    def train_model(self):
        """Train the Random Forest model with sample data."""
        try:
            # For demo purposes, we'll use sample data
            # In production, you would load your actual training data here
            X_train = np.random.rand(100, 4)  # Sample features
            y_train = np.random.rand(100)     # Sample target
            
            self.predictor.train(X_train, y_train)
            
            QMessageBox.information(self, "Success", "Model trained successfully!")
            self.results_text.append("Model trained successfully!\n")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error training model: {str(e)}")
            self.results_text.append(f"Error training model: {str(e)}\n")

    def predict(self):
        """Make prediction based on input values."""
        if self.predictor.model is None:
            QMessageBox.warning(self, "Warning", "Please train the model first!")
            return
            
        try:
            # Get input values
            input_values = []
            for name in ['QC_Re', 'QC_Rm', 'QC_A', 'Dimension']:
                value = float(self.inputs[name].text())
                input_values.append(value)
            
            # Create feature array
            X = np.array(input_values).reshape(1, -1)
            
            # Make prediction
            prediction = self.predictor.predict(X)[0]
            
            # Get grade and thickness for requirements check
            grade = self.grade_combo.currentText()
            thickness = float(self.inputs['Dimension'].text())
            min_strength = self.get_min_yield_strength(thickness, grade)
            
            # Check if prediction meets requirements
            margin = prediction - min_strength if min_strength else 0
            passes = margin >= 0 if min_strength else None
            
            # Format results
            result_text = f"""
Prediction Results:
------------------
Predicted Yield Strength: {prediction:.1f} MPa
Minimum Required Strength: {min_strength:.1f} MPa
Margin: {margin:.1f} MPa
Status: {"PASS" if passes else "FAIL"} 
"""
            self.results_text.setText(result_text)
            
            # Show appropriate message box
            if passes:
                QMessageBox.information(self, "Result", "Material PASSES requirements!")
            else:
                QMessageBox.warning(self, "Result", "Material FAILS requirements!")
                
        except ValueError as e:
            QMessageBox.critical(self, "Error", "Please enter valid numeric values for all fields.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error making prediction: {str(e)}")
