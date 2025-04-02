# Money Patcher для Schedule I (English README - [Readme_Eng](https://github.com/Sparki1337/Schedule-I-Cheat-money/blob/main/README_EN.md))

Программа для изменения значения баланса в файлах сохранений игры Schedule I. 

## Веб-сайт программы

Для удобства пользователей создан официальный веб-сайт: [Money Patcher для Schedule I](https://sparki1337.github.io/Schedule-I-Cheat-money/)

> **Важно:** При каждом посещении сайта рекомендуется обновить страницу (нажать F5), чтобы корректно загрузились все стили и скрипты.

На сайте доступно:
- Описание всех возможностей программы
- Скачивание актуальных версий программы
- Инструкции по использованию
- Переключение между русским и английским языками

## Описание

Эта программа автоматически находит все сохранения игры Schedule I (для всех пользователей) и изменяет значение `OnlineBalance` на любую указанную пользователем сумму в файле `Money.json`. Также программа может изменять сумму наличных денег в инвентаре игрока (файл `Inventory.json`). Программа создает резервную копию сохранений перед внесением изменений и позволяет восстановить их при необходимости.

## Как использовать

1. Убедитесь, что у вас установлен Python 3.6 или выше
2. Запустите файл `money_patcher.py` двойным кликом или из командной строки:
   ```
   python money_patcher.py
   ```
3. В главном меню выберите нужное действие:
   - Изменить деньги в сохранениях (редактирует Money.json)
   - Изменить наличные деньги (редактирует Inventory.json)
   - Показать текущий баланс
   - Настройки программы
   - Запустить игру
   - Загрузить backup
   - Показать историю изменений (changelog)
   - Выход

## Возможности программы

- 💵 **Изменение денег на счету (банковская карта):** работает как в онлайн, так и в одиночном режиме
- 💰 **Изменение наличных денег:** работает в основном только в одиночном режиме
- 👁️ **Просмотр текущего баланса** во всех сохранениях
- 🚀 **Автоматический запуск игры** после внесения изменений (опционально)
- 📂 **Настройка пути к exe-файлу игры** через проводник Windows
- ⚡ **Возможность отключения анимаций** для более быстрой работы
- 💾 **Загрузка сохранений** из ранее созданных резервных копий
- 🔍 **Автоматический поиск** всех папок пользователей (работает с любыми ID пользователей)
- 🔄 **Обновление всех найденных сохранений**
- 🔒 **Резервное копирование** всех сохранений на рабочий стол перед внесением изменений
- 🔙 **Возможность восстановить сохранения** из резервной копии
- 📊 **Итоговая статистика** о количестве обработанных и обновленных файлов
- ✨ **Визуальные анимации и прогресс-бары** для отслеживания хода выполнения
- ⌨️ **Улучшенная обработка ввода** с учетом разных раскладок клавиатуры при выборе да/нет
- 🌐 **Многоязычный интерфейс** (русский и английский) с автоматическим определением языка системы

## Структура программы

Программа разделена на 3 модуля для лучшей организации кода:

1. **money_patcher.py** - основной файл с главным меню и основными функциями программы
2. **settings.py** - модуль для управления настройками и конфигурацией программы
3. **utils.py** - модуль с вспомогательными функциями (анимации, бэкапы, загрузка игры)

## Меню настроек

В программе доступны следующие настройки:

- **Настройка пути к игре**: выбор exe-файла игры через проводник Windows
- **Настройка автозапуска**: включение/отключение автоматического запуска игры после патча
- **Настройка анимаций**: включение/отключение визуальных эффектов для более быстрой работы на слабых компьютерах
- **Выбор языка**: выбор языка интерфейса (русский или английский)

## Визуальные эффекты

- Красивый ASCII-заголовок при запуске
- Анимации при загрузке и поиске файлов
- Эффект "печатной машинки" для важных сообщений
- Прогресс-бар при обновлении файлов
- Анимированный обратный отсчет перед удалением
- Эмодзи для выделения важных сообщений

## Работа с резервными копиями

- Резервная копия создается на рабочем столе в папке `Schedule_I_Backup_YYYY-MM-DD_HH-MM-SS`
- Программа предлагает восстановить сохранения сразу после выполнения патча
- Отдельный пункт меню "Загрузить backup" для восстановления из любой ранее созданной резервной копии
- Возможность удаления папки резервной копии после восстановления
- Выбор папки с резервной копией через проводник Windows

## История изменений

### Версия 1.9
- Добавлена поддержка многоязычности (русский и английский языки)
- Автоматическое определение языка системы при первом запуске
- Добавлена возможность выбора языка интерфейса в настройках

### Версия 1.8.2
- Удалена функция сохранения последнего использованного значения
- Добавлено обязательное требование ввода значения при каждом использовании
- Оптимизирован интерфейс ввода значений

### Версия 1.8.1
- Исправлена работа с Inventory.json для корректного отображения и изменения наличных денег
- Улучшен интерфейс: добавлено подменю для выбора типа денег (наличные/счет)
- Переработана логика чтения и обновления файлов JSON
- Добавлена поддержка более сложной структуры сохранений

### Версия 1.8
- Добавлена возможность изменения наличных денег в инвентаре (Inventory.json)
- Улучшена работа с файлами сохранений, добавлена поддержка десятичных значений

### Версия 1.7
- Добавлена улучшенная обработка ввода с учетом разных раскладок клавиатуры
- Добавлена поддержка ввода да/нет независимо от текущей раскладки

### Версия 1.6
- Реорганизована структура программы на 3 файла для лучшей поддержки

### Версия 1.5
- Добавлен отдельный пункт меню "Загрузить backup"
- Улучшена система восстановления из резервных копий
- Добавлено удаление папки бэкапа после восстановления

### Версия 1.4
- Добавлен отдельный пункт меню "Настройки"
- Добавлена возможность включения/отключения анимаций

### Версия 1.3
- Добавлен выбор exe-файла игры через проводник Windows
- Удален автоматический режим поиска exe-файла

### Версия 1.2
- Добавлена опция просмотра текущего баланса без изменений
- Добавлена возможность автозапуска игры после патча
- Добавлена функция выбора и сохранения пути к exe-файлу игры

### Версия 1.1
- Добавлена возможность выбора пользовательской суммы денег
- Обновлен текст сообщений с учетом пользовательской суммы

### Версия 1.0
- Первоначальный релиз программы
- Реализована функция изменения денег на фиксированную сумму 10000
- Добавлено создание резервных копий сохранений
- Добавлена возможность восстановления из резервных копий

## Технические детали

- Программа использует базовый путь к сохранениям игры: `C:\Users\[пользователь]\AppData\LocalLow\TVGS\Schedule I\Saves\`
- Автоматически находит все ID пользователей в папке сохранений
- Обрабатывает все папки с префиксом SaveGame_
- В файле `Money.json` значение поля "OnlineBalance" изменяется на указанную пользователем сумму
- В файле `Inventory.json` значение поля "CashBalance" для наличных денег изменяется на указанное пользователем значение
- Настройки программы сохраняются в файле `money_patcher_config.ini` .
