import os
import sqlite3
from datetime import datetime, timedelta

import telebot

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
memes_chat_id = int(os.getenv("MEMES_CHAT_ID"))
flood_thread_id = int(os.getenv("FLOOD_THREAD_ID", 1))
memes_thread_id = int(os.getenv("MEMES_THREAD_ID", 1))

conn = sqlite3.connect("memes.db", check_same_thread=False)


def main():
    seven_days_ago = datetime.now() - timedelta(days=7)
    query = "SELECT user_id, MAX(username), SUM(old_hat_votes) FROM memes_posts WHERE created_at > ? GROUP BY user_id ORDER BY SUM(old_hat_votes) DESC LIMIT 1"
    row = conn.execute(query, (seven_days_ago,)).fetchone()
    user_id, username, old_hat_votes = row
    msg = (
        "Звание главное баяниста этой недели получает "
        + "["
        + username
        + "](tg://user?id="
        + str(user_id)
        + ") - 🪗 {}".format(old_hat_votes)
        + "\nГоните его насмехайтесь над ним"
    )
    bot.send_message(
        memes_chat_id,
        msg,
        message_thread_id=flood_thread_id,
        parse_mode="Markdown",
    )


if __name__ == "__main__":
    main()
