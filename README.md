## CircuitPython Essentials 

This is a helper library for the most basic functions in CircuitPython. I've made it mainly to overcome my inability to remember how to use these functions by heart. It is heavily inspiried and sampled from Adafruits own helper library for the Circuit Playground platform and the SimpleIO library. Please contact me if I'm crediting or using your material wrongly!

```
# setup
import circuitpython_essentials as cp
import board

# initialization                            # call
led = cp.DigitalOut(board.D13)              led.value=True
btn = cp.DigitalIn(board.D7)                btn.value, btn.pull_up(), btn.pull_down()
adc = cp.AnalogIn(board.A8)                 adc.value
dac = cp.AnalogOut(board.A0)                dac.value=65535
pwm = cp.PWMOut(board.D13)                  pwm.value=65535
cap = cp.TouchIn(board.D4)                  cap.value
buz = cp.ToneOut(board.A0)                  buz.value=440, buz.stop()

# deinitialization
btn.deinit() ...etc.

# sound
cp.play_tone(board.A0, 440, 1)         
cp.play_wav(board.A0, "filename.wav")   
cp.play_mp3(board.A0, "filename.mp3")             

# temperature
cp.temperature()

# deep sleep
cp.deep_sleep(10)
cp.deep_sleep(board.D4)
cp.deep_sleep(board.D4, value=True, pull=True)

# map
cp.map_range(value, fromLow, fromHigh, toLow, toHigh)
```

## Installation
Place the file called "circuitpython_essentials.py" in a folder called "lib" in the root directory of your CircuitPython microcontroller

## Examples

#### Blink
```
import circuitpython_essentials as cp
import board
import time

led = cp.DigitalOut(board.LED)

while True:
    led.value = not led.value
    time.sleep(1)
 ```

#### Deep sleep
```
import circuitpython_essentials as cp
import board
import time

led = cp.DigitalOut(board.LED)

for i in range(20):
    led.value = not led.value
    time.sleep(0.1)
    
cp.deep_sleep(board.D4)     
```
