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
import tkinter as tk
from tkinter import filedialog

# Импорт функций из модулей
from settings import (
    CHANGELOG, load_config, save_config, program_settings, 
    select_game_exe, toggle_animations, toggle_auto_launch
)
from utils import (
    animate_loading, progress_bar, animated_text, animate_countdown,
    create_backup, restore_backup, launch_game, show_changelog, check_yes_input
)

def show_current_balance():
    """Отображает текущий баланс денег в сохранениях"""
    # Базовый путь к папке сохранений игры
    base_saves_path = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\TVGS\Schedule I\Saves")
    
    # Проверка существования базовой папки
    if not os.path.exists(base_saves_path):
        print(f"❌ Папка сохранений не найдена: {base_saves_path}")
        return
    
    # Анимируем поиск папок
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=animate_loading, args=(stop_event, "Поиск сохранений"))
    loading_thread.daemon = True
    loading_thread.start()
    
    # Получаем список всех папок пользователей
    user_folders = [f for f in os.listdir(base_saves_path) if os.path.isdir(os.path.join(base_saves_path, f))]
    time.sleep(1)  # Даем анимации немного поработать для визуального эффекта
    
    # Останавливаем анимацию
    stop_event.set()
    loading_thread.join()
    
    if not user_folders:
        print("❌ Не найдены папки пользователей в директории сохранений.")
        return
    
    # Собираем данные о балансах
    balances = []
    
    # Анимируем анализ файлов
    animated_text("🔍 Анализируем файлы сохранений...", 0.02)
    
    for user_folder in user_folders:
        user_path = os.path.join(base_saves_path, user_folder)
        
        # Находим все папки сохранений для данного пользователя
        save_folders = [f for f in os.listdir(user_path) if f.startswith("SaveGame_")]
        
        for folder in save_folders:
            # Информация о сохранении для отображения
            save_time_str = folder.replace("SaveGame_", "")
            try:
                # Пытаемся преобразовать в формат даты, если возможно
                save_time = datetime.datetime.strptime(save_time_str, "%Y-%m-%d-%H-%M-%S")
                formatted_time = save_time.strftime("%d.%m.%Y %H:%M:%S")
            except ValueError:
                formatted_time = save_time_str
            
            # Словарь для хранения данных о балансе
            save_data = {
                "user": user_folder,
                "save": folder,
                "balance": None,
                "cash": None,
                "time": formatted_time
            }
            
            # Путь к файлу денег
            money_file_path = os.path.join(user_path, folder, "Money.json")
            
            # Проверяем и считываем деньги на счету
            if os.path.exists(money_file_path):
                try:
                    # Читаем содержимое файла
                    with open(money_file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    
                    # Если есть баланс, добавляем в словарь
                    if "OnlineBalance" in data:
                        save_data["balance"] = data["OnlineBalance"]
                except Exception as e:
                    print(f"⚠️ Ошибка при анализе {folder}/Money.json: {str(e)}")
            
            # Ищем наличные деньги
            player_folder_path = os.path.join(user_path, folder, "Players", "Player_0")
            if os.path.exists(player_folder_path):
                inventory_file_path = os.path.join(player_folder_path, "Inventory.json")
                if os.path.exists(inventory_file_path):
                    try:
                        # Читаем содержимое файла инвентаря
                        with open(inventory_file_path, 'r', encoding='utf-8') as file:
                            inventory_data = json.load(file)
                            
                        # Проверяем, что есть список Items
                        if "Items" in inventory_data:
                            # Ищем запись о наличных в списке Items
                            for item_str in inventory_data["Items"]:
                                # Проверяем, содержит ли строка упоминание CashData
                                if "CashData" in item_str and "CashBalance" in item_str:
                                    # Извлекаем значение CashBalance с помощью регулярного выражения
                                    cash_pattern = r'CashBalance\":([0-9.]+)'
                                    match = re.search(cash_pattern, item_str)
                                    
                                    if match:
                                        save_data["cash"] = float(match.group(1))
                    except Exception as e:
                        print(f"⚠️ Ошибка при анализе инвентаря {folder}: {str(e)}")
            
            # Добавляем данные в общий список, если есть хотя бы один из балансов
            if save_data["balance"] is not None or save_data["cash"] is not None:
                balances.append(save_data)
    
    # Отображаем результаты
    if balances:
        print("\n" + "=" * 100)
        print(f"{'Пользователь':<15} {'Сохранение':<25} {'Время':<20} {'Баланс счета':>15} {'Наличные':>15}")
        print("=" * 100)
        
        for bal in sorted(balances, key=lambda x: x["time"], reverse=True):
            # Форматируем данные для отображения
            balance_str = f"{bal['balance']}" if bal['balance'] is not None else "Нет данных"
            cash_str = f"{bal['cash']:.2f}" if bal['cash'] is not None else "Нет данных"
            
            print(f"{bal['user']:<15} {bal['save']:<25} {bal['time']:<20} {balance_str:>15} {cash_str:>15}")
        
        print("=" * 100)
        print(f"Всего найдено сохранений: {len(balances)}")
    else:
        print("ℹ️ Не найдены файлы с балансом денег.")
    
    input("\nНажмите Enter для возврата в меню...")

def load_backup():
    """Загружает сохранения из резервной копии"""
    # Базовый путь к папке сохранений игры
    base_saves_path = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\TVGS\Schedule I\Saves")
    
    if not os.path.exists(base_saves_path):
        print(f"❌ Папка сохранений не найдена: {base_saves_path}")
        input("\nНажмите Enter для продолжения...")
        return
    
    # Используем проводник для выбора папки бэкапа
    root = tk.Tk()
    root.withdraw()
    
    animated_text("🔍 Выберите папку с резервной копией...", 0.02)
    
    # Выбираем директорию на рабочем столе
    desktop_path = os.path.expandvars(r"%USERPROFILE%\Desktop")
    backup_path = filedialog.askdirectory(
        title="Выберите папку с резервной копией",
        initialdir=desktop_path
    )
    
    root.destroy()
    
    if not backup_path:
        animated_text("❌ Выбор отменен", 0.02)
        input("\nНажмите Enter для продолжения...")
        return
    
    # Проверяем, что папка содержит структуру сохранений
    is_valid_backup = False
    backup_folders = [f for f in os.listdir(backup_path) if os.path.isdir(os.path.join(backup_path, f))]
    
    for folder in backup_folders:
        subfolder_path = os.path.join(backup_path, folder)
        if os.path.isdir(subfolder_path):
            save_folders = [f for f in os.listdir(subfolder_path) if f.startswith("SaveGame_")]
            if save_folders:
                is_valid_backup = True
                break
    
    if not is_valid_backup:
        animated_text("❌ Выбранная папка не является корректной резервной копией сохранений!", 0.02)
        animated_text("Резервная копия должна содержать папки с именами пользователей и подпапки SaveGame_*", 0.02)
        input("\nНажмите Enter для продолжения...")
        return
    
    # Создаем дополнительную резервную копию текущих сохранений перед восстановлением
    confirmation = input("⚠️ Восстановление заменит все текущие сохранения! Создать резервную копию текущих сохранений? (д/н): ")
    
    if check_yes_input(confirmation):
        backup_current = create_backup(base_saves_path)
        if not backup_current:
            confirm_continue = input("❌ Не удалось создать резервную копию. Продолжить без бэкапа? (д/н): ")
            if not check_yes_input(confirm_continue):
                animated_text("❌ Восстановление отменено пользователем", 0.02)
                input("\nНажмите Enter для продолжения...")
                return
    
    # Последнее подтверждение
    final_confirm = input(f"\n⚠️ Вы действительно хотите восстановить сохранения из:\n{backup_path}\n\nВсе текущие сохранения будут заменены! (д/н): ")
    
    if not check_yes_input(final_confirm):
        animated_text("❌ Восстановление отменено пользователем", 0.02)
        input("\nНажмите Enter для продолжения...")
        return
    
    # Восстанавливаем из бэкапа
    if restore_backup(backup_path, base_saves_path):
        animated_text("✅ Сохранения успешно восстановлены из бэкапа", 0.02)
        
        # Спрашиваем об удалении бэкапа после восстановления
        delete_confirm = input("\n🗑️ Удалить папку бэкапа после восстановления? (д/н): ")
        
        if check_yes_input(delete_confirm):
            # Анимированный обратный отсчет
            animate_countdown(3, "🗑️ Удаление папки бэкапа через")
            
            try:
                shutil.rmtree(backup_path)
                animated_text(f"✅ Папка бэкапа успешно удалена: {backup_path}", 0.02)
            except Exception as e:
                print(f"⚠️ Ошибка при удалении папки бэкапа: {str(e)}")
    else:
        animated_text("❌ Не удалось восстановить сохранения из бэкапа", 0.02)
    
    input("\nНажмите Enter для продолжения...")

def patch_cash_inventory():
    """Изменяет наличные деньги в файле инвентаря игрока"""
    # Базовый путь к папке сохранений игры
    base_saves_path = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\TVGS\Schedule I\Saves")
    
    # Загружаем конфигурацию
    config = load_config()
    
    # Проверка существования базовой папки
    if not os.path.exists(base_saves_path):
        print(f"❌ Папка сохранений не найдена: {base_saves_path}")
        return
    
    # Спрашиваем у пользователя сумму наличных для установки
    while True:
        try:
            custom_cash = input("💸 Введите сумму НАЛИЧНЫХ денег для установки: ")
            if custom_cash.strip() == "":
                print("⚠️ Значение не может быть пустым!")
                continue
            custom_cash = float(custom_cash)
            break
        except ValueError:
            print("⚠️ Пожалуйста, введите число (можно с десятичной точкой)!")
    
    animated_text(f"💵 Будет установлена сумма наличных: {custom_cash}", 0.02)
    
    # Создаем резервную копию перед изменениями
    backup_path = create_backup(base_saves_path)
    if not backup_path:
        user_choice = input("⚠️ Не удалось создать резервную копию. Продолжить без бэкапа? (д/н): ")
        if not check_yes_input(user_choice):
            return
    
    # Анимируем поиск папок
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=animate_loading, args=(stop_event, "Поиск сохранений"))
    loading_thread.daemon = True
    loading_thread.start()
    
    # Получаем список всех папок пользователей
    user_folders = [f for f in os.listdir(base_saves_path) if os.path.isdir(os.path.join(base_saves_path, f))]
    time.sleep(1)  # Даем анимации немного поработать для визуального эффекта
    
    # Останавливаем анимацию
    stop_event.set()
    loading_thread.join()
    
    if not user_folders:
        print("❌ Не найдены папки пользователей в директории сохранений.")
        return
    
    # Счетчики для отчета
    total_files_processed = 0
    total_files_updated = 0
    files_to_update = []
    
    # Сначала собираем все файлы, которые нужно обновить
    animated_text("🔍 Анализируем файлы сохранений...", 0.02)
    
    for user_folder in user_folders:
        user_path = os.path.join(base_saves_path, user_folder)
        
        # Находим все папки сохранений для данного пользователя
        save_folders = [f for f in os.listdir(user_path) if f.startswith("SaveGame_")]
        
        for folder in save_folders:
            # Путь к папке игрока (только Player_0)
            player_folder_path = os.path.join(user_path, folder, "Players", "Player_0")
            
            # Проверяем существование папки
            if not os.path.exists(player_folder_path):
                continue
            
            # Путь к файлу инвентаря
            inventory_file_path = os.path.join(player_folder_path, "Inventory.json")
            
            # Проверяем существование файла
            if not os.path.exists(inventory_file_path):
                continue
            
            try:
                total_files_processed += 1
                
                # Читаем содержимое файла
                with open(inventory_file_path, 'r', encoding='utf-8') as file:
                    inventory_data = json.load(file)
                
                # Проверяем, что есть список Items
                if "Items" in inventory_data:
                    # Флаг, указывающий, нужно ли обновлять файл
                    need_update = False
                    
                    # Ищем запись о наличных в списке Items
                    for i, item_str in enumerate(inventory_data["Items"]):
                        # Проверяем, содержит ли строка упоминание CashData
                        if "CashData" in item_str and "CashBalance" in item_str:
                            # Извлекаем значение CashBalance с помощью регулярного выражения
                            cash_pattern = r'CashBalance\":([0-9.]+)'
                            match = re.search(cash_pattern, item_str)
                            
                            if match:
                                current_cash = float(match.group(1))
                                
                                # Если значение отличается, нужно обновить
                                if current_cash != custom_cash:
                                    # Заменяем значение CashBalance
                                    updated_item = item_str.replace(
                                        f'CashBalance":{current_cash}',
                                        f'CashBalance":{custom_cash}'
                                    )
                                    
                                    # Обновляем данные в списке Items
                                    inventory_data["Items"][i] = updated_item
                                    need_update = True
                    
                    # Если нужно обновлять файл, добавляем в список на обновление
                    if need_update:
                        files_to_update.append((inventory_file_path, inventory_data, user_folder, folder))
                
            except Exception as e:
                print(f"⚠️ Ошибка при анализе {folder}: {str(e)}")
    
    # Если есть файлы для обновления, показываем прогресс-бар
    if files_to_update:
        animated_text(f"🔄 Найдено файлов для обновления: {len(files_to_update)}", 0.02)
        print()
        
        # Обновляем файлы с прогресс-баром
        for i, (file_path, data, user_folder, folder) in enumerate(files_to_update):
            progress_bar(i + 1, len(files_to_update), 
                         prefix=f'Прогресс обновления: ({i+1}/{len(files_to_update)})', 
                         suffix='Завершено', length=40)
            
            try:
                # Записываем обновленный JSON обратно в файл
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4)
                
                total_files_updated += 1
                time.sleep(0.2)  # Небольшая задержка для визуального эффекта прогресс-бара
            except Exception as e:
                print(f"\n⚠️ Ошибка при обновлении {folder}: {str(e)}")
        
        print()
        animated_text(f"✅ Обновлено файлов с наличными: {total_files_updated} из {total_files_processed}", 0.02)
    else:
        animated_text(f"ℹ️ Файлы для обновления наличных не найдены или все балансы уже установлены на {custom_cash}", 0.02)
    
    # В конце функции после всех обновлений добавляем автозапуск
    if config.getboolean('Settings', 'auto_launch_game', fallback=False):
        launch_choice = input("\n🎮 Запустить игру сейчас? (д/н): ")
        if check_yes_input(launch_choice):
            launch_game()

def patch_money_file():
    """Изменяет деньги в файлах сохранений"""
    # Базовый путь к папке сохранений игры
    base_saves_path = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\TVGS\Schedule I\Saves")
    
    # Загружаем конфигурацию
    config = load_config()
    
    # Проверка существования базовой папки
    if not os.path.exists(base_saves_path):
        print(f"❌ Папка сохранений не найдена: {base_saves_path}")
        return
    
    # Спрашиваем у пользователя сумму денег для установки
    while True:
        try:
            custom_money = input("💰 Введите сумму денег для установки: ")
            if custom_money.strip() == "":
                print("⚠️ Значение не может быть пустым!")
                continue
            custom_money = int(custom_money)
            break
        except ValueError:
            print("⚠️ Пожалуйста, введите целое число!")
    
    animated_text(f"💵 Будет установлена сумма: {custom_money}", 0.02)
    
    # Создаем резервную копию перед изменениями
    backup_path = create_backup(base_saves_path)
    if not backup_path:
        user_choice = input("⚠️ Не удалось создать резервную копию. Продолжить без бэкапа? (д/н): ")
        if not check_yes_input(user_choice):
            return
    
    # Анимируем поиск папок
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=animate_loading, args=(stop_event, "Поиск сохранений"))
    loading_thread.daemon = True
    loading_thread.start()
    
    # Получаем список всех папок пользователей
    user_folders = [f for f in os.listdir(base_saves_path) if os.path.isdir(os.path.join(base_saves_path, f))]
    time.sleep(1)  # Даем анимации немного поработать для визуального эффекта
    
    # Останавливаем анимацию
    stop_event.set()
    loading_thread.join()
    
    if not user_folders:
        print("❌ Не найдены папки пользователей в директории сохранений.")
        return
    
    # Счетчики для отчета
    total_files_processed = 0
    total_files_updated = 0
    files_to_update = []
    
    # Сначала собираем все файлы, которые нужно обновить
    animated_text("🔍 Анализируем файлы сохранений...", 0.02)
    
    for user_folder in user_folders:
        user_path = os.path.join(base_saves_path, user_folder)
        
        # Находим все папки сохранений для данного пользователя
        save_folders = [f for f in os.listdir(user_path) if f.startswith("SaveGame_")]
        
        for folder in save_folders:
            money_file_path = os.path.join(user_path, folder, "Money.json")
            
            # Проверяем существование файла
            if not os.path.exists(money_file_path):
                continue
            
            try:
                total_files_processed += 1
                
                # Читаем содержимое файла
                with open(money_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Проверяем, нужно ли обновлять
                if "OnlineBalance" in data and data["OnlineBalance"] != custom_money:
                    files_to_update.append((money_file_path, data, user_folder, folder))
            except Exception as e:
                print(f"⚠️ Ошибка при анализе {folder}: {str(e)}")
    
    # Если есть файлы для обновления, показываем прогресс-бар
    if files_to_update:
        animated_text(f"🔄 Найдено файлов для обновления: {len(files_to_update)}", 0.02)
        print()
        
        # Обновляем файлы с прогресс-баром
        for i, (file_path, data, user_folder, folder) in enumerate(files_to_update):
            progress_bar(i + 1, len(files_to_update), 
                         prefix=f'Прогресс обновления: ({i+1}/{len(files_to_update)})', 
                         suffix='Завершено', length=40)
            
            try:
                # Устанавливаем новое значение
                data["OnlineBalance"] = custom_money
                
                # Записываем обновленный JSON обратно в файл
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=2)
                
                total_files_updated += 1
                time.sleep(0.2)  # Небольшая задержка для визуального эффекта прогресс-бара
            except Exception as e:
                print(f"\n⚠️ Ошибка при обновлении {folder}: {str(e)}")
        
        print()
        animated_text(f"✅ Обновлено файлов: {total_files_updated} из {total_files_processed}", 0.02)
    else:
        animated_text(f"ℹ️ Файлы для обновления не найдены или все балансы уже установлены на {custom_money}", 0.02)
    
    # В конце функции после всех обновлений добавляем автозапуск
    if config.getboolean('Settings', 'auto_launch_game', fallback=False):
        launch_choice = input("\n🎮 Запустить игру сейчас? (д/н): ")
        if check_yes_input(launch_choice):
            launch_game()

def edit_money_menu():
    """Меню выбора типа денег для изменения"""
    while True:
        print("\n" + "=" * 50)
        animated_text("Выберите тип денег для изменения:", 0.02)
        animated_text("1. 💳 Деньги на счету (Money.json)", 0.02)
        animated_text("2. 💸 Наличные деньги (Inventory.json)", 0.02)
        animated_text("3. 🔙 Вернуться в главное меню", 0.02)
        print("=" * 50)
        
        choice = input("\nВаш выбор (1-3): ")
        
        if choice == "1":
            # Запускаем функцию патча счета
            patch_money_file()
            return
        elif choice == "2":
            # Запускаем функцию патча наличных
            patch_cash_inventory()
            return
        elif choice == "3":
            return
        else:
            print("⚠️ Неверный выбор. Пожалуйста, введите число от 1 до 3.")
        
        # Ждем подтверждения для продолжения
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    # Очищаем экран и выводим красивый заголовок
    os.system('cls' if os.name == 'nt' else 'clear')
    
    title = """
    ╔╦╗╔═╗╔╗╔╔═╗╦ ╦  ╔═╗╔═╗╔╦╗╔═╗╦ ╦╔═╗╦═╗
    ║║║║ ║║║║║╣ ╚╦╝  ╠═╝╠═╣ ║ ║  ╠═╣║╣ ╠╦╝
    ╩ ╩╚═╝╝╚╝╚═╝ ╩   ╩  ╩ ╩ ╩ ╚═╝╩ ╩╚═╝╩╚═
           для Schedule I v1.8.2 by Sparki)
    """
    
    for line in title.split('\n'):
        animated_text(line, 0.01)
    
    print("-" * 50)
    
    # Главное меню
    while True:
        print("\n" + "=" * 50)
        animated_text("Выберите действие:", 0.02)
        animated_text("1. 💵 Изменить деньги в сохранениях", 0.02)
        animated_text("2. 👁️ Показать текущий баланс", 0.02)
        animated_text("3. ⚙️ Настройки программы", 0.02)
        animated_text("4. 🚀 Запустить игру", 0.02)
        animated_text("5. 💾 Загрузить backup", 0.02)
        animated_text("6. 📋 Показать историю изменений (changelog)", 0.02)
        animated_text("7. ❌ Выход", 0.02)
        print("=" * 50)
        
        choice = input("\nВаш выбор (1-7): ")
        
        if choice == "1":
            # Показываем подменю выбора типа денег
            edit_money_menu()
        elif choice == "2":
            # Показываем текущий баланс
            show_current_balance()
        elif choice == "3":
            # Открываем меню настроек программы
            program_settings(animated_text, input, os)
        elif choice == "4":
            # Запускаем игру
            launch_game()
            input("\nНажмите Enter для продолжения...")
        elif choice == "5":
            # Загружаем сохранения из резервной копии
            load_backup()
        elif choice == "6":
            # Показываем changelog
            show_changelog(CHANGELOG)
        elif choice == "7":
            animated_text("\n✅ До свидания! Нажмите Enter для выхода...", 0.02)
            input()
            break
        else:
            print("⚠️ Неверный выбор. Пожалуйста, введите число от 1 до 7.")
        
        # Очищаем экран после каждого действия
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Показываем заголовок снова
        for line in title.split('\n'):
            animated_text(line, 0.01)
        
        print("-" * 50)