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

from settings import (
    CHANGELOG, load_config, save_config, program_settings, 
    select_game_exe, toggle_animations, toggle_auto_launch,
    TRANSLATIONS, language_menu, get_system_language
)
from utils import (
    animate_loading, progress_bar, animated_text, animate_countdown,
    create_backup, restore_backup, launch_game, show_changelog, check_yes_input
)

def show_current_balance(lang):
    base_saves_path = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\TVGS\Schedule I\Saves")
    if not os.path.exists(base_saves_path):
        print(f"{TRANSLATIONS[lang]['savings_path_not_found'].format(base_saves_path)}")
        return
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=animate_loading, args=(stop_event, "Поиск сохранений"))
    loading_thread.daemon = True
    loading_thread.start()
    user_folders = [f for f in os.listdir(base_saves_path) if os.path.isdir(os.path.join(base_saves_path, f))]
    time.sleep(1)
    stop_event.set()
    loading_thread.join()
    if not user_folders:
        print(f"{TRANSLATIONS[lang]['no_user_folders']}")
        return
    balances = []
    animated_text("🔍 Анализируем файлы сохранений...", 0.02)
    for user_folder in user_folders:
        user_path = os.path.join(base_saves_path, user_folder)
        save_folders = [f for f in os.listdir(user_path) if f.startswith("SaveGame_")]
        for folder in save_folders:
            save_time_str = folder.replace("SaveGame_", "")
            try:
                save_time = datetime.datetime.strptime(save_time_str, "%Y-%m-%d-%H-%M-%S")
                formatted_time = save_time.strftime("%d.%m.%Y %H:%M:%S")
            except ValueError:
                formatted_time = save_time_str
            save_data = {
                "user": user_folder,
                "save": folder,
                "balance": None,
                "cash": None,
                "time": formatted_time
            }
            money_file_path = os.path.join(user_path, folder, "Money.json")
            if os.path.exists(money_file_path):
                try:
                    with open(money_file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    if "OnlineBalance" in data:
                        save_data["balance"] = data["OnlineBalance"]
                except Exception as e:
                    print(f"⚠️ Ошибка при анализе {folder}/Money.json: {str(e)}")
            player_folder_path = os.path.join(user_path, folder, "Players", "Player_0")
            if os.path.exists(player_folder_path):
                inventory_file_path = os.path.join(player_folder_path, "Inventory.json")
                if os.path.exists(inventory_file_path):
                    try:
                        with open(inventory_file_path, 'r', encoding='utf-8') as file:
                            inventory_data = json.load(file)
                        if "Items" in inventory_data:
                            for item_str in inventory_data["Items"]:
                                if "CashData" in item_str and "CashBalance" in item_str:
                                    cash_pattern = r'CashBalance\":([0-9.]+)'
                                    match = re.search(cash_pattern, item_str)
                                    if match:
                                        save_data["cash"] = float(match.group(1))
                    except Exception as e:
                        print(f"⚠️ Ошибка при анализе инвентаря {folder}: {str(e)}")
            if save_data["balance"] is not None or save_data["cash"] is not None:
                balances.append(save_data)
    if balances:
        print("\n" + "=" * 100)
        print(f"{TRANSLATIONS[lang]['user']:<15} {TRANSLATIONS[lang]['save']:<25} {TRANSLATIONS[lang]['time']:<20} {TRANSLATIONS[lang]['balance']:>15} {TRANSLATIONS[lang]['cash']:>15}")
        print("=" * 100)
        for bal in sorted(balances, key=lambda x: x["time"], reverse=True):
            balance_str = f"{bal['balance']}" if bal['balance'] is not None else "Нет данных"
            cash_str = f"{bal['cash']:.2f}" if bal['cash'] is not None else "Нет данных"
            print(f"{bal['user']:<15} {bal['save']:<25} {bal['time']:<20} {balance_str:>15} {cash_str:>15}")
        print("=" * 100)
        print(f"{TRANSLATIONS[lang]['total_saves']}: {len(balances)}")
    else:
        print("ℹ️ Не найдены файлы с балансом денег.")
    input(f"\n{TRANSLATIONS[lang]['enter_to_continue']}")

def load_backup(lang):
    base_saves_path = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\TVGS\Schedule I\Saves")
    if not os.path.exists(base_saves_path):
        print(f"{TRANSLATIONS[lang]['savings_path_not_found'].format(base_saves_path)}")
        input(f"\n{TRANSLATIONS[lang]['enter_to_continue']}")
        return
    root = tk.Tk()
    root.withdraw()
    animated_text(f"🔍 {TRANSLATIONS[lang]['select_backup_folder']}...", 0.02)
    desktop_path = os.path.expandvars(r"%USERPROFILE%\Desktop")
    backup_path = filedialog.askdirectory(
        title=TRANSLATIONS[lang]['select_backup_folder'],
        initialdir=desktop_path
    )
    root.destroy()
    if not backup_path:
        animated_text(f"❌ {TRANSLATIONS[lang]['selection_canceled']}", 0.02)
        input(f"\n{TRANSLATIONS[lang]['enter_to_continue']}")
        return
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
        animated_text(f"❌ {TRANSLATIONS[lang]['invalid_backup_folder']}", 0.02)
        animated_text(f"{TRANSLATIONS[lang]['backup_folder_requirements']}", 0.02)
        input(f"\n{TRANSLATIONS[lang]['enter_to_continue']}")
        return
    confirmation = input(f"⚠️ {TRANSLATIONS[lang]['restore_warning']} ({TRANSLATIONS[lang]['yes_no_choice']}): ")
    if check_yes_input(confirmation):
        backup_current = create_backup(base_saves_path, lang)
        if not backup_current:
            confirmation = input(f"⚠️ {TRANSLATIONS[lang]['continue_without_backup']} ({TRANSLATIONS[lang]['yes_no_choice']}): ")
            if not check_yes_input(confirmation):
                return
    if restore_backup(backup_path, base_saves_path, lang):
        delete_backup = input(f"\n{TRANSLATIONS[lang]['delete_backup_after_restore']} ({TRANSLATIONS[lang]['yes_no_choice']}): ")
        if check_yes_input(delete_backup):
            try:
                animated_text(f"🔄 {TRANSLATIONS[lang]['deleting_backup']}...", 0.02)
                animate_countdown(3, f"{TRANSLATIONS[lang]['deletion_countdown']}")
                shutil.rmtree(backup_path)
                animated_text(f"✅ {TRANSLATIONS[lang]['backup_deleted']}", 0.02)
            except Exception as e:
                print(f"⚠️ {TRANSLATIONS[lang]['deletion_error']}: {str(e)}")
    input(f"\n{TRANSLATIONS[lang]['enter_to_continue']}")

def patch_cash_inventory(lang):
    base_saves_path = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\TVGS\Schedule I\Saves")
    config = load_config()
    if not os.path.exists(base_saves_path):
        print(f"❌ Папка сохранений не найдена: {base_saves_path}")
        return
    while True:
        try:
            custom_cash = input(f"{TRANSLATIONS[lang]['enter_cash']}: ")
            if custom_cash.strip() == "":
                print("⚠️ Значение не может быть пустым!")
                continue
            custom_cash = float(custom_cash)
            break
        except ValueError:
            print("⚠️ Пожалуйста, введите число (можно с десятичной точкой)!")
    animated_text(f"💵 Будет установлена сумма наличных: {custom_cash}", 0.02)
    backup_path = create_backup(base_saves_path)
    if not backup_path:
        user_choice = input("⚠️ Не удалось создать резервную копию. Продолжить без бэкапа? (д/н): ")
        if not check_yes_input(user_choice):
            return
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=animate_loading, args=(stop_event, "Поиск сохранений"))
    loading_thread.daemon = True
    loading_thread.start()
    user_folders = [f for f in os.listdir(base_saves_path) if os.path.isdir(os.path.join(base_saves_path, f))]
    time.sleep(1)
    stop_event.set()
    loading_thread.join()
    if not user_folders:
        print("❌ Не найдены папки пользователей в директории сохранений.")
        return
    total_files_processed = 0
    total_files_updated = 0
    files_to_update = []
    animated_text("🔍 Анализируем файлы сохранений...", 0.02)
    for user_folder in user_folders:
        user_path = os.path.join(base_saves_path, user_folder)
        save_folders = [f for f in os.listdir(user_path) if f.startswith("SaveGame_")]
        for folder in save_folders:
            player_folder_path = os.path.join(user_path, folder, "Players", "Player_0")
            if not os.path.exists(player_folder_path):
                continue
            inventory_file_path = os.path.join(player_folder_path, "Inventory.json")
            if not os.path.exists(inventory_file_path):
                continue
            try:
                total_files_processed += 1
                with open(inventory_file_path, 'r', encoding='utf-8') as file:
                    inventory_data = json.load(file)
                if "Items" in inventory_data:
                    need_update = False
                    for i, item_str in enumerate(inventory_data["Items"]):
                        if "CashData" in item_str and "CashBalance" in item_str:
                            cash_pattern = r'CashBalance\":([0-9.]+)'
                            match = re.search(cash_pattern, item_str)
                            if match:
                                current_cash = float(match.group(1))
                                if current_cash != custom_cash:
                                    updated_item = item_str.replace(
                                        f'CashBalance":{current_cash}',
                                        f'CashBalance":{custom_cash}'
                                    )
                                    inventory_data["Items"][i] = updated_item
                                    need_update = True
                    if need_update:
                        files_to_update.append((inventory_file_path, inventory_data, user_folder, folder))
            except Exception as e:
                print(f"⚠️ Ошибка при анализе {folder}: {str(e)}")
    if files_to_update:
        animated_text(f"🔄 Найдено файлов для обновления: {len(files_to_update)}", 0.02)
        print()
        for i, (file_path, data, user_folder, folder) in enumerate(files_to_update):
            progress_bar(i + 1, len(files_to_update), 
                         prefix=f'{TRANSLATIONS[lang]["progress_update"]} ({i+1}/{len(files_to_update)})', 
                         suffix=TRANSLATIONS[lang]['completed'], length=40)
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4)
                total_files_updated += 1
                time.sleep(0.2)
            except Exception as e:
                print(f"\n⚠️ {TRANSLATIONS[lang]['error_update']} {folder}: {str(e)}")
        print()
        animated_text(f"✅ {TRANSLATIONS[lang]['updated_cash']}: {total_files_updated} из {total_files_processed}", 0.02)
    else:
        animated_text(f"ℹ️ {TRANSLATIONS[lang]['no_update_cash']} или все балансы уже установлены на {custom_cash}", 0.02)
    if config.getboolean('Settings', 'auto_launch_game', fallback=False):
        launch_choice = input("\n🎮 Запустить игру сейчас? (д/н): ")
        if check_yes_input(launch_choice):
            launch_game()

def patch_money_file(lang):
    base_saves_path = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\TVGS\Schedule I\Saves")
    config = load_config()
    if not os.path.exists(base_saves_path):
        print(f"❌ Папка сохранений не найдена: {base_saves_path}")
        return
    while True:
        try:
            custom_money = input(f"{TRANSLATIONS[lang]['enter_money']}: ")
            if custom_money.strip() == "":
                print("⚠️ Значение не может быть пустым!")
                continue
            custom_money = int(custom_money)
            break
        except ValueError:
            print("⚠️ Пожалуйста, введите целое число!")
    animated_text(f"💵 Будет установлена сумма: {custom_money}", 0.02)
    backup_path = create_backup(base_saves_path)
    if not backup_path:
        user_choice = input("⚠️ Не удалось создать резервную копию. Продолжить без бэкапа? (д/н): ")
        if not check_yes_input(user_choice):
            return
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=animate_loading, args=(stop_event, "Поиск сохранений"))
    loading_thread.daemon = True
    loading_thread.start()
    user_folders = [f for f in os.listdir(base_saves_path) if os.path.isdir(os.path.join(base_saves_path, f))]
    time.sleep(1)
    stop_event.set()
    loading_thread.join()
    if not user_folders:
        print("❌ Не найдены папки пользователей в директории сохранений.")
        return
    total_files_processed = 0
    total_files_updated = 0
    files_to_update = []
    animated_text("🔍 Анализируем файлы сохранений...", 0.02)
    for user_folder in user_folders:
        user_path = os.path.join(base_saves_path, user_folder)
        save_folders = [f for f in os.listdir(user_path) if f.startswith("SaveGame_")]
        for folder in save_folders:
            money_file_path = os.path.join(user_path, folder, "Money.json")
            if not os.path.exists(money_file_path):
                continue
            try:
                total_files_processed += 1
                with open(money_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                if "OnlineBalance" in data and data["OnlineBalance"] != custom_money:
                    files_to_update.append((money_file_path, data, user_folder, folder))
            except Exception as e:
                print(f"⚠️ Ошибка при анализе {folder}: {str(e)}")
    if files_to_update:
        animated_text(f"🔄 Найдено файлов для обновления: {len(files_to_update)}", 0.02)
        print()
        for i, (file_path, data, user_folder, folder) in enumerate(files_to_update):
            progress_bar(i + 1, len(files_to_update), 
                         prefix=f'{TRANSLATIONS[lang]["progress_update"]} ({i+1}/{len(files_to_update)})', 
                         suffix=TRANSLATIONS[lang]['completed'], length=40)
            try:
                data["OnlineBalance"] = custom_money
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=2)
                total_files_updated += 1
                time.sleep(0.2)
            except Exception as e:
                print(f"\n⚠️ {TRANSLATIONS[lang]['error_update']} {folder}: {str(e)}")
        print()
        animated_text(f"✅ {TRANSLATIONS[lang]['updated_money']}: {total_files_updated} из {total_files_processed}", 0.02)
    else:
        animated_text(f"ℹ️ {TRANSLATIONS[lang]['no_update_money']} или все балансы уже установлены на {custom_money}", 0.02)
    if config.getboolean('Settings', 'auto_launch_game', fallback=False):
        launch_choice = input("\n🎮 Запустить игру сейчас? (д/н): ")
        if check_yes_input(launch_choice):
            launch_game()

def edit_money_menu(lang):
    while True:
        print("\n" + "=" * 50)
        animated_text(f"{TRANSLATIONS[lang]['select_money_type']}", 0.02)
        animated_text(f"1. {TRANSLATIONS[lang]['account_money']}", 0.02)
        animated_text(f"2. {TRANSLATIONS[lang]['cash_money']}", 0.02)
        animated_text(f"3. {TRANSLATIONS[lang]['return_to_main']}", 0.02)
        print("=" * 50)
        choice = input("\nВаш выбор (1-3): ")
        if choice == "1":
            patch_money_file(lang)
            return
        elif choice == "2":
            patch_cash_inventory(lang)
            return
        elif choice == "3":
            return
        else:
            print(f"{TRANSLATIONS[lang]['invalid_choice'].format(3)}")
        input(f"\n{TRANSLATIONS[lang]['enter_to_continue']}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    config = load_config()
    lang = config.get('Settings', 'language', fallback=get_system_language())
    title = """
    ╔╦╗╔═╗╔╗╔╔═╗╦ ╦  ╔═╗╔═╗╔╦╗╔═╗╦ ╦╔═╗╦═╗
    ║║║║ ║║║║║╣ ╚╦╝  ╠═╝╠═╣ ║ ║  ╠═╣║╣ ╠╦╝
    ╩ ╩╚═╝╝╚╝╚═╝ ╩   ╩  ╩ ╩ ╩ ╚═╝╩ ╩╚═╝╩╚═
           для Schedule I v1.9 by Sparki)
    """
    for line in title.split('\n'):
        animated_text(line, 0.01)
    print("-" * 50)
    while True:
        print("\n" + "=" * 50)
        animated_text(f"{TRANSLATIONS[lang]['select_action']}", 0.02)
        animated_text(f"1. {TRANSLATIONS[lang]['edit_money']}", 0.02)
        animated_text(f"2. {TRANSLATIONS[lang]['show_balance']}", 0.02)
        animated_text(f"3. {TRANSLATIONS[lang]['settings']}", 0.02)
        animated_text(f"4. {TRANSLATIONS[lang]['launch_game']}", 0.02)
        animated_text(f"5. {TRANSLATIONS[lang]['load_backup']}", 0.02)
        animated_text(f"6. {TRANSLATIONS[lang]['show_changelog']}", 0.02)
        animated_text(f"7. {TRANSLATIONS[lang]['exit']}", 0.02)
        print("=" * 50)
        choice = input("\nВаш выбор (1-7): ")
        if choice == "1":
            edit_money_menu(lang)
        elif choice == "2":
            show_current_balance(lang)
        elif choice == "3":
            new_lang = program_settings(animated_text, input, os)
            if new_lang:
                lang = new_lang
        elif choice == "4":
            launch_game()
            input(f"\n{TRANSLATIONS[lang]['enter_to_continue']}")
        elif choice == "5":
            load_backup(lang)
        elif choice == "6":
            show_changelog(CHANGELOG, lang)
        elif choice == "7":
            animated_text(f"\n{TRANSLATIONS[lang]['goodbye']}", 0.02)
            input()
            break
        else:
            print(f"{TRANSLATIONS[lang]['invalid_choice'].format(7)}")
        os.system('cls' if os.name == 'nt' else 'clear')
        for line in title.split('\n'):
            animated_text(line, 0.01)
        print("-" * 50)
