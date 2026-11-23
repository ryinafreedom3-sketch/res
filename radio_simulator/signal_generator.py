# Signal Generator Module
import numpy as np
from scipy.signal import chirp, square

class SignalGenerator:
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.t = None

    def generate_signal(self, signal_type='sine', duration=1.0, freq=1000):
        if duration <= 0:
            raise ValueError("Длительность должна быть положительной")
        self.t = np.arange(int(duration * self.sample_rate)) / self.sample_rate
        if signal_type == 'sine':
            return np.sin(2 * np.pi * freq * self.t)
        elif signal_type == 'square':
            return square(2 * np.pi * freq * self.t)
        elif signal_type == 'chirp':
            return chirp(self.t, f0=1000, t1=duration, f1=3000, method='linear')
        else:
            raise ValueError(f"Неподдерживаемый тип сигнала: {signal_type}")

    def get_time_axis(self):
        return self.t