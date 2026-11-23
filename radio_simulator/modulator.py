# Modulator Module
import numpy as np

class Modulator:
    def __init__(self, carrier_freq=10000, fm_index=5.0):
        self.carrier_freq = carrier_freq
        self.fm_index = fm_index
        self.time_axis = None
        self.sample_rate = None

    def set_time_axis(self, time_axis):
        self.time_axis = np.asarray(time_axis)
        if len(self.time_axis) > 1:
            self.sample_rate = 1.0 / (self.time_axis[1] - self.time_axis[0])
        return self

    def modulate(self, signal, modulation_type='am', mod_index=0.7):
        if self.time_axis is None:
            raise RuntimeError("Сначала вызовите set_time_axis()")
        if len(signal) != len(self.time_axis):
            raise ValueError("Длина сигнала не совпадает с осью времени")

        carrier = np.cos(2 * np.pi * self.carrier_freq * self.time_axis)

        if modulation_type == 'am':
            # Классическая AM: (1 + m·s(t))·cos(2πf_c t)
            return (1.0 + mod_index * signal) * carrier

        elif modulation_type == 'dsb_sc':
            # Двухполосная с подавленной несущей (как было раньше)
            return signal * carrier

        elif modulation_type == 'fm':
            dt = 1.0 / self.sample_rate
            integrated = np.cumsum(signal) * dt
            peak = np.max(np.abs(signal)) or 1.0
            phase = (2 * np.pi * self.carrier_freq * self.time_axis
                     + self.fm_index * (integrated / peak) * 2 * np.pi)
            return np.sin(phase)

        else:
            raise ValueError("Поддерживаются AM, DSB-SC и FM")