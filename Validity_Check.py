from FileGen import Generate as Gen
from pathlib import Path
import os
def Check():
    try:
        Test_F = open("Config.txt", "r")
        Test_F.close()
        Assets_Check = Path(os.path.join(os.getcwd(), "Assets"))
        if Assets_Check.is_dir():
            pass
        else:
            raise TimeoutError
    except FileNotFoundError:
        Gen()
    except TimeoutError:
        os.makedirs(os.path.join(os.getcwd(), "Assets"))
        Gen()