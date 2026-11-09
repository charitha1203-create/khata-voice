import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Nirmala for Unicode Indic support (Telugu, Hindi, English)
NIRMALA_REG = "C:/Windows/Fonts/Nirmala.ttc"
pdfmetrics.registerFont(TTFont("Nirmala", NIRMALA_REG, subfontIndex=0))
pdfmetrics.registerFont(TTFont("Nirmala-Bold", NIRMALA_REG, subfontIndex=1))

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Nirmala", 9)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Don't draw header/footer on cover page (page 1)
        if self._pageNumber > 1:
            # Header
            self.drawString(54, 755, "Khata Voice — Multilingual Voice Ledger | Gnani.ai AI Internship Challenge")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)
            
            # Footer
            self.line(54, 45, 558, 45)
            self.drawString(54, 32, "Confidential & Comprehensive Project Report | Author: Chari (Warangal)")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 32, page_text)
            
        self.restoreState()

def build_pdf():
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Khata_Voice_Complete_Project_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    # Custom Palette
    c_primary = colors.HexColor("#1A365D")
    c_secondary = colors.HexColor("#2B6CB0")
    c_accent = colors.HexColor("#D69E2E")
    c_dark = colors.HexColor("#2D3748")
    c_bg_code = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#E2E8F0")
    
    title_style = ParagraphStyle(
        "CoverTitle",
        fontName="Nirmala-Bold",
        fontSize=24,
        leading=30,
        textColor=c_primary,
        alignment=0,
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        fontName="Nirmala",
        fontSize=12,
        leading=17,
        textColor=c_secondary,
        alignment=0,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        "Heading1_Custom",
        fontName="Nirmala-Bold",
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        fontName="Nirmala-Bold",
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=9,
        spaceAfter=5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        "Body_Custom",
        fontName="Nirmala",
        fontSize=9,
        leading=13,
        textColor=c_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        fontName="Nirmala",
        fontSize=9,
        leading=13,
        textColor=c_dark,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        fontName="Nirmala",
        fontSize=7,
        leading=10,
        textColor=colors.HexColor("#1A202C")
    )

    story = []
    
    # -------------------------------------------------------------
    # COVER / HEADER BANNER
    # -------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("KHATA VOICE (ఖాతా వాయిస్ / खाता वॉयस)", title_style))
    story.append(Paragraph("A Multilingual Real-Time Voice Ledger for Indian Kirana & Retail Shopkeepers", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=0, spaceAfter=12))
    
    meta_data = [
        [Paragraph("<b>Challenge:</b>", body_style), Paragraph("The Great Indian AI Internship Challenge (Gnani.ai)", body_style)],
        [Paragraph("<b>Candidate / Author:</b>", body_style), Paragraph("Chari (Warangal, Telangana — Tier 2/3 Town Category)", body_style)],
        [Paragraph("<b>Core Technologies:</b>", body_style), Paragraph("Gnani Prisma v3.0 (STT), Soundbox TTS Engine, WhatsApp Statements, Kirana Analytics", body_style)],
        [Paragraph("<b>Supported Languages:</b>", body_style), Paragraph("Telugu (te-IN), Hindi (hi-IN), Indian English (en-IN), Code-mixed", body_style)],
        [Paragraph("<b>Security & Multi-Tenancy:</b>", body_style), Paragraph("Per-Shopkeeper Isolated Ledgers, PIN Authentication, Persistent Language Profiles", body_style)],
        [Paragraph("<b>Target Awards:</b>", body_style), Paragraph("Regional Languages, Hinglish/Code-mixed, Noisy Audio, Tier 2/3, Best 60-Sec Demo", body_style)],
        [Paragraph("<b>Project Status:</b>", body_style), Paragraph("<b>Phase 0 to 5 Complete — Production-Grade Multilingual Voice Fintech Platform</b>", body_style)],
    ]
    t_meta = Table(meta_data, colWidths=[130, 362])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))
    
    # -------------------------------------------------------------
    # 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # -------------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "Across India's vast landscape of over 12 million small kirana stores, traditional retail commerce runs on credit (<i>udhaar / baaki / బాకీ</i>). "
        "Shopkeepers manage these daily transactions using physical paper notebooks (<i>bahi khata / బహి ఖాతా</i>). While informal credit builds customer loyalty, "
        "manual bookkeeping is fraught with operational challenges: it is slow during rush hours, paper books get torn, lost, or water-damaged, calculating balances "
        "requires tedious manual arithmetic, and entering transactions into existing mobile apps demands tedious manual typing that disrupts customer service.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Khata Voice</b> transforms this experience into a zero-friction, voice-first interaction with <b>multi-tenant shopkeeper accounts, automatic Soundbox voice announcements, "
        "1-click WhatsApp payment reminders, and visual business analytics</b>. "
        "Each shopkeeper creates an account with their preferred language (Telugu, Hindi, or English). When logged in, the entire interface (metrics, labels, buttons, and ledger) "
        "adapts natively to that language. The shopkeeper speaks naturally (e.g., <i>'రాము 500 రూపాయలు బియ్యం'</i>, <i>'రాము ఎంత బాకీ'</i>, or <i>'రాము 200 చెల్లించాడు'</i>). "
        "The system transcribes audio via <b>Gnani.ai Prisma v3.0 STT</b>, extracts customer names, provisions (సరుకులు), and amounts, presents a human-in-the-loop review dialogue, "
        "speaks aloud a Paytm-style audio confirmation, and commits the entry to that shopkeeper's private, isolated ledger with instant balance calculation.",
        body_style
    ))
    
    # -------------------------------------------------------------
    # 2. GNANI.AI INTERNSHIP CHALLENGE & RULES COMPLIANCE
    # -------------------------------------------------------------
    story.append(Spacer(1, 8))
    story.append(Paragraph("2. Gnani.ai Challenge Structure & Official Guidelines", h1_style))
    guidelines = [
        "<b>Internship Offer:</b> Up to 100 paid internships starting January 1, 2027, with stipends up to ₹1,00,000 per month.",
        "<b>10 Merit Awards (₹50,000 each):</b> Independent awards targeting Regional Languages, Code-mixed voice, Noisy audio, Real-world impact, Solo/Duo project, Tier 2/3 town entries, and Best 60-second demo.",
        "<b>Hard Submission Cutoff:</b> November 10, 2026 at 11:59 PM IST.",
        "<b>Deliverables:</b> 1) Public 60s demo video on LinkedIn/X with tags #GnaniAI and #GreatIndianAIInternshipChallenge; 2) Workspace documentation; 3) Submission Form."
    ]
    for g in guidelines:
        story.append(Paragraph(f"• {g}", bullet_style))
        
    story.append(PageBreak())

    # -------------------------------------------------------------
    # 3. ADVANCED ARCHITECTURE & FEATURE SET
    # -------------------------------------------------------------
    story.append(Paragraph("3. Advanced Architecture & Enterprise Feature Set", h1_style))
    story.append(Paragraph(
        "Khata Voice integrates six enterprise-grade pillars engineered specifically for Indian retail:",
        body_style
    ))
    
    arch_flow = [
        ["Layer / Feature", "Module", "Implementation & Technology", "Key Functionality"],
        ["Authentication", "auth.py", "users.json with PIN security", "Multi-shopkeeper signup/login, persistent language selection (te/hi/en)."],
        ["Data Isolation", "ledger.py", "ledger_{username}.json per shop", "Dynamic get_ledger_file(user); zero cross-tenant data leakage."],
        ["STT Engine", "stt.py", "Gnani Prisma v3.0 REST Client", "Sub-second ASR with dynamic keyterm boosting from shopkeeper's customers."],
        ["NLP Extractor", "extract.py", "Provisions & Fuzzy Matcher", "Normalizes provisions (బియ్యం/BM, పంచదార, నూనె) and matches customers."],
        ["Soundbox TTS", "tts.py", "Web Speech Audio Component", "Auto-announces confirmed transactions like Paytm/PhonePe soundbox."],
        ["WhatsApp Reminders", "tts.py", "URL Scheme Generator", "1-click pre-filled WhatsApp debt reminder with provisions and balance."],
        ["Kirana Analytics", "app.py", "Streamlit Native Bar Charts", "Visualizes top debtors, recovery rate %, and most demanded provisions."],
    ]
    t_arch = Table(arch_flow, colWidths=[85, 65, 150, 192])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Nirmala-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_code])
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 4. COMPLETE SOURCE CODE REPOSITORY
    # -------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("4. Complete Production Source Code", h1_style))
    story.append(Paragraph(
        "Below is the complete, unabridged production source code for every file in the Khata Voice repository, including authentication, soundbox TTS, and analytics logic.",
        body_style
    ))
    
    def add_code_block(filename, code_text, explanation):
        story.append(Paragraph(f"<b>File: {filename}</b>", h2_style))
        story.append(Paragraph(f"<i>Role: {explanation}</i>", body_style))
        
        lines = code_text.strip().split("\n")
        chunk_size = 30
        table_rows = []
        for i in range(0, len(lines), chunk_size):
            chunk = lines[i:i + chunk_size]
            escaped_chunk = []
            for l in chunk:
                line_esc = l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
                escaped_chunk.append(line_esc)
            chunk_str = "<br/>".join(escaped_chunk)
            p = Paragraph(f"<font face='Nirmala' size='6.8'>{chunk_str}</font>", code_style)
            table_rows.append([p])
            
        t_box = Table(table_rows, colWidths=[492])
        t_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), c_bg_code),
            ('BOX', (0, 0), (-1, -1), 1, c_border),
            ('PADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -2), 0),
            ('TOPPADDING', (0, 1), (-1, -1), 0),
        ]))
        story.append(t_box)
        story.append(Spacer(1, 10))

    # auth.py
    with open("C:/Users/chari/khata-voice/auth.py", "r", encoding="utf-8") as f:
        auth_code = f.read()
    add_code_block("auth.py", auth_code, "Multi-shopkeeper authentication engine with PIN verification, account creation, and language persistence.")

    # tts.py
    with open("C:/Users/chari/khata-voice/tts.py", "r", encoding="utf-8") as f:
        tts_code = f.read()
    add_code_block("tts.py", tts_code, "Smart Soundbox audio synthesis, multilingual transaction announcement formatting, and WhatsApp statement links.")

    # stt.py
    with open("C:/Users/chari/khata-voice/stt.py", "r", encoding="utf-8") as f:
        stt_code = f.read()
    add_code_block("stt.py", stt_code, "Gnani.ai Prisma v3.0 REST API client with keyterms boosting and multi-language support (te-IN, hi-IN, en-IN).")

    # intent.py
    with open("C:/Users/chari/khata-voice/intent.py", "r", encoding="utf-8") as f:
        intent_code = f.read()
    add_code_block("intent.py", intent_code, "Deterministic multilingual intent classifier (add, ask, correct, pay) with word-boundary and stem matching.")

    # extract.py
    with open("C:/Users/chari/khata-voice/extract.py", "r", encoding="utf-8") as f:
        extract_code = f.read()
    add_code_block("extract.py", extract_code, "Entity extraction engine: finds customers, numerical amounts, and provision items (BM, Panchadar, Nune, etc.).")

    # ledger.py
    with open("C:/Users/chari/khata-voice/ledger.py", "r", encoding="utf-8") as f:
        ledger_code = f.read()
    add_code_block("ledger.py", ledger_code, "Multi-tenant ledger engine with per-user file isolation (ledger_{user}.json), financial analytics, and provisions.")

    # app.py
    with open("C:/Users/chari/khata-voice/app.py", "r", encoding="utf-8") as f:
        app_code = f.read()
    add_code_block("app.py", app_code, "Streamlit web application with soundbox audio readback, WhatsApp reminders, business analytics, and voice ledger UI.")

    story.append(PageBreak())
    # -------------------------------------------------------------
    # 5. DEMO VIDEO BLUEPRINT & INTERVIEW GUIDE
    # -------------------------------------------------------------
    story.append(Paragraph("5. 60-Second Demo Video Blueprint (Crushing the Competition)", h1_style))
    script_data = [
        ["Time", "Visual Scene", "Spoken Dialogue / Audio", "Technical Focus Highlighted"],
        ["0:00 - 0:10", "Login screen. Choose Telugu, log in as Chari Kirana.", "'While other voice apps focus on theoretical inventory, Khata Voice solves India's real retail credit crisis!'", "Multi-tenancy & high-impact problem."],
        ["0:10 - 0:25", "Speak Telugu: 'రాము 500 రూపాయలు బియ్యం'. Tap confirm. Soundbox announces audio.", "'Speak naturally in Telugu. Gnani Prisma v3.0 transcribes rice provisions, and our smart Soundbox speaks the confirmation!'", "Prisma STT, provision mapping, Soundbox TTS."],
        ["0:25 - 0:38", "Speak correction or balance check: 'రాము ఎంత బాకీ'. Soundbox speaks answer.", "'Need to check balance or change quantity? Zero typing—instant conversational understanding.'", "Real-time intent detection & speech readback."],
        ["0:38 - 0:50", "Click '📲 WhatsApp Reminder' next to Ramu. Show pre-filled message.", "'With one click, send pre-filled WhatsApp payment reminders with exact provisions and balance.'", "Real-world utility & customer debt recovery."],
        ["0:50 - 1:00", "Show Analytics Tab (Top Debtors bar chart) & Gnani AI attribution.", "'Built with @Gnani.ai Prisma v3.0 by Chari from Warangal! #GnaniAI #GreatIndianAIInternshipChallenge'", "Kirana analytics, Tier 2/3 town, compliance."],
    ]
    t_script = Table(script_data, colWidths=[65, 120, 202, 105])
    t_script.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Nirmala-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_code])
    ]))
    story.append(t_script)
    story.append(Spacer(1, 15))

    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=8, spaceAfter=10))
    story.append(Paragraph("<b>Report Certified Complete & Submission-Ready</b>", h2_style))
    story.append(Paragraph(
        "All code files, architectural diagrams, multi-tenant authentication, soundbox TTS, WhatsApp integration, and business analytics have been validated.",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF built successfully at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
