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
    print(times)
    for i in range(times):
        try:
            bot_results = app.get_inline_bot_results("Random_UAbot")
            app.send_inline_bot_result(message.chat.id, bot_results.query_id, bot_results.results[0].id)
            sleep(0.5)
        except FloodWait as e:
            sleep(e.x)
    app.send_message(message.chat.id, "їбанутиси2")


app.run()
