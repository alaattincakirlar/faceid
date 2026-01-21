PYTHON-BASED BIOMETRIC FACIAL VERIFICATION SYSTEM 

In this repo, to protect systems or database, the program that works with face detection and recognition algorithms to unlock system by verification of the authorized user's face is created.

Features:
-Biometric Authentication
-Data Privacy via Pickle
-Logging History

Requirements and libraries:
-Python 3.10+
-OpenCV
-Face_Recognition
-Pickle

Project structure:
-Data/  : The file where facial data stores in.
-config.py  : System configuration.
-register.py  : Creating and saving facial data.
-main.py  : Authentication file.
-status.json  : Successful attempts history.

To add authorized user:
-Faces should be added to the system one by one.
-Run "register.py"
-Center the user's face.
-Press 's' to save the facial data, 'q' to exit.
-Enter the name in the terminal.

To verify and unlock the system:
-Run "main.py"
-Center the user's face to verify it.
-Successful attempts is logged on a file.

Installation:
git clone [https://github.com/alaattincakirlar/faceid.git](https://github.com/alaattincakirlar/faceid.git)
pip install -r requirements.txt
