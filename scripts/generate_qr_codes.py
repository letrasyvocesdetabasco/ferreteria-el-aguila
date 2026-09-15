#!/usr/bin/env python3
"""
Generador de Códigos QR Publicitarios para Ferretería y Tlapalería El Águila
Genera 5 formatos de alta resolución listos para impresión (lonas, volantes, tarjetas, mostrador):
1. qr-01-azul-corporativo.png (1200x1200px - Identidad oficial azul rey y oro)
2. qr-02-dorado-premium.png (1200x1200px - Alto impacto para exhibidores y acrílicos)
3. qr-03-lona-exterior-gran-formato.png (1800x2400px - Lona publicitaria exterior de 3:4)
4. qr-04-tarjeta-minimalista.png (1050x600px - Tarjeta de presentación 3.5x2 pulg a 300 DPI)
5. qr-05-flyer-publicitario-mostrador.png (1240x1754px - Volante publicitario tamaño A5)
"""

import os
from PIL import Image, ImageDraw, ImageFont
import qrcode

URL_TARGET = "https://ferreteriaytlapaleria-elaguila.com"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "qr")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo-aguila.png")
LOGO_GOLD_PATH = os.path.join(ASSETS_DIR, "logo-aguila-gold.png")
LOGO_WHITE_PATH = os.path.join(ASSETS_DIR, "logo-aguila-white.png")

# Paleta oficial extraída de la lona
COLOR_BLUE = (0, 75, 151)       # Azul Rey Corporativo #004b97
COLOR_BLUE_DARK = (10, 37, 64)   # Azul Marino Profundo #0a2540
COLOR_GOLD = (255, 203, 5)       # Amarillo/Oro Fachada #ffcb05
COLOR_GOLD_DARK = (217, 119, 6)  # Oro ámbar oscuro
COLOR_DARK = (30, 41, 59)        # Slate Dark #1e293b
COLOR_WHITE = (255, 255, 255)
COLOR_CARD_BG = (248, 250, 252)  # Blanco grisáceo suave
COLOR_GREEN = (37, 211, 102)     # WhatsApp Green

# Fuentes seguras de Linux
FONT_BOLD = "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/TTF/DejaVuSans.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def create_base_qr(url, box_size=10, border=2, fill_color="black", back_color="white", error_correction=qrcode.constants.ERROR_CORRECT_H):
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

def paste_center_logo(qr_img, logo_path, scale_ratio=0.22, bg_circle=True, bg_color=COLOR_WHITE, border_color=COLOR_GOLD):
    if not os.path.exists(logo_path):
        return qr_img

    logo = Image.open(logo_path).convert("RGBA")
    qr_w, qr_h = qr_img.size
    target_size = int(min(qr_w, qr_h) * scale_ratio)
    
    # Redimensionar logo manteniendo proporción
    logo.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
    lw, lh = logo.size

    if bg_circle:
        badge_radius = int(target_size * 0.72)
        cx, cy = qr_w // 2, qr_h // 2
        badge = Image.new("RGBA", (qr_w, qr_h), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(badge)
        
        bdraw.ellipse(
            [cx - badge_radius, cy - badge_radius, cx + badge_radius, cy + badge_radius],
            fill=bg_color,
            outline=border_color,
            width=max(4, target_size // 15)
        )
        qr_img = Image.alpha_composite(qr_img, badge)

    pos_x = (qr_w - lw) // 2
    pos_y = (qr_h - lh) // 2
    qr_img.paste(logo, (pos_x, pos_y), logo)
    return qr_img

# ==============================================================================
# FORMATO 1: AZUL CORPORATIVO (1200 x 1200 px)
# ==============================================================================
def generate_format_1():
    print("-> Generando Formato 1: Azul Corporativo...")
    W, H = 1200, 1200
    img = Image.new("RGBA", (W, H), COLOR_WHITE)
    draw = ImageDraw.Draw(img)

    margin = 40
    draw.rounded_rectangle(
        [margin, margin, W - margin, H - margin],
        radius=36,
        outline=COLOR_BLUE,
        width=12
    )
    inner_margin = margin + 18
    draw.rounded_rectangle(
        [inner_margin, inner_margin, W - inner_margin, H - inner_margin],
        radius=26,
        outline=COLOR_GOLD,
        width=4
    )

    font_title = get_font(FONT_BOLD, 46)
    font_sub = get_font(FONT_BOLD, 26)
    font_body = get_font(FONT_REGULAR, 24)
    font_footer = get_font(FONT_BOLD, 28)

    title_text = "FERRETERÍA Y TLAPALERÍA EL ÁGUILA"
    sub_text = "¡TODO EN UN SOLO LUGAR PARA TU HOGAR Y TRABAJO!"

    bbox_t = draw.textbbox((0, 0), title_text, font=font_title)
    draw.text(((W - (bbox_t[2] - bbox_t[0])) // 2, 85), title_text, font=font_title, fill=COLOR_BLUE)

    bbox_s = draw.textbbox((0, 0), sub_text, font=font_sub)
    draw.text(((W - (bbox_s[2] - bbox_s[0])) // 2, 150), sub_text, font=font_sub, fill=COLOR_GOLD_DARK)

    qr_img = create_base_qr(URL_TARGET, box_size=16, border=2, fill_color=COLOR_BLUE, back_color=COLOR_WHITE)
    qr_img = paste_center_logo(qr_img, LOGO_GOLD_PATH, scale_ratio=0.22, bg_circle=True, bg_color=COLOR_WHITE, border_color=COLOR_GOLD)
    
    qw, qh = qr_img.size
    qr_x = (W - qw) // 2
    qr_y = 220
    img.paste(qr_img, (qr_x, qr_y), qr_img)

    bar_y = 960
    draw.rounded_rectangle([100, bar_y, W - 100, bar_y + 80], radius=20, fill=COLOR_BLUE)
    badge_text = "📱 ESCANEA PARA VER EL CATÁLOGO COMPLETO (17,641 ARTÍCULOS)"
    bbox_b = draw.textbbox((0, 0), badge_text, font=font_body)
    draw.text(((W - (bbox_b[2] - bbox_b[0])) // 2, bar_y + 26), badge_text, font=font_body, fill=COLOR_WHITE)

    url_text = "ferreteriaytlapaleria-elaguila.com"
    bbox_u = draw.textbbox((0, 0), url_text, font=font_footer)
    draw.text(((W - (bbox_u[2] - bbox_u[0])) // 2, 1070), url_text, font=font_footer, fill=COLOR_BLUE)

    out_path = os.path.join(OUTPUT_DIR, "qr-01-azul-corporativo.png")
    img.save(out_path, "PNG", dpi=(300, 300))
    print(f"   [OK] Guardado: {out_path}")

# ==============================================================================
# FORMATO 2: DORADO PREMIUM (1200 x 1200 px)
# ==============================================================================
def generate_format_2():
    print("-> Generando Formato 2: Dorado Premium...")
    W, H = 1200, 1200
    img = Image.new("RGBA", (W, H), COLOR_BLUE_DARK)
    draw = ImageDraw.Draw(img)

    margin = 35
    draw.rounded_rectangle([margin, margin, W - margin, H - margin], radius=32, outline=COLOR_GOLD, width=8)

    font_title = get_font(FONT_BOLD, 42)
    font_sub = get_font(FONT_BOLD, 26)
    font_wa = get_font(FONT_BOLD, 28)
    font_url = get_font(FONT_REGULAR, 24)

    title_text = "FERRETERÍA EL ÁGUILA"
    bbox_t = draw.textbbox((0, 0), title_text, font=font_title)
    draw.text(((W - (bbox_t[2] - bbox_t[0])) // 2, 75), title_text, font=font_title, fill=COLOR_GOLD)

    sub_text = "¡ESCANEA Y COTIZA DIRECTO POR WHATSAPP!"
    bbox_s = draw.textbbox((0, 0), sub_text, font=font_sub)
    draw.text(((W - (bbox_s[2] - bbox_s[0])) // 2, 135), sub_text, font=font_sub, fill=COLOR_WHITE)

    card_w, card_h = 750, 750
    cx = (W - card_w) // 2
    cy = 195
    draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=28, fill=COLOR_WHITE)

    qr_img = create_base_qr(URL_TARGET, box_size=15, border=2, fill_color=COLOR_DARK, back_color=COLOR_WHITE)
    qr_img = paste_center_logo(qr_img, LOGO_GOLD_PATH, scale_ratio=0.22, bg_circle=True, bg_color=COLOR_WHITE, border_color=COLOR_GOLD)
    qw, qh = qr_img.size
    img.paste(qr_img, (cx + (card_w - qw) // 2, cy + (card_h - qh) // 2), qr_img)

    wa_y = 980
    draw.rounded_rectangle([120, wa_y, W - 120, wa_y + 85], radius=42, fill=COLOR_GREEN)
    wa_text = "💬 Precios Reales con IVA • Recolección en Mostrador"
    bbox_w = draw.textbbox((0, 0), wa_text, font=font_wa)
    draw.text(((W - (bbox_w[2] - bbox_w[0])) // 2, wa_y + 26), wa_text, font=font_wa, fill=COLOR_WHITE)

    url_text = "ferreteriaytlapaleria-elaguila.com"
    bbox_u = draw.textbbox((0, 0), url_text, font=font_url)
    draw.text(((W - (bbox_u[2] - bbox_u[0])) // 2, 1095), url_text, font=font_url, fill=COLOR_GOLD)

    out_path = os.path.join(OUTPUT_DIR, "qr-02-dorado-premium.png")
    img.save(out_path, "PNG", dpi=(300, 300))
    print(f"   [OK] Guardado: {out_path}")

# ==============================================================================
# FORMATO 3: LONA EXTERIOR GRAN FORMATO (1800 x 2400 px - Proporción 3:4)
# ==============================================================================
def generate_format_3():
    print("-> Generando Formato 3: Lona Exterior Gran Formato (1800x2400)...")
    W, H = 1800, 2400
    img = Image.new("RGBA", (W, H), COLOR_WHITE)
    draw = ImageDraw.Draw(img)

    header_h = 380
    draw.rectangle([0, 0, W, header_h], fill=COLOR_BLUE)
    draw.rectangle([0, header_h - 18, W, header_h], fill=COLOR_GOLD)

    font_h1 = get_font(FONT_BOLD, 68)
    font_h2 = get_font(FONT_BOLD, 40)
    font_cta = get_font(FONT_BOLD, 54)
    font_sub_cta = get_font(FONT_REGULAR, 36)
    font_branch_title = get_font(FONT_BOLD, 38)
    font_branch_body = get_font(FONT_REGULAR, 28)
    font_branch_wa = get_font(FONT_BOLD, 34)

    if os.path.exists(LOGO_GOLD_PATH):
        l_img = Image.open(LOGO_GOLD_PATH).convert("RGBA")
        l_img.thumbnail((200, 200), Image.Resampling.LANCZOS)
        img.paste(l_img, (80, (header_h - l_img.height) // 2), l_img)

    draw.text((280, 90), "FERRETERÍA Y TLAPALERÍA", font=font_h2, fill=COLOR_GOLD)
    draw.text((280, 145), "EL ÁGUILA", font=font_h1, fill=COLOR_WHITE)
    draw.text((280, 245), "¡TODO EN UN SOLO LUGAR PARA TU HOGAR O TRABAJO!", font=font_sub_cta, fill=COLOR_WHITE)

    cta_y = 440
    cta_text = "CATÁLOGO DIGITAL EN TU CELULAR"
    bbox_cta = draw.textbbox((0, 0), cta_text, font=font_cta)
    draw.text(((W - (bbox_cta[2] - bbox_cta[0])) // 2, cta_y), cta_text, font=font_cta, fill=COLOR_BLUE)

    pill_y = 525
    draw.rounded_rectangle([300, pill_y, W - 300, pill_y + 70], radius=35, fill=COLOR_GOLD)
    pill_text = "⚡ 17,641 ARTÍCULOS CON PRECIO REAL Y EXISTENCIAS ⚡"
    bbox_p = draw.textbbox((0, 0), pill_text, font=font_branch_body)
    draw.text(((W - (bbox_p[2] - bbox_p[0])) // 2, pill_y + 18), pill_text, font=font_branch_body, fill=COLOR_DARK)

    qr_img = create_base_qr(URL_TARGET, box_size=24, border=2, fill_color=COLOR_DARK, back_color=COLOR_WHITE)
    qr_img = paste_center_logo(qr_img, LOGO_GOLD_PATH, scale_ratio=0.22, bg_circle=True, bg_color=COLOR_WHITE, border_color=COLOR_GOLD)
    qw, qh = qr_img.size
    qr_x = (W - qw) // 2
    qr_y = 635

    draw.rounded_rectangle([qr_x - 30, qr_y - 30, qr_x + qw + 30, qr_y + qh + 30], radius=36, outline=COLOR_BLUE, width=10)
    img.paste(qr_img, (qr_x, qr_y), qr_img)

    scan_msg = "📲 Apunta la cámara de tu celular aquí para cotizar al instante"
    bbox_sm = draw.textbbox((0, 0), scan_msg, font=font_sub_cta)
    draw.text(((W - (bbox_sm[2] - bbox_sm[0])) // 2, 1720), scan_msg, font=font_sub_cta, fill=COLOR_DARK)

    bot_y = 1810
    card_margin = 70
    card_w = (W - (card_margin * 3)) // 2
    card_h = 440

    # Las Delicias
    x1 = card_margin
    draw.rounded_rectangle([x1, bot_y, x1 + card_w, bot_y + card_h], radius=24, fill=COLOR_CARD_BG, outline=COLOR_BLUE, width=4)
    draw.rounded_rectangle([x1, bot_y, x1 + card_w, bot_y + 70], radius=24, fill=COLOR_BLUE)
    draw.text((x1 + 30, bot_y + 15), "📍 SUCURSAL LAS DELICIAS", font=font_branch_title, fill=COLOR_WHITE)
    draw.text((x1 + 30, bot_y + 95), "Av. Revolución 1203, Cuadrante II", font=font_branch_body, fill=COLOR_DARK)
    draw.text((x1 + 30, bot_y + 140), "Ref: A un lado del Centro de Salud", font=font_branch_body, fill=COLOR_GOLD_DARK)
    draw.text((x1 + 30, bot_y + 185), "Villahermosa, Tabasco", font=font_branch_body, fill=COLOR_DARK)
    
    draw.rounded_rectangle([x1 + 30, bot_y + 260, x1 + card_w - 30, bot_y + 340], radius=20, fill=COLOR_GREEN)
    draw.text((x1 + 55, bot_y + 282), "💬 WA: 993 289 2935", font=font_branch_wa, fill=COLOR_WHITE)
    draw.text((x1 + 30, bot_y + 370), "🏬 Recolección en mostrador sin filas", font=get_font(FONT_REGULAR, 22), fill=COLOR_DARK)

    # Buena Vista
    x2 = x1 + card_w + card_margin
    draw.rounded_rectangle([x2, bot_y, x2 + card_w, bot_y + card_h], radius=24, fill=COLOR_CARD_BG, outline=COLOR_BLUE, width=4)
    draw.rounded_rectangle([x2, bot_y, x2 + card_w, bot_y + 70], radius=24, fill=COLOR_BLUE)
    draw.text((x2 + 30, bot_y + 15), "📍 ESTRELLAS DE BUENA VISTA", font=font_branch_title, fill=COLOR_WHITE)
    draw.text((x2 + 30, bot_y + 95), "Carr. Villahermosa a La Isla Km 5.300", font=font_branch_body, fill=COLOR_DARK)
    draw.text((x2 + 30, bot_y + 140), "Buena Vista 1ra Sección", font=font_branch_body, fill=COLOR_GOLD_DARK)
    draw.text((x2 + 30, bot_y + 185), "Villahermosa, Tabasco", font=font_branch_body, fill=COLOR_DARK)
    
    draw.rounded_rectangle([x2 + 30, bot_y + 260, x2 + card_w - 30, bot_y + 340], radius=20, fill=COLOR_GREEN)
    draw.text((x2 + 55, bot_y + 282), "💬 WA: 993 192 8313", font=font_branch_wa, fill=COLOR_WHITE)
    draw.text((x2 + 30, bot_y + 370), "🏬 Recolección en mostrador sin filas", font=get_font(FONT_REGULAR, 22), fill=COLOR_DARK)

    draw.rectangle([0, H - 90, W, H], fill=COLOR_BLUE_DARK)
    web_text = "🌐 Visita: ferreteriaytlapaleria-elaguila.com • ¡Aparta por WhatsApp y recoge en tienda!"
    bbox_wb = draw.textbbox((0, 0), web_text, font=font_branch_body)
    draw.text(((W - (bbox_wb[2] - bbox_wb[0])) // 2, H - 65), web_text, font=font_branch_body, fill=COLOR_WHITE)

    out_path = os.path.join(OUTPUT_DIR, "qr-03-lona-exterior-gran-formato.png")
    img.save(out_path, "PNG", dpi=(300, 300))
    print(f"   [OK] Guardado: {out_path}")

# ==============================================================================
# FORMATO 4: TARJETA DE PRESENTACIÓN MINIMALISTA (1050 x 600 px)
# ==============================================================================
def generate_format_4():
    print("-> Generando Formato 4: Tarjeta Minimalista (1050x600)...")
    W, H = 1050, 600
    img = Image.new("RGBA", (W, H), COLOR_WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, 24, H], fill=COLOR_BLUE)
    draw.rectangle([24, 0, 32, H], fill=COLOR_GOLD)

    font_brand = get_font(FONT_BOLD, 28)
    font_sub = get_font(FONT_BOLD, 15)
    font_owner = get_font(FONT_BOLD, 22)
    font_info = get_font(FONT_REGULAR, 15)
    font_info_bold = get_font(FONT_BOLD, 15)
    font_qr_caption = get_font(FONT_BOLD, 14)
    font_url = get_font(FONT_BOLD, 16)

    if os.path.exists(LOGO_PATH):
        l_img = Image.open(LOGO_PATH).convert("RGBA")
        l_img.thumbnail((70, 70), Image.Resampling.LANCZOS)
        img.paste(l_img, (55, 40), l_img)

    draw.text((140, 42), "FERRETERÍA Y TLAPALERÍA EL ÁGUILA", font=font_brand, fill=COLOR_BLUE)
    draw.text((140, 78), "¡Todo en un solo lugar para tu hogar o trabajo!", font=font_sub, fill=COLOR_GOLD_DARK)

    draw.line([55, 115, 620, 115], fill=(226, 232, 240), width=2)

    draw.text((55, 135), "Atención Directa: Timoteo Méndez", font=font_owner, fill=COLOR_DARK)
    draw.text((55, 170), "Tlapalería • Plomería • Eléctrico • Tornillería • Herramientas", font=font_info, fill=(100, 116, 139))

    # Sucursal 1
    draw.text((55, 215), "📍 Suc. Las Delicias:", font=font_info_bold, fill=COLOR_BLUE)
    draw.text((215, 215), "Av. Revolución 1203 (Junto a Centro de Salud)", font=font_info, fill=COLOR_DARK)
    draw.text((55, 240), "📱 WhatsApp / Tel:", font=font_info_bold, fill=COLOR_BLUE)
    draw.text((215, 240), "993 289 2935", font=font_info_bold, fill=COLOR_DARK)

    # Sucursal 2
    draw.text((55, 285), "📍 Suc. Buena Vista:", font=font_info_bold, fill=COLOR_BLUE)
    draw.text((215, 285), "Carr. a La Isla Km 5.300, 1ra Secc", font=font_info, fill=COLOR_DARK)
    draw.text((55, 310), "📱 WhatsApp / Tel:", font=font_info_bold, fill=COLOR_BLUE)
    draw.text((215, 310), "993 192 8313", font=font_info_bold, fill=COLOR_DARK)

    draw.text((55, 370), "🏬 Recolección en mostrador sin filas", font=font_info_bold, fill=COLOR_GOLD_DARK)
    draw.text((55, 410), "🌐 ferreteriaytlapaleria-elaguila.com", font=font_url, fill=COLOR_BLUE)

    qr_img = create_base_qr(URL_TARGET, box_size=8, border=2, fill_color=COLOR_BLUE, back_color=COLOR_WHITE)
    qr_img = paste_center_logo(qr_img, LOGO_GOLD_PATH, scale_ratio=0.22, bg_circle=True, bg_color=COLOR_WHITE, border_color=COLOR_GOLD)
    qw, qh = qr_img.size
    
    qr_card_x = 670
    qr_card_y = 110
    draw.rounded_rectangle([qr_card_x - 15, qr_card_y - 15, qr_card_x + qw + 15, qr_card_y + qh + 80], radius=16, fill=COLOR_CARD_BG, outline=COLOR_BLUE, width=2)
    img.paste(qr_img, (qr_card_x, qr_card_y), qr_img)

    cap1 = "ESCANEA PARA"
    cap2 = "VER CATÁLOGO"
    cap3 = "17,641 ARTÍCULOS"
    bbox1 = draw.textbbox((0, 0), cap1, font=font_qr_caption)
    bbox2 = draw.textbbox((0, 0), cap2, font=font_qr_caption)
    bbox3 = draw.textbbox((0, 0), cap3, font=font_qr_caption)
    draw.text((qr_card_x + (qw - (bbox1[2]-bbox1[0]))//2, qr_card_y + qh + 8), cap1, font=font_qr_caption, fill=COLOR_DARK)
    draw.text((qr_card_x + (qw - (bbox2[2]-bbox2[0]))//2, qr_card_y + qh + 26), cap2, font=font_qr_caption, fill=COLOR_DARK)
    draw.text((qr_card_x + (qw - (bbox3[2]-bbox3[0]))//2, qr_card_y + qh + 46), cap3, font=font_qr_caption, fill=COLOR_BLUE)

    out_path = os.path.join(OUTPUT_DIR, "qr-04-tarjeta-minimalista.png")
    img.save(out_path, "PNG", dpi=(300, 300))
    print(f"   [OK] Guardado: {out_path}")

# ==============================================================================
# FORMATO 5: FLYER PUBLICITARIO DE MOSTRADOR (1240 x 1754 px - Tamaño A5)
# ==============================================================================
def generate_format_5():
    print("-> Generando Formato 5: Flyer Publicitario de Mostrador (A5)...")
    W, H = 1240, 1754
    img = Image.new("RGBA", (W, H), COLOR_WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 260], fill=COLOR_BLUE)
    draw.rectangle([0, 260, W, 275], fill=COLOR_GOLD)

    font_h1 = get_font(FONT_BOLD, 46)
    font_h2 = get_font(FONT_BOLD, 26)
    font_tagline = get_font(FONT_REGULAR, 22)
    font_title = get_font(FONT_BOLD, 36)
    font_bullet = get_font(FONT_REGULAR, 24)
    font_bullet_bold = get_font(FONT_BOLD, 24)
    font_box_title = get_font(FONT_BOLD, 28)
    font_box_body = get_font(FONT_REGULAR, 20)

    if os.path.exists(LOGO_GOLD_PATH):
        l_img = Image.open(LOGO_GOLD_PATH).convert("RGBA")
        l_img.thumbnail((150, 150), Image.Resampling.LANCZOS)
        img.paste(l_img, (50, 55), l_img)

    draw.text((220, 55), "FERRETERÍA Y TLAPALERÍA", font=font_h2, fill=COLOR_GOLD)
    draw.text((220, 95), "EL ÁGUILA", font=font_h1, fill=COLOR_WHITE)
    draw.text((220, 160), "¡Todo en un solo lugar para tu hogar o trabajo!", font=font_tagline, fill=COLOR_WHITE)
    draw.text((220, 195), "Villahermosa, Tabasco • Precios Netos con IVA", font=get_font(FONT_BOLD, 20), fill=COLOR_GOLD)

    draw.text((60, 315), "¿NECESITAS MATERIAL O HERRAMIENTAS?", font=font_title, fill=COLOR_BLUE)
    draw.text((60, 365), "Cotiza al momento desde tu celular sin esperar:", font=font_bullet, fill=COLOR_DARK)

    benefits = [
        ("✅ Catálogo Completo en Línea:", " Más de 17,641 productos disponibles."),
        ("✅ Precios Reales con IVA:", " Sin sorpresas al pagar en mostrador."),
        ("✅ Aparta por WhatsApp:", " Te tenemos tu pedido listo para recolección."),
        ("✅ Sin Filas ni Esperas:", " Ahorra tiempo en tus obras y reparaciones.")
    ]

    by = 425
    for title, desc in benefits:
        draw.text((60, by), title, font=font_bullet_bold, fill=COLOR_BLUE)
        draw.text((60 + draw.textlength(title, font=font_bullet_bold), by), desc, font=font_bullet, fill=COLOR_DARK)
        by += 45

    qr_card_y = 635
    qr_card_w = 680
    qr_card_h = 680
    cx = (W - qr_card_w) // 2
    draw.rounded_rectangle([cx, qr_card_y, cx + qr_card_w, qr_card_y + qr_card_h], radius=32, fill=COLOR_CARD_BG, outline=COLOR_BLUE, width=4)

    qr_img = create_base_qr(URL_TARGET, box_size=13, border=2, fill_color=COLOR_BLUE, back_color=COLOR_WHITE)
    qr_img = paste_center_logo(qr_img, LOGO_GOLD_PATH, scale_ratio=0.22, bg_circle=True, bg_color=COLOR_WHITE, border_color=COLOR_GOLD)
    qw, qh = qr_img.size
    img.paste(qr_img, (cx + (qr_card_w - qw) // 2, qr_card_y + 35), qr_img)

    cta_qr = "¡ESCANEA AQUÍ CON TU CÁMARA!"
    bbox_cq = draw.textbbox((0, 0), cta_qr, font=get_font(FONT_BOLD, 24))
    draw.text((cx + (qr_card_w - (bbox_cq[2]-bbox_cq[0])) // 2, qr_card_y + qh + 45), cta_qr, font=get_font(FONT_BOLD, 24), fill=COLOR_GOLD_DARK)

    sy = 1350
    sw = 535
    sh = 300

    # Sucursal Las Delicias
    sx1 = 60
    draw.rounded_rectangle([sx1, sy, sx1 + sw, sy + sh], radius=20, fill=COLOR_CARD_BG, outline=COLOR_BLUE, width=3)
    draw.rounded_rectangle([sx1, sy, sx1 + sw, sy + 55], radius=20, fill=COLOR_BLUE)
    draw.text((sx1 + 20, sy + 12), "📍 Sucursal Las Delicias", font=font_box_title, fill=COLOR_WHITE)
    draw.text((sx1 + 20, sy + 75), "Av. Revolución 1203, Cuadrante II", font=font_box_body, fill=COLOR_DARK)
    draw.text((sx1 + 20, sy + 105), "(A un lado de Centro de Salud San Joaquín)", font=get_font(FONT_BOLD, 17), fill=COLOR_GOLD_DARK)
    draw.text((sx1 + 20, sy + 140), "📞 Tel: 993 289 2935", font=font_box_body, fill=COLOR_DARK)
    draw.rounded_rectangle([sx1 + 20, sy + 180, sx1 + sw - 20, sy + 235], radius=12, fill=COLOR_GREEN)
    draw.text((sx1 + 35, sy + 195), "💬 WhatsApp: 993 289 2935", font=get_font(FONT_BOLD, 20), fill=COLOR_WHITE)
    draw.text((sx1 + 20, sy + 255), "🏬 Recolección en mostrador", font=get_font(FONT_BOLD, 18), fill=COLOR_DARK)

    # Sucursal Estrellas de Buena Vista
    sx2 = sx1 + sw + 50
    draw.rounded_rectangle([sx2, sy, sx2 + sw, sy + sh], radius=20, fill=COLOR_CARD_BG, outline=COLOR_BLUE, width=3)
    draw.rounded_rectangle([sx2, sy, sx2 + sw, sy + 55], radius=20, fill=COLOR_BLUE)
    draw.text((sx2 + 20, sy + 12), "📍 Suc. Buena Vista", font=font_box_title, fill=COLOR_WHITE)
    draw.text((sx2 + 20, sy + 75), "Carr. a La Isla Km 5.300, 1ra Secc", font=font_box_body, fill=COLOR_DARK)
    draw.text((sx2 + 20, sy + 105), "Buena Vista 1ra Secc, Villahermosa", font=get_font(FONT_BOLD, 17), fill=COLOR_GOLD_DARK)
    draw.text((sx2 + 20, sy + 140), "📞 Tel: 993 192 8313", font=font_box_body, fill=COLOR_DARK)
    draw.rounded_rectangle([sx2 + 20, sy + 180, sx2 + sw - 20, sy + 235], radius=12, fill=COLOR_GREEN)
    draw.text((sx2 + 35, sy + 195), "💬 WhatsApp: 993 192 8313", font=get_font(FONT_BOLD, 20), fill=COLOR_WHITE)
    draw.text((sx2 + 20, sy + 255), "🏬 Recolección en mostrador", font=get_font(FONT_BOLD, 18), fill=COLOR_DARK)

    draw.rectangle([0, H - 65, W, H], fill=COLOR_BLUE_DARK)
    f_txt = "ferreteriaytlapaleria-elaguila.com • ¡Tu ferretería de confianza en Tabasco!"
    bbox_f = draw.textbbox((0, 0), f_txt, font=get_font(FONT_BOLD, 20))
    draw.text(((W - (bbox_f[2]-bbox_f[0])) // 2, H - 45), f_txt, font=get_font(FONT_BOLD, 20), fill=COLOR_WHITE)

    out_path = os.path.join(OUTPUT_DIR, "qr-05-flyer-publicitario-mostrador.png")
    img.save(out_path, "PNG", dpi=(300, 300))
    print(f"   [OK] Guardado: {out_path}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"=== INICIANDO GENERACIÓN DE CÓDIGOS QR PARA FERRETERÍA EL ÁGUILA ===")
    print(f"URL de Destino: {URL_TARGET}")
    print(f"Directorio de Salida: {OUTPUT_DIR}")
    
    generate_format_1()
    generate_format_2()
    generate_format_3()
    generate_format_4()
    generate_format_5()

    print("=== TODOS LOS 5 FORMATOS DE CÓDIGOS QR GENERADOS CON ÉXITO ===")

if __name__ == "__main__":
    main()
