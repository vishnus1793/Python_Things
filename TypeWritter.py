import pyautogui as pag
import time

print("Press Ctrl-C to stop.")

try:
    while True:
        pag.typewrite(" Once Again Repeated ")
        time.sleep(1)
        pag.press('backspace', presses=22)  
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nProgram stopped.")
