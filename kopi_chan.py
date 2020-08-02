import os
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, ConversationHandler, CallbackQueryHandler)
from conversations import *
from credentials.telegram_token import TOKEN


# Heroku app name
APP_NAME = "kopi-chan"
# Port is given by Heroku
PORT = os.environ.get('PORT')


def main():
    # Create the Updater and pass it your bot's TOKEN.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('order', order),
            CommandHandler('feedback', feedback)
        ],

        states={
            BUTTON_MENU: [MessageHandler(Filters.all, button_menu)],
            MENU_BUTTON_CLICKED: [CallbackQueryHandler(menu_button_clicked)],
            ICE_BUTTON_CLICKED: [CallbackQueryHandler(ice_button_clicked)],
            SERVINGS_BUTTON_CLICKED: [CallbackQueryHandler(servings_button_clicked)],
            LOG_FEEDBACK: [MessageHandler(Filters.text, log_feedback)]
        },

        fallbacks=[CommandHandler('cancel', cancel)],

        allow_reentry=True
    )

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('menu', today_menu))
    dp.add_handler(CommandHandler('cancel', cancel))
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # # Uncomment to start the Bot locally
    # updater.start_polling()

    # Uncomment to tart the webhook for hosting bot on Heroku
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(f"https://{APP_NAME}.herokuapp.com/{TOKEN}")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
