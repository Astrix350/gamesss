TEXTS = {
    "ru": {
        "link": "Ссылка:",
        "price": "Цена:",
        "status": "Статус:",
        "status_pending": "Ожидает ответа ⏳",
        "status_accepted": "Принят ✅",
        "status_rejected": "Отклонен ❌",
        "btn_accept": "Принять ✅",
        "btn_reject": "Отклонить ❌",
        "accepted_alert": "Оффер принят! Открытие контакта администратора...",
        "rejected_alert": "Оффер отклонен.",
        "already_processed": "Этот оффер уже был обработан.",
        "help_text": (
            "🤖 **Telegram NFT Offer Bot**\n\n"
            "Команды:\n"
            "• `/offer [ссылка] [stars/gram] [сумма] [ru/uk/en] [style]` — создать оффер\n"
            "• `/setup` — текущие настройки\n"
            "• `/help` — справка\n\n"
            "Команды администратора:\n"
            "• `/setaccount [username]` — установить контакт для сделки\n"
            "• `/setstyle [classic/premium/minimal/neon]` — стиль по умолчанию\n"
            "• `/setcurrency [stars/gram]` — валюта по умолчанию\n"
            "• `/stats` — статистика офферов\n"
            "• `/preview` — предпросмотр стилей\n"
        ),
        "setup_text": "⚙️ **Текущие настройки:**\n• Аккаунт: @{account}\n• Стиль: {style}\n• Валюта: {currency}",
        "stats_text": "📊 **Статистика офферов:**\n• Всего создано: {total}\n• Принято: {accepted}\n• Отклонено: {rejected}",
        "err_args": "❌ Неверный формат. Пример:\n`/offer https://t.me/nft/example stars 100 ru premium`",
        "only_admin": "⛔ Эта команда доступна только администратору.",
    },
    "uk": {
        "link": "Посилання:",
        "price": "Ціна:",
        "status": "Статус:",
        "status_pending": "Очікує відповіді ⏳",
        "status_accepted": "Прийнято ✅",
        "status_rejected": "Відхилено ❌",
        "btn_accept": "Прийняти ✅",
        "btn_reject": "Відхилити ❌",
        "accepted_alert": "Офер прийнято! Відкриття контакту адміністратора...",
        "rejected_alert": "Офер відхилено.",
        "already_processed": "Цей офер вже було оброблено.",
        "help_text": (
            "🤖 **Telegram NFT Offer Bot**\n\n"
            "Команди:\n"
            "• `/offer [посилання] [stars/gram] [сума] [ru/uk/en] [style]` — створити офер\n"
            "• `/setup` — поточні налаштування\n"
            "• `/help` — довідка\n\n"
            "Команди адміністратора:\n"
            "• `/setaccount [username]` — встановити контакт для угоди\n"
            "• `/setstyle [classic/premium/minimal/neon]` — стиль за замовчуванням\n"
            "• `/setcurrency [stars/gram]` — валюта за замовчуванням\n"
            "• `/stats` — статистика оферів\n"
            "• `/preview` — попередній перегляд стилів\n"
        ),
        "setup_text": "⚙️ **Поточні налаштування:**\n• Акаунт: @{account}\n• Стиль: {style}\n• Валюта: {currency}",
        "stats_text": "📊 **Статистика оферів:**\n• Всього створено: {total}\n• Прийнято: {accepted}\n• Відхилено: {rejected}",
        "err_args": "❌ Невірний формат. Приклад:\n`/offer https://t.me/nft/example stars 100 ru premium`",
        "only_admin": "⛔ Ця команда доступна лише адміністратору.",
    },
    "en": {
        "link": "Link:",
        "price": "Price:",
        "status": "Status:",
        "status_pending": "Pending response ⏳",
        "status_accepted": "Accepted ✅",
        "status_rejected": "Rejected ❌",
        "btn_accept": "Accept ✅",
        "btn_reject": "Reject ❌",
        "accepted_alert": "Offer accepted! Opening admin contact...",
        "rejected_alert": "Offer rejected.",
        "already_processed": "This offer has already been processed.",
        "help_text": (
            "🤖 **Telegram NFT Offer Bot**\n\n"
            "Commands:\n"
            "• `/offer [link] [stars/gram] [amount] [ru/uk/en] [style]` — create offer\n"
            "• `/setup` — current settings\n"
            "• `/help` — help\n\n"
            "Admin commands:\n"
            "• `/setaccount [username]` — set admin contact\n"
            "• `/setstyle [classic/premium/minimal/neon]` — default style\n"
            "• `/setcurrency [stars/gram]` — default currency\n"
            "• `/stats` — offer statistics\n"
            "• `/preview` — preview styles\n"
        ),
        "setup_text": "⚙️ **Current Settings:**\n• Account: @{account}\n• Style: {style}\n• Currency: {currency}",
        "stats_text": "📊 **Offer Statistics:**\n• Total created: {total}\n• Accepted: {accepted}\n• Rejected: {rejected}",
        "err_args": "❌ Invalid format. Example:\n`/offer https://t.me/nft/example stars 100 ru premium`",
        "only_admin": "⛔ This command is only available to the administrator.",
    }
}