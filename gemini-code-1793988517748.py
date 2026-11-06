import io
from PIL import Image, ImageDraw, ImageFont

def generate_nft_card(link: str, currency: str, amount: float, status: str, style: str, lang: str) -> io.BytesIO:
    width, height = 1000, 600
    image = Image.new("RGB", (width, height), color=(20, 20, 20))
    draw = ImageDraw.Draw(image)

    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        font_med = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except IOError:
        font_large = ImageFont.load_default()
        font_med = ImageFont.load_default()
        font_small = ImageFont.load_default()

    if style == "premium":
        bg_color = (15, 15, 20)
        card_bg = (28, 28, 38)
        border_color = (212, 175, 55)
        text_color = (240, 240, 245)
        accent_color = (212, 175, 55)
    elif style == "neon":
        bg_color = (10, 10, 15)
        card_bg = (20, 20, 30)
        border_color = (0, 240, 255)
        text_color = (255, 255, 255)
        accent_color = (255, 0, 128)
    elif style == "minimal":
        bg_color = (245, 245, 247)
        card_bg = (255, 255, 255)
        border_color = (200, 200, 205)
        text_color = (30, 30, 35)
        accent_color = (0, 122, 255)
    else: # classic
        bg_color = (40, 45, 50)
        card_bg = (60, 65, 75)
        border_color = (100, 110, 125)
        text_color = (255, 255, 255)
        accent_color = (70, 130, 180)

    image.paste(bg_color, [0, 0, width, height])

    margin = 40
    draw.rounded_rectangle(
        [margin, margin, width - margin, height - margin],
        radius=24,
        fill=card_bg,
        outline=border_color,
        width=4
    )

    title_map = {
        "ru": "TELEGRAM NFT OFFER",
        "uk": "TELEGRAM NFT OFFER",
        "en": "TELEGRAM NFT OFFER"
    }
    title = title_map.get(lang, title_map["en"])
    draw.text((margin + 40, margin + 35), title, fill=text_color, font=font_large)

    box_x1, box_y1 = margin + 40, margin + 110
    box_x2, box_y2 = margin + 320, height - margin - 40
    draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], radius=16, fill=bg_color, outline=border_color, width=2)
    
    draw.text((box_x1 + 65, box_y1 + 125), "NFT CARD", fill=text_color, font=font_med)
    
    det_x = box_x2 + 40
    cur_label = "⭐️ Stars" if currency.lower() == "stars" else "💎 TON (Gram)"
    
    draw.text((det_x, margin + 120), "🔗 NFT Link:", fill=border_color, font=font_small)
    display_link = link if len(link) < 32 else link[:29] + "..."
    draw.text((det_x, margin + 150), display_link, fill=text_color, font=font_med)

    draw.text((det_x, margin + 220), "💰 Price:", fill=border_color, font=font_small)
    draw.text((det_x, margin + 250), f"{amount} {cur_label}", fill=accent_color, font=font_large)

    status_text_map = {
        "pending": "⏳ Pending",
        "accepted": "✅ Accepted",
        "rejected": "❌ Rejected"
    }
    status_display = status_text_map.get(status, "⏳ Pending")
    draw.text((det_x, margin + 340), "Status:", fill=border_color, font=font_small)
    draw.text((det_x, margin + 370), status_display, fill=text_color, font=font_med)

    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output