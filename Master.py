from FileGen import Generate as Gen
from pathlib import Path
import sys
import argparse
import os
from Anima import Anima
#Back to the Basics: The variable that controls the 'while' Loop for the application.
App_Run = True
#Application Loop
while App_Run:
    try:
        ExtC = Anima("", True)
        if ExtC == "Theme_Change_Exit":
            pass
        elif ExtC == "Normal_Exit":
            App_Run = False
    except Exception as E:
        print(E)
        App_Run = False