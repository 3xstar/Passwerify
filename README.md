Passwerify - Password Security Analyzer


PROJECT TOPIC:
Password Security Analysis and Evaluation Tool


PURPOSE OF THE PROJECT:
Passwerify is a desktop application that analyzes password strength and provides detailed security feedback. The tool evaluates passwords based on multiple criteria, assigns letter grades (A-F), and offers specific recommendations for improvement.


KEY FEATURES:
Password strength analysis and scoring

Visual grade display (A through F with images)

Security level classification (Very Low to Very High)

Detailed good and bad aspects of each password

Error handling and validation

Easy navigation between password input and results


INSTRUCTIONS FOR LAUNCHING:

PREREQUISITES
Python 3.7 or higher
PyQt5 library

INSTALLATION
Clone or download the project
Install dependencies:
pip install PyQt5==5.15.9


PROJECT STRUCTURE:
PASSWERIFY/
├── main.py
├── images/
│   ├── agrade.png
│   ├── bgrade.png
│   ├── cgrade.png
│   ├── dgrade.png
│   └── fgrade.png
├── ui/
│   ├── main_page.ui
│   └── verify_page.ui
└── backend/
    ├── password_checker.py
    └── app_logic.py


RUNNING THE APPLICATION:
Open terminal in project directory
Execute:
python main.py


HOW TO USE:
ENTER PASSWORD: Type password in main window

CLICK VERIFY: Analyze password strength

VIEW RESULTS: See security grade, level, and feedback

OPTIONS:

"CREATE NEW PASSWORD": Clear field and return to input

"FIX CURRENT PASSWORD": Edit the analyzed password


SUPPORTED PLATFORMS
Windows

macOS

Linux