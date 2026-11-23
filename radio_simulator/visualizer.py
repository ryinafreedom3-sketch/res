# Visualizer Module
import numpy as np
from matplotlib import pyplot as plt

class SignalVisualizer:
    def __init__(self):
        self.plt = plt

    def plot_signal(self, signal, time_axis=None, title="Сигнал", color='blue'):
        self.plt.figure(figsize=(10, 4))
        x = time_axis if time_axis is not None else np.arange(len(signal))
        self.plt.plot(x, signal, color=color)
        self.plt.title(title)
        self.plt.xlabel('Время [сек]' if time_axis is not None else 'Отсчёт')
        self.plt.ylabel('Амплитуда')
        self.plt.grid(True)
        self.plt.tight_layout()
        self.plt.show()

    def plot_modulated_signal(self, base_signal, modulated_signal, time_axis=None,
                              title="Модулированный сигнал"):
        self.plt.figure(figsize=(10, 4))
        x = time_axis if time_axis is not None else np.arange(len(base_signal))
        self.plt.plot(x, base_signal, label='Базовый', alpha=0.7)
        self.plt.plot(x, modulated_signal, label='Модулированный', alpha=0.7)
        self.plt.title(title)
        self.plt.legend()
        self.plt.xlabel('Время [сек]' if time_axis is not None else 'Отсчёт')
        self.plt.ylabel('Амплитуда')
        self.plt.grid(True)
        self.plt.tight_layout()
        self.plt.show()

    def save_plot_to_file(self, fig, filename):
        try:
            fig.tight_layout()
            fig.savefig(f"{filename}.png", dpi=100)
            print(f"Изображение сохранено в {filename}.png")
            return True
        except Exception as e:
            print(f"Ошибка сохранения файла: {e}")
            return False
        finally:
            self.plt.close(fig)  # закрываем фигуру, чтобы не копить память