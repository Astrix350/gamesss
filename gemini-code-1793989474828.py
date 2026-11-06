import aiosqlite

DB_PATH = "bot_database.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                chat_id INTEGER PRIMARY KEY,
                account TEXT DEFAULT 'durov',
                style TEXT DEFAULT 'premium',
                currency TEXT DEFAULT 'stars'
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                offer_id TEXT PRIMARY KEY,
                chat_id INTEGER,
                message_id INTEGER,
                nft_link TEXT,
                currency TEXT,
                amount REAL,
                lang TEXT,
                style TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def get_settings(chat_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT account, style, currency FROM settings WHERE chat_id = ?", (chat_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"account": row[0], "style": row[1], "currency": row[2]}
            else:
                return {"account": "durov", "style": "premium", "currency": "stars"}

async def update_setting(chat_id: int, key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO settings (chat_id) VALUES (?)", (chat_id,))
        if key == "account":
            await db.execute("UPDATE settings SET account = ? WHERE chat_id = ?", (value, chat_id))
        elif key == "style":
            await db.execute("UPDATE settings SET style = ? WHERE chat_id = ?", (value, chat_id))
        elif key == "currency":
            await db.execute("UPDATE settings SET currency = ? WHERE chat_id = ?", (value, chat_id))
        await db.commit()

async def save_offer(offer_id: str, chat_id: int, message_id: int, nft_link: str, currency: str, amount: float, lang: str, style: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO offers (offer_id, chat_id, message_id, nft_link, currency, amount, lang, style, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (offer_id, chat_id, message_id, nft_link, currency, amount, lang, style))
        await db.commit()

async def get_offer(offer_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT offer_id, chat_id, message_id, nft_link, currency, amount, lang, style, status FROM offers WHERE offer_id = ?", (offer_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "offer_id": row[0], "chat_id": row[1], "message_id": row[2],
                    "nft_link": row[3], "currency": row[4], "amount": row[5],
                    "lang": row[6], "style": row[7], "status": row[8]
                }
            return None

async def update_offer_status(offer_id: str, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE offers SET status = ? WHERE offer_id = ?", (status, offer_id))
        await db.commit()

async def get_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*), SUM(CASE WHEN status='accepted' THEN 1 ELSE 0 END), SUM(CASE WHEN status='rejected' THEN 1 ELSE 0 END) FROM offers") as cursor:
            row = await cursor.fetchone()
            return {"total": row[0] or 0, "accepted": row[1] or 0, "rejected": row[2] or 0}