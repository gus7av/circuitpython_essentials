import circuitpython_essentials as cp
import board
import time

led = cp.output(board.D13)

while True:
    led.value = not led.value
    time.sleep(1)