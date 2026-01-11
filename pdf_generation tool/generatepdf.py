# generate_email_template_pdf_v2.py
# pip install reportlab

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT_PDF = "email_template.pdf"
LOGO_FILE = "logo.png"

PAGE_LABELS = [
    ("Imobiliare.ro", "imobiliare"),
    ("OLX", "olx"),
    ("Storia", "storia"),
]

# ---- Styling (tweak here) ----
ACCENT = colors.HexColor("#F2B6B6")     # very pale red
BORDER = colors.HexColor("#D9D9D9")     # light grey
TEXT = colors.HexColor("#1A1A1A")
MUTED = colors.HexColor("#666666")
FIELD_BORDER = colors.HexColor("#CFCFCF")
FIELD_BG = colors.HexColor("#FFFFFF")
HEADER_BG = colors.HexColor("#FAFAFA")

# Try to register a Unicode font (fixes black squares for diacritics)
def register_unicode_font():
    # Common paths on Windows for DejaVu (often shipped with Python, or can be installed)
    candidate_paths = [
        os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf"),
        r"C:\Windows\Fonts\DejaVuSans.ttf",
        r"C:\Windows\Fonts\dejavusans.ttf",
        r"C:\Windows\Fonts\arial.ttf",  # fallback (usually has RO diacritics)
    ]

    for p in candidate_paths:
        if os.path.exists(p):
            font_name = "AppFont"
            pdfmetrics.registerFont(TTFont(font_name, p))
            return font_name, p

    # Last resort: Helvetica (may cause squares for diacritics)
    return "Helvetica", None


def draw_border_and_background(c: canvas.Canvas, w: float, h: float):
    margin = 14 * mm

    # Page background (subtle)
    c.setFillColor(colors.white)
    c.rect(0, 0, w, h, stroke=0, fill=1)

    # Outer border
    c.setStrokeColor(BORDER)
    c.setLineWidth(1.2)
    c.rect(margin, margin, w - 2 * margin, h - 2 * margin, stroke=1, fill=0)

    # Accent top line
    c.setStrokeColor(ACCENT)
    c.setLineWidth(3.0)
    c.line(margin, h - margin, w - margin, h - margin)


def draw_header(c: canvas.Canvas, w: float, h: float, title: str, font: str, logo_path: str | None):
    margin = 18 * mm
    header_h = 22 * mm
    top = h - margin

    # Header band
    c.setFillColor(HEADER_BG)
    c.setStrokeColor(colors.transparent)
    c.rect(margin, top - header_h, w - 2 * margin, header_h, stroke=0, fill=1)

    # Left: Title
    c.setFillColor(TEXT)
    c.setFont(font, 16)
    c.drawString(margin + 10, top - 15, f"Raport platformă: {title}")

    c.setFont(font, 9.5)
    c.setFillColor(MUTED)
    c.drawString(margin + 10, top - 30, "Template PDF (fillable) pentru email — completare din UiPath")

    # Right: Logo slot (optional)
    logo_box_w = 30 * mm
    logo_box_h = 14 * mm
    logo_x = w - margin - logo_box_w - 10
    logo_y = top - header_h + (header_h - logo_box_h) / 2

    if logo_path and os.path.exists(logo_path):
        try:
            img = ImageReader(logo_path)
            c.drawImage(img, logo_x, logo_y, width=logo_box_w, height=logo_box_h, preserveAspectRatio=True, mask="auto")
        except Exception:
            # If image fails, draw placeholder box
            c.setStrokeColor(FIELD_BORDER)
            c.setLineWidth(1)
            c.rect(logo_x, logo_y, logo_box_w, logo_box_h, stroke=1, fill=0)
            c.setFont(font, 8.5)
            c.setFillColor(MUTED)
            c.drawString(logo_x + 4, logo_y + 4, "LOGO")
    else:
        # Placeholder
        c.setStrokeColor(FIELD_BORDER)
        c.setLineWidth(1)
        c.rect(logo_x, logo_y, logo_box_w, logo_box_h, stroke=1, fill=0)
        c.setFont(font, 8.5)
        c.setFillColor(MUTED)
        c.drawString(logo_x + 4, logo_y + 4, "LOGO")


def add_label(c: canvas.Canvas, x: float, y: float, text: str, font: str):
    c.setFont(font, 11.5)
    c.setFillColor(TEXT)
    c.drawString(x, y, text)


def add_multiline_field(c: canvas.Canvas, name: str, x: float, y: float, width: float, height: float, font: str):
    """
    IMPORTANT: ReportLab AcroForm fields only support the standard 14 fonts.
    So we force Helvetica for form fields, while using 'font' for drawn text elsewhere.
    """
    c.acroForm.textfield(
        name=name,
        tooltip=name,
        x=x,
        y=y,
        width=width,
        height=height,
        borderStyle="inset",
        borderWidth=1,
        borderColor=FIELD_BORDER,
        fillColor=FIELD_BG,
        textColor=TEXT,
        fontName="Helvetica",  # <-- MUST be one of standard 14 for AcroForm
        fontSize=10,
        value="",
        fieldFlags=4096,       # multiline
    )



def main():
    font, font_path = register_unicode_font()
    print(f"Using font: {font}" + (f" ({font_path})" if font_path else " (built-in)"))

    w, h = A4
    c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
    c.setTitle("Email Template (Imobiliare / OLX / Storia)")

    logo_path = os.path.join(os.path.dirname(__file__), LOGO_FILE)

    for display_title, key in PAGE_LABELS:
        draw_border_and_background(c, w, h)
        draw_header(c, w, h, display_title, font, logo_path)

        margin = 18 * mm
        content_left = margin + 10
        content_right = w - margin - 10
        content_w = content_right - content_left

        # Content area below header
        header_bottom = h - margin - (22 * mm) - 8 * mm
        bottom_margin = margin + 10

        content_h = header_bottom - bottom_margin

        # Layout: AI summary smaller, Listings bigger
        # e.g. 35% summary, 60% listings, 5% gap
        gap = 8 * mm
        summary_h = content_h * 0.35
        listings_h = content_h - summary_h - gap

        # Summary field (top)
        label1_y = header_bottom - 12
        field1_y = header_bottom - 12 - 6 - summary_h

        add_label(c, content_left, label1_y, "AI summary (text generat de AI)", font)
        add_multiline_field(
            c,
            name=f"{key}_ai_summary",
            x=content_left,
            y=field1_y,
            width=content_w,
            height=summary_h,
            font=font,
        )

        # Listings field (bottom)
        label2_y = field1_y - gap - 12
        field2_y = label2_y - 6 - listings_h

        add_label(c, content_left, label2_y, "Anunțuri + link-uri (ex: titlu + preț + URL)", font)
        add_multiline_field(
            c,
            name=f"{key}_listings_links",
            x=content_left,
            y=field2_y,
            width=content_w,
            height=listings_h,
            font=font,
        )

        # Small footer (optional)
        c.setFont(font, 8.5)
        c.setFillColor(MUTED)
        c.drawString(content_left, margin + 2, f"Fields: {key}_ai_summary, {key}_listings_links")

        c.showPage()

    c.save()
    print(f"Generated: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
