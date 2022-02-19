from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from time import sleep

app = Client("my_account", api_id=876100, api_hash="ab03c3758ababdad2d8859e08244ae40")


@app.on_message(filters.command("print", "!") & filters.me)
def type_style(_, message):
    text = message.text.split("!print ", maxsplit=1)[1]
    to_print = ""
    typing_symbol = '▒'
    while len(text) != 0:
        try:
            message.edit(to_print + typing_symbol)
            sleep(0.002)
            to_print += text[0]
            text = text[1:]
            message.edit(to_print)
            sleep(0.001)
        except FloodWait as e:
            sleep(e.x)


@app.on_message(filters.command("rusak", "!") & filters.me)
def rusak_battle(_, message):
    times = int(message.text[6:])
    chat_id = message.chat.id
    app.delete_messages(chat_id, message.message_id)
    for i in range(times):
        try:
            if i % 10 == 0:
                buy_heal(_, message)
            bot_results = app.get_inline_bot_results("Random_UAbot")
            app.send_inline_bot_result(chat_id, bot_results.query_id, bot_results.results[0].id)
            sleep(2)
        except FloodWait as e:
            sleep(e.x)


@app.on_message(filters.command("heal", "!"))
def buy_heal(_, message):
    chat_id = message.chat.id
    app.send_message(chat_id, "чекаю хп в боті")
    sent = app.send_message("Random_UAbot", "/rusak")
    sleep(2)
    health = int(app.get_messages("Random_UAbot", sent.message_id + 1).caption.split()[18])
    if health < 30:
        app.send_message(chat_id, "треба аптечку")
        sent = app.send_message("Random_UAbot", "/shop")
        sleep(2)
        bot_shop = app.get_messages("Random_UAbot", sent.message_id + 1)
        bot_shop.click(3)
        app.send_message(chat_id, "купив аптечку")
    else:
        app.send_message(chat_id, "норм, жити можна")


app.run()
