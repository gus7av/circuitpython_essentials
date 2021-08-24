## CircuitPython Essentials Helper 

This is a helper library for the most basic functions in CircuitPython. I've made it mainly to overcome my inability to remember how to use these functions by heart. It is heavily inspiried and sampled from Adafruits own helper library for the Circuit Playground platform. Thanks to @kattni and @tannewt for creating that library. Please contact me if I'm crediting or using your material wrongly!

```
# cheatsheet circuitpython_essentials

# setup
import circuitpython_essentials as cp
import board

# initialization                        # call
led = cp.output(board.D13)              led.value=True
btn = cp.input_pullup(board.D7)         btn.value
btn = cp.input_pulldown(board.D4)       btn.value
adc = cp.analog_input(board.A8)         adc.value
dac = cp.analog_output(board.A0)        dac.value=65535
pwm = cp.pwm_output(board.D13)          pwn.value=65535

# deinitialization
btn.disable() ...etc.

# sound
cp.play_tone(board.A0, 440, 1)         
cp.play_wav("filename.wav", board.A0)   
cp.play_mp3("filename.mp3", board.A0)             

# temperature
cp.temperature()

# deep sleep
cp.deep_sleep(10)
cp.deep_sleep(board.D4)
cp.deep_sleep(board.D4, True, True)    (defaults for value and pull)
```

## Installation
Place the file called "circuitpython_essentials.py" in a folder called "lib" in the root directory of your CircuitPython microcontroller

## Examples

#### Blink
```
import circuitpython_essentials as cp
import board
import time

led = cp.output(board.D13)

while True:
    led.value = not led.value
    time.sleep(1)
 ```

#### Deep sleep
```
import circuitpython_essentials as cp
import board
import time

led = cp.output(board.D13)

for i in range(20):
    led.value = not led.value
    time.sleep(0.1)
    
cp.deep_sleep(board.D4)     
# cp.deep_sleep(10)
```
