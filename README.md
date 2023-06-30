# Notify bot
This is a Telegram bot that sends regular notifications to a chat. You can customize the notifications by editing the config.yaml file.

## Installation

To use this bot, please follow the instructions below:

1. Clone this repository to your local machine and go to the project folder:
```shell
git clone https://github.com/Ranwud/noty_bot.git
```

```shell
cd noty_bot
```

2. Make sure you have Python 3.x installed.
3. Install the required libraries by running the following command:

```shell
pip install -r requirements.txt
```

4. Create a new Telegram bot and obtain the bot token. You can create a new bot by talking to @BotFather on Telegram and following the instructions.
5. Open the config.yaml file and edit it according to your notification requirements. Please make sure to strictly adhere to the specified format and indentation.
6. To start the Telegram notification bot, run the following command in the terminal:

```shell
python main.py
```
or comand

```shell
python3 main.py
```

The bot will start reading the config.yaml file and sending notifications based on the specified configurations.

Make sure to keep the bot running in the background or on a server to ensure continuous notifications.

## Requirements

The required libraries for running this bot are listed in the `requirements.txt` file. You can install them using the following command:

```shell
pip install -r requirements.txt
```

Please note that it's recommended to create a virtual environment before installing the requirements to keep your Python environment clean.

Now you are ready to set up and use the Telegram notification bot. Customize the `config.yaml` file according to your notification needs, start the bot, and enjoy regular notifications in your specified Telegram chat!


## Description of config.yaml:

* bot_token - The token of the Telegram bot. You can create a new bot using @BotFather and obtain its token.
* period - The name of the notification. For example weekday, technical, special_important
* start_time - The time when the notifications should start. It should be specified in square brackets and quotes. You can specify multiple start times. Example: start_time: ['00:00:00', '17:00:00'].
* end_time - The time when the notifications should end. It should be specified in square brackets and quotes. You can specify multiple end times. Example: end_time: ['00:00:00', '17:00:00'].
* days_of_week - The days of the week when the notifications should be sent. Where 0 represents Monday and 6 represents Sunday. This field is similar to the 'period' field. It is not necessary to include this field if the 'period' is set to daily.
* interval - The interval in minutes after which the bot will send a new notification.
* chat_id - The ID of the Telegram chat where the bot should send the notifications. First, the bot needs to be added to this chat. If it's a private message, you need to go to the bot in Telegram and press the START button.
* text - The text that the bot should send.
