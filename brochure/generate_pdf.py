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

PAGE_W, PAGE_H = A4
MARGIN = 24
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

PHONE = "06 78 23 58 75"
EMAIL = "martineznicolas13@gmail.com"
SITE = "https://www.activite-physique-adaptee-nicolas-martinez.fr/"
BROCHURE_PAGE = SITE + "brochure/"
BROCHURE_PDF = BROCHURE_PAGE + "nicolas-martinez-brochure.pdf"


def round_rect(pdf, x, y, w, h, radius=18, fill=SURFACE, stroke=LINE, line_width=1):
    pdf.setLineWidth(line_width)
    pdf.setStrokeColor(stroke)
    pdf.setFillColor(fill)
    pdf.roundRect(x, y, w, h, radius, stroke=1, fill=1)


def draw_wrapped(pdf, text, x, y_top, width, font="Helvetica", size=10, color=TEXT_MUTED, leading=None, max_lines=None):
    pdf.setFont(font, size)
    pdf.setFillColor(color)
    leading = leading or size * 1.38
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


def fit_image(pdf, image_path, x, y, w, h):
    reader = ImageReader(str(image_path))
    img_w, img_h = reader.getSize()
    scale = min(w / img_w, h / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    draw_x = x + (w - draw_w) / 2
    draw_y = y + (h - draw_h) / 2
    pdf.drawImage(reader, draw_x, draw_y, width=draw_w, height=draw_h, mask="auto")


def pill(pdf, label, x, y, w, h, fill=SAGE_SOFT, stroke=colors.white, text_color=SAGE, font_size=9):
    pdf.setFillColor(fill)
    pdf.setStrokeColor(stroke)
    pdf.roundRect(x, y, w, h, h / 2, stroke=0, fill=1)
    pdf.setFillColor(text_color)
    pdf.setFont("Helvetica-Bold", font_size)
    text_y = y + (h - font_size) / 2 + 2
    text_width = pdf.stringWidth(label, "Helvetica-Bold", font_size)
    pdf.drawString(x + (w - text_width) / 2, text_y, label)


def card_title(pdf, label, title, x, y, w):
    pdf.setFillColor(SAGE)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(x, y, label.upper())
    pdf.setFillColor(TEXT)
    pdf.setFont("Times-Bold", 15)
    pdf.drawString(x, y - 18, title)


def draw_bullets(pdf, items, x, y_top, width, size=9.2, leading=14):
    y = y_top
    for item in items:
        pdf.setFillColor(SAGE)
        pdf.circle(x + 3, y - 4, 2.2, stroke=0, fill=1)
        y = draw_wrapped(pdf, item, x + 12, y, width - 12, size=size, color=TEXT_MUTED, leading=leading)
        y -= 3
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

    # Main panel
    round_rect(pdf, CONTENT_X, CONTENT_Y, CONTENT_W, CONTENT_H, radius=28, fill=SURFACE, stroke=LINE)

    # Header
    header_y = PAGE_H - 78
    if LOGO.exists():
        fit_image(pdf, LOGO, CONTENT_X + 18, header_y - 6, 184, 46)
    else:
        pdf.setFillColor(TEXT)
        pdf.setFont("Times-Bold", 20)
        pdf.drawString(CONTENT_X + 22, header_y + 12, "Nicolas Martinez")
    pill(pdf, "Séance d'essai offerte", CONTENT_X + CONTENT_W - 180, header_y + 8, 154, 28)

    # Title / lead block
    left_x = CONTENT_X + 22
    title_top = PAGE_H - 126
    pdf.setFillColor(SAGE)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(left_x, title_top, "SPORT SANTÉ · APA · SAINT-MAIME")

    pdf.setFillColor(TEXT)
    pdf.setFont("Times-Bold", 25)
    title_lines = simpleSplit(
        "Bouger mieux, retrouver confiance, préserver votre autonomie.",
        "Times-Bold",
        25,
        300,
    )
    y = title_top - 18
    for line in title_lines:
        pdf.drawString(left_x, y, line)
        y -= 28

    summary = (
        "Accompagnement sérieux, chaleureux et réellement adapté pour les personnes âgées, jeunes retraités "
        "et toute personne qui souhaite reprendre une activité en douceur, améliorer son équilibre ou retrouver "
        "plus d'aisance au quotidien."
    )
    y = draw_wrapped(pdf, summary, left_x, y - 4, 308, size=10.2, leading=14.4)

    chip_y = y - 8
    pill(pdf, "À domicile & en extérieur", left_x, chip_y, 136, 22, fill=SAGE_SOFT, text_color=SAGE, font_size=8.5)
    pill(pdf, "EHPAD possible", left_x + 144, chip_y, 90, 22, fill=SAGE_SOFT, text_color=SAGE, font_size=8.5)
    pill(pdf, "Suivi progressif", left_x, chip_y - 28, 110, 22, fill=colors.HexColor("#F8EEE6"), text_color=TERRACOTTA, font_size=8.5)
    pill(pdf, "20 à 30 km autour de Saint-Maime", left_x + 118, chip_y - 28, 190, 22, fill=colors.HexColor("#F8EEE6"), text_color=TERRACOTTA, font_size=8.5)

    # Hero right panel
    hero_x = CONTENT_X + CONTENT_W - 210
    hero_y = PAGE_H - 334
    hero_w = 188
    hero_h = 238
    round_rect(pdf, hero_x, hero_y, hero_w, hero_h, radius=22, fill=SAND, stroke=colors.HexColor("#E7D3BE"))
    image_h = 128
    pdf.saveState()
    path = pdf.beginPath()
    path.roundRect(hero_x + 12, hero_y + hero_h - image_h - 12, hero_w - 24, image_h, 18)
    pdf.clipPath(path, stroke=0, fill=0)
    if HERO.exists():
        fit_image(pdf, HERO, hero_x + 12, hero_y + hero_h - image_h - 12, hero_w - 24, image_h)
    pdf.restoreState()
    pdf.setFillColor(TEXT)
    pdf.setFont("Times-Bold", 14)
    pdf.drawString(hero_x + 16, hero_y + 78, "En bref")
    draw_wrapped(pdf, "Domicile, extérieur ou EHPAD selon le besoin, le rythme et le contexte.", hero_x + 16, hero_y + 60, hero_w - 32, size=9.2, leading=12.8)
    draw_wrapped(pdf, "Objectif : mobilité, équilibre, marche, respiration, confiance et autonomie.", hero_x + 16, hero_y + 26, hero_w - 32, size=9.2, leading=12.8)

    # APA definition card
    apa_x = CONTENT_X + 22
    apa_y = 466
    apa_w = 256
    apa_h = 108
    round_rect(pdf, apa_x, apa_y, apa_w, apa_h, radius=18, fill=SAGE_SOFT, stroke=LINE)
    card_title(pdf, "L'APA, c'est quoi ?", "Une activité utile et personnalisée.", apa_x + 16, apa_y + apa_h - 20, apa_w - 32)
    draw_wrapped(
        pdf,
        "Bouger sans logique de performance, avec un cadre progressif, rassurant et adapté à l'âge, à la condition physique et aux objectifs du moment.",
        apa_x + 16,
        apa_y + 48,
        apa_w - 30,
        size=9.1,
        leading=12.8,
        max_lines=4,
    )

    # Publics card
    publics_x = apa_x + apa_w + 12
    publics_y = apa_y
    publics_w = CONTENT_X + CONTENT_W - 22 - publics_x
    publics_h = 108
    round_rect(pdf, publics_x, publics_y, publics_w, publics_h, radius=18, fill=colors.HexColor("#FFF9F3"), stroke=colors.HexColor("#EEDCCB"))
    card_title(pdf, "Pour qui ?", "Des profils qui veulent rester actifs.", publics_x + 16, publics_y + publics_h - 20, publics_w - 32)
    draw_bullets(
        pdf,
        [
            "Personnes âgées : autonomie, équilibre et gestes du quotidien.",
            "Jeunes retraités : garder la forme et reprendre sans pression.",
            "Fragilités ou objectif santé : marche, coordination, effort progressif.",
        ],
        publics_x + 16,
        publics_y + 48,
        publics_w - 30,
        size=8.5,
        leading=11.2,
    )

    # Services strip
    services_x = CONTENT_X + 22
    services_y = 344
    services_w = CONTENT_W - 44
    services_h = 106
    round_rect(pdf, services_x, services_y, services_w, services_h, radius=18, fill=SURFACE, stroke=LINE)
    card_title(pdf, "Accompagnements", "Des séances adaptées au quotidien.", services_x + 16, services_y + services_h - 18, services_w - 32)

    service_items = [
        ("Séances individuelles à domicile", "Environnement familier, rassurant et sur mesure."),
        ("Séances en extérieur", "Marche, respiration et mobilité sans logique de performance."),
        ("Interventions en EHPAD", "En individuel, en couple ou en petit groupe selon le besoin."),
        ("Suivi dans le temps", "Des progrès concrets, utiles et durables au quotidien."),
    ]
    box_w = (services_w - 16 * 5) / 4
    box_y = services_y + 14
    for index, (title, desc) in enumerate(service_items):
        box_x = services_x + 16 + index * (box_w + 16)
        round_rect(pdf, box_x, box_y, box_w, 48, radius=14, fill=colors.HexColor("#FCFCF9"), stroke=LINE, line_width=0.8)
        pdf.setFillColor(TEXT)
        pdf.setFont("Helvetica-Bold", 8.8)
        draw_wrapped(pdf, title, box_x + 10, box_y + 34, box_w - 18, font="Helvetica-Bold", size=8.8, color=TEXT, leading=10.8, max_lines=2)
        draw_wrapped(pdf, desc, box_x + 10, box_y + 14, box_w - 18, size=7.8, color=TEXT_MUTED, leading=9.6, max_lines=2)

    # Steps strip
    steps_x = CONTENT_X + 22
    steps_y = 246
    steps_w = CONTENT_W - 44
    steps_h = 84
    round_rect(pdf, steps_x, steps_y, steps_w, steps_h, radius=18, fill=colors.HexColor("#F7FAF0"), stroke=LINE)
    card_title(pdf, "Déroulé", "Un parcours simple et rassurant.", steps_x + 16, steps_y + steps_h - 18, steps_w - 32)
    steps = [
        ("01", "Premier échange", "Besoin présenté par téléphone, email ou message."),
        ("02", "Essai offert", "Observation de la situation et premiers repères."),
        ("03", "Plan adapté", "Cadre pensé selon niveau, objectif et rythme de vie."),
        ("04", "Suivi", "Les séances évoluent pour installer des progrès utiles."),
    ]
    step_w = (steps_w - 16 * 5) / 4
    for index, (number, title, desc) in enumerate(steps):
        x = steps_x + 16 + index * (step_w + 16)
        pdf.setFillColor(SAGE)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(x, steps_y + 42, number)
        pdf.setFillColor(TEXT)
        pdf.setFont("Helvetica-Bold", 8.8)
        pdf.drawString(x + 24, steps_y + 42, title)
        draw_wrapped(pdf, desc, x, steps_y + 25, step_w - 2, size=7.8, color=TEXT_MUTED, leading=9.2, max_lines=3)

    # Bottom cards
    bio_x = CONTENT_X + 22
    bio_y = 118
    bio_w = 250
    bio_h = 112
    round_rect(pdf, bio_x, bio_y, bio_w, bio_h, radius=18, fill=colors.HexColor("#FFFDF8"), stroke=colors.HexColor("#EEDCCB"))
    card_title(pdf, "Qui suis-je ?", "Nicolas Martinez", bio_x + 16, bio_y + bio_h - 20, bio_w - 32)
    draw_wrapped(
        pdf,
        "Titulaire d'une licence d'enseignant en activité physique adaptée et santé, j'accompagne depuis près de 10 ans avec patience, empathie et une vraie adaptation à la personne.",
        bio_x + 16,
        bio_y + 52,
        bio_w - 30,
        size=8.9,
        leading=11.8,
        max_lines=5,
    )

    contact_x = bio_x + bio_w + 12
    contact_y = bio_y
    contact_w = CONTENT_X + CONTENT_W - 22 - contact_x
    contact_h = 112
    round_rect(pdf, contact_x, contact_y, contact_w, contact_h, radius=18, fill=CONTACT_BG, stroke=colors.HexColor("#E7D7C3"))
    card_title(pdf, "Contact & zone", "Parlons de votre besoin.", contact_x + 16, contact_y + contact_h - 20, contact_w - 32)
    draw_wrapped(pdf, "Saint-Maime (04300) · Forcalquier · Volx · Manosque · Villeneuve · Pierrevert · Mane et environs.", contact_x + 16, contact_y + 54, contact_w - 32, size=8.9, leading=11.8, max_lines=3)
    pdf.setFont("Helvetica-Bold", 9.2)
    pdf.setFillColor(TEXT)
    pdf.drawString(contact_x + 16, contact_y + 22, PHONE)
    pdf.drawString(contact_x + 120, contact_y + 22, EMAIL)
    add_link(pdf, contact_x + 16, contact_y + 14, 88, 16, "tel:0678235875")
    add_link(pdf, contact_x + 120, contact_y + 14, 150, 16, f"mailto:{EMAIL}")

    # Footer strip
    footer_x = CONTENT_X + 22
    footer_y = 54
    footer_w = CONTENT_W - 44
    footer_h = 42
    round_rect(pdf, footer_x, footer_y, footer_w, footer_h, radius=16, fill=colors.HexColor("#F4F7EC"), stroke=LINE)
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(footer_x + 14, footer_y + 25, "Brochure publique :")
    pdf.setFont("Helvetica", 8.8)
    pdf.drawString(footer_x + 92, footer_y + 25, "activite-physique-adaptee-nicolas-martinez.fr/brochure/")
    pdf.drawString(footer_x + 14, footer_y + 11, "PDF direct :")
    pdf.drawString(footer_x + 92, footer_y + 11, "activite-physique-adaptee-nicolas-martinez.fr/brochure/nicolas-martinez-brochure.pdf")
    add_link(pdf, footer_x + 92, footer_y + 18, 260, 12, BROCHURE_PAGE)
    add_link(pdf, footer_x + 92, footer_y + 4, 340, 12, BROCHURE_PDF)

    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
