from ruamel.yaml import YAML
import telebot
import datetime
import time
import logging
import shutil

# Создание экземпляра YAML
yaml = YAML()

# Инициализация логгера
logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Добавление обработчика для записи в файл
file_handler = logging.FileHandler('bot.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Добавление обработчика для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Загрузка параметров из файла config.yaml
def load_config():
    try:
        with open("config.yaml", "r") as file:
            config = yaml.load(file)
        return config
    except Exception as e:
        logger.error(f"Failed to load config.yaml. Error: {str(e)}")
        return None

# Сохранение параметров в файл config.yaml
def save_config(config):
    try:
        with open("config.yaml", "w") as file:
            yaml.dump(config, file)
    except Exception as e:
        logger.error(f"Failed to save config.yaml. Error: {str(e)}")

# Перезагрузка параметров из файла config.yaml
def reload_config(config, config_copy):
    new_config = load_config()
    if new_config is not None:
        last_notifications = {}
        for notification in config_copy['notifications']:
            key = (notification['chat_id'], notification['text'])
            last_notifications[key] = notification.get('last_notification', None)
        config_copy.clear()
        config_copy.update(new_config)
        for notification in config_copy['notifications']:
            key = (notification['chat_id'], notification['text'])
            if key in last_notifications:
                notification['last_notification'] = last_notifications[key]

# Создание копии файла config.yaml
def create_config_copy():
    shutil.copy2("config.yaml", "config_copy.yaml")

# Загрузка параметров из файла config_copy.yaml
def load_config_copy():
    try:
        with open("config_copy.yaml", "r") as file:
            config_copy = yaml.load(file)
        return config_copy
    except Exception as e:
        logger.error(f"Failed to load config_copy.yaml. Error: {str(e)}")
        return None

# Сохранение параметров в файл config_copy.yaml
def save_config_copy(config_copy):
    try:
        with open("config_copy.yaml", "w") as file:
            yaml.dump(config_copy, file)
    except Exception as e:
        logger.error(f"Failed to save config_copy.yaml. Error: {str(e)}")

# Отправка уведомления
def send_notification(bot, chat_id, text, config_copy):
    try:
        bot.send_message(chat_id, text, parse_mode='HTML')
        logger.info(f"Sent notification to chat_id {chat_id}: {text}")
        notification = next(
            (n for n in config_copy['notifications'] if n['chat_id'] == chat_id and n['text'] == text), None
        )
        if notification:
            notification['last_notification'] = datetime.datetime.now()
            save_config_copy(config_copy)  # Обновление параметров в файле config_copy.yaml
    except Exception as e:
        logger.error(f"Failed to send notification to chat_id {chat_id}: {text}. Error: {str(e)}")

# Проверка, нужно ли отправлять уведомление
def should_send_notification(notification):
    now = datetime.datetime.now()
    start_time = [datetime.datetime.strptime(t, '%H:%M:%S').time() for t in notification['start_time']]
    end_time = [datetime.datetime.strptime(t, '%H:%M:%S').time() for t in notification['end_time']]
    interval = notification['interval']
    days_of_week = notification.get('days_of_week', None)
    last_notification = notification.get('last_notification', None)

    if last_notification is not None:
        time_since_last_notification = (now - last_notification).total_seconds() / 60
        if time_since_last_notification < interval:
            return False

    if days_of_week is not None:
        if now.weekday() in days_of_week:
            for start, end in zip(start_time, end_time):
                if start <= now.time() <= end:
                    return True

    return False

# Основная функция бота
def main():
    # Создание копии файла config.yaml
    create_config_copy()

    # Загрузка параметров из файла config_copy.yaml
    config_copy = load_config_copy()

    if not config_copy:
        logger.error("Failed to start the bot. Config copy not loaded.")
        return

    # Создание экземпляра бота
    bot = telebot.TeleBot(config_copy['bot_token'])

    config = load_config()

    # Бесконечный цикл для проверки и отправки уведомлений
    while True:
        try:
            # Перезагрузка параметров из файла config.yaml при каждой итерации
            config = load_config()
            reload_config(config, config_copy)  # Обновление config_copy

            for notification in config_copy['notifications']:
                if should_send_notification(notification):
                    chat_id = notification['chat_id']
                    text = notification['text']
                    send_notification(bot, chat_id, text, config_copy)  # Вызов функции send_notification после создания бота

            time.sleep(60)  # Задержка в 1 минуту перед следующей проверкой
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
