"""
Лабораторная работа №4: Основы объектно-ориентированного программирования в Python
Тема: Проектирование классов для системы телекоммуникационных устройств.
Цели: Овладение инкапсуляцией, наследованием, полиморфизмом и абстракцией.
"""

from abc import ABC, abstractmethod


# -----------------------------------------------------------------------------
# 1. ИНКАПСУЛЯЦИЯ И АБСТРАКЦИЯ
# Базовый класс хранит внутренние данные в защищённых атрибутах и задаёт
# единый интерфейс show_status() для всех телекоммуникационных устройств.
# -----------------------------------------------------------------------------

class BaseTelecomDevice(ABC):
    """Базовый класс телекоммуникационного устройства (абстракция)."""

    def __init__(self, device_name: str, ip_address: str, manufacturer: str):
        self._name = device_name            # защищённое свойство
        self._ip = ip_address               # защищённое свойство
        self._manufacturer = manufacturer   # защищённое свойство

    @property
    def name(self):
        """Публичное свойство для чтения имени устройства."""
        return self._name

    def __str__(self):
        return f"Устройство: {self._name} | IP: {self._ip}"

    @abstractmethod
    def show_status(self):
        """Абстрактный метод: статус конкретного устройства."""
        pass


# -----------------------------------------------------------------------------
# 2. НАСЛЕДОВАНИЕ
# Классы Router и Switch наследуют общие свойства и методы базового класса,
# а затем расширяют его собственной функциональностью.
# -----------------------------------------------------------------------------

class Router(BaseTelecomDevice):
    """Маршрутизатор — устройство с набором сетевых интерфейсов."""

    def __init__(self, device_name: str, ip_address: str, manufacturer: str):
        super().__init__(device_name, ip_address, manufacturer)
        self._interfaces = []

    def add_interface(self, name: str):
        """Добавление сетевого интерфейса."""
        self._interfaces.append(name)
        return f"Интерфейс {name} добавлен."

    def show_status(self):
        interfaces = ", ".join(self._interfaces) if self._interfaces else "нет"
        return (f"Маршрутизатор {self._name} ({self._manufacturer}): "
                f"IP {self._ip}, интерфейсы: {interfaces}")


class Switch(BaseTelecomDevice):
    """Коммутатор — устройство с портами доступа."""

    def __init__(self, device_name: str, ip_address: str, manufacturer: str):
        super().__init__(device_name, ip_address, manufacturer)
        self._ports = 0

    def connect_port(self, count: int):
        """Подключение портов."""
        self._ports += count
        return f"Подключено {count} новых портов."

    def show_status(self):
        return (f"Коммутатор {self._name} ({self._manufacturer}): "
                f"IP {self._ip}, подключено портов: {self._ports}")


# -----------------------------------------------------------------------------
# 3. ПОЛИМОРФИЗМ
# Менеджер хранит устройства в одном списке и вызывает show_status() через
# ссылку на базовый класс. Для каждого объекта выполняется своя реализация.
# -----------------------------------------------------------------------------

class TelecomSystemManager:
    """Класс-менеджер системы (управление объектами, хранение данных)."""

    def __init__(self):
        self._devices = []

    def add_device(self, device: BaseTelecomDevice):
        """Добавление устройства любого типа, унаследованного от базового."""
        self._devices.append(device)
        print(f"[{device.__class__.__name__}] {device.name} добавлен в сеть.")

    def system_status_check(self):
        """Полиморфный обход всех устройств системы."""
        print("\n--- Отчёт о системе ---")
        for device in self._devices:
            print(device.show_status())


# -----------------------------------------------------------------------------
# 4. ИСПОЛЬЗОВАНИЕ ПРИНЦИПОВ ООП
# -----------------------------------------------------------------------------

def main():
    print("=== Телекоммуникационная Система: Лабораторная работа №4 ===\n")

    system = TelecomSystemManager()

    # Создание объектов (наследование и инкапсуляция)
    r1 = Router("Core-Router-01", "192.168.1.1", "Cisco")
    sw1 = Switch("Main-Switch-A", "192.168.1.254", "HPE")

    # Добавление в систему (полиморфизм)
    system.add_device(r1)
    system.add_device(sw1)

    # Расширение функциональности дочерних классов
    print(r1.add_interface("GigabitEthernet0/0"))
    print(sw1.connect_port(48))

    print("\n--- Проверка полиморфного интерфейса ---")
    system.system_status_check()


if __name__ == "__main__":
    main()
