import asyncio
import logging
import sys
import uuid

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, ADMIN_ID
from database import init_db, get_settings, update_setting, save_offer, get_offer, update_offer_status, get_stats
from texts import TEXTS
from generator import generate_nft_card

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

router = Router()

def get_texts(lang: str):
    return TEXTS.get(lang, TEXTS["en"])

def get_keyboard(offer_id: str, lang: str, status: str, admin_username: str):
    texts = get_texts(lang)
    if status != "pending":
        status_label = texts["status_accepted"] if status == "accepted" else texts["status_rejected"]
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=status_label, callback_data="noop")]
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=texts["btn_accept"], url=f"https://t.me/{admin_username}"),
            InlineKeyboardButton(text=texts["btn_reject"], callback_data=f"reject_{offer_id}")
        ]
    ])

@router.message(Command("help"))
async def cmd_help(message: Message):
    lang = "ru"
    if message.from_user and message.from_user.language_code in ["uk", "en"]:
        lang = message.from_user.language_code
    texts = get_texts(lang)
    await message.answer(texts["help_text"], parse_mode="Markdown")

@router.message(Command("setup"))
async def cmd_setup(message: Message):
    settings = await get_settings(message.chat.id)
    texts = get_texts("ru")
    text = texts["setup_text"].format(
        account=settings["account"],
        style=settings["style"],
        currency=settings["currency"]
    )
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("setaccount"))
async def cmd_setaccount(message: Message, command: CommandObject):
    if message.from_user.id != ADMIN_ID:
        await message.answer(get_texts("ru")["only_admin"])
        return
    if not command.args:
        await message.answer("❌ Укажите юзернейм: `/setaccount username` (без @)", parse_mode="Markdown")
        return
    username = command.args.strip().lstrip("@")
    await update_setting(message.chat.id, "account", username)
    await message.answer(f"✅ Аккаунт для сделок успешно изменен на: @{username}")

@router.message(Command("setstyle"))
async def cmd_setstyle(message: Message, command: CommandObject):
    if message.from_user.id != ADMIN_ID:
        await message.answer(get_texts("ru")["only_admin"])
        return
    styles = ["classic", "premium", "minimal", "neon"]
    if not command.args or command.args.strip().lower() not in styles:
        await message.answer(f"❌ Неверный стиль. Выберите из: {', '.join(styles)}")
        return
    style = command.args.strip().lower()
    await update_setting(message.chat.id, "style", style)
    await message.answer(f"✅ Стиль по умолчанию изменен на: `{style}`", parse_mode="Markdown")

@router.message(Command("setcurrency"))
async def cmd_setcurrency(message: Message, command: CommandObject):
    if message.from_user.id != ADMIN_ID:
        await message.answer(get_texts("ru")["only_admin"])
        return
    currencies = ["stars", "gram", "ton"]
    if not command.args or command.args.strip().lower() not in currencies:
        await message.answer("❌ Неверная валюта. Выберите из: stars, gram", parse_mode="Markdown")
        return
    currency = command.args.strip().lower()
    if currency == "ton":
        currency = "gram"
    await update_setting(message.chat.id, "currency", currency)
    await message.answer(f"✅ Валюта по умолчанию изменена на: `{currency}`", parse_mode="Markdown")

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer(get_texts("ru")["only_admin"])
        return
    stats = await get_stats()
    texts = get_texts("ru")
    text = texts["stats_text"].format(
        total=stats["total"],
        accepted=stats["accepted"],
        rejected=stats["rejected"]
    )
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("preview"))
async def cmd_preview(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer(get_texts("ru")["only_admin"])
        return
    styles = ["classic", "premium", "minimal", "neon"]
    for st in styles:
        img_bytes = generate_nft_card(
            link="https://t.me/nft/preview",
            currency="stars",
            amount=500,
            status="pending",
            style=st,
            lang="ru"
        )
        photo = BufferedInputFile(img_bytes.read(), filename=f"{st}.png")
        await message.answer_photo(photo=photo, caption=f"🎨 Стиль: **{st}**", parse_mode="Markdown")

@router.message(Command("offer"))
async def cmd_offer(message: Message, command: CommandObject):
    settings = await get_settings(message.chat.id)
    
    args = (command.args or "").split()
    if not args:
        await message.answer(get_texts("ru")["err_args"], parse_mode="Markdown")
        return

    nft_link = args[0]
    currency = args[1] if len(args) > 1 else settings["currency"]
    
    try:
        amount = float(args[2]) if len(args) > 2 else 100.0
    except ValueError:
        amount = 100.0

    lang = args[3] if len(args) > 3 and args[3] in ["ru", "uk", "en"] else "ru"
    style = args[4] if len(args) > 4 and args[4] in ["classic", "premium", "minimal", "neon"] else settings["style"]

    offer_id = str(uuid.uuid4())[:8]
    
    img_bytes = generate_nft_card(
        link=nft_link,
        currency=currency,
        amount=amount,
        status="pending",
        style=style,
        lang=lang
    )
    photo = BufferedInputFile(img_bytes.read(), filename="nft_offer.png")
    
    texts = get_texts(lang)
    keyboard = get_keyboard(offer_id, lang, "pending", settings["account"])

    caption = (
        f"🔗 **{texts['link']}** {nft_link}\n"
        f"💰 **{texts['price']}** {amount} {currency.upper()}\n"
        f"📌 **{texts['status']}** {texts['status_pending']}"
    )

    sent_msg = await message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

    await save_offer(
        offer_id=offer_id,
        chat_id=message.chat.id,
        message_id=sent_msg.message_id,
        nft_link=nft_link,
        currency=currency,
        amount=amount,
        lang=lang,
        style=style
    )

    try:
        await message.delete()
    except Exception:
        pass

@router.callback_query(F.data.startswith("reject_"))
async def callback_reject(callback: CallbackQuery):
    offer_id = callback.data.split("_")[1]
    offer = await get_offer(offer_id)
    if not offer:
        await callback.answer("❌ Offer not found.", show_alert=True)
        return
    
    if offer["status"] != "pending":
        texts = get_texts(offer["lang"])
        await callback.answer(texts["already_processed"], show_alert=True)
        return

    await update_offer_status(offer_id, "rejected")
    settings = await get_settings(offer["chat_id"])
    texts = get_texts(offer["lang"])

    img_bytes = generate_nft_card(
        link=offer["nft_link"],
        currency=offer["currency"],
        amount=offer["amount"],
        status="rejected",
        style=offer["style"],
        lang=offer["lang"]
    )
    photo = BufferedInputFile(img_bytes.read(), filename="nft_offer.png")

    caption = (
        f"🔗 **{texts['link']}** {offer['nft_link']}\n"
        f"💰 **{texts['price']}** {offer['amount']} {offer['currency'].upper()}\n"
        f"📌 **{texts['status']}** {texts['status_rejected']}"
    )

    keyboard = get_keyboard(offer_id, offer["lang"], "rejected", settings["account"])

    try:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=photo, caption=caption, parse_mode="Markdown"),
            reply_markup=keyboard
        )
    except Exception:
        try:
            await callback.message.edit_caption(caption=caption, reply_markup=keyboard, parse_mode="Markdown")
        except Exception:
            pass

    await callback.answer(texts["rejected_alert"], show_alert=True)

@router.callback_query(F.data == "noop")
async def callback_noop(callback: CallbackQuery):
    await callback.answer("Этот оффер уже обработан.", show_alert=True)

async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    logger.info("Starting Telegram NFT Offer Bot on Koyeb...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())