# Noise Module
import numpy as np

class NoiseGenerator:
    def __init__(self, noise_type='white', signal_power=1.0):
        self.noise_type = noise_type
        self.signal_power = signal_power

    def add_noise(self, signal, snr_db=20):
        signal = np.asarray(signal, dtype=float)
        if self.noise_type == 'white':
            noise = np.random.normal(0, 1, signal.shape)
        elif self.noise_type == 'colored':
            noise = self._generate_colored_noise(len(signal))
        else:
            raise ValueError("Поддерживается белый и цветной шум")

        # Правильный расчёт мощности
        p_signal = np.mean(signal ** 2)
        if p_signal == 0:
            return signal.copy()
        p_noise = p_signal / (10 ** (snr_db / 10.0))
        noise_std = np.sqrt(p_noise)
        return signal + noise * noise_std

    def _generate_colored_noise(self, n):
        # "Розовый" шум через фильтрацию белого (простая аппроксимация)
        white = np.random.randn(n)
        # Простой однополюсный ФНЧ для окрашивания
        b = 0.99
        colored = np.zeros(n)
        prev = 0.0
        for i in range(n):
            prev = b * prev + (1 - b) * white[i]
            colored[i] = prev
        # Нормируем дисперсию к 1
        std = np.std(colored) or 1.0
        return colored / std