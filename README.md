# Steel Strength Predictor

A Windows desktop application for predicting steel yield strength using a Random Forest model. This application helps determine if steel materials meet the required specifications based on various input parameters.

## Features

- Predict steel yield strength using Random Forest model
- Automatic requirement checking for S355 and S690 steel grades
- User-friendly PyQt6-based interface
- Real-time predictions with confidence intervals
- Detailed results including pass/fail status and margins

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ErdUi/steel-predictor-app.git
cd steel-predictor-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python src/main.py
```

2. Train the model using the "Train Model" button
3. Enter the required parameters:
   - Certificate yield strength (QC_Re)
   - Certificate tensile strength (QC_Rm)
   - Certificate Elongation (QC_A)
   - Thickness (Dimension)
   - Select manufacturer
   - Select grade (S355 or S690)
4. Click "Predict" to get results

## Building Executable

To create a standalone Windows executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/main.py
```

The executable will be created in the `dist` directory.

## Project Structure

```
steel-predictor-app/
├── src/
│   ├── main.py
│   ├── model/
│   │   ├── __init__.py
│   │   └── predictor.py
│   └── ui/
│       ├── __init__.py
│       └── main_window.py
├── requirements.txt
├── README.md
└── LICENSE
```

## License

MIT License