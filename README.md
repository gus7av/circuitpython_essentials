## USAGE


### Setup
`import circuitpython_essentials as cp`  
`import board`  

### Initialization                    
`led = cp.output(board.D13)`             
`btn = cp.input_pullup(board.D7)`      
`btn = cp.input_pulldown(board.D4)`     
`adc = cp.analog_input(board.A8)`           
`dac = cp.analog_output(board.A0)`    
`pwm = cp.pwm_output(board.D13)`        

### Call
`led.value=True`  
`btn.value`  
`adc.value`  
`dac.value=65535-0`  
`pwn.value=65535-0`  

### Deinitialization
`btn.disable()`  

### Sound
`cp.play_tone(board.A0, 440, 1)`  
`cp.play_wav("filename.wav", board.A0)`   
`cp.play_mp3("filename.mp3", board.A0)`          

### Temperature
`cp.temperature()`  
