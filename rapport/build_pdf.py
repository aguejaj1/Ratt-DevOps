from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Rapport_CICD_Django.pdf"
W, H = letter
BLUE = HexColor("#0D6EFD")
NAVY = HexColor("#163A63")
GRAY = HexColor("#667085")
LIGHT = HexColor("#F5F7FA")
PALE_BLUE = HexColor("#EAF2FF")
GREEN = HexColor("#DFF4E5")
GREEN_TEXT = HexColor("#176B35")
RED = HexColor("#FDE7E7")
RED_TEXT = HexColor("#A61B1B")

styles = getSampleStyleSheet()
body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.4, leading=12.2, textColor=HexColor("#1F2937"), spaceAfter=5)
small = ParagraphStyle("Small", parent=body, fontSize=8.2, leading=10.3, textColor=GRAY)
h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=NAVY, spaceBefore=5, spaceAfter=6)
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=4, spaceAfter=4)
kicker = ParagraphStyle("Kicker", parent=small, fontName="Helvetica-Bold", fontSize=8.5, textColor=BLUE, spaceAfter=2)
center = ParagraphStyle("Center", parent=small, alignment=TA_CENTER)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawRightString(W - 0.72 * inch, H - 0.35 * inch, "RATT DEVOPS  |  RAPPORT CI/CD")
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(W / 2, 0.3 * inch, f"Django • GitHub Actions • Vercel  |  {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(str(OUT), pagesize=letter, leftMargin=0.72 * inch, rightMargin=0.72 * inch, topMargin=0.55 * inch, bottomMargin=0.48 * inch)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates(PageTemplate(id="report", frames=frame, onPage=header_footer))


def P(text, style=body):
    return Paragraph(text, style)


def status(label, text, good=True):
    fill, ink = (GREEN, GREEN_TEXT) if good else (RED, RED_TEXT)
    t = Table([[P(f"<b>{label}</b>", ParagraphStyle("s", parent=small, textColor=ink, alignment=TA_CENTER)), P(text, body)]], colWidths=[1.22 * inch, 5.02 * inch])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fill), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BOX", (0, 0), (-1, -1), 0.6, fill), ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return KeepTogether([t, Spacer(1, 4)])


def capture(title, instruction, height=48):
    content = P(f"<b>{title}</b><br/>{instruction}", center)
    t = Table([[content]], colWidths=[6.24 * inch], rowHeights=[height])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LIGHT), ("BOX", (0, 0), (-1, -1), 0.7, HexColor("#D0D5DD")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14)]))
    return KeepTogether([t, Spacer(1, 5)])


story = []
story += [P("RAPPORT TECHNIQUE", kicker), P("<b>Pipeline CI/CD Django</b>", ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=NAVY, spaceAfter=3)), P("Contrôle automatique de la couleur de fond et déploiement Vercel", ParagraphStyle("Sub", parent=body, fontSize=11.5, textColor=GRAY, spaceAfter=10))]
story.append(status("ÉTAT LOCAL", "Tests validés avec fond bleu ; échec reproduit avec fond orange."))
story += [P("1. Architecture mise en place", h1), P("L'application Django contient une vue unique et un template HTML minimaliste. La couleur de fond est définie sur <b>body</b>. Le script <b>tests/test_background_color.py</b> lit cette déclaration et refuse explicitement orange, #ffa500, #ff8c00 et leurs équivalents RGB.")]

data = [
    [P("<b>Branche test</b>", small), P("Branche de travail et de push par défaut", small)],
    [P("<b>Pull request</b>", small), P("test → main ; exécute le contrôle avant fusion", small)],
    [P("<b>Branche main</b>", small), P("Production ; protégée par le statut Tests obligatoires", small)],
    [P("<b>Vercel</b>", small), P("Déploiement automatique uniquement depuis main", small)],
]
t = Table(data, colWidths=[1.5 * inch, 4.74 * inch])
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), PALE_BLUE), ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#D0D5DD")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
story += [t, P("2. Paramètres GitHub indispensables", h1), P("Dans <b>Settings → Branches</b>, protéger main avec « Require a pull request before merging » et « Require status checks to pass before merging », puis sélectionner <b>Tests obligatoires</b>. Sans cette règle, GitHub Actions signale l'échec mais ne bloque pas strictement la fusion."), P("Le workflow est déclenché sur <b>pull_request</b> vers main et sur <b>push</b> vers main. Le premier événement bloque la fusion ; le second vérifie aussi l'état réel de la production.", small), PageBreak()]

story += [P("SCÉNARIO 1", ParagraphStyle("kg", parent=kicker, textColor=GREEN_TEXT)), P("Succès — fond bleu", h1), P("<b>1.</b> Le template conserve <b>background-color: #0d6efd</b>. Le développeur pousse le commit sur test, puis ouvre une pull request vers main."), capture("CAPTURE A — Push sur test + page bleue", "Insérer le terminal montrant « git push origin test » et la page locale/preview bleue.", 50), P("<b>2.</b> GitHub Actions installe Python 3.12, exécute le test de couleur puis les tests Django. Les deux commandes terminent avec OK."), status("SUCCÈS", "test_background_is_not_orange ... ok  |  test_home_page_is_available ... ok"), capture("CAPTURE B — GitHub Actions vert", "Insérer l'onglet Checks/Actions avec le job Tests obligatoires réussi.", 48), P("<b>3.</b> La pull request devient fusionnable. Après merge, Vercel détecte main et publie l'application."), capture("CAPTURE C — Merge + Vercel", "Insérer la PR fusionnée, puis le site Vercel affichant le fond bleu et son URL.", 68), P("<b>Résultat attendu :</b> main contient la version bleue ; le déploiement Vercel est fonctionnel.", ParagraphStyle("ok", parent=body, textColor=GREEN_TEXT)), PageBreak()]

story += [P("SCÉNARIO 2", ParagraphStyle("kr", parent=kicker, textColor=RED_TEXT)), P("Échec provoqué — fond orange", h1), P("<b>1.</b> Sur test, remplacer temporairement #0d6efd par <b>orange</b>, committer et pousser. La pull request vers main relance automatiquement le contrôle."), capture("CAPTURE D — Modification orange", "Insérer le diff du template et la page orange sur la branche test.", 48), P("<b>2.</b> Le test détecte la valeur interdite et termine avec un code de sortie 1. L'échec a été reproduit localement avant remise du rapport :"), status("ÉCHEC", "AssertionError: Déploiement bloqué : le fond 'orange' est orange.", False), capture("CAPTURE E — GitHub Actions rouge", "Insérer le log du job Vérifier la couleur de fond avec FAILED (failures=1).", 48), P("<b>3.</b> La protection de main affiche un contrôle requis en échec : le bouton de fusion est bloqué. Puisque main n'est pas modifiée, aucun déploiement de production Vercel ne doit partir."), capture("CAPTURE F — Blocage strict", "Insérer la PR avec Required check failed / Merge blocked et l'absence de nouveau déploiement Production sur Vercel.", 62), status("CONCLUSION", "Le mécanisme protège la production avant la fusion, à condition que la règle de protection de main soit activée."), P("<b>Note de rendu :</b> les cadres A–F doivent être remplacés par les captures du dépôt GitHub public et du projet Vercel de l'étudiant. Ces preuves dépendent des comptes externes et ne peuvent pas être fabriquées localement.", small)]

doc.build(story)
print(OUT)
