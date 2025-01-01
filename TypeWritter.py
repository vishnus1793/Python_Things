import pyautogui as pag
import time

print("Press Ctrl-C to stop.")

try:
    while True:
        pag.typewrite("OnePiece Is Real")
        time.sleep(1)
        pag.press('backspace', presses=22)  
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nProgram stopped.")
