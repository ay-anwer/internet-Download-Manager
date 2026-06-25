import sys
import os
import truststore
truststore.inject_into_ssl()                                                                              #   Injecting Operating System (Windows) Certificates into Python to Fix SSL Issues

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl
from PySide6.QtQuickControls2 import QQuickStyle
import bridge

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))               # 1. Dynamically and absolutely determining the current folder containing the script file (main.py)
    
    qml_file_path = os.path.join(current_dir, "main.qml")                       # 2 Joining the current directory with the interface file name to obtain the full absolute path
    
    qml_url = QUrl.fromLocalFile(qml_file_path)                                      # 3. Converting the path to QUrl format, which is the preferred  format for the QML engine in Pyside6
    
    QQuickStyle.setStyle("Material")

    engine.load(qml_url )                                                                               # 4. Loading the UI file using the dynamic absolute path

    if not engine.rootObjects():
        sys.exit(-1)
        
    sys.exit(app.exec())
