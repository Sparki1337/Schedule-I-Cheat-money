import json
import os
import re
import glob
import shutil
import datetime
import time
import sys
import itertools
import threading
import configparser
import subprocess

# Функции для отображения анимаций и UI эффектов

# Добавляем новую функцию для обработки ответов Да/Нет с учетом раскладки клавиатуры
def check_yes_input(user_input):
    """
    Проверяет, является ли ввод пользователя положительным ответом (да/yes)
    с учетом возможных вариантов в разных раскладках клавиатуры.
    
    Аргументы:
        user_input (str): Строка ввода пользователя
        
    Возвращает:
        bool: True для положительного ответа, False для отрицательного
    """
    # Приводим ввод к нижнему регистру для единообразия
    user_input = user_input.lower().strip()
    
    # Список возможных положительных ответов в обеих раскладках
    positive_answers = [
        'д', 'да', 'y', 'yes',      # Стандартные ответы на русском и английском
        'l', 'lf', 'la', 'lfla',    # Русские буквы на английской раскладке
        't', 'n', 'tn', 'ntn'       # Английские буквы на русской раскладке
    ]
    
    return user_input in positive_answers

def animate_loading(stop_event, message="Загрузка"):
    """Отображает анимацию загрузки"""
    # Проверяем, включены ли анимации
    # Импортируем load_config здесь, чтобы избежать циклической зависимости
    from settings import load_config
    config = load_config()
    if not config.getboolean('Settings', 'animations_enabled', fallback=True):
        print(f"{message}... ", end="", flush=True)
        while not stop_event.is_set():
            time.sleep(0.1)
        print("Готово!")
        return
        
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    while not stop_event.is_set():
        sys.stdout.write('\r' + message + ' ' + next(spinner) + ' ')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')
    sys.stdout.flush()

def progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """Отображает прогресс-бар"""
    # Проверяем, включены ли анимации
    # Импортируем load_config здесь, чтобы избежать циклической зависимости
    from settings import load_config
    config = load_config()
    if not config.getboolean('Settings', 'animations_enabled', fallback=True):
        if iteration == total:
            print(f"{prefix} {suffix} 100%")
        return
        
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '░' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()

def animated_text(text, delay=0.03):
    """Выводит текст с эффектом печатной машинки"""
    # Проверяем, включены ли анимации
    # Импортируем load_config здесь, чтобы избежать циклической зависимости
    from settings import load_config
    config = load_config()
    if not config.getboolean('Settings', 'animations_enabled', fallback=True):
        print(text)
        return
        
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def animate_countdown(seconds, message="Удаление через", lang=None):
    """Анимированный обратный отсчет"""
    # Импортируем здесь для избежания циклических импортов
    from settings import load_config, TRANSLATIONS, get_system_language
    
    if lang is None:
        config = load_config()
        lang = config.get('Settings', 'language', fallback=get_system_language())
    
    config = load_config()
    if not config.getboolean('Settings', 'animations_enabled', fallback=True):
        print(f"{message} {seconds} {TRANSLATIONS[lang]['seconds']}...")
        time.sleep(seconds)
        return
        
    for i in range(seconds, 0, -1):
        sys.stdout.write(f'\r{message} {i} {TRANSLATIONS[lang]["seconds"]}... ')
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\r' + ' ' * (len(message) + 15) + '\r')
    sys.stdout.flush()

# Функции работы с файлами сохранений

def create_backup(base_saves_path, lang=None):
    """Создает резервную копию папки сохранений на рабочем столе"""
    # Импортируем здесь для избежания циклических импортов
    from settings import TRANSLATIONS, load_config, get_system_language
    
    if lang is None:
        config = load_config()
        lang = config.get('Settings', 'language', fallback=get_system_language())
    
    # Получаем путь к рабочему столу
    desktop_path = os.path.expandvars(r"%USERPROFILE%\Desktop")
    
    # Создаем имя папки для бэкапа с текущей датой и временем
    backup_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_folder_name = f"Schedule_I_Backup_{backup_time}"
    backup_path = os.path.join(desktop_path, backup_folder_name)
    
    try:
        # Начинаем анимацию загрузки в отдельном потоке
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=animate_loading, args=(stop_event, TRANSLATIONS[lang]['creating_backup']))
        loading_thread.daemon = True
        loading_thread.start()
        
        # Копируем всю папку сохранений
        shutil.copytree(base_saves_path, backup_path)
        
        # Останавливаем анимацию
        stop_event.set()
        loading_thread.join()
        
        animated_text(f"✅ {TRANSLATIONS[lang]['backup_created']}: {backup_path}")
        return backup_path
    except Exception as e:
        if 'stop_event' in locals() and not stop_event.is_set():
            stop_event.set()
            loading_thread.join()
        print(f"❌ {TRANSLATIONS[lang]['backup_error']}: {str(e)}")
        return None

def restore_backup(backup_path, base_saves_path, lang=None):
    """Восстанавливает сохранения из резервной копии"""
    # Импортируем здесь для избежания циклических импортов
    from settings import TRANSLATIONS, load_config, get_system_language
    
    if lang is None:
        config = load_config()
        lang = config.get('Settings', 'language', fallback=get_system_language())
    
    if not os.path.exists(backup_path):
        print(f"❌ {TRANSLATIONS[lang]['backup_not_found']}")
        return False
        
    try:
        # Начинаем анимацию загрузки в отдельном потоке
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=animate_loading, args=(stop_event, TRANSLATIONS[lang]['restoring_saves']))
        loading_thread.daemon = True
        loading_thread.start()
        
        # Удаляем текущие сохранения
        shutil.rmtree(base_saves_path)
        # Копируем обратно из бэкапа
        shutil.copytree(backup_path, base_saves_path)
        
        # Останавливаем анимацию
        stop_event.set()
        loading_thread.join()
        
        animated_text(f"✅ {TRANSLATIONS[lang]['saves_restored']}: {backup_path}")
        return True
    except Exception as e:
        if 'stop_event' in locals() and not stop_event.is_set():
            stop_event.set()
            loading_thread.join()
        print(f"❌ {TRANSLATIONS[lang]['restore_error']}: {str(e)}")
        return False

def launch_game(lang=None):
    """Запускает игру, если путь настроен"""
    # Импортируем здесь для избежания циклических импортов
    from settings import load_config, TRANSLATIONS, get_system_language
    
    if lang is None:
        config = load_config()
        lang = config.get('Settings', 'language', fallback=get_system_language())
    else:
        config = load_config()
    
    game_path = config.get('Settings', 'game_exe_path', fallback='')
    
    if game_path and os.path.exists(game_path):
        animated_text(f"🚀 {TRANSLATIONS[lang]['launching_game']}: {game_path}", 0.02)
        try:
            # Используем shell=True и исправляем потенциальные проблемы с путем
            # Экранируем путь в кавычки для обработки пробелов и спец. символов
            game_path = game_path.replace('\\', '/')  # Исправляем слеши для Windows
            
            # Пытаемся запустить игру с правами администратора через команду start
            if os.name == 'nt':  # Для Windows
                subprocess.Popen(f'start "" "{game_path}"', shell=True)
            else:  # Для Linux/Mac
                subprocess.Popen(f'"{game_path}"', shell=True)
                
            return True
        except Exception as e:
            print(f"❌ {TRANSLATIONS[lang]['launch_error']}: {str(e)}")
            animated_text(f"🛠️ {TRANSLATIONS[lang]['launch_solution']}", 0.02)
            animated_text(f"   {TRANSLATIONS[lang]['launch_manually']}", 0.02)
            return False
    else:
        print(f"❌ {TRANSLATIONS[lang]['path_not_configured_full']}")
        print(f"{TRANSLATIONS[lang]['use_settings']}")
        return False

# Функция для отображения истории изменений
def show_changelog(CHANGELOG, lang=None):
    """Отображает историю изменений программы"""
    # Импортируем здесь для избежания циклических импортов
    from settings import TRANSLATIONS
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Если язык не указан, используем русский по умолчанию
    if lang is None:
        from settings import load_config, get_system_language
        config = load_config()
        lang = config.get('Settings', 'language', fallback=get_system_language())
    
    animated_text("📋 ИСТОРИЯ ИЗМЕНЕНИЙ", 0.02)
    print("-" * 50)
    
    # Отображаем changelog в порядке убывания версий
    for version in sorted(CHANGELOG.keys(), key=lambda v: [int(x) for x in v.split('.')], reverse=True):
        animated_text(f"\n🔹 Версия {version}:", 0.02)
        for change in CHANGELOG[version]:
            animated_text(f"  • {change}", 0.01)
    
    print("\n" + "-" * 50)
    input(f"{TRANSLATIONS[lang]['enter_to_continue']}") 