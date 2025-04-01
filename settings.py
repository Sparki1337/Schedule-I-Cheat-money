import os
import configparser
import tkinter as tk
from tkinter import filedialog
import sys
import locale

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
    "1.9": [
        "Добавлена поддержка мультиязычности (русский и английский языки)",
        "Автоматическое определение языка системы при первом запуске",
        "Добавлена возможность выбора языка интерфейса в настройках"
    ],
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

# Словарь с переводами для мультиязычности
TRANSLATIONS = {
    "ru": {
        # Общие сообщения
        "enter_to_continue": "Нажмите Enter для продолжения...",
        "yes_no_choice": "д/н",
        "invalid_choice": "⚠️ Неверный выбор. Пожалуйста, введите число от 1 до {0}.",
        "savings_path_not_found": "❌ Папка сохранений не найдена: {0}",
        "no_user_folders": "❌ Не найдены папки пользователей в директории сохранений.",
        "progress_update": "Прогресс обновления",
        "completed": "Завершено",
        "error_update": "Ошибка при обновлении",
        
        # Для функций в utils.py
        "creating_backup": "Создание резервной копии",
        "backup_created": "Создана резервная копия",
        "backup_error": "Ошибка при создании резервной копии",
        "backup_not_found": "Резервная копия не найдена!",
        "restoring_saves": "Восстановление сохранений",
        "saves_restored": "Сохранения восстановлены из",
        "restore_error": "Ошибка при восстановлении",
        "launching_game": "Запуск игры",
        "launch_error": "Ошибка при запуске игры",
        "launch_solution": "Возможное решение: запустите эту программу с правами администратора",
        "launch_manually": "или запустите игру вручную из Steam",
        "path_not_configured_full": "Путь к игре не настроен или файл не существует.",
        "use_settings": "Используйте опцию 'Настроить путь к игре' в меню.",
        
        # Для функции load_backup
        "select_backup_folder": "Выберите папку с резервной копией",
        "selection_canceled": "Выбор отменен",
        "invalid_backup_folder": "Выбранная папка не является корректной резервной копией сохранений!",
        "backup_folder_requirements": "Резервная копия должна содержать папки с именами пользователей и подпапки SaveGame_*",
        "restore_warning": "Восстановление заменит все текущие сохранения! Создать резервную копию текущих сохранений?",
        "continue_without_backup": "Не удалось создать резервную копию. Продолжить без бэкапа?",
        "delete_backup_after_restore": "Удалить использованную резервную копию?",
        "deleting_backup": "Удаление резервной копии",
        "deletion_countdown": "Удаление через",
        "backup_deleted": "Резервная копия удалена",
        "deletion_error": "Ошибка при удалении резервной копии",
        
        # Главное меню
        "select_action": "Выберите действие:",
        "edit_money": "💵 Изменить деньги в сохранениях",
        "show_balance": "👁️ Показать текущий баланс",
        "settings": "⚙️ Настройки программы",
        "launch_game": "🚀 Запустить игру",
        "load_backup": "💾 Загрузить backup",
        "show_changelog": "📋 Показать историю изменений (changelog)",
        "exit": "❌ Выход",
        "goodbye": "✅ До свидания! Нажмите Enter для выхода...",
        
        # Меню выбора типа денег
        "select_money_type": "Выберите тип денег для изменения:",
        "account_money": "💳 Деньги на счету (Money.json)",
        "cash_money": "💸 Наличные деньги (Inventory.json)",
        "return_to_main": "🔙 Вернуться в главное меню",
        
        # Вспомогательные функции для show_current_balance
        "user": "Пользователь",
        "save": "Сохранение",
        "time": "Время",
        "balance": "Баланс счета", 
        "cash": "Наличные",
        "total_saves": "Всего найдено сохранений",
        
        # Функции патчинга денег
        "enter_money": "💰 Введите сумму денег для установки",
        "enter_cash": "💸 Введите сумму НАЛИЧНЫХ денег для установки",
        "updated_money": "✅ Обновлено файлов",
        "updated_cash": "✅ Обновлено файлов с наличными",
        "no_update_money": "ℹ️ Файлы для обновления не найдены",
        "no_update_cash": "ℹ️ Файлы для обновления наличных не найдены",
        
        # Настройки
        "settings_title": "📋 НАСТРОЙКИ ПРОГРАММЫ",
        "animations": "• Анимации: {0}",
        "enabled": "✅ Включены",
        "disabled": "❌ Отключены",
        "auto_launch": "• Автозапуск игры: {0}",
        "game_path": "• Путь к игре: {0}",
        "path_not_configured": "❌ Не настроен",
        "language": "• Язык интерфейса: {0}",
        "configure_game_path": "🎮 Настроить путь к игре",
        "configure_auto_launch": "🚀 Настроить автозапуск игры",
        "toggle_animations": "✨ Включить/отключить анимации",
        "change_language": "🌐 Изменить язык интерфейса",
        "return_to_main_menu": "🔙 Вернуться в главное меню",
        
        # Выбор языка
        "language_menu": "Выберите язык интерфейса:",
        "russian": "🇷🇺 Русский",
        "english": "🇬🇧 Английский (English)",
        "language_changed": "✅ Язык интерфейса изменен на {0}",
        "language_name": "Русский",
        
        # Для функции animate_countdown
        "seconds": "сек",
    },
    "en": {
        # Common messages
        "enter_to_continue": "Press Enter to continue...",
        "yes_no_choice": "y/n",
        "invalid_choice": "⚠️ Invalid choice. Please enter a number from 1 to {0}.",
        "savings_path_not_found": "❌ Save folder not found: {0}",
        "no_user_folders": "❌ No user folders found in the saves directory.",
        "progress_update": "Update progress",
        "completed": "Completed",
        "error_update": "Error updating",
        
        # For utils.py functions
        "creating_backup": "Creating backup",
        "backup_created": "Backup created",
        "backup_error": "Error creating backup",
        "backup_not_found": "Backup not found!",
        "restoring_saves": "Restoring saves",
        "saves_restored": "Saves restored from",
        "restore_error": "Error restoring",
        "launching_game": "Launching game",
        "launch_error": "Error launching game",
        "launch_solution": "Possible solution: run this program as administrator",
        "launch_manually": "or launch the game manually from Steam",
        "path_not_configured_full": "Game path is not configured or file does not exist.",
        "use_settings": "Use the 'Configure game path' option in the settings menu.",
        
        # For load_backup function
        "select_backup_folder": "Select backup folder",
        "selection_canceled": "Selection canceled",
        "invalid_backup_folder": "The selected folder is not a valid save backup!",
        "backup_folder_requirements": "Backup must contain user folders and SaveGame_* subfolders",
        "restore_warning": "Restoration will replace all current saves! Create a backup of current saves?",
        "continue_without_backup": "Failed to create backup. Continue without backup?",
        "delete_backup_after_restore": "Delete the used backup folder?",
        "deleting_backup": "Deleting backup",
        "deletion_countdown": "Deleting in",
        "backup_deleted": "Backup deleted",
        "deletion_error": "Error deleting backup",
        
        # Main menu
        "select_action": "Select an action:",
        "edit_money": "💵 Edit money in saves",
        "show_balance": "👁️ Show current balance",
        "settings": "⚙️ Program settings",
        "launch_game": "🚀 Launch game",
        "load_backup": "💾 Load backup",
        "show_changelog": "📋 Show changelog",
        "exit": "❌ Exit",
        "goodbye": "✅ Goodbye! Press Enter to exit...",
        
        # Money type selection menu
        "select_money_type": "Select money type to edit:",
        "account_money": "💳 Account money (Money.json)",
        "cash_money": "💸 Cash money (Inventory.json)",
        "return_to_main": "🔙 Return to main menu",
        
        # Helper functions for show_current_balance
        "user": "User",
        "save": "Save",
        "time": "Time",
        "balance": "Account Balance", 
        "cash": "Cash",
        "total_saves": "Total saves found",
        
        # Money patching functions
        "enter_money": "💰 Enter the amount of money to set",
        "enter_cash": "💸 Enter the amount of CASH to set",
        "updated_money": "✅ Files updated",
        "updated_cash": "✅ Cash files updated",
        "no_update_money": "ℹ️ No files to update found",
        "no_update_cash": "ℹ️ No cash files to update found",
        
        # Settings
        "settings_title": "📋 PROGRAM SETTINGS",
        "animations": "• Animations: {0}",
        "enabled": "✅ Enabled",
        "disabled": "❌ Disabled",
        "auto_launch": "• Auto game launch: {0}",
        "game_path": "• Game path: {0}",
        "path_not_configured": "❌ Not configured",
        "language": "• Interface language: {0}",
        "configure_game_path": "🎮 Configure game path",
        "configure_auto_launch": "🚀 Configure auto game launch",
        "toggle_animations": "✨ Enable/disable animations",
        "change_language": "🌐 Change interface language",
        "return_to_main_menu": "🔙 Return to main menu",
        
        # Language selection
        "language_menu": "Select interface language:",
        "russian": "🇷🇺 Russian (Русский)",
        "english": "🇬🇧 English",
        "language_changed": "✅ Interface language changed to {0}",
        "language_name": "English",
        
        # Для функции animate_countdown
        "seconds": "sec",
    }
}

def get_system_language():
    """Определяет язык системы"""
    try:
        # Получаем локаль системы
        system_locale = locale.getdefaultlocale()[0]
        
        # Если локаль начинается с ru, выбираем русский язык
        if system_locale and system_locale.startswith('ru'):
            return 'ru'
        # Иначе выбираем английский
        else:
            return 'en'
    except:
        # В случае ошибки, выбираем английский по умолчанию
        return 'en'

def load_config():
    """Загружает настройки из файла конфигурации"""
    config = configparser.ConfigParser()
    
    # Настройки по умолчанию
    default_config = {
        'Settings': {
            'game_exe_path': '',
            'auto_launch_game': 'False',
            'animations_enabled': 'True',
            'language': get_system_language()  # Определяем язык системы
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

def select_game_exe(animated_text, input, os, lang):
    """Позволяет выбрать exe файл игры через проводник Windows и сохраняет путь в настройки"""
    config = load_config()
    
    current_path = config.get('Settings', 'game_exe_path', fallback='')
    
    if current_path and os.path.exists(current_path):
        animated_text(f"📂 {TRANSLATIONS[lang]['game_path'].format(current_path)}", 0.02)
    else:
        animated_text(f"📂 {TRANSLATIONS[lang]['game_path'].format(TRANSLATIONS[lang]['path_not_configured'])}", 0.02)
    
    print("\n" + "=" * 50)
    animated_text("1. Выбрать exe-файл игры через проводник", 0.02)
    animated_text(f"2. {TRANSLATIONS[lang]['return_to_main_menu']}", 0.02)
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
                animated_text(f"✅ {TRANSLATIONS[lang]['game_path'].format(file_path)}", 0.02)
                
                # Настройка автозапуска
                auto_launch = input(f"\nВключить автозапуск игры после патча? ({TRANSLATIONS[lang]['yes_no_choice']}): ")
                auto_launch_value = 'True' if check_yes_input(auto_launch) else 'False'
                config.set('Settings', 'auto_launch_game', auto_launch_value)
                save_config(config)
                
                if auto_launch_value == 'True':
                    animated_text(f"✅ {TRANSLATIONS[lang]['auto_launch'].format(TRANSLATIONS[lang]['enabled'])}", 0.02)
                else:
                    animated_text(f"ℹ️ {TRANSLATIONS[lang]['auto_launch'].format(TRANSLATIONS[lang]['disabled'])}", 0.02)
            else:
                print("❌ Выбранный файл не является exe-файлом!")
        else:
            print("⚠️ Выбор файла отменен.")
    
    input(f"\n{TRANSLATIONS[lang]['enter_to_continue']}")

def toggle_animations(animated_text, input, lang):
    """Включает или отключает анимации"""
    config = load_config()
    current_state = config.getboolean('Settings', 'animations_enabled', fallback=True)
    
    # Инвертируем текущее состояние
    new_state = not current_state
    config.set('Settings', 'animations_enabled', str(new_state))
    save_config(config)
    
    if new_state:
        animated_text(f"✅ {TRANSLATIONS[lang]['animations'].format(TRANSLATIONS[lang]['enabled'])}", 0.02)
    else:
        print(f"✅ {TRANSLATIONS[lang]['animations'].format(TRANSLATIONS[lang]['disabled'])}")
    
    input(f"\n{TRANSLATIONS[lang]['enter_to_continue']}")

def toggle_auto_launch(animated_text, input, lang):
    """Включает или отключает автозапуск игры"""
    config = load_config()
    current_state = config.getboolean('Settings', 'auto_launch_game', fallback=False)
    
    # Инвертируем текущее состояние
    new_state = not current_state
    config.set('Settings', 'auto_launch_game', str(new_state))
    save_config(config)
    
    if new_state:
        animated_text(f"✅ {TRANSLATIONS[lang]['auto_launch'].format(TRANSLATIONS[lang]['enabled'])}", 0.02)
    else:
        animated_text(f"❌ {TRANSLATIONS[lang]['auto_launch'].format(TRANSLATIONS[lang]['disabled'])}", 0.02)
    
    input(f"\n{TRANSLATIONS[lang]['enter_to_continue']}")

def language_menu(animated_text, input, os):
    """Меню выбора языка интерфейса"""
    config = load_config()
    current_lang = config.get('Settings', 'language', fallback='ru')
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        animated_text(f"{TRANSLATIONS[current_lang]['language_menu']}", 0.02)
        print("=" * 50)
        
        # Отображаем текущие настройки
        animated_text(f"\n1. {TRANSLATIONS[current_lang]['russian']}", 0.02)
        animated_text(f"2. {TRANSLATIONS[current_lang]['english']}", 0.02)
        animated_text(f"3. {TRANSLATIONS[current_lang]['return_to_main_menu']}", 0.02)
        print("=" * 50)
        
        choice = input(f"\nВаш выбор (1-3): ")
        
        if choice == "1" and current_lang != 'ru':
            config.set('Settings', 'language', 'ru')
            save_config(config)
            animated_text(f"{TRANSLATIONS['ru']['language_changed'].format(TRANSLATIONS['ru']['language_name'])}", 0.02)
            input(f"\n{TRANSLATIONS['ru']['enter_to_continue']}")
            return 'ru'
        elif choice == "2" and current_lang != 'en':
            config.set('Settings', 'language', 'en')
            save_config(config)
            animated_text(f"{TRANSLATIONS['en']['language_changed'].format(TRANSLATIONS['en']['language_name'])}", 0.02)
            input(f"\n{TRANSLATIONS['en']['enter_to_continue']}")
            return 'en'
        elif choice == "3":
            return current_lang
        else:
            if choice not in ["1", "2", "3"]:
                print(f"{TRANSLATIONS[current_lang]['invalid_choice'].format(3)}")
            else:
                print(f"✅ {TRANSLATIONS[current_lang]['language'].format(TRANSLATIONS[current_lang]['language_name'])}")
            input(f"\n{TRANSLATIONS[current_lang]['enter_to_continue']}")

def program_settings(animated_text, input, os):
    """Меню настроек программы"""
    config = load_config()
    lang = config.get('Settings', 'language', fallback='ru')
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        animations_enabled = config.getboolean('Settings', 'animations_enabled', fallback=True)
        auto_launch = config.getboolean('Settings', 'auto_launch_game', fallback=False)
        game_path = config.get('Settings', 'game_exe_path', fallback='')
        
        print("=" * 50)
        animated_text(f"{TRANSLATIONS[lang]['settings_title']}", 0.02)
        print("=" * 50)
        
        # Отображаем текущие настройки
        animations_state = TRANSLATIONS[lang]['enabled'] if animations_enabled else TRANSLATIONS[lang]['disabled']
        animated_text(f"\n{TRANSLATIONS[lang]['animations'].format(animations_state)}", 0.02)
        
        auto_launch_state = TRANSLATIONS[lang]['enabled'] if auto_launch else TRANSLATIONS[lang]['disabled']
        animated_text(f"{TRANSLATIONS[lang]['auto_launch'].format(auto_launch_state)}", 0.02)
        
        if game_path and os.path.exists(game_path):
            animated_text(f"{TRANSLATIONS[lang]['game_path'].format(game_path)}", 0.02)
        else:
            animated_text(f"{TRANSLATIONS[lang]['game_path'].format(TRANSLATIONS[lang]['path_not_configured'])}", 0.02)
        
        animated_text(f"{TRANSLATIONS[lang]['language'].format(TRANSLATIONS[lang]['language_name'])}", 0.02)
        
        print("\n" + "=" * 50)
        animated_text(f"1. {TRANSLATIONS[lang]['configure_game_path']}", 0.02)
        animated_text(f"2. {TRANSLATIONS[lang]['configure_auto_launch']}", 0.02)
        animated_text(f"3. {TRANSLATIONS[lang]['toggle_animations']}", 0.02)
        animated_text(f"4. {TRANSLATIONS[lang]['change_language']}", 0.02)
        animated_text(f"5. {TRANSLATIONS[lang]['return_to_main_menu']}", 0.02)
        print("=" * 50)
        
        choice = input(f"\nВаш выбор (1-5): ")
        
        if choice == "1":
            select_game_exe(animated_text, input, os, lang)
        elif choice == "2":
            toggle_auto_launch(animated_text, input, lang)
        elif choice == "3":
            toggle_animations(animated_text, input, lang)
        elif choice == "4":
            new_lang = language_menu(animated_text, input, os)
            if new_lang != lang:
                lang = new_lang
                config = load_config()  # Обновляем конфигурацию
        elif choice == "5":
            break
        else:
            print(f"{TRANSLATIONS[lang]['invalid_choice'].format(5)}")
            input(f"\n{TRANSLATIONS[lang]['enter_to_continue']}") 