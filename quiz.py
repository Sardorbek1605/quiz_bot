#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from connect import *

from telegram import __version__ as TG_VER, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import requests

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

KEYBOARD = [
        [
            KeyboardButton("Start Quiz", ),
        ],
    ]



# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    # print(update)
    # print(user)
    await update.message.reply_html(
        rf"Hi {user.first_name}!",
        reply_markup=ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True)
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # print(update)
    message = update.message.text
    if message == "Start Quiz":
        sql_select_Query = "select * from questions"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        # get all records
        records = cursor.fetchall()
        # print("Total number of rows in table: ", cursor.rowcount)
        # print(records)
        # print("\nPrinting each row\n")
        for row in records:
            print("id = ", row[0], )
            # print("question = ", row[1], )
            id = str(row[0])
            sql_query_for_options = f"select * from options where question_id={id}"
            # print(sql_query_for_options)
            cursor_option = connection.cursor()
            cursor_option.execute(sql_query_for_options)
            options = cursor_option.fetchall()
            await update.message.reply_html(
                rf"{row[1]}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(options[0][2], callback_data=options[0][0]),InlineKeyboardButton(options[1][2], callback_data=options[1][0])],
                    [InlineKeyboardButton(options[2][2], callback_data=options[2][0]),InlineKeyboardButton(options[3][2], callback_data=options[3][0])],
                ])
            )

        # await update.message.reply_html(
        #     rf"Question1",
        #     reply_markup=InlineKeyboardMarkup([
        #         [InlineKeyboardButton("Option 1", callback_data="1"), InlineKeyboardButton("Option 1", callback_data="1")],
        #         [InlineKeyboardButton("Option 1", callback_data="1"), InlineKeyboardButton("Option 1", callback_data="1")],
        #     ])
        # )
    else:
        await update.message.reply_text(update.message.text)

async def get_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # print(update)
    query = update.callback_query
    print(query.data)
    # await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5407487407:AAH0hYWGmvYb6rljo26rCq9SJoDoxqKAc3o").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(get_callback))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()