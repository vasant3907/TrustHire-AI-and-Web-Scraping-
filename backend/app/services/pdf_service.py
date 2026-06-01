import json
from io import BytesIO


PAGE_WIDTH = 612
PAGE_HEIGHT = 792
MARGIN_X = 42
CONTENT_WIDTH = PAGE_WIDTH - (MARGIN_X * 2)
BOTTOM_Y = 58

COLORS = {
    "navy": (15, 23, 42),
    "blue": (29, 78, 216),
    "sky": (219, 234, 254),
    "red": (185, 28, 28),
    "red_bg": (254, 242, 242),
    "amber": (194, 65, 12),
    "amber_bg": (255, 247, 237),
    "emerald": (4, 120, 87),
    "emerald_bg": (236, 253, 245),
    "slate": (51, 65, 85),
    "muted": (100, 116, 139),
    "border": (226, 232, 240),
    "panel": (248, 250, 252),
    "white": (255, 255, 255),
}


def build_report_pdf(report) -> bytes:
    intelligence = _loads(report.company_intelligence, {})
    keywords = _loads(report.suspicious_keywords, [])
    reviews = intelligence.get("reviews") or []

    doc = _PdfDoc(report)
    doc.add_cover_header()
    doc.add_score_grid()
    doc.add_risk_overview()
    doc.add_panel(
        "AI Explanation",
        report.ai_summary or "No AI explanation available.",
        accent="blue",
    )
    doc.add_panel(
        "Recommended Action",
        report.recommendation or "No recommendation available.",
        accent=_risk_accent(report.risk_level),
    )
    doc.add_panel(
        "Public Review Summary",
        report.review_summary or "No public review summary available.",
        accent="emerald",
    )
    doc.add_keyword_panel(keywords)
    doc.add_intelligence_table(report, intelligence, reviews)
    doc.add_review_cards(reviews)
    doc.finish()
    return doc.render()


class _PdfDoc:
    def __init__(self, report):
        self.report = report
        self.pages = []
        self.page = self._new_page()

    def _new_page(self):
        return {"commands": [], "y": 720}

    def new_page(self):
        self.add_footer()
        self.pages.append(self.page)
        self.page = self._new_page()
        self.add_repeat_header()

    def ensure(self, height):
        if self.page["y"] - height < BOTTOM_Y:
            self.new_page()

    def add_cover_header(self):
        risk = (self.report.risk_level or "unknown").title()
        risk_color = COLORS.get(_risk_accent(self.report.risk_level), COLORS["amber"])

        _rect(self.page, 0, 650, PAGE_WIDTH, 142, *COLORS["navy"])
        _rect(self.page, 0, 650, 10, 142, *COLORS["blue"])
        _text(self.page, "TRUSTHIRE AI", MARGIN_X, 746, 11, "F2", *COLORS["sky"])
        _text(self.page, "Job Scam Detection Report", MARGIN_X, 718, 25, "F2", *COLORS["white"])
        _text(self.page, "AI-backed risk analysis, public web signals, and practical verification guidance.", MARGIN_X, 696, 10, "F1", *COLORS["sky"])

        _round_pill(self.page, 444, 732, 120, 28, risk_color, f"{risk} Risk", COLORS["white"])
        _text(self.page, f"Report #{self.report.id}", 444, 704, 10, "F2", *COLORS["white"])
        created = self.report.created_at.strftime("%d %b %Y, %I:%M %p") if self.report.created_at else "Generated report"
        _text(self.page, created, 444, 687, 8, "F1", *COLORS["sky"])
        self.page["y"] = 618

    def add_repeat_header(self):
        _text(self.page, "TrustHire AI Report", MARGIN_X, 758, 14, "F2", *COLORS["navy"])
        _text(self.page, f"Report #{self.report.id}", 492, 758, 9, "F1", *COLORS["muted"])
        _line(self.page, MARGIN_X, 742, PAGE_WIDTH - MARGIN_X, 742, *COLORS["border"])
        self.page["y"] = 710

    def add_score_grid(self):
        cards = [
            ("Trust Score", f"{round(self.report.trust_score or 0)}%", "blue", "Higher is safer"),
            ("Scam Probability", f"{round(self.report.scam_probability or 0)}%", "red", "Lower is safer"),
            ("Risk Level", (self.report.risk_level or "unknown").title(), _risk_accent(self.report.risk_level), "Current verdict"),
            ("Company Presence", f"{round(self.report.company_presence_score or 0)}%", "emerald", "Public signal score"),
        ]
        card_w = (CONTENT_WIDTH - 18) / 4
        x = MARGIN_X
        y = self.page["y"] - 78
        for title, value, color_key, caption in cards:
            _card(self.page, x, y, card_w, 70)
            _text(self.page, title, x + 10, y + 48, 8, "F2", *COLORS["muted"])
            _text(self.page, value, x + 10, y + 24, 20, "F2", *COLORS[color_key])
            _text(self.page, caption, x + 10, y + 10, 7, "F1", *COLORS["muted"])
            x += card_w + 6
        self.page["y"] = y - 22

    def add_risk_overview(self):
        trust = max(0, min(100, float(self.report.trust_score or 0)))
        scam = max(0, min(100, float(self.report.scam_probability or 0)))
        self.ensure(102)
        y = self.page["y"] - 94
        _card(self.page, MARGIN_X, y, CONTENT_WIDTH, 92)
        _text(self.page, "Executive Risk Overview", MARGIN_X + 16, y + 65, 14, "F2", *COLORS["navy"])
        _text(self.page, "Use this summary before sharing documents, paying fees, or continuing with a recruiter.", MARGIN_X + 16, y + 47, 9, "F1", *COLORS["muted"])
        self._bar(MARGIN_X + 16, y + 24, 210, "Trust", trust, "blue")
        self._bar(MARGIN_X + 270, y + 24, 210, "Scam", scam, "red")
        self.page["y"] = y - 18

    def _bar(self, x, y, width, label, value, color_key):
        _text(self.page, f"{label} {round(value)}%", x, y + 18, 8, "F2", *COLORS["slate"])
        _rect(self.page, x, y, width, 8, *COLORS["border"])
        _rect(self.page, x, y, width * value / 100, 8, *COLORS[color_key])

    def add_panel(self, title, body, accent="blue"):
        lines = _wrap_text(str(body), 92)
        while lines:
            max_lines = min(len(lines), max(4, int((self.page["y"] - BOTTOM_Y - 58) / 13)))
            chunk = lines[:max_lines]
            panel_h = 44 + (len(chunk) * 13)
            self.ensure(panel_h + 14)
            y = self.page["y"] - panel_h
            _card(self.page, MARGIN_X, y, CONTENT_WIDTH, panel_h)
            _rect(self.page, MARGIN_X, y, 5, panel_h, *COLORS[accent])
            _text(self.page, title, MARGIN_X + 16, y + panel_h - 25, 13, "F2", *COLORS["navy"])
            text_y = y + panel_h - 44
            for line in chunk:
                _text(self.page, line, MARGIN_X + 16, text_y, 9, "F1", *COLORS["slate"])
                text_y -= 13
            self.page["y"] = y - 16
            lines = lines[max_lines:]
            if lines:
                self.new_page()

    def add_keyword_panel(self, keywords):
        label = ", ".join(keywords) if keywords else "No suspicious keywords detected."
        self.add_panel("Suspicious Keywords", label, accent="red" if keywords else "emerald")

    def add_intelligence_table(self, report, intelligence, reviews):
        rows = [
            ("Website", intelligence.get("website") or "Not found"),
            ("LinkedIn", intelligence.get("linkedin_url") or "Public listing not found"),
            ("Naukri", intelligence.get("naukri_url") or "Public listing not found"),
            ("Public Reviews", f"{len(reviews)} reachable review link(s)"),
            ("Salary Signal", report.salary_validity or "unknown"),
            ("Email Signal", report.email_validity or "unknown"),
        ]
        self.ensure(190)
        panel_h = 40 + len(rows) * 23
        y = self.page["y"] - panel_h
        _card(self.page, MARGIN_X, y, CONTENT_WIDTH, panel_h)
        _rect(self.page, MARGIN_X, y, 5, panel_h, *COLORS["emerald"])
        _text(self.page, "Company Web Intelligence", MARGIN_X + 16, y + panel_h - 25, 13, "F2", *COLORS["navy"])
        row_y = y + panel_h - 50
        for index, (key, value) in enumerate(rows):
            if index % 2 == 0:
                _rect(self.page, MARGIN_X + 12, row_y - 5, CONTENT_WIDTH - 24, 19, *COLORS["panel"])
            _text(self.page, key, MARGIN_X + 22, row_y, 8, "F2", *COLORS["muted"])
            for offset, line in enumerate(_wrap_text(str(value), 62)[:2]):
                _text(self.page, line, MARGIN_X + 155, row_y - (offset * 10), 8, "F1", *COLORS["slate"])
            row_y -= 23
        self.page["y"] = y - 16

    def add_review_cards(self, reviews):
        if not reviews:
            return
        self.ensure(70)
        _text(self.page, "Public Review Snippets", MARGIN_X, self.page["y"], 13, "F2", *COLORS["navy"])
        self.page["y"] -= 18
        for review in reviews[:5]:
            title = review.get("title") or review.get("review_source") or "Public review"
            snippet = review.get("snippet") or review.get("url") or ""
            lines = _wrap_text(f"{title}: {snippet}", 88)[:4]
            h = 26 + len(lines) * 12
            self.ensure(h + 8)
            y = self.page["y"] - h
            _card(self.page, MARGIN_X, y, CONTENT_WIDTH, h, fill=COLORS["white"])
            _rect(self.page, MARGIN_X, y, 4, h, *COLORS["blue"])
            text_y = y + h - 18
            for line in lines:
                _text(self.page, line, MARGIN_X + 14, text_y, 8, "F1", *COLORS["slate"])
                text_y -= 12
            self.page["y"] = y - 8

    def add_footer(self):
        _line(self.page, MARGIN_X, 42, PAGE_WIDTH - MARGIN_X, 42, *COLORS["border"])
        _text(self.page, "Generated by TrustHire AI. Verify risky opportunities through official company channels before acting.", MARGIN_X, 26, 7, "F1", *COLORS["muted"])

    def finish(self):
        self.add_footer()
        self.pages.append(self.page)

    def render(self):
        return _render_pdf(self.pages)


def _risk_accent(risk_level):
    if risk_level == "low":
        return "emerald"
    if risk_level == "medium":
        return "amber"
    return "red"


def _loads(value, fallback):
    try:
        return json.loads(value or "")
    except Exception:
        return fallback


def _wrap_text(text, width):
    lines = []
    for paragraph in str(text).replace("\t", " ").split("\n"):
        words = paragraph.split()
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if len(candidate) > width and current:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        elif not words:
            lines.append("")
    return lines or [""]


def _card(page, x, y, width, height, fill=None):
    fill = fill or COLORS["white"]
    _rect(page, x + 2, y - 2, width, height, 226, 232, 240)
    _rect(page, x, y, width, height, *fill)
    _line(page, x, y, x + width, y, *COLORS["border"])
    _line(page, x, y + height, x + width, y + height, *COLORS["border"])
    _line(page, x, y, x, y + height, *COLORS["border"])
    _line(page, x + width, y, x + width, y + height, *COLORS["border"])


def _round_pill(page, x, y, width, height, fill, text, text_color):
    _rect(page, x, y, width, height, *fill)
    _text(page, text, x + 14, y + 9, 10, "F2", *text_color)


def _rect(page, x, y, width, height, r, g, b):
    page["commands"].append(f"{r / 255:.3f} {g / 255:.3f} {b / 255:.3f} rg {x:.2f} {y:.2f} {width:.2f} {height:.2f} re f")


def _line(page, x1, y1, x2, y2, r, g, b):
    page["commands"].append(f"{r / 255:.3f} {g / 255:.3f} {b / 255:.3f} RG 0.7 w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")


def _text(page, text, x, y, size, font, r, g, b):
    safe = str(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    page["commands"].append(
        f"BT {r / 255:.3f} {g / 255:.3f} {b / 255:.3f} rg /{font} {size} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm ({safe}) Tj ET"
    )


def _render_pdf(pages):
    stream = BytesIO()
    page_count = len(pages)
    font_regular_id = 3 + page_count
    font_bold_id = font_regular_id + 1
    content_start_id = font_bold_id + 1

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        f"<< /Type /Pages /Kids [{' '.join(f'{3 + i} 0 R' for i in range(page_count))}] /Count {page_count} >>".encode(),
    ]

    for index in range(page_count):
        content_id = content_start_id + index
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
                f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R >> >> "
                f"/Contents {content_id} 0 R >>"
            ).encode()
        )

    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    for page in pages:
        content_bytes = "\n".join(page["commands"]).encode("latin-1", errors="replace")
        objects.append(b"<< /Length " + str(len(content_bytes)).encode() + b" >>\nstream\n" + content_bytes + b"\nendstream")

    stream.write(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(stream.tell())
        stream.write(f"{index} 0 obj\n".encode())
        stream.write(obj)
        stream.write(b"\nendobj\n")

    xref = stream.tell()
    stream.write(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        stream.write(f"{offset:010d} 00000 n \n".encode())
    stream.write(f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode())
    return stream.getvalue()
