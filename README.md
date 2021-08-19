```
# cheatsheet circuitpython_essentials

import circuitpython_essentials as cp
import board

# BASIC IO-FUNCTIONS

# initialization                        # call
led = cp.output(board.D13)              led.value=True
btn = cp.input_pullup(board.D7)         btn.value
btn = cp.input_pulldown(board.D4)       btn.value
adc = cp.analog_input(board.A8)         adc.value
dac = cp.analog_output(board.A0)        dac.value=65535-0
pwm = cp.pwm_output(board.D13)          pwn.value=65535-0

# deinitialization
btn.disable()

# SOUND
cp.play_tone(board.A0, 440, 1)          # pin, frequency, duration (s)
cp.play_wav("filename.wav", board.A0)   
cp.play_mp3("filename.mp3", board.A0             

# CPU temperature
cp.temperature()
```
