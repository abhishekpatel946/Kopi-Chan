# Kopi-Chan

## Description

This is a Telegram Bot made for a coffee/tea enthusiasts group in NUS.

It serves a few functions:

1. Easy collection and tracking of orders for data analysis of demand and costs.
2. Provide our customer an automated guide to properly order from us.
3. Encourage donations by providing one-click donations link.

## Get Started

Run `pip install -r requirements.txt` or

```
pip install python-telegram-bot --upgrade
pip install pyrebase
pip install pytz
```

individually to install the required packages.

Make sure in the root folder, there is a `credentials` folder that contains the Firebase credentials as below:

```
Kopi-Chan
└───credentials
|   |   telegram_token.py
│   │   firebase_config.py
│   │   firebase_service_account_credentials.json
|...
```

## How to run Bot for local development

In `kopi_chan.py`, make sure the following lines are uncommented:

```python
# Uncomment to start the Bot locally
updater.start_polling()
```

Make sure the folliwng lines are commented as they are for hosting on Heroku:

```python
# # Uncomment to tart the webhook for hosting bot on Heroku
# updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=TOKEN)
# updater.bot.setWebhook(f"https://{APP_NAME}.herokuapp.com/{TOKEN}")
```

Go to Heroku's `kopi-chan` app page, Settings tab, Maintenance Mode, and turn on maintenance mode to take the online bot instance offline temporarily.

Simply run `python kopi_chan.py` to start the local bot instance.

## How to deploy Bot for to Heroku

kopi-chan is deployed on Heroku using Heroku CLI.

In `kopi_chan.py`, make sure the following lines are uncommented:

```python
# Uncomment to tart the webhook for hosting bot on Heroku
updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=TOKEN)
updater.bot.setWebhook(f"https://{APP_NAME}.herokuapp.com/{TOKEN}")
```

Make sure the folliwng lines are commented as they are for local hosting:

```python
# # Uncomment to start the Bot locally
# updater.start_polling()
```

To deploy to Heroku, simply run `git push heroku master`.
