# Main Script
import numpy as np
import matplotlib.pyplot as plt

from signal_generator import SignalGenerator
from modulator import Modulator
from visualizer import SignalVisualizer
from noise import NoiseGenerator


def main():
    # ---- Параметры ----
    sample_rate   = 48000
    duration      = 1.0
    freq          = 1000         # сообщение, 1 кГц
    carrier_freq  = 10000        # НЕ 24000! Несущая << fs/2
    mod_index     = 0.7          # глубина AM
    snr_db        = 20

    # Окна для наглядной визуализации
    zoom_msg    = int(0.005 * sample_rate)   # 5 мс = 5 периодов 1 кГц
    zoom_noise  = int(0.020 * sample_rate)   # 20 мс

    # ---- Генерация ----
    sg = SignalGenerator(sample_rate=sample_rate)
    signal = sg.generate_signal('sine', duration, freq)
    time_axis = sg.get_time_axis()

    # ---- Модуляция ----
    mod = Modulator(carrier_freq=carrier_freq)
    mod.set_time_axis(time_axis)
    modulated = mod.modulate(signal, 'am', mod_index=mod_index)
    envelope  = 1.0 + mod_index * signal           # верхняя огибающая AM

    # ---- Визуализация ----
    vis = SignalVisualizer()

    # 1) Базовый сигнал — zoom 5 мс
    vis.plot_signal(
        signal[:zoom_msg], time_axis[:zoom_msg],
        title="Базовый сигнал (5 мс)"
    )

    # 2) AM — zoom 5 мс (видны и несущая, и огибающая)
    vis.plot_modulated_signal(
        signal[:zoom_msg], modulated[:zoom_msg], time_axis[:zoom_msg],
        title="AM модуляция (5 мс, m=0.7)"
    )

    # 3) AM — полный сигнал с огибающей
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time_axis, modulated, linewidth=0.4, alpha=0.6,
            label='Модулированный')
    ax.plot(time_axis,  envelope, color='red', linewidth=1.8,
            label='Огибающая')
    ax.plot(time_axis, -envelope, color='red', linewidth=1.8)
    ax.set_xlabel('Время [сек]'); ax.set_ylabel('Амплитуда')
    ax.set_title('AM модуляция (полный сигнал + огибающая)')
    ax.legend(); ax.grid(True)
    vis.save_plot_to_file(fig, "radio_simulator_am")

    # 4) Шум — zoom 20 мс
    noise_gen   = NoiseGenerator('white')
    noisy       = noise_gen.add_noise(signal, snr_db=snr_db)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time_axis[:zoom_noise], signal[:zoom_noise],
            label='Оригинал', linewidth=2)
    ax.plot(time_axis[:zoom_noise], noisy[:zoom_noise],
            label=f'С шумом (SNR={snr_db} дБ)', linewidth=0.8, alpha=0.8)
    ax.set_xlabel('Время [сек]'); ax.set_ylabel('Амплитуда')
    ax.set_title(f'Сигнал + белый шум, окно 20 мс, SNR={snr_db} дБ')
    ax.legend(); ax.grid(True)
    vis.save_plot_to_file(fig, "radio_simulator_with_noise")


if __name__ == '__main__':
    try:
        main()
        print("Симулятор радиоканала выполнен успешно!")
    except Exception as e:
        print(f"Ошибка при выполнении: {e}")