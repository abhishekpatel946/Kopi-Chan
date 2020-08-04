# Kopi-Chan

## Description

This is a Telegram Bot made for a coffee/tea enthusiasts group in NUS.

It serves a few functions:

1. Easy collection and tracking of orders for data analysis of demand and costs.
2. Provide our customer an automated guide to properly order from us.
3. Encourage donations by providing one-click donations link.

## Get started

Run `pip install -r requirements.txt` or

```
pip install python-telegram-bot --upgrade
pip install pyrebase
pip install pytz
```

individually to install the required packages.

Make sure in the root folder, there is a `credentials` folder (can be found in IG Drive) that contains the Firebase credentials as below:

```
Kopi-Chan
└───credentials
|   |   telegram_token.py
│   │   firebase_config.py
│   │   firebase_service_account_credentials.json
|...
```

## How to run Bot for local development

1. In `kopi_chan.py`, make sure the following lines are uncommented:

   ```python
   # Uncomment to start the Bot locally
   updater.start_polling()
   ```

2. Make sure the folliwng lines are commented as they are for hosting on Heroku:

   ```python
   # # Uncomment to tart the webhook for hosting bot on Heroku
   # updater.start_webhook(listen="0.0.0.0",
                         port=int(PORT),
                         url_path=TOKEN)
   # updater.bot.setWebhook(f"https://{APP_NAME}.herokuapp.com/{TOKEN}")
   ```

3. Go to Heroku's `kopi-chan` app page, Settings tab, Maintenance Mode, and turn on maintenance mode to take the online bot instance offline temporarily.

4. Simply run `python kopi_chan.py` to start the local bot instance.

## How to deploy Bot on Heroku

kopi-chan is deployed on Heroku using Heroku CLI.

1. In `kopi_chan.py`, make sure the following lines are uncommented:

   ```python
   # Uncomment to tart the webhook for hosting bot on Heroku
   updater.start_webhook(listen="0.0.0.0",
                         port=int(PORT),
                         url_path=TOKEN)
   updater.bot.setWebhook(f"https://{APP_NAME}.herokuapp.com/{TOKEN}")
   ```

2. Make sure the folliwng lines are commented as they are for local hosting:

   ```python
   # # Uncomment to start the Bot locally
   # updater.start_polling()
   ```

3. To deploy to Heroku, simply run `git push heroku master`.
