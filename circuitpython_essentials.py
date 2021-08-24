# updated 24-08-21

import digitalio
import analogio
import pwmio
import touchio
import time
import array
import audiocore
import microcontroller

try:
    import alarm
except ImportError:
    pass  # not supported by every board!

try:
    import audiomp3
except ImportError:
    pass  # not supported by every board!

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not supported by every board!

class output:

    def __init__(self, pin):
        self.iopin = digitalio.DigitalInOut(pin)
        self.iopin.switch_to_output()

    @property
    def value(self):
        return self.iopin.value

    @value.setter
    def value(self, value):
        self.iopin.value = value

    def disable(self):
        self.iopin.deinit()

class input:

    def __init__(self, pin):
        self.iopin = digitalio.DigitalInOut(pin)
        self.iopin.switch_to_input()

    @property
    def value(self):
        return self.iopin.value

    def disable(self):
        self.iopin.deinit()

class input_pullup:

    def __init__(self, pin):
        self.iopin = digitalio.DigitalInOut(pin)
        self.iopin.switch_to_input(pull=digitalio.Pull.UP)

    @property
    def value(self):
        return self.iopin.value

    def disable(self):
        self.iopin.deinit()

class input_pulldown:

    def __init__(self, pin):
        self.iopin = digitalio.DigitalInOut(pin)
        self.iopin.switch_to_input(pull=digitalio.Pull.DOWN)

    @property
    def value(self):
        return self.iopin.value

    def disable(self):
        self.iopin.deinit()

class analog_input:

    def __init__(self, pin):
        self.iopin = analogio.AnalogIn(pin)

    @property
    def value(self):
        return self.iopin.value

    def disable(self):
        self.iopin.deinit()

class analog_output:

    def __init__(self, pin):
        self.iopin = analogio.AnalogOut(pin)

    @property
    def value(self):
        return self.iopin.value

    @value.setter
    def value(self, value):
        self.iopin.value = value

    def disable(self):
        self.iopin.deinit()

class pwm_output:

    def __init__(self, pin):
        self.iopin = pwmio.PWMOut(pin, frequency=5000, duty_cycle=0)

    @property
    def value(self):
        return self.iopin.value

    @value.setter
    def value(self, value):
        self.iopin.duty_cycle = value

    def disable(self):
        self.iopin.deinit()

class touch_input:

    def __init__(self, pin):
        self.iopin = touchio.TouchIn(pin)

    @property
    def value(self):
        return self.iopin.value

    def disable(self):
        self.iopin.deinit()

def play_wav(file_name, pin):

    with AudioOut(pin) as audio:
        wavefile = audiocore.WaveFile(open(file_name, "rb"))
        audio.play(wavefile)
        while audio.playing:
            pass

def play_mp3(file_name, pin):

    with AudioOut(pin) as audio:
        mp3file = audiomp3.MP3Decoder(open(file_name, "rb"))
        audio.play(mp3file)
        while audio.playing:
            pass

def play_tone(pin, frequency, duration=1, length=100):

    if length * frequency > 350000:
        length = 350000 // frequency
    try:
        # pin with PWM
        # pylint: disable=no-member
        with pwmio.PWMOut(
            pin, frequency=int(frequency), variable_frequency=False
        ) as pwm:
            pwm.duty_cycle = 0x8000
            time.sleep(duration)
        # pylint: enable=no-member
    except ValueError:
        # pin without PWM
        sample_length = length
        square_wave = array.array("H", [0] * sample_length)
        for i in range(sample_length / 2):
            square_wave[i] = 0xFFFF
        square_wave_sample = audiocore.RawSample(square_wave)
        square_wave_sample.sample_rate = int(len(square_wave) * frequency)
        with AudioOut(pin) as dac:
            if not dac.playing:
                dac.play(square_wave_sample, loop=True)
                time.sleep(duration)
            dac.stop()

def deep_sleep(time_or_pin, logic=True, pull_enable=True):

    if isinstance(time_or_pin, int) is True:
        time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + time_or_pin)
        alarm.exit_and_deep_sleep_until_alarms(time_alarm)

    else:
        pin_alarm = alarm.pin.PinAlarm(pin=time_or_pin, value=logic, pull=pull_enable)
        alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
        
def temperature():
    return microcontroller.cpu.temperature
