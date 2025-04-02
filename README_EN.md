# Money Patcher for Schedule I

A program for changing the balance value in the Schedule I game save files.

## Program Website

For user convenience, an official website has been created: [Money Patcher for Schedule I](https://sparki1337.github.io/Schedule-I-Cheat-money/)

> **Important:** Each time you visit the site, it is recommended to refresh the page (press F5) so that all styles and scripts load correctly.

The website offers:
- Description of all program features
- Download links for the latest program versions
- Usage instructions
- Switching between Russian and English languages

## Description

This program automatically finds all Schedule I game saves (for all users) and changes the `OnlineBalance` value to any user-specified amount in the `Money.json` file. The program can also change the amount of cash in the player's inventory (`Inventory.json` file). The program creates a backup of the saves before making changes and allows you to restore them if necessary.

## How to Use

1. Make sure you have Python 3.6 or higher installed
2. Run the `money_patcher.py` file by double-clicking or from the command line:
   ```
   python money_patcher.py
   ```
3. In the main menu, select the desired action:
   - Edit money in saves (edits Money.json)
   - Edit cash money (edits Inventory.json)
   - Show current balance
   - Program settings
   - Launch game
   - Load backup
   - Show changelog
   - Exit

## Features

- Change the amount of money in saves to any user-specified amount
- Change the amount of cash in the player's inventory
- View the current balance (both account and cash) in all saves without making changes
- Automatic game launch after making changes (optional)
- Configure the path to the game exe file through Windows Explorer
- Option to disable animations for faster operation
- Load saves from previously created backups
- Automatic search for all user folders (works with any user IDs)
- Update all found saves
- Backup all saves to the desktop before making changes
- Ability to restore saves from a backup
- Final statistics on the number of processed and updated files
- Visual animations and progress bars to track execution progress
- Improved input handling considering different keyboard layouts when choosing yes/no
- Multilingual interface (Russian and English) with automatic system language detection

## Program Structure

The program is divided into 3 modules for better code organization:

1. **money_patcher.py** - the main file with the main menu and basic program functions
2. **settings.py** - module for managing settings and program configuration
3. **utils.py** - module with auxiliary functions (animations, backups, game loading)

## Settings Menu

The following settings are available in the program:

- **Game path settings**: select the game exe file through Windows Explorer
- **Auto-launch settings**: enable/disable automatic game launch after patch
- **Animation settings**: enable/disable visual effects for faster operation on less powerful computers
- **Language settings**: choose interface language (Russian or English)

## Visual Effects

- Beautiful ASCII header at startup
- Animations when loading and searching for files
- "Typewriter" effect for important messages
- Progress bar when updating files
- Animated countdown before deletion
- Emojis to highlight important messages

## Working with Backups

- Backup is created on the desktop in the `Schedule_I_Backup_YYYY-MM-DD_HH-MM-SS` folder
- The program offers to restore saves immediately after executing the patch
- Separate menu item "Load backup" for restoring from any previously created backup
- Ability to delete the backup folder after restoration
- Selecting the backup folder through Windows Explorer

## Changelog

### Version 1.9
- Added multilingual support (Russian and English)
- Automatic system language detection at first launch
- Added ability to select interface language in settings

### Version 1.8.2
- Removed the function of saving the last used value
- Added mandatory requirement to enter a value each time
- Optimized the value input interface

### Version 1.8.1
- Fixed working with Inventory.json for correct display and changing of cash
- Improved interface: added a submenu for selecting the type of money (cash/account)
- Reworked the logic of reading and updating JSON files
- Added support for more complex save structure

### Version 1.8
- Added the ability to change cash in inventory (Inventory.json)
- Improved work with save files, added support for decimal values

### Version 1.7
- Added improved input handling considering different keyboard layouts
- Added support for yes/no input regardless of current layout

### Version 1.6
- Reorganized program structure into 3 files for better support

### Version 1.5
- Added a separate menu item "Load backup"
- Improved backup recovery system
- Added backup folder deletion after recovery

### Version 1.4
- Added a separate menu item "Settings"
- Added the ability to enable/disable animations

### Version 1.3
- Added game exe file selection through Windows Explorer
- Removed automatic mode of exe file search

### Version 1.2
- Added option to view current balance without changes
- Added ability to auto-launch the game after patching
- Added function to select and save path to game exe file

### Version 1.1
- Added the ability to select a custom amount of money
- Updated message text based on custom amount

### Version 1.0
- Initial program release
- Implemented function to change money to a fixed amount of 10000
- Added creation of save backups
- Added ability to restore from backups

## Technical Details

- The program uses the base path to the game saves: `C:\Users\[user]\AppData\LocalLow\TVGS\Schedule I\Saves\`
- Automatically finds all user IDs in the saves folder
- Processes all folders with the prefix SaveGame_
- In the `Money.json` file, the value of the "OnlineBalance" field is changed to the amount specified by the user
- In the `Inventory.json` file, the value of the "CashBalance" field for cash is changed to the value specified by the user
- Program settings are saved in the `money_patcher_config.ini` file 