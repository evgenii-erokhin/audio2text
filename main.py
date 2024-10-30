import logging
import os

import whisper
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
OGG_PATH = os.path.join(BASE_DIR, 'voice', 'oog', 'voice_note.ogg')
WAV_PATH = os.path.join(BASE_DIR, 'voice', 'wav', 'voice_note.wav')
MODEL = 'turbo'


def create_dirs() -> None:
    """
    Создает директории для хранения аудио сообщений.

    Перед началом транскрибирования аудио в текст создаются директории по пути:
    ./voice/oog; ./voice/wav для хранения  аудио файлов

    :return: None
    """
    os.makedirs(os.path.dirname(OGG_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(WAV_PATH), exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start, отправляющий приветственное сообщение пользователю.

    :param update: Объект Update, содержащий информацию о событии telegram, включая данные сообщения.
    :param context: Контекст выполнения, предоставляет доступ к bot и другим полезным свойствам.
    :return: None
    """
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text='Транскрибирую ваш войс в текст.'
    )


async def get_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает голосовые сообщения отправленные в чат, сохраняя их локально и транскрибируя в текст.

    Функция извлекает голосовое сообщение из объекта обновления Telegram, сохраняет его в локальной
    файловой системе и выполняет транскрипцию аудио на текст с помощью функции `audio_to_text`.
    Сообщает пользователю о начале процесса конвертации и затем отправляет результат транскрипции.
    В случае возникновения ошибок логирует их и отправляет уведомление о неудаче пользователю.

    :param update: Объект Update, содержащий информацию о событии telegram, включая данные сообщения.
    :param context: Контекст выполнения, предоставляет доступ к bot и другим полезным свойствам.
    :return: None

    :raises TelegramError: Обрабатывает исключения при работе с API Telegram.
    :raises: Exception: Обрабатывает любые другие возникшие исключения.

    """
    chat_id = update.effective_chat.id
    try:
        file = await context.bot.get_file(update.message.voice.file_id)
        await file.download_to_drive(custom_path=OGG_PATH)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f'Голосовое сообщение конвертируется. Пожалуйста, ожидайте, это может занять некоторое время...'
        )
        logging.info('voice message successfully sended')
        await context.bot.send_message(
            chat_id=chat_id,
            text=f'Голосовое сообщение: "{audio_to_text()}"'
        )
    except TelegramError as tg_err:
        logging.error(f'Telegram API error: {tg_err}')
        await context.bot.send_message(chat_id=chat_id, text=f'Произошла ошибка: {tg_err}')
    finally:
        cleanup_files(OGG_PATH, WAV_PATH)


def ogg_to_wav() -> str:
    """
    Конвертирует аудиофайл из формата OGG в WAV с монофоническим звуком.

    Читает аудиофайл формата OGG, преобразует его в монофонический WAV и возвращает путь к сохраненному файлу.
    Если возникают ошибки в процессе конвертации, они логируются, и исключение перенаправляется вверх по стеку вызовов.
    :return: Путь к сохраненному файлу в формате WAV.

    :raises: FileNotFoundError: Если исходный файл не найден.
    :raises: CouldntDecodeError: Если не удалось декодировать аудиофайл.
    :raises: OSError: Если возникают проблемы с чтением или записью файла.
    """
    try:
        audio = AudioSegment.from_ogg(OGG_PATH)
        audio = audio.set_channels(1)
        audio.export(WAV_PATH, format='wav', codec='pcm_s16le')
        logging.info('Successfully converted audio file from oog to wav.')
        return WAV_PATH
    except FileNotFoundError as fnf_err:
        logging.error(f'File in path {OGG_PATH} is not found: {fnf_err}')
        raise fnf_err
    except CouldntDecodeError as decode_err:
        logging.error(f'Could not decode OGG file {decode_err}')
        raise decode_err
    except OSError as os_err:
        logging.error(f'OS error during file conversion: {os_err}')
        raise os_err


def audio_to_text() -> str:
    """
    Транскрибирует аудиофайл в формате WAV в текст.

    Загружает модель Whisper, конвертирует аудио из OGG в WAV и транскрибирует его с использованием
    русской языковой модели. Возвращает распознанный текст.
    :return: Распознанный текст из аудиофайла.

    :raises: FileNotFoundError: Error если файл не найден.
    :raises: RuntimeError: Если возникли проблемы при конвертации.
    :raises: ValueError: Если переданы недопустимые аргументы или неправильные форматы данных.
    :raises: ImportError: Если модель или её зависимости загружены неправильно или отсутствуют.
    """
    try:
        model = whisper.load_model(MODEL)
        result = model.transcribe(ogg_to_wav(), language='ru', fp16=False)['text']
        logging.info(f'Successfully transcribed audio to text.')
        return result

    except FileNotFoundError as fnf_err:
        logging.error(f'Audio file not found: : {fnf_err}')
        raise fnf_err
    except RuntimeError as runtime_err:
        logging.error(f'Runtime error during Whisper processing: {runtime_err}')
        raise runtime_err
    except ValueError as value_err:
        logging.error(f'Value error during model invocation: {value_err}')
        raise value_err
    except ImportError as import_err:
        logging.error(f'Import error: {import_err}')
        raise import_err


def cleanup_files(*file_paths):
    """
    Удаляет указанные файлы по путям после конвертации в текст.

    :param file_paths:  Строки, представляющие пути до файлов, которые необходимо удалить.
    :return: None
    :raises OSError: Если возникает ошибка при удалении файлов.
    """
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
                logging.info(f'Successfully deleted file: {path}')
        except OSError as error:
            logging.error(f'Error while deleting file {path}: {error}')
            raise error


def main() -> None:
    logging.basicConfig(
        encoding='utf-8',
        level=logging.DEBUG,
        filename='./logs/main.log',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s - %(name)s'
    )

    create_dirs()

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    starting = CommandHandler('start', start)
    forwarded_voice = MessageHandler(filters.FORWARDED, get_voice_message)
    chat_voice = MessageHandler(filters.VOICE, get_voice_message)

    application.add_handler(starting)
    application.add_handler(forwarded_voice)
    application.add_handler(chat_voice)

    application.run_polling()


if __name__ == '__main__':
    main()
