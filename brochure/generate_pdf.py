from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
BROCHURE_DIR = ROOT / "brochure"
OUTPUT = BROCHURE_DIR / "nicolas-martinez-brochure.pdf"
LOGO = ROOT / "images" / "logo-nicolas-martinez-apa.png"
HERO = ROOT / "images" / "hero-parcours-equilibre.png"
PHOTO = ROOT / "images" / "story-coach-halteres.png"

PAGE_W, PAGE_H = A4
MARGIN = 20
CONTENT_X = MARGIN
CONTENT_Y = MARGIN
CONTENT_W = PAGE_W - 2 * MARGIN
CONTENT_H = PAGE_H - 2 * MARGIN

BG = colors.HexColor("#FAFAF5")
SURFACE = colors.HexColor("#FFFFFF")
SAGE = colors.HexColor("#6B7B3C")
SAGE_LIGHT = colors.HexColor("#8FA058")
SAGE_SOFT = colors.HexColor("#EEF2E2")
TEXT = colors.HexColor("#23231F")
TEXT_MUTED = colors.HexColor("#5D5D50")
LINE = colors.HexColor("#DCE2CB")
SAND = colors.HexColor("#F1E3D3")
TERRACOTTA = colors.HexColor("#C67B5C")
CONTACT_BG = colors.HexColor("#F5EFE4")
CREAM = colors.HexColor("#FFF9F3")
SOFT_GREY = colors.HexColor("#FCFCF8")

PHONE = "06 78 23 58 75"
EMAIL = "martineznicolas13@gmail.com"
SITE_SHORT = "activite-physique-adaptee-nicolas-martinez.fr"


def round_rect(pdf, x, y, w, h, radius=18, fill=SURFACE, stroke=LINE, line_width=1):
    pdf.setLineWidth(line_width)
    pdf.setStrokeColor(stroke)
    pdf.setFillColor(fill)
    pdf.roundRect(x, y, w, h, radius, stroke=1, fill=1)


def draw_wrapped(pdf, text, x, y_top, width, font="Helvetica", size=10, color=TEXT_MUTED, leading=None, max_lines=None):
    pdf.setFont(font, size)
    pdf.setFillColor(color)
    leading = leading or size * 1.36
    lines = simpleSplit(text, font, size, width)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        if lines:
            lines[-1] = lines[-1].rstrip(" .") + "…"
    y = y_top
    for line in lines:
        pdf.drawString(x, y, line)
        y -= leading
    return y


def contain_image(pdf, image_path, x, y, w, h):
    reader = ImageReader(str(image_path))
    img_w, img_h = reader.getSize()
    scale = min(w / img_w, h / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    draw_x = x + (w - draw_w) / 2
    draw_y = y + (h - draw_h) / 2
    pdf.drawImage(reader, draw_x, draw_y, width=draw_w, height=draw_h, mask="auto")


def cover_image(pdf, image_path, x, y, w, h, radius=18):
    reader = ImageReader(str(image_path))
    img_w, img_h = reader.getSize()
    scale = max(w / img_w, h / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    draw_x = x + (w - draw_w) / 2
    draw_y = y + (h - draw_h) / 2

    pdf.saveState()
    path = pdf.beginPath()
    path.roundRect(x, y, w, h, radius)
    pdf.clipPath(path, stroke=0, fill=0)
    pdf.drawImage(reader, draw_x, draw_y, width=draw_w, height=draw_h, mask="auto")
    pdf.restoreState()


def pill(pdf, label, x, y, w, h, fill=SAGE_SOFT, stroke=colors.white, text_color=SAGE, font_size=8.5):
    pdf.setFillColor(fill)
    pdf.setStrokeColor(stroke)
    pdf.roundRect(x, y, w, h, h / 2, stroke=0, fill=1)
    pdf.setFillColor(text_color)
    pdf.setFont("Helvetica-Bold", font_size)
    text_y = y + (h - font_size) / 2 + 2
    text_width = pdf.stringWidth(label, "Helvetica-Bold", font_size)
    pdf.drawString(x + (w - text_width) / 2, text_y, label)


def card_title(pdf, label, title, x, y):
    pdf.setFillColor(SAGE)
    pdf.setFont("Helvetica-Bold", 7.8)
    pdf.drawString(x, y, label.upper())
    pdf.setFillColor(TEXT)
    pdf.setFont("Times-Bold", 14.2)
    pdf.drawString(x, y - 16, title)


def draw_bullets(pdf, items, x, y_top, width, size=8.4, leading=10.8, bullet_color=SAGE, gap=2):
    y = y_top
    for item in items:
        pdf.setFillColor(bullet_color)
        pdf.circle(x + 2.6, y - 3.2, 1.8, stroke=0, fill=1)
        y = draw_wrapped(pdf, item, x + 10, y, width - 10, size=size, color=TEXT_MUTED, leading=leading)
        y -= gap
    return y


def add_link(pdf, x, y, w, h, url):
    pdf.linkURL(url, (x, y, x + w, y + h), relative=0)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=A4)
    pdf.setTitle("Brochure Nicolas Martinez - Activité physique adaptée")
    pdf.setAuthor("Nous Hermes Agent")
    pdf.setSubject("Brochure une page - Nicolas Martinez APA")
    pdf.setKeywords("Nicolas Martinez, activité physique adaptée, APA, sport santé, brochure")

    pdf.setFillColor(BG)
    pdf.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    round_rect(pdf, CONTENT_X, CONTENT_Y, CONTENT_W, CONTENT_H, radius=28, fill=SURFACE, stroke=LINE)

    # Header
    header_y = PAGE_H - 76
    if LOGO.exists():
        contain_image(pdf, LOGO, CONTENT_X + 18, header_y - 4, 188, 46)
    else:
        pdf.setFillColor(TEXT)
        pdf.setFont("Times-Bold", 20)
        pdf.drawString(CONTENT_X + 20, header_y + 11, "Nicolas Martinez")
    pill(pdf, "Séance d'essai offerte", CONTENT_X + CONTENT_W - 182, header_y + 8, 156, 28)

    # Hero area
    left_x = CONTENT_X + 22
    title_top = PAGE_H - 124
    pdf.setFillColor(SAGE)
    pdf.setFont("Helvetica-Bold", 8.2)
    pdf.drawString(left_x, title_top, "SPORT SANTÉ · APA · SAINT-MAIME")

    pdf.setFillColor(TEXT)
    pdf.setFont("Times-Bold", 23.5)
    title_lines = simpleSplit(
        "Bouger mieux, reprendre confiance, préserver l'autonomie.",
        "Times-Bold",
        23.5,
        304,
    )
    y = title_top - 17
    for line in title_lines:
        pdf.drawString(left_x, y, line)
        y -= 25

    summary = (
        "Nicolas Martinez accompagne les personnes âgées, jeunes retraités et profils fragilisés avec des séances d'activité physique adaptée, progressives et rassurantes."
    )
    y = draw_wrapped(pdf, summary, left_x, y - 2, 308, size=9.8, leading=13.2, max_lines=4)

    chip_y = y - 8
    pill(pdf, "Domicile & extérieur", left_x, chip_y, 128, 21)
    pill(pdf, "EHPAD", left_x + 136, chip_y, 64, 21)
    pill(pdf, "Suivi progressif", left_x + 208, chip_y, 100, 21, fill=colors.HexColor("#F8EEE6"), text_color=TERRACOTTA)
    pill(pdf, "Autour de Saint-Maime", left_x, chip_y - 27, 148, 21, fill=colors.HexColor("#F8EEE6"), text_color=TERRACOTTA)
    pill(pdf, "1 page claire à partager", left_x + 156, chip_y - 27, 152, 21)

    hero_x = CONTENT_X + CONTENT_W - 206
    hero_y = 590
    hero_w = 184
    hero_h = 208
    round_rect(pdf, hero_x, hero_y, hero_w, hero_h, radius=20, fill=SAND, stroke=colors.HexColor("#E7D3BE"))
    if HERO.exists():
        cover_image(pdf, HERO, hero_x + 12, hero_y + hero_h - 118 - 12, hero_w - 24, 118, radius=16)
    pdf.setFillColor(TEXT)
    pdf.setFont("Times-Bold", 13.6)
    pdf.drawString(hero_x + 16, hero_y + 68, "En bref")
    draw_bullets(
        pdf,
        [
            "Domicile, extérieur ou EHPAD selon le besoin.",
            "Mobilité, équilibre, marche, respiration.",
            "Objectif : plus de stabilité et d'aisance au quotidien.",
        ],
        hero_x + 16,
        hero_y + 50,
        hero_w - 28,
        size=8.25,
        leading=10.2,
        gap=1,
    )

    # Row 2
    apa_x = CONTENT_X + 22
    apa_y = 474
    apa_w = 248
    apa_h = 96
    round_rect(pdf, apa_x, apa_y, apa_w, apa_h, radius=18, fill=SAGE_SOFT, stroke=LINE)
    card_title(pdf, "L'APA, c'est quoi ?", "Une activité utile et adaptée.", apa_x + 16, apa_y + apa_h - 18)
    draw_wrapped(
        pdf,
        "Une pratique pensée selon l'âge, la condition physique et le besoin du moment, sans logique de performance.",
        apa_x + 16,
        apa_y + 42,
        apa_w - 30,
        size=8.6,
        leading=11.2,
        max_lines=4,
    )

    publics_x = apa_x + apa_w + 12
    publics_y = apa_y
    publics_w = CONTENT_X + CONTENT_W - 22 - publics_x
    publics_h = 96
    round_rect(pdf, publics_x, publics_y, publics_w, publics_h, radius=18, fill=CREAM, stroke=colors.HexColor("#EEDCCB"))
    card_title(pdf, "Pour qui ?", "Des profils qui veulent rester actifs.", publics_x + 16, publics_y + publics_h - 18)
    draw_bullets(
        pdf,
        [
            "Seniors : équilibre, appuis et gestes du quotidien.",
            "Jeunes retraités : garder la forme ou reprendre en douceur.",
            "Fragilités / objectif santé : marche, coordination, effort progressif.",
        ],
        publics_x + 16,
        publics_y + 40,
        publics_w - 30,
        size=8.0,
        leading=9.8,
        gap=1,
    )

    # Services strip
    services_x = CONTENT_X + 22
    services_y = 352
    services_w = CONTENT_W - 44
    services_h = 108
    round_rect(pdf, services_x, services_y, services_w, services_h, radius=18, fill=SURFACE, stroke=LINE)
    card_title(pdf, "Accompagnements", "Des séances adaptées au quotidien.", services_x + 16, services_y + services_h - 18)

    service_items = [
        ("Domicile", "Cadre familier, rassurant et sur mesure."),
        ("Extérieur", "Marche, souffle et mobilité sans pression."),
        ("EHPAD", "Individuel, duo ou petit groupe selon le contexte."),
        ("Suivi", "Des séances qui évoluent avec les progrès."),
    ]
    box_w = (services_w - 16 * 5) / 4
    box_y = services_y + 14
    for index, (title, desc) in enumerate(service_items):
        box_x = services_x + 16 + index * (box_w + 16)
        round_rect(pdf, box_x, box_y, box_w, 54, radius=14, fill=SOFT_GREY, stroke=LINE, line_width=0.8)
        draw_wrapped(pdf, title, box_x + 10, box_y + 37, box_w - 18, font="Helvetica-Bold", size=8.9, color=TEXT, leading=10.4, max_lines=1)
        draw_wrapped(pdf, desc, box_x + 10, box_y + 18, box_w - 18, size=7.5, color=TEXT_MUTED, leading=9.0, max_lines=3)

    # Steps strip
    steps_x = CONTENT_X + 22
    steps_y = 252
    steps_w = CONTENT_W - 44
    steps_h = 84
    round_rect(pdf, steps_x, steps_y, steps_w, steps_h, radius=18, fill=colors.HexColor("#F7FAF0"), stroke=LINE)
    card_title(pdf, "Déroulé", "Un parcours simple et rassurant.", steps_x + 16, steps_y + steps_h - 18)
    steps = [
        ("01", "Échange", "Appel ou email pour comprendre le besoin."),
        ("02", "Essai", "Séance offerte pour faire le point."),
        ("03", "Plan", "Rythme et objectifs adaptés à la personne."),
        ("04", "Suivi", "Progression utile dans le quotidien."),
    ]
    step_w = (steps_w - 16 * 5) / 4
    for index, (number, title, desc) in enumerate(steps):
        step_x = steps_x + 16 + index * (step_w + 16)
        pdf.setFillColor(SAGE)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(step_x, steps_y + 40, number)
        pdf.setFillColor(TEXT)
        pdf.setFont("Helvetica-Bold", 8.7)
        pdf.drawString(step_x + 24, steps_y + 40, title)
        draw_wrapped(pdf, desc, step_x, steps_y + 23, step_w - 2, size=7.5, color=TEXT_MUTED, leading=8.8, max_lines=3)

    # Bottom row
    bio_x = CONTENT_X + 22
    bio_y = 116
    bio_w = 248
    bio_h = 122
    round_rect(pdf, bio_x, bio_y, bio_w, bio_h, radius=18, fill=colors.HexColor("#FFFDF8"), stroke=colors.HexColor("#EEDCCB"))
    card_title(pdf, "Qui suis-je ?", "Nicolas Martinez", bio_x + 16, bio_y + bio_h - 18)

    photo_x = bio_x + 16
    photo_y = bio_y + 16
    photo_w = 76
    photo_h = 72
    round_rect(pdf, photo_x, photo_y, photo_w, photo_h, radius=16, fill=SAGE_SOFT, stroke=LINE, line_width=0.8)
    if PHOTO.exists():
        cover_image(pdf, PHOTO, photo_x, photo_y, photo_w, photo_h, radius=16)
    pill(pdf, "APA & santé", photo_x + 4, photo_y + 5, 68, 15, fill=colors.Color(1, 1, 1, alpha=0.9), stroke=colors.Color(1, 1, 1, alpha=0), text_color=SAGE, font_size=7.0)

    bio_text_x = photo_x + photo_w + 12
    draw_wrapped(
        pdf,
        "Licence APA-Santé et près de 10 ans d'accompagnement, avec une approche fondée sur l'écoute, la patience et l'adaptation réelle à la personne.",
        bio_text_x,
        bio_y + 74,
        bio_w - (bio_text_x - bio_x) - 14,
        size=7.95,
        leading=9.5,
        max_lines=6,
    )

    contact_x = bio_x + bio_w + 12
    contact_y = bio_y
    contact_w = CONTENT_X + CONTENT_W - 22 - contact_x
    contact_h = 122
    round_rect(pdf, contact_x, contact_y, contact_w, contact_h, radius=18, fill=CONTACT_BG, stroke=colors.HexColor("#E7D7C3"))
    card_title(pdf, "Contact & zone", "Parlons de votre besoin.", contact_x + 16, contact_y + contact_h - 18)
    draw_wrapped(
        pdf,
        "Saint-Maime, Forcalquier, Volx, Manosque, Villeneuve, Pierrevert, Mane et communes proches.",
        contact_x + 16,
        contact_y + 64,
        contact_w - 32,
        size=8.3,
        leading=10.6,
        max_lines=3,
    )
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica-Bold", 8.2)
    pdf.drawString(contact_x + 16, contact_y + 34, "TÉLÉPHONE")
    pdf.drawString(contact_x + 16, contact_y + 16, PHONE)
    pdf.drawString(contact_x + 114, contact_y + 34, "EMAIL")
    pdf.drawString(contact_x + 114, contact_y + 16, EMAIL)
    add_link(pdf, contact_x + 16, contact_y + 8, 84, 16, "tel:0678235875")
    add_link(pdf, contact_x + 114, contact_y + 8, 128, 16, f"mailto:{EMAIL}")

    # Footer strip
    footer_x = CONTENT_X + 22
    footer_y = 58
    footer_w = CONTENT_W - 44
    footer_h = 38
    round_rect(pdf, footer_x, footer_y, footer_w, footer_h, radius=14, fill=colors.HexColor("#F4F7EC"), stroke=LINE)
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica-Bold", 9.0)
    pdf.drawString(footer_x + 14, footer_y + 22, "APA & sport santé · Écoute, progression, autonomie")
    pdf.setFont("Helvetica", 8.2)
    pdf.setFillColor(TEXT_MUTED)
    pdf.drawString(footer_x + 14, footer_y + 9, f"{SITE_SHORT} · {PHONE}")
    add_link(pdf, footer_x + 182, footer_y + 2, 84, 16, "tel:0678235875")

    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
