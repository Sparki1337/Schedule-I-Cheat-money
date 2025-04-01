import os
import configparser
import tkinter as tk
from tkinter import filedialog
import sys

# Добавляем путь к текущей директории для импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
    
# Импорт из utils должен быть после добавления пути
from utils import check_yes_input

# Путь к файлу настроек
CONFIG_FILE = "money_patcher_config.ini"

# Changelog для отслеживания изменений программы
CHANGELOG = {
    "1.8.2": [
        "Удалена функция сохранения последнего использованного значения",
        "Добавлено обязательное требование ввода значения при каждом использовании",
        "Оптимизирован интерфейс ввода значений"
    ],
    "1.8.1": [
        "Исправлена работа с Inventory.json для корректного отображения и изменения наличных денег",
        "Улучшен интерфейс: добавлено подменю для выбора типа денег (наличные/счет)",
        "Переработана логика чтения и обновления файлов JSON",
        "Добавлена поддержка более сложной структуры сохранений"
    ],
    "1.8": [
        "Добавлена возможность изменения наличных денег в инвентаре (Inventory.json)",
        "Улучшена работа с файлами сохранений, добавлена поддержка десятичных значений"
    ],
    "1.7": [
        "Добавлена улучшенная обработка ввода с учетом разных раскладок клавиатуры",
        "Добавлена поддержка ввода да/нет независимо от текущей раскладки"
    ],
    "1.6": [
        "Реорганизована структура программы на 3 файла для лучшей поддержки"
    ],
    "1.5": [
        "Добавлен отдельный пункт меню 'Загрузить backup'",
        "Улучшена система восстановления из резервных копий",
        "Добавлено удаление папки бэкапа после восстановления"
    ],
    "1.4": [
        "Добавлен отдельный пункт меню 'Настройки'",
        "Добавлена возможность включения/отключения анимаций"
    ],
    "1.3": [
        "Добавлен выбор exe-файла игры через проводник Windows",
        "Удален автоматический режим поиска exe-файла"
    ],
    "1.2": [
        "Добавлена опция просмотра текущего баланса без изменений",
        "Добавлена возможность автозапуска игры после патча",
        "Добавлена функция выбора и сохранения пути к exe-файлу игры"
    ],
    "1.1": [
        "Добавлена возможность выбора пользовательской суммы денег",
        "Обновлен текст сообщений с учетом пользовательской суммы"
    ],
    "1.0": [
        "Первоначальный релиз программы",
        "Реализована функция изменения денег на фиксированную сумму 10000",
        "Добавлено создание резервных копий сохранений",
        "Добавлена возможность восстановления из резервных копий"
    ]
}

def load_config():
    """Загружает настройки из файла конфигурации"""
    config = configparser.ConfigParser()
    
    # Настройки по умолчанию
    default_config = {
        'Settings': {
            'game_exe_path': '',
            'last_money_value': '10000',
            'last_cash_value': '10000',
            'auto_launch_game': 'False',
            'animations_enabled': 'True'
        }
    }
    
    # Если файл существует, загружаем из него
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    else:
        # Иначе создаем с настройками по умолчанию
        for section, options in default_config.items():
            if not config.has_section(section):
                config.add_section(section)
            for option, value in options.items():
                config.set(section, option, value)
        
        # Сохраняем файл
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
    
    return config

def save_config(config):
    """Сохраняет настройки в файл конфигурации"""
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)

def select_game_exe(animated_text, input):
    """Позволяет выбрать exe файл игры через проводник Windows и сохраняет путь в настройки"""
    config = load_config()
    
    current_path = config.get('Settings', 'game_exe_path', fallback='')
    
    if current_path and os.path.exists(current_path):
        animated_text(f"📂 Текущий путь к игре: {current_path}", 0.02)
    else:
        animated_text("📂 Путь к игре не настроен", 0.02)
    
    print("\n" + "=" * 50)
    animated_text("1. Выбрать exe-файл игры через проводник", 0.02)
    animated_text("2. Вернуться в главное меню", 0.02)
    print("=" * 50)
    
    choice = input("\nВаш выбор (1-2): ")
    
    if choice == "1":
        # Создаем скрытое окно Tkinter для вызова диалога выбора файла
        root = tk.Tk()
        root.withdraw()  # Скрываем основное окно
        
        # Показываем диалог выбора файла
        animated_text("📂 Открываю проводник для выбора exe-файла...", 0.02)
        file_path = filedialog.askopenfilename(
            title="Выберите exe-файл игры Schedule I",
            filetypes=[("Исполняемые файлы", "*.exe")],
            initialdir=os.path.expandvars(r"%ProgramFiles%\Steam\steamapps\common")
        )
        
        # Закрываем окно Tkinter
        root.destroy()
        
        if file_path:
            if os.path.exists(file_path) and file_path.lower().endswith('.exe'):
                config.set('Settings', 'game_exe_path', file_path)
                save_config(config)
                animated_text(f"✅ Путь к игре сохранен: {file_path}", 0.02)
                
                # Настройка автозапуска
                auto_launch = input("\nВключить автозапуск игры после патча? (д/н): ")
                auto_launch_value = 'True' if check_yes_input(auto_launch) else 'False'
                config.set('Settings', 'auto_launch_game', auto_launch_value)
                save_config(config)
                
                if auto_launch_value == 'True':
                    animated_text("✅ Автозапуск игры включен", 0.02)
                else:
                    animated_text("ℹ️ Автозапуск игры отключен", 0.02)
            else:
                print("❌ Выбранный файл не является exe-файлом!")
        else:
            print("⚠️ Выбор файла отменен.")
    
    input("\nНажмите Enter для продолжения...")

def toggle_animations(animated_text, input):
    """Включает или отключает анимации"""
    config = load_config()
    current_state = config.getboolean('Settings', 'animations_enabled', fallback=True)
    
    # Инвертируем текущее состояние
    new_state = not current_state
    config.set('Settings', 'animations_enabled', str(new_state))
    save_config(config)
    
    if new_state:
        animated_text("✅ Анимации включены", 0.02)
    else:
        print("✅ Анимации отключены")
    
    input("\nНажмите Enter для продолжения...")

def toggle_auto_launch(animated_text, input):
    """Включает или отключает автозапуск игры"""
    config = load_config()
    current_state = config.getboolean('Settings', 'auto_launch_game', fallback=False)
    
    # Инвертируем текущее состояние
    new_state = not current_state
    config.set('Settings', 'auto_launch_game', str(new_state))
    save_config(config)
    
    if new_state:
        animated_text("✅ Автозапуск игры включен", 0.02)
    else:
        animated_text("❌ Автозапуск игры отключен", 0.02)
    
    input("\nНажмите Enter для продолжения...")

def program_settings(animated_text, input, os):
    """Меню настроек программы"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        config = load_config()
        animations_enabled = config.getboolean('Settings', 'animations_enabled', fallback=True)
        auto_launch = config.getboolean('Settings', 'auto_launch_game', fallback=False)
        game_path = config.get('Settings', 'game_exe_path', fallback='')
        
        print("=" * 50)
        animated_text("📋 НАСТРОЙКИ ПРОГРАММЫ", 0.02)
        print("=" * 50)
        
        # Отображаем текущие настройки
        animated_text(f"\n• Анимации: {'✅ Включены' if animations_enabled else '❌ Отключены'}", 0.02)
        animated_text(f"• Автозапуск игры: {'✅ Включен' if auto_launch else '❌ Отключен'}", 0.02)
        
        if game_path and os.path.exists(game_path):
            animated_text(f"• Путь к игре: {game_path}", 0.02)
        else:
            animated_text("• Путь к игре: ❌ Не настроен", 0.02)
        
        print("\n" + "=" * 50)
        animated_text("1. 🎮 Настроить путь к игре", 0.02)
        animated_text("2. 🚀 Настроить автозапуск игры", 0.02)
        animated_text("3. ✨ Включить/отключить анимации", 0.02)
        animated_text("4. 🔙 Вернуться в главное меню", 0.02)
        print("=" * 50)
        
        choice = input("\nВаш выбор (1-4): ")
        
        if choice == "1":
            select_game_exe(animated_text, input)
        elif choice == "2":
            toggle_auto_launch(animated_text, input)
        elif choice == "3":
            toggle_animations(animated_text, input)
        elif choice == "4":
            break
        else:
            print("⚠️ Неверный выбор. Пожалуйста, введите число от 1 до 4.")
            input("\nНажмите Enter для продолжения...") 