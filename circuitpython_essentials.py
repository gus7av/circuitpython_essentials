# updated 05-04-22

import digitalio
import analogio
import pwmio
import touchio
import time
import array
import microcontroller

try:
    import audiocore
except ImportError:
    pass  # not supported by every board!

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


class DigitalOut:
    def __init__(self, pin):
        self.iopin = digitalio.DigitalInOut(pin)
        self.iopin.switch_to_output()

    @property
    def value(self):
        return self.iopin.value

    @value.setter
    def value(self, value):
        self.iopin.value = value

    def deinit(self):
        self.iopin.deinit()


class DigitalIn:
    def __init__(self, pin):
        self.iopin = digitalio.DigitalInOut(pin)
        self.iopin.switch_to_input()

    @property
    def value(self):
        return self.iopin.value

    def pull_down(self):
        self.iopin.switch_to_input(pull=digitalio.Pull.DOWN)

    def pull_up(self):
        self.iopin.switch_to_input(pull=digitalio.Pull.UP)

    def deinit(self):
        self.iopin.deinit()


class AnalogIn:
    def __init__(self, pin):
        self.iopin = analogio.AnalogIn(pin)

    @property
    def value(self):
        return self.iopin.value

    def deinit(self):
        self.iopin.deinit()


class AnalogOut:
    def __init__(self, pin):
        self.iopin = analogio.AnalogOut(pin)

    @property
    def value(self):
        return self.iopin.value

    @value.setter
    def value(self, value):
        self.iopin.value = value

    def deinit(self):
        self.iopin.deinit()


class PWMOut:
    def __init__(self, pin):
        self.iopin = pwmio.PWMOut(pin, frequency=5000, duty_cycle=0)

    @property
    def value(self):
        return self.iopin.duty_cycle

    @value.setter
    def value(self, value):
        self.iopin.duty_cycle = value

    def deinit(self):
        self.iopin.deinit()


class ToneOut:
    def __init__(self, pin):
        self.iopin = pwmio.PWMOut(
            pin, frequency=440, duty_cycle=0, variable_frequency=True
        )

    @property
    def value(self):
        return self.iopin.frequency

    @property
    def volume(self):
        return self.iopin.duty_cycle

    @value.setter
    def value(self, value):
        self.iopin.duty_cycle = 0x8000
        self.iopin.frequency = value

    @volume.setter
    def volume(self, volume):
        self.iopin.duty_cycle = min(volume, 0x8000)

    def stop(self):
        self.iopin.duty_cycle = 0

    def deinit(self):
        self.iopin.deinit()


class TouchIn:
    def __init__(self, pin):
        self.iopin = touchio.TouchIn(pin)

    @property
    def value(self):
        return self.iopin.value

    def deinit(self):
        self.iopin.deinit()


def play_wav(pin, file_name):

    with AudioOut(pin) as audio:
        wavefile = audiocore.WaveFile(open(file_name, "rb"))
        audio.play(wavefile)
        while audio.playing:
            pass


def play_mp3(pin, file_name):

    with AudioOut(pin) as audio:
        mp3file = audiomp3.MP3Decoder(open(file_name, "rb"))
        audio.play(mp3file)
        while audio.playing:
            pass


def play_tone(pin, frequency, duration=0.1, length=100):

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


def deep_sleep(time_or_pin, value=True, pull=True):

    if isinstance(time_or_pin, (int, float)):
        time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + time_or_pin)
        alarm.exit_and_deep_sleep_until_alarms(time_alarm)

    else:
        pin_alarm = alarm.pin.PinAlarm(pin=time_or_pin, value=value, pull=pull)
        alarm.exit_and_deep_sleep_until_alarms(pin_alarm)


def temperature():

    return microcontroller.cpu.temperature


def map_range(x, in_min, in_max, out_min, out_max):

    in_range = in_max - in_min
    in_delta = x - in_min
    if in_range != 0:
        mapped = in_delta / in_range
    elif in_delta != 0:
        mapped = in_delta
    else:
        mapped = 0.5
    mapped *= out_max - out_min
    mapped += out_min
    if out_min <= out_max:
        return max(min(mapped, out_max), out_min)
    return min(max(mapped, out_max), out_min)
