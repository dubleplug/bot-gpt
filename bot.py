import asyncio
import os
import random
from datetime import datetime

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

# =============== НАСТРОЙКИ ===============
BOT_TOKEN = "8231589001:AAERhTujrOaUp8KraFkG1A6NB3COgqaw0cI"

# Папка с фотографиями товаров
PHOTOS_DIR = "photos"

# Реквизиты для оплаты
PAYMENT_DETAILS = {
    "₿ Bitcoin": "bc1qx0uumahy0ztyenqh0wtwyunkw96n5jwu7symt6",
    "💵 USDT": "TA4PzsvPCVGW8obsSZ97Fot2YZFZp2b45F",
    "💳 Перевод на карту": "2204320309969592 ОЗОН БАНК (Ангелина П.)",
}

# Приветствие
WELCOME_TEXT = (
    "🏪 <b>HOOD 2 HOOD STORE</b> Приветствует Вас\n\n"
    "+10000 сделок, доверенный магазин\n"
    "Самое низкое число не находов среди магазинов телеграмм.\n"
    "Мы тщательно следим за работой каждого сотрудника, чтобы у вас оставались только положительные эмоции.\n"
    "Качество товара проверяется постоянно.\n"
    "Мы проводим обучение курьеров, чтобы у вас не возникало проблем с прохождением квеста.\n"
    "Проводим много акций, делаем скидки.\n"
    "Оператор всегда идет на встречу, мы всегда ответим и поможем вам, если возникли проблемы.\n"
    "Мы работаем около трёх лет и мы знаем своё дело.\n\n"
    "👅 Приятных покупок в H2H 👅"
)

# Список товаров
PRODUCTS = {
    "Саратов": [
        {"name": "🍫Гашиш Изолятор🍫 1г", "price": 3000, "desc": "Имеет яркий запах. Эффект  наступает уже в первые минуты. Легкий HIGH сменяется  глубоким STONE. Снимает стресс после марафонов,  способствует крепкому сну. Накур плавный и глубокий.  Еда, прогулки, музыка, мысли о великом - он подходит  для чего угодно!, 1 грамм", "photo": "saratov_1.jpg"},
        {"name": "🍫Гашиш Изолятор🍫 2г", "price": 5800, "desc": "Имеет яркий запах. Эффект  наступает уже в первые минуты. Легкий HIGH сменяется  глубоким STONE. Снимает стресс после марафонов,  способствует крепкому сну. Накур плавный и глубокий.  Еда, прогулки, музыка, мысли о великом - он подходит  для чего угодно!, 2 грамма", "photo": "saratov_1.jpg"},
        {"name": "🍫Гашиш Изолятор🍫 4г", "price": 10000, "desc": "Имеет яркий запах. Эффект  наступает уже в первые минуты. Легкий HIGH сменяется  глубоким STONE. Снимает стресс после марафонов,  способствует крепкому сну. Накур плавный и глубокий.  Еда, прогулки, музыка, мысли о великом - он подходит  для чего угодно!, 4 грамм", "photo": "saratov_1.jpg"},
        {"name": "🌿Шишки Брюс беннер🌿 1г", "price": 2000, "desc": "Этот сорт известен всем из-за своего убойного и продолжительного эффекта, иногда может затянуться на более трёх часов.Сильная генетика этого вида — сочетание таких сортов как Haze и Northern Lights. Внешний вид сорта Amnesia больше похож на Indica, но преобладает в нем Sativa., 1 грамм", "photo": "saratov_2.jpg"},
        {"name": "🌿Шишки Брюс беннер🌿 2г", "price": 3800, "desc": "Этот сорт известен всем из-за своего убойного и продолжительного эффекта, иногда может затянуться на более трёх часов.Сильная генетика этого вида — сочетание таких сортов как Haze и Northern Lights. Внешний вид сорта Amnesia больше похож на Indica, но преобладает в нем Sativa., 2 грамма", "photo": "saratov_2.jpg"},
        {"name": "🌿Шишки Брюс беннер🌿 5г", "price": 9000, "desc": "Этот сорт известен всем из-за своего убойного и продолжительного эффекта, иногда может затянуться на более трёх часов.Сильная генетика этого вида — сочетание таких сортов как Haze и Northern Lights. Внешний вид сорта Amnesia больше похож на Indica, но преобладает в нем Sativa., 5 грамм", "photo": "saratov_2.jpg"},
        {"name": "🫐Шишка Блюбери🫐 2г", "price": 3800, "desc": "Этот сорт поразит вас в самое сердце. Гибрид сативы и индики 20/80, ТГК 19%. Благодаря обилию смолы, шишки каменные. Пахнет лесными ягодами и свежескошенной травой. Вкус сладкий, ягодный, горло не дерёт., 2 грамма", "photo": "saratov_3.jpg"},
        {"name": "🫐Шишка Блюбери🫐 5г", "price": 9000, "desc": "Этот сорт поразит вас в самое сердце. Гибрид сативы и индики 20/80, ТГК 19%. Благодаря обилию смолы, шишки каменные. Пахнет лесными ягодами и свежескошенной травой. Вкус сладкий, ягодный, горло не дерёт., 5 грамм", "photo": "saratov_3.jpg"},
        {"name": "✨ МЕФ crystal VHQ 99%✨ 1г", "price": 3500, "desc": "МЕФЕДРОН Эффекты: • Заряд энергии и прилив жизненных сил • Эйфория, эмоциональный подъём • Желание много двигаться, общаться и делиться самым сокровенным • Появляется чувство безмятежности и все проблемы уходят на второй план • Сексуальная возбужденность • Открытость по отношению к окружающим людям Характеристики • Цвет – белоснежный • Структура – кристаллическая • Кристаллы попадаются как крупные, так и более мелкие • Эффект удерживается в среднем 2 часа, 1 грамм", "photo": "saratov_4.jpg"},
        {"name": "✨ МЕФ crystal VHQ 99%✨ 2г", "price": 6900, "desc": "МЕФЕДРОН Эффекты: • Заряд энергии и прилив жизненных сил • Эйфория, эмоциональный подъём • Желание много двигаться, общаться и делиться самым сокровенным • Появляется чувство безмятежности и все проблемы уходят на второй план • Сексуальная возбужденность • Открытость по отношению к окружающим людям Характеристики • Цвет – белоснежный • Структура – кристаллическая • Кристаллы попадаются как крупные, так и более мелкие • Эффект удерживается в среднем 2 часа, 1 грамм", "photo": "saratov_4.jpg"},
        {"name": "✨ МЕФ crystal VHQ 99%✨ 4г", "price": 13000, "desc": "МЕФЕДРОН Эффекты: • Заряд энергии и прилив жизненных сил • Эйфория, эмоциональный подъём • Желание много двигаться, общаться и делиться самым сокровенным • Появляется чувство безмятежности и все проблемы уходят на второй план • Сексуальная возбужденность • Открытость по отношению к окружающим людям Характеристики • Цвет – белоснежный • Структура – кристаллическая • Кристаллы попадаются как крупные, так и более мелкие • Эффект удерживается в среднем 2 часа, 1 грамм", "photo": "saratov_4.jpg"},
        {"name": "💍 A-PVP Белый кристалл 💍 0.5г", "price": 2750, "desc": "Для эскиза нашей альфы мы взяли за основу палитру глубины и высокий градус эмоций - от эстетики до мурашек. Работая с материалами премиум-класса, нам удалось получить кристаллы рекордных размеров, наделенные только чистым кайфом художественной магии.", "photo": "saratov_5.jpg"},
        {"name": "💍 A-PVP Белый кристалл 💍 1г", "price": 4000, "desc": "Для эскиза нашей альфы мы взяли за основу палитру глубины и высокий градус эмоций - от эстетики до мурашек. Работая с материалами премиум-класса, нам удалось получить кристаллы рекордных размеров, наделенные только чистым кайфом художественной магии.", "photo": "saratov_5.jpg"},
        {"name": "💍 A-PVP Белый кристалл 💍 2г", "price": 7000, "desc": "Для эскиза нашей альфы мы взяли за основу палитру глубины и высокий градус эмоций - от эстетики до мурашек. Работая с материалами премиум-класса, нам удалось получить кристаллы рекордных размеров, наделенные только чистым кайфом художественной магии.", "photo": "saratov_5.jpg"},
        {"name": "💍 Героин Свежий привоз 💍 0.3г", "price": 2750, "desc": "чистый героин., 0.3г", "photo": "saratov_6.jpg"},
        {"name": "💍 Героин Свежий привоз 💍 0.5г", "price": 4000, "desc": "чистый героин., 0.5г", "photo": "saratov_6.jpg"},
    ],
    "Армавир": [
        {"name": "🍫Гашиш Изолятор🍫 1г", "price": 3000, "desc": "Имеет яркий запах. Эффект  наступает уже в первые минуты. Легкий HIGH сменяется  глубоким STONE. Снимает стресс после марафонов,  способствует крепкому сну. Накур плавный и глубокий.  Еда, прогулки, музыка, мысли о великом - он подходит  для чего угодно!, 1 грамм", "photo": "saratov_1.jpg"},
        {"name": "🍫Гашиш Изолятор🍫 2г", "price": 5800, "desc": "Имеет яркий запах. Эффект  наступает уже в первые минуты. Легкий HIGH сменяется  глубоким STONE. Снимает стресс после марафонов,  способствует крепкому сну. Накур плавный и глубокий.  Еда, прогулки, музыка, мысли о великом - он подходит  для чего угодно!, 2 грамма", "photo": "saratov_1.jpg"},
        {"name": "🍫Гашиш Изолятор🍫 5г", "price": 12000, "desc": "Имеет яркий запах. Эффект  наступает уже в первые минуты. Легкий HIGH сменяется  глубоким STONE. Снимает стресс после марафонов,  способствует крепкому сну. Накур плавный и глубокий.  Еда, прогулки, музыка, мысли о великом - он подходит  для чего угодно!, 4 грамм", "photo": "saratov_1.jpg"},
        {"name": "🌿Шишки Брюс беннер🌿 1г", "price": 2000, "desc": "Этот сорт известен всем из-за своего убойного и продолжительного эффекта, иногда может затянуться на более трёх часов.Сильная генетика этого вида — сочетание таких сортов как Haze и Northern Lights. Внешний вид сорта Amnesia больше похож на Indica, но преобладает в нем Sativa., 1 грамм", "photo": "saratov_2.jpg"},
        {"name": "🌿Шишки Брюс беннер🌿 2г", "price": 3800, "desc": "Этот сорт известен всем из-за своего убойного и продолжительного эффекта, иногда может затянуться на более трёх часов.Сильная генетика этого вида — сочетание таких сортов как Haze и Northern Lights. Внешний вид сорта Amnesia больше похож на Indica, но преобладает в нем Sativa., 2 грамма", "photo": "saratov_2.jpg"},
        {"name": "🌿Шишки Брюс беннер🌿 0.5г", "price": 1100, "desc": "Этот сорт известен всем из-за своего убойного и продолжительного эффекта, иногда может затянуться на более трёх часов.Сильная генетика этого вида — сочетание таких сортов как Haze и Northern Lights. Внешний вид сорта Amnesia больше похож на Indica, но преобладает в нем Sativa., 5 грамм", "photo": "saratov_2.jpg"},
        {"name": "🫐Шишка Блюбери🫐 2г", "price": 3800, "desc": "Этот сорт поразит вас в самое сердце. Гибрид сативы и индики 20/80, ТГК 19%. Благодаря обилию смолы, шишки каменные. Пахнет лесными ягодами и свежескошенной травой. Вкус сладкий, ягодный, горло не дерёт., 2 грамма", "photo": "saratov_3.jpg"},
        {"name": "🫐Шишка Блюбери🫐 1г", "price": 2000, "desc": "Этот сорт поразит вас в самое сердце. Гибрид сативы и индики 20/80, ТГК 19%. Благодаря обилию смолы, шишки каменные. Пахнет лесными ягодами и свежескошенной травой. Вкус сладкий, ягодный, горло не дерёт., 5 грамм", "photo": "saratov_3.jpg"},
    ],
}

# Районы теперь зависят от товара (2–5 наименований на товар)
DISTRICTS = {
    "Саратов": {
        "🍫Гашиш Изолятор🍫 1г": ["Центр", "Кировский", "Фрунзенский"],
        "🍫Гашиш Изолятор🍫 2г": ["Октябрьский"],
        "🍫Гашиш Изолятор🍫 4г": ["Центр", "Октябрьский", "Ленинский", "Фрунзенский"],
        "🌿Шишки Брюс беннер🌿 1г": ["Кировский", "Центр"],
        "🌿Шишки Брюс беннер🌿 2г": ["Ленинский", "Кировский", "Центр"],
        "🌿Шишки Брюс беннер🌿 5г": ["Фрунзенский", "Октябрьский"],
        "🫐Шишка Блюбери🫐 2г": ["Центр", "Ленинский", "Кировский", "Фрунзенский"],
        "🫐Шишка Блюбери🫐 5г": ["Кировский", "Ленинский"],
        "✨ МЕФ crystal VHQ 99%✨ 1г": ["Центр", "Фрунзенский", "Октябрьский", "Ленинский"],
        "✨ МЕФ crystal VHQ 99%✨ 2г": ["Кировский", "Центр"],
        "✨ МЕФ crystal VHQ 99%✨ 4г": ["Фрунзенский", "Ленинский", "Центр"],
        "💍 A-PVP Белый кристалл 💍 0.5г": ["Октябрьский", "Кировский", "Центр", "Фрунзенский"],
        "💍 A-PVP Белый кристалл 💍 1г": ["Ленинский", "Октябрьский"],
        "💍 A-PVP Белый кристалл 💍 4г": ["Центр", "Кировский", "Фрунзенский", "Ленинский", "Октябрьский"],
        "💍 Героин Свежий привоз 💍 0.3г": ["Фрунзенский", "Центр"],
        "💍 Героин Свежий привоз 💍 0.5г": ["Фрунзенский", "Центр"],
    },
    "Армавир": {
        "🍫Гашиш Изолятор🍫 1г": ["Центр", "Северный"],
        "🍫Гашиш Изолятор🍫 2г": ["Южный", "Центр", "Северный"],
        "🍫Гашиш Изолятор🍫 5г": ["Северный", "Южный"],
        "🌿Шишки Брюс беннер🌿 1г": ["Центр", "Южный", "Северный"],
        "🌿Шишки Брюс беннер🌿 2г": ["Южный", "Центр"],
        "🌿Шишки Брюс беннер🌿 0.5г": ["Северный", "Центр", "Южный",],  # можно удалить "Северный-2", если нет такого района
        "🫐Шишка Блюбери🫐 2г": ["Центр", "Северный"],
        "🫐Шишка Блюбери🫐 1г": ["Северный", "Центр", "Южный",],         
    },
}

# Если где-то промахнулись с районом, можно убрать «Северный-2» и т.п.
for city, mapping in DISTRICTS.items():
    for prod_name in list(mapping.keys()):
        # Чистим дубликаты и странные названия (пример)
        cleaned = [d for d in mapping[prod_name] if d in {"Центр", "Кировский", "Фрунзенский", "Октябрьский", "Ленинский", "Северный", "Южный"}]
        if cleaned:
            mapping[prod_name] = list(dict.fromkeys(cleaned))[:5]  # максимум 5 районов
        else:
            # Фолбэк на случай опечаток — дадим по городу дефолт
            default_by_city = {
                "Саратов": ["Центр", "Кировский", "Фрунзенский", "Октябрьский", "Ленинский"],
                "Армавир": ["Центр", "Северный", "Южный"],
            }
            mapping[prod_name] = default_by_city.get(city, [])[:3]

# Способы оплаты
PAYMENTS = ["₿ Bitcoin", "💵 USDT", "💳 Перевод на карту"]

ORDERS_FILE = "orders.txt"
# ========================================

# Память по пользователям
# Сохраняем:
#   city, product, district, payment
user_state: dict[int, dict] = {}

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ===== ВСПОМОГАТЕЛЬНЫЕ КЛАВИАТУРЫ =====
def kb_main_menu() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🛒 Купить", callback_data="menu:buy")
    kb.button(text="💼 Работа", callback_data="menu:job")
    kb.button(text="🛍 Покупки", callback_data="menu:purchases")
    kb.button(text="📜 Правила", callback_data="menu:rules")
    kb.button(text="ℹ️ Информация", callback_data="menu:info")
    kb.button(text="👨‍💻 Оператор", url="https://t.me/skyw_scm")
    kb.adjust(2, 2, 2)  # по две кнопки в строке
    return kb.as_markup()

def kb_cities() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for city in PRODUCTS.keys():
        kb.button(text=city, callback_data=f"city:{city}")
    kb.button(text="⬅️ Назад", callback_data="back:main")
    kb.adjust(2, 1)
    return kb.as_markup()

def kb_products(city: str) -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for idx, item in enumerate(PRODUCTS[city]):
        kb.button(text=f"{item['name']} — {item['price']}₽", callback_data=f"prod:{idx}")
    kb.button(text="⬅️ Назад", callback_data="back:cities")
    kb.adjust(1)
    return kb.as_markup()

def kb_districts(city: str, product_name: str) -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    options = DISTRICTS.get(city, {}).get(product_name, [])
    if not options:
        # Фолбэк на случай отсутствия настроек
        options = {
            "Саратов": ["Центр", "Кировский", "Фрунзенский", "Октябрьский", "Ленинский"],
            "Армавир": ["Центр", "Северный", "Южный"],
        }.get(city, [])
    for d in options:
        kb.button(text=d, callback_data=f"dist:{d}")
    kb.button(text="⬅️ Назад", callback_data="back:products")
    kb.adjust(2, 1)
    return kb.as_markup()

def kb_payments() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for p in PAYMENTS:
        kb.button(text=p, callback_data=f"pay:{p}")
    kb.button(text="⬅️ Назад", callback_data="back:districts")
    kb.adjust(1)
    return kb.as_markup()

def kb_order_final() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 Главное меню", callback_data="back:main")
    kb.button(text="❌ Отменить заказ", callback_data="order:cancel")
    kb.button(text="👨‍💻 Оператор", url="https://t.me/h2h_operator")
    kb.adjust(2, 1)
    return kb.as_markup()

# =============== КАПЧА ===============
def generate_captcha():
    # один целевой смайл и 5 ложных
    correct = random.choice(["😀", "😎", "😍", "🤓", "😇", "🤠"])
    pool = ["😂", "😭", "😡", "😱", "🤯", "🥶", "🥳", "😴", "🤪", "😏"]
    wrong = random.sample(pool, 5)
    options = wrong + [correct]
    random.shuffle(options)

    kb = InlineKeyboardBuilder()
    for e in options:
        kb.button(text=e, callback_data=f"captcha:{e}:{correct}")
    kb.adjust(3, 3)
    return correct, kb.as_markup()

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    correct, kb = generate_captcha()
    await message.answer(
        f"Выберите такой же смайлик:\n\n<b style='font-size:20px'>{correct}</b>",
        reply_markup=kb
    )

@dp.callback_query(F.data.startswith("captcha:"))
async def on_captcha(cb: types.CallbackQuery):
    _, chosen, correct = cb.data.split(":")
    if chosen == correct:
        await cb.message.edit_text(WELCOME_TEXT, reply_markup=kb_main_menu())
    else:
        new_correct, new_kb = generate_captcha()
        await cb.message.edit_text(
            f"❌ Неверно! Попробуйте снова.\n\nВыберите такой же смайлик:\n\n<b>{new_correct}</b>",
            reply_markup=new_kb
        )
    await cb.answer()

# ============ ГЛАВНОЕ МЕНЮ ============
@dp.callback_query(F.data == "menu:buy")
async def on_buy(cb: types.CallbackQuery):
    await safe_edit(cb.message, "Выберите город:", kb_cities())
    await cb.answer()

@dp.callback_query(F.data.in_({"menu:job", "menu:purchases", "menu:rules", "menu:info"}))
async def on_other_sections(cb: types.CallbackQuery):
    texts = {
        "menu:job": "💼 Раздел «Работа».\nИщем курьеров и водителей по всем городам:\n1) Возраст 14+.\n2) Берем только с залогом, никакие документы не принимаются.\n4) Берем только адекватных и вежливых людей. \n Писать в поддержку  ",
        "menu:purchases": "🛍 Раздел «Покупки».\nВаши прошлые заказы будут отображаться здесь.",
        "menu:rules": "📜 Раздел «Правила».\n1) Оператор работает с 10 до 04 мск без перерывов и выходных.\n2)Магазин не несет ответственности, если покупатель по ошибке купил клад не в том регионе.\n3) Передача адреса третьим лицам строго запрещена.\n4) После оплаты — пишите оператору.",
        "menu:info": "ℹ️ Раздел «Информация».\n 📩Если возникают трудности в пользовании бота, есть вопросы по товару/ сделать заказ/ оформить предзаказ/ обратитесь к оператору. Приятных покупок в HOOD2HOOD store",
    }
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data="back:main")
    await safe_edit(cb.message, texts[cb.data], kb.as_markup())
    await cb.answer()

@dp.callback_query(F.data == "back:main")
async def back_main(cb: types.CallbackQuery):
    await safe_edit(cb.message, WELCOME_TEXT, kb_main_menu())
    await cb.answer()

# ============ ВЕТКА ПОКУПКИ ============
@dp.callback_query(F.data.startswith("city:"))
async def on_city(cb: types.CallbackQuery):
    city = cb.data.split(":", 1)[1]
    user_state[cb.from_user.id] = {"city": city}
    await safe_edit(cb.message, f"Товары в городе <b>{city}</b>:", kb_products(city))
    await cb.answer()

@dp.callback_query(F.data == "back:cities")
async def back_cities(cb: types.CallbackQuery):
    await safe_edit(cb.message, "Выберите город:", kb_cities())
    await cb.answer()

@dp.callback_query(F.data == "back:products")
async def back_products(cb: types.CallbackQuery):
    st = user_state.get(cb.from_user.id, {})
    city = st.get("city")
    if not city:
        await safe_edit(cb.message, "Выберите город:", kb_cities())
    else:
        await safe_edit(cb.message, f"Товары в городе <b>{city}</b>:", kb_products(city))
    await cb.answer()

@dp.callback_query(F.data.startswith("prod:"))
async def on_product(cb: types.CallbackQuery):
    idx = int(cb.data.split(":")[1])
    st = user_state.get(cb.from_user.id, {})
    city = st.get("city")
    if not city:
        await safe_edit(cb.message, "Сначала выберите город:", kb_cities())
        await cb.answer()
        return

    product = PRODUCTS[city][idx]
    st["product"] = product
    user_state[cb.from_user.id] = st

    # Пытаемся заменить текущее сообщение на фото; если нельзя — удаляем и шлём фото
    await show_product_with_districts(cb.message, city, product)
    await cb.answer()

@dp.callback_query(F.data.startswith("dist:"))
async def on_district(cb: types.CallbackQuery):
    district = cb.data.split(":", 1)[1]
    st = user_state.setdefault(cb.from_user.id, {})
    st["district"] = district
    user_state[cb.from_user.id] = st

    # На экране района у нас фото; чтобы избежать ошибок edit_text для media,
    # аккуратно меняем только клавиатуру (оставляем фото), показывая оплату.
    await safe_edit_reply_markup(cb.message, kb_payments())
    await cb.answer()

@dp.callback_query(F.data == "back:districts")
async def back_districts(cb: types.CallbackQuery):
    st = user_state.get(cb.from_user.id, {})
    city = st.get("city")
    product = st.get("product")
    if not city or not product:
        await safe_edit(cb.message, "Выберите город:", kb_cities())
        await cb.answer()
        return

    # Возвращаем клавиатуру районов под тем же фото товара
    await safe_edit_reply_markup(cb.message, kb_districts(city, product["name"]))
    await cb.answer()

@dp.callback_query(F.data.startswith("pay:"))
async def on_payment(cb: types.CallbackQuery):
    pay_label = cb.data.split(":", 1)[1]
    st = user_state.setdefault(cb.from_user.id, {})
    st["payment"] = pay_label

    city = st.get("city", "—")
    pr = st.get("product", {})
    district = st.get("district", "—")
    price = pr.get("price", "—")
    name = pr.get("name", "—")
    details = PAYMENT_DETAILS.get(pay_label, "—")

    result = (
        "✅ <b>Ваш заказ</b>\n"
        f"Город: <b>{city}</b>\n"
        f"Товар: <b>{name}</b>\n"
        f"Цена: <b>{price}₽</b>\n"
        f"Район: <b>{district}</b>\n"
        f"Оплата: <b>{pay_label}</b>\n\n"
        f"💳 <b>Реквизиты</b>: <code>{details}</code>\n"
        f"После оплаты напишите <a href='https://t.me/h2h_operator'>оператору</a>."
    )

    # Итог показываем как текст: заменим сообщение целиком (если это фото — сначала удалим)
    await replace_with_text(cb.message, result, kb_order_final())

    # Логирование заказа в файл
    try:
        with open(ORDERS_FILE, "a", encoding="utf-8") as f:
            f.write(
                f"{datetime.now().isoformat()} | user:{cb.from_user.id} (@{cb.from_user.username}) | "
                f"city:{city} | product:{name} | price:{price} | district:{district} | pay:{pay_label}\n"
            )
    except Exception:
        pass

    await cb.answer()

@dp.callback_query(F.data == "order:cancel")
async def order_cancel(cb: types.CallbackQuery):
    user_state.pop(cb.from_user.id, None)
    await replace_with_text(cb.message, WELCOME_TEXT, kb_main_menu())
    await cb.answer()

# ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ РЕНДЕРА =====

async def safe_edit(message: types.Message, text: str, reply_markup: types.InlineKeyboardMarkup | None = None):
    """
    Универсально меняем текущий экран:
    - если сообщение текстовое — edit_text
    - если фото — edit_caption
    - если не получилось — удаляем и отправляем новое текстовое
    """
    try:
        if message.photo:
            await message.edit_caption(caption=text, reply_markup=reply_markup)
        else:
            await message.edit_text(text, reply_markup=reply_markup)
    except Exception:
        try:
            await message.delete()
        except Exception:
            pass
        await message.answer(text, reply_markup=reply_markup)

async def safe_edit_reply_markup(message: types.Message, reply_markup: types.InlineKeyboardMarkup | None = None):
    """
    Меняет только клавиатуру у текущего сообщения, не трогая текст/фото.
    Подходит, когда текущее сообщение — фото, и нужно не ловить ошибку edit_text.
    """
    try:
        await message.edit_reply_markup(reply_markup=reply_markup)
    except Exception:
        # Фолбэк — пересоздаём текст
        text = "..."
        if message.photo:
            # Если было фото, попробуем хотя бы заменить подпись
            cap = message.caption or " "
            await safe_edit(message, cap, reply_markup)
        else:
            txt = message.text or " "
            await safe_edit(message, txt, reply_markup)

async def show_product_with_districts(message: types.Message, city: str, product: dict):
    """
    Показать фото товара с подписью и клавиатурой районов.
    Пробуем edit_media, если текущее сообщение уже media. Если нет — удаляем и шлём новое фото.
    """
    path = os.path.join(PHOTOS_DIR, product["photo"])
    caption = f"<b>{product['name']}</b>\nЦена: <b>{product['price']}₽</b>\n{product['desc']}"
    try:
        media = types.InputMediaPhoto(
            media=FSInputFile(path),
            caption=caption,
            parse_mode="HTML"
        )
        await message.edit_media(media=media, reply_markup=kb_districts(city, product["name"]))
    except Exception:
        # Если текущее сообщение было текстом — Telegram не даст edit_media: удаляем и шлём фото
        try:
            await message.delete()
        except Exception:
            pass
        await message.answer_photo(
            FSInputFile(path),
            caption=caption,
            reply_markup=kb_districts(city, product["name"])
        )

async def replace_with_text(message: types.Message, text: str, reply_markup: types.InlineKeyboardMarkup | None = None):
    """
    Универсально заменить экран на чистый текст (для итога заказа и т.п.).
    Если текущее — фото, сначала удалим его, затем отправим текст.
    """
    try:
        if message.photo:
            raise RuntimeError("media_to_text")
        await message.edit_text(text, reply_markup=reply_markup)
    except Exception:
        try:
            await message.delete()
        except Exception:
            pass
        await message.answer(text, reply_markup=reply_markup)

# ============== ЗАПУСК ==============
async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
