import os

import telebot
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
OR_TOKEN = os.getenv("OR_TOKEN")

bot = telebot.TeleBot(TG_TOKEN)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OR_TOKEN,
)

PERSONALITIES = {
    "scientist": {
        "name": "🔬 Scientist",
        "prompt": "You're an eccentric physics professor. Explain everything through crazy metaphors and scientific facts. Like to say, 'But in the quantum world...'",
    },
    "grumpy_grandpa": {
        "name": "👴 Grumpy Grandpa",
        "prompt": "You're an old man who thinks that everything was better in his time. Criticize everything. Say, 'In our time...', 'Young people are so...', 'We didn't have computers!'",
    },
    "cyberpunk": {
        "name": "🖤 Cyberpunk",
        "prompt": "You're a hacker from 2077. Speak darkly, with jargon: 'grid', 'blood code', 'hacked reality'. Everything is through the prism of technology and the fight against the system.",
    },
    "poet": {
        "name": "✒️ Poet",
        "prompt": "You are a romantic poet of the 19th century. Answer with 4-line poems. The theme is meaningful. Use images: moon, heart, fog, love, fate.",
    },
    "genie": {
        "name": "🧞‍♂️ Genie",
        "prompt": "You are an ancient genie from a lamp. Speak sublimely, with irony. Each answer is like a curse or a blessing. Call the user 'mortal'.",
    },
    "survivalist": {
        "name": "🪓 Survivalist",
        "prompt": "You're an apocalypse veteran. Explain everything as survival: 'If this happened in 2045...' Even study tips are 'shelter assembly instructions'.",
    },
}


user_mode = {}
# user_mode = {'217312873': 'survivalist'}


@bot.message_handler(commands=["start", "hello"])
def start(message):
    welcome_text = (
        "🌌 Welcome to MindForge\n\n"
        "Choose who I'll be today — and let's start the conversation:\n\n"
        "🔹 Scientist — will explain everything through quanta and black holes\n"
        "🔹 Grumbling Grandpa* — will say that it was better in his time\n"
        "🔹 Cyberpunk — will hack your problem from the future\n"
        "🔹 Poet — will answer with poems from the heart\n"
        "🔹 Genie — will grant a wish... with a catch\n"
        "🔹 Survivalist — will survive even your exam\n\n"
        "👉 Just click one of the buttons below:"
    )

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btns = []
    for i in PERSONALITIES:
        btns.append(telebot.types.KeyboardButton(PERSONALITIES[i]["name"]))
    keyboard.add(*btns)
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    chat_id = message.chat.id
    text = message.text

    person_key = None
    for key, data in PERSONALITIES.items():
        if text == data["name"]:
            person_key = key
            break

    if person_key:
        user_mode[chat_id] = person_key
        char = PERSONALITIES[person_key]["name"]
        bot.send_message(
            chat_id,
            f"Excellent! You chose a character: {char}, now, you can ask your question:",
        )
        return

    if chat_id not in user_mode:
        bot.send_message(chat_id, "First, choose a personality - press /start")
        return

    person_key = user_mode[chat_id]
    sys_prompt = PERSONALITIES[person_key]["prompt"]
    bot.send_message(chat_id, "*🧠 Bot is thinking hard, wait...*")

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": text},
            ],
        )
        answer = response.choices[0].message.content
        answer = (
            answer[:4000] + "\n\n(The answer is cut off...)"
            if len(answer) > 4000
            else answer
        )
        bot.send_message(chat_id, f"Your answer: {answer}")

    except Exception as e:
        bot.send_message(chat_id, "An error occurred 😥")
        print(f"ERORR - {e}")


bot.polling()


# ДЗ

# * ДЛЯ АМАНТАЯ
# Стилизовать карточку из прошлой домашней работы. Стили должны быть на основе дизайна


# * ДЛЯ ДАСТАНА
# Написать telegram bot с использованием ai.
# 1) Отследить все сообщения, если пользователь пишет о проблема ai должен отправить номер телефона "+99999999"
# 2) Если обычный вопрос, тогда просто отвечать


# * ДЛЯ АЛИХАНА
# Написать telegram bot с использованием ai.
# 1) Отследить все сообщения, если пользователь пишет о проблема ai должен отправить номер телефона "+99999999"
# 2) Если обычный вопрос, тогда просто отвечать


# * ДЛЯ НУРАКА
# Имя: Алексей
# Возраст: 27 лет
# Пол: Мужской
# Есть машина: Да
# Любимая еда: гречка с курицей, рамен из магазина, чёрный кофе без сахара
# График: Подъём: 7:30, Завтрак: 7:50, Работа: 8:30
# ? Для всех приведенных выше данных, выбрать правильные название переменных
# ? и подходящий тип данных
