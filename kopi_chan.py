import logging
import pprint
import random
import time
import telegram
from datetime import datetime
from telegram import (KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
from sheets_log import (insert_order, insert_feedback)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

pp = pprint.PrettyPrinter()

BUTTON_MENU, MENU_BUTTON_CLICKED, ICE_BUTTON_CLICKED, SERVINGS_BUTTON_CLICKED, LOG_FEEDBACK = range(5)

token = "908143577:AAEjKlF05FauSivmwYeQ1Hv1HHZRlLaNHsw"

# menu_items = [
#         'Pour-over Coffee', 
#         'French Press Coffee',
#         'Cold-brew Coffee',
#         'Cold-brew Tea',
#         'Hot Tea',
#         'Thai Milk Tea', 
#         'Macha Latte',
#         'Brown Sugar Milk Tea'
#         ]

menu_items = [
        'Black Coffee',
        'Mocha',
        # 'Thai Milk Tea', 
        'Matcha Latte',
        'Brown Sugar Milk Tea',
        "Pu'er Tea"
        ]

suggested_donation = {
        'Pour-over Coffee': 1.70, 
        'Black Coffee': 1.00,
        'Mocha': 1.50,
        'Cold-brew Coffee': 1.50,
        'Cold-brew Tea': 0.90,
        'Hot Tea': 0.90,
        'Thai Milk Tea': 1.00, 
        'Matcha Latte': 1.90,
        'Brown Sugar Milk Tea': 1.80,
        "Pu'er Tea": 0.50
        }

# print(suggested_donation['Pour-over Coffee'])

def start(update, context):
    context.chat_data['chatid'] = update.effective_chat.id
    update.message.reply_text(
        'Hi! Kopi chan here! 😀\nReady to get caffeinated?\n\n'
        "Send /menu to see what's on the menu today!\n\n"
        'Send /order to TREAT YO SELF!\n\n'
        'Send /feedback to give us your valuable inputs!\n\n'
        'Send /cancel to stop talking to me 🥺\n')

    return ConversationHandler.END

def menu(update, context):
    context.chat_data['chatid'] = update.effective_chat.id
    str_menu = "\n".join(menu_items)

    context.bot.sendMessage(
        chat_id = context.chat_data['chatid'], 
        text = "*Today's Menu\n\n*" + str_menu,
        parse_mode = telegram.ParseMode.MARKDOWN)

    return ConversationHandler.END

def order(update, context):
    context.chat_data['chatid'] = update.effective_chat.id
    update.message.reply_text('I am ready to take your order! 😊\n\n')
    update.message.reply_text('What\'s your name?\n')

    return BUTTON_MENU

def button_menu(update, context):
    if update.message.text == '/cancel':
        cancel(update, context)
        return ConversationHandler.END
    elif update.message.text  == '/menu':
        menu(update, context)
        return ConversationHandler.END
    elif update.message.text  == '/order':
        order(update, context)
        return ConversationHandler.END
    else:
        context.user_data['user'] = update.message.from_user.username
        context.user_data['input_name'] = update.message.text  
            
        button_list = [[InlineKeyboardButton(s, callback_data=s)] for s in menu_items]
        reply_markup = InlineKeyboardMarkup(button_list)

        update.message.reply_text('Hi {NAME}!\n\nWhat would you like to have for today?\n'.format(NAME = context.user_data['input_name']),
            reply_markup=reply_markup)
        
        return MENU_BUTTON_CLICKED

def menu_button_clicked(update, context):
    praises = ['Nice choice! 😍', 'Good taste~', 'Lovely 😍', 'Sounds great 🤩']
    context.user_data['selected_order'] = update.callback_query.data
    update.callback_query.answer()
    update.callback_query.edit_message_text(text = "{ORDER}! {PRAISE}".format(
        ORDER = context.user_data['selected_order'], 
        PRAISE = praises[random.randint(0, len(praises)-1)]))
    customize_ice(update, context)
    return ICE_BUTTON_CLICKED

def customize_ice(update, context):

    cust_opts = [
        'Iced',
        'No ice'
    ]

    button_list = [[InlineKeyboardButton(s, callback_data=s)] for s in cust_opts]
    reply_markup = InlineKeyboardMarkup(button_list)

    context.bot.sendMessage(context.chat_data['chatid'], 'Do you want it iced?\n', reply_markup=reply_markup)  
    return ICE_BUTTON_CLICKED 

def ice_button_clicked(update, context):
    context.user_data['if_ice'] = update.callback_query.data
    update.callback_query.answer()
    update.callback_query.edit_message_text(text = "{}! Nice 👌".format(context.user_data['if_ice']))
    servings(update, context)
    return SERVINGS_BUTTON_CLICKED


# def custumize_sugar(update, context):

#     if (context.user_data['selected_order'] == 'Pour-over Coffee' or 
#         context.user_data['selected_order'] == 'Cold-brew Coffee' or
#         context.user_data['selected_order'] == 'Cold-brew Tea'):
        
#     else: 
#         cust_opts = [
#             '100% sugar',
#             'Less sugar',
#             'No sugar'
#         ]

#     button_list = [[InlineKeyboardButton(s, callback_data=s)] for s in cust_opts]
#     reply_markup = InlineKeyboardMarkup(button_list)

#     context.bot.sendMessage(context.chat_data['chatid'], 'Choose your sugar level!\n', reply_markup=reply_markup) 
#     return SERVINGS_BUTTON_CLICKED 

# def sugar_button_clicked(update, context):
#     context.user_data['sugar_level'] = update.callback_query.data
#     update.callback_query.answer()
#     update.callback_query.edit_message_text(text = "Your order details:\n\n{ORDER}\n{SUGAR}".format(
#         ORDER = context.user_data['selected_order'], 
#         SUGAR = context.user_data['sugar_level']))
#     servings(update, context)
#     return SERVINGS_BUTTON_CLICKED


def servings(update, context):
    servings_opts = [1, 2, 3]
        
    button_list = [[InlineKeyboardButton(i, callback_data=i)] for i in servings_opts]
    reply_markup = InlineKeyboardMarkup(button_list)

    context.bot.sendMessage(context.chat_data['chatid'], 'How many servings?\n', reply_markup=reply_markup)  
    return SERVINGS_BUTTON_CLICKED


def servings_button_clicked(update, context):
    context.user_data['servings'] = int(update.callback_query.data)
    update.callback_query.answer()

    complete_order(update, context)

    return ConversationHandler.END

def complete_order(update, context):
    # Show order summary
    update.callback_query.edit_message_text(
        text = "Let's see what we have here...\n\n*x{SERVINGS} {ORDER}, {ICE}, for {NAME}*!".format(
            SERVINGS = context.user_data['servings'] , 
            ORDER = context.user_data['selected_order'],
            ICE = context.user_data['if_ice'],
            NAME = context.user_data['input_name']),
        parse_mode = telegram.ParseMode.MARKDOWN)
    
    # Preparation instructions
    if (context.user_data['if_ice'] == 'Iced'):
        context.bot.sendMessage(
            chat_id=context.chat_data['chatid'], 
            text = 'Your order has been successfully submitted!\n\n✳*Please get a cup filled with ice from DH and proceed to one of our lovely baristas!*\n',
            parse_mode = telegram.ParseMode.MARKDOWN)
    elif (context.user_data['if_ice'] == 'No ice'):
        context.bot.sendMessage(
            chat_id = context.chat_data['chatid'], 
            text = 'Your order has been successfully submitted!\n\n✳*Please get an empty cup and proceed to one of our lovely baristas!*\n',
            parse_mode = telegram.ParseMode.MARKDOWN)

    time.sleep(1.5)

    # Recommend donations amount
    context.user_data['recommended_dontation'] = suggested_donation[context.user_data['selected_order']] * context.user_data['servings']

    context.bot.sendMessage(
        chat_id = context.chat_data['chatid'], 
        text = 'We accept PayLah donations at http://gg.gg/donateUSCaff\n\n*The recommended donation amount for your order is: ${0:.2f}* \n\nThis recommended donation amount will help us cover our costs!'.format(context.user_data['recommended_dontation']),
        parse_mode = telegram.ParseMode.MARKDOWN)

    context.bot.sendMessage(context.chat_data['chatid'],
        'Thank you and enjoy your {ORDER}! ❤ Hope to see you again {NAME}! '.format(ORDER = context.user_data['selected_order'], NAME = context.user_data['input_name']))
    
    # log order data to Google sheet
    log_order_data(context.user_data)

    return ConversationHandler.END


def log_order_data(context_data):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    name = context_data['input_name']
    username = context_data['user']
    order = context_data['selected_order']
    servings = context_data['servings']
    is_iced	= context_data['if_ice']
    donation = context_data['recommended_dontation']
    sugar_level = '-'
    pp.pprint(context_data)
    insert_order([date, name, username, order, servings, is_iced, sugar_level, donation])

    return

def feedback(update, context):
    context.chat_data['chatid'] = update.effective_chat.id
    update.message.reply_text('Please send me your feedback!\n\nIt could be on any area of improvment on your experience with USCaffeinated or any recommendation!')

    return LOG_FEEDBACK

def log_feedback(update, context):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    username = update.message.from_user.username
    feedback_text = update.message.text

    insert_feedback([date, username, feedback_text])

    update.message.reply_text('Thank you for your feedback! Your input means a lot to us!')
    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! Hope to see you again soon uwu~',
                              reply_markup=ReplyKeyboardRemove())\

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

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

        allow_reentry = True
    )


    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('menu', menu))
    dp.add_handler(CommandHandler('cancel', cancel))
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
