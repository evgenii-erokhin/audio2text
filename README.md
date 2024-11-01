# Telegram bot: audio2text 
# Описание
Этот бот предназначен для преобразования голосовых сообщений в текст. Он принимает голосовые сообщения пользователя, сохраняет их локально, конвертирует аудио из формата OGG в WAV, а затем транскрибирует его в текст, используя модель whisper.

# Технологии
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
<img src="https://img.shields.io/badge/Python_Telegram_Bot-blue?style=for-the-badge&logo=python telegram bot&logoColor=green"/>
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Whisper](https://img.shields.io/badge/Whisper-0A0A0A?style=for-the-badge&logo=openai&logoColor=white)

# Установка и настройка
1. **Клонируйте репозиторий:**
```commandline
git clomne git@github.com:evgenii-erokhin/audio2text.git
```
2. **Настройка окружения:** Создайте файл .env в корневом каталоге проекта и добавьте необходимые переменные окружения.
```commandline
TELEGRAM_TOKEN=your_telegram_bot_token_here
MODEL=the_whisper_model_you_want_to_use
```
3. **Запуск с помощью Docker Compose:** Убедитесь, что у вас запущен Docker, затем выполните:
```commandline
docker-compose up -d
```
# Использование:
1. **Начало работы:** Пользователь может взаимодействовать с ботом, используя команду /start. Бот ответит приветственным сообщением.
2. Отправка голосовых сообщений:
- **Для преобразования:**
  - Перешлите голосовое сообщение боту или добавьте бота в групповой чат, назначьте ему права `admin`и отправьте голосовое сообщение в груповой чат
  - Бот ответит, сообщив, что работает над конвертацией сообщения и вскоре вышлет результат.

# Контакты
**Евгений Ерохин**  

<a href="https://t.me/juandart" target="_blank">
<img src=https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white />
</a>
<a href="mailto:evgeniierokhin@proton.me?">
<img src=https://img.shields.io/badge/ProtonMail-8B89CC?style=for-the-badge&logo=protonmail&logoColor=white />
</a>
