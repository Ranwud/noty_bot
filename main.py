import yaml
import telebot
import datetime
import time
import logging

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
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logger.error(f"Failed to load config.yaml. Error: {str(e)}")
        return None

# Перезагрузка параметров из файла config.yaml
def reload_config(config):
    new_config = load_config()
    if new_config:
        config.update(new_config)

# Отправка уведомления
def send_notification(bot, chat_id, text):
    try:
        bot.send_message(chat_id, text, parse_mode='HTML')
        logger.info(f"Sent notification to chat_id {chat_id}: {text}")
    except Exception as e:
        logger.error(f"Failed to send notification to chat_id {chat_id}: {text}. Error: {str(e)}")

# Проверка, должно ли быть отправлено уведомление в данный момент
def should_send_notification(notification):
    now = datetime.datetime.now()
    start_time = [datetime.datetime.strptime(t, '%H:%M:%S').time() for t in notification['start_time']]
    end_time = [datetime.datetime.strptime(t, '%H:%M:%S').time() for t in notification['end_time']]
    interval = notification['interval']
    period = notification['period']
    day_of_week = notification.get('day_of_week', None)
    days_of_week = notification.get('days_of_week', None)
    last_notification = notification.get('last_notification', None)

    if last_notification is not None:
        time_since_last_notification = (now - last_notification).total_seconds() / 60
        if time_since_last_notification < interval:
            return False

    if period == 'daily':
        for start, end in zip(start_time, end_time):
            if start <= now.time() <= end:
                return True
    elif period == 'weekday':
        if now.weekday() < 5:
            for start, end in zip(start_time, end_time):
                if start <= now.time() <= end:
                    return True
    elif period == 'weekend':
        if now.weekday() >= 5:
            for start, end in zip(start_time, end_time):
                if start <= now.time() <= end:
                    return True
    elif period in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        if now.weekday() == ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].index(period):
            for start, end in zip(start_time, end_time):
                if start <= now.time() <= end:
                    return True
    elif period == 'weekly' and day_of_week is not None:
        if now.weekday() == day_of_week:
            for start, end in zip(start_time, end_time):
                if start <= now.time() <= end:
                    return True
    elif period == 'weekday' and days_of_week is not None:
        if now.weekday() in days_of_week:
            for start, end in zip(start_time, end_time):
                if start <= now.time() <= end:
                    return True

    return False

# Обработка ошибок при отправке уведомления
def handle_send_notification_error(bot, chat_id, text, error):
    logger.error(f"Failed to send notification to chat_id {chat_id}: {text}. Error: {str(error)}")
    # Дополнительная логика обработки ошибки, например, отправка уведомления администратору

# Основная функция бота
def main():
    # Загрузка параметров из файла config.yaml
    config = load_config()

    if not config:
        logger.error("Failed to start the bot. Config not loaded.")
        return

    # Создание экземпляра бота
    bot = telebot.TeleBot(config['bot_token'])

    # Бесконечный цикл для проверки и отправки уведомлений
    while True:
        try:
            reload_config(config)  # Перезагрузка параметров из файла config.yaml
            for notification in config['notifications']:
                if should_send_notification(notification):
                    chat_id = notification['chat_id']
                    text = notification['text']
                    try:
                        send_notification(bot, chat_id, text)
                    except Exception as e:
                        handle_send_notification_error(bot, chat_id, text, e)
            time.sleep(60)  # Задержка в 1 минуту перед следующей проверкой
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
