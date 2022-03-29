import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from time import sleep

app = Client("my_account", api_id=876100, api_hash="ab03c3758ababdad2d8859e08244ae40")  # сюда встав коди
nickname = "deadnfixed"
drop = ["пил і гнилі недоїдки", "класове спорядження", "дрин і щит", "пошкоджений уламок бронетехніки",
        "50 гривень", "ящиком горілки", "мертвий русак", "Мухомор королівський", "упаковок фольги",
        "Крім гаманця", "ручний протитанковий", "неушкоджений Бронежилет", "парадна форма"]

drop_texts = ["⚪ Пил і гнилі недоїдки", "⚪ Класове спорядження", "⚪ Дрин і щит", "⚪ Уламок", "🔵 50 гривень",
              "🔵 Ящик горілки", "🔵 Мертвий русак", "🟣 Мухомор королівський", "🟣 Шапочка", "🟣 Їжа", "🟡 РПГ-7",
              "🟡 Бронік Вагнерівця", "🟡 Погон"]


@app.on_message(filters.command("rusak", "!") & filters.me)
def rusak_battle(_, message):
    times = int(message.text[6:])
    chat_id = message.chat.id
    app.delete_messages(chat_id, message.message_id)
    if times > 30:
        app.send_message(chat_id, "Задохуя, ставлю 30")
        times = 30
    fight(_, message, times, chat_id)


@app.on_message(filters.command("huyak", "!"))
def rusak_battle(_, message):
    splited = message.text.split(" ")
    times = int(splited[2])
    target = splited[1]
    chat_id = -786803186
    app.delete_messages(chat_id, message.message_id)
    if target != nickname:
        return
    if times > 30:
        app.send_message(chat_id, "Задохуя, ставлю 30")
        times = 30
    elif times < 1:
        app.send_message(chat_id, "Дурачок? Ну вот нашо таке робити...")
        times = 1
    fight(_, message, times, chat_id)


@app.on_message(filters.command("heal", "!"))
def buy_heal(_, message):
    chat_id = message.chat.id
    app.send_message(chat_id, "чекаю хп в боті")
    sent = app.send_message("Random_UAbot", "/rusak")
    sleep(3)
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


@app.on_message(filters.command("click", "!") & filters.me)
def click_buttons(_, message):
    times = int(message.text[6:])
    start_message_id = message.reply_to_message.message_id
    chat_id = message.chat.id
    app.delete_messages(chat_id, message.message_id)
    if times > 40:
        app.send_message(chat_id, "задофіга, ставлю 30")
        times = 40
    elif times < 1:
        app.send_message(chat_id, "дурачок? буде 1")
        times = 1
    buy_heal(_, message)
    click(_, message, start_message_id, times, chat_id)


@app.on_message(filters.command("info", "!"))
def info(_, message):
    app.send_message(message.chat.id, message.reply_to_message)


@app.on_message(filters.command("ebash", "!"))
def ebash(_, message):
    chat_id = message.chat.id
    if chat_id != -751052700:
        return
    splited = message.text.split(" ")
    times = 30
    target = splited[1]
    if target != nickname:
        return
    buy_heal(_, message)
    fight(_, message, times, chat_id)
    text = f"!cluck {message.from_user.username}"
    sent = app.send_message(chat_id, "получаю ід повідомлення")
    app.send_message(chat_id, text, reply_to_message_id=app.get_messages(chat_id, sent.message_id - 2).message_id)


@app.on_message(filters.command("cluck", "!"))
def force_click(_, message):
    chat_id = message.chat.id
    if chat_id != -751052700:
        return
    splited = message.text.split(" ")
    times = 30
    target = splited[1]
    if target != nickname:
        return
    start_message_id = message.reply_to_message.message_id
    buy_heal(_, message)
    click(_, message, start_message_id, times, chat_id)
    app.send_message(chat_id, "наклікався")
    sleep(5)
    buy_heal(_, message)
    fight(_, message, times, chat_id)
    text = f"!cluck {message.from_user.username}"
    sent = app.send_message(chat_id, "получаю ід повідомлення")
    sleep(5)
    app.send_message(chat_id, text, reply_to_message_id=app.get_messages(chat_id, sent.message_id-2).message_id)


@app.on_message(filters.command("packs", "!"))
def analyze(_, message):
    chat_id = message.chat.id
    if chat_id != 1466731329:
        app.send_message(chat_id, "всі дивіться, я дебіл")
        return
    splited = message.text.split(" ")
    sent = app.send_message("Random_UAbot", "/shop")
    sleep(1)
    money = int(app.get_messages("Random_UAbot", sent.message_id + 1).text.split()[2])
    to_spend = int(splited[1])
    commands = int(splited[2])
    if to_spend > money * 0.95:
        app.send_message(chat_id, "далбайоб")
        return
    times = int((to_spend/20)/commands)
    if times == 0:
        app.send_message(chat_id, "далбайоб")
        return
    app.send_message(chat_id, f"Буде відкрито {int(to_spend/20)} пак-s, "
                              f"тобто при наведеній кількості команд pack, буде виконано {times} ітерацій")
    sleep(5)

    messages_to_forward = []
    start = 511585
    matches = []
    for i in range(len(drop)):
        matches.append(0)
    for i in range(commands):
        messages_to_forward.append(start)
        start -= 1

    for i in range(times):
        app.forward_messages(chat_id, -786803186, messages_to_forward)
        sleep(10)
        sent = app.send_message(chat_id, "получаю ід повідомлення")
        click(_, message, sent.message_id - 1, commands, chat_id)
        for j in range(sent.message_id - commands, sent.message_id + 1):
            msg = app.get_messages(chat_id, j)
            for k in range(len(drop)):
                if drop[k] in msg.text:
                    matches[k] = matches[k] + 1

    stats = f"Статистика по відкриттю {int(to_spend/20)} паків\n"
    for i in range(len(drop)):
        stats += f"{drop_texts[i]} - {matches[i]}\n"
    app.send_message(chat_id, stats)


def fight(_, message, times, chat_id):
    for i in range(times):
        try:
            if i % 30 == 0:
                buy_heal(_, message)
            bot_results = app.get_inline_bot_results("Random_UAbot")
            app.send_inline_bot_result(chat_id, bot_results.query_id, bot_results.results[0].id)
            sleep(1)
        except FloodWait as e:
            sleep(e.x)
    app.send_message(chat_id, "кінчив")


def click(_, message, start_message_id, times, chat_id):
    for i in range(start_message_id - times, start_message_id + 1):
        message_to_click = app.get_messages(chat_id, i)
        try:
            message_to_click.click(0, timeout=1)
        except TimeoutError as e:   # skip timeout
            pass
        except ValueError as e:     # skip non-battle messages
            pass


app.run()
