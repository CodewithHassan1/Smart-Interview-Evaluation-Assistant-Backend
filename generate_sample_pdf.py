import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

filename = "sample_candidate_evaluation.pdf"
story = []
styles = getSampleStyleSheet()
heading = ParagraphStyle(
    name="Heading",
    parent=styles["Heading1"],
    alignment=1,
    textColor=colors.HexColor("#1f2937"),
)

story.append(Paragraph("Interview Evaluation Sample", heading))
story.append(Spacer(1, 16))

sections = [
    ("Candidate", "Amina Khan"),
    ("Position", "Frontend Developer"),
    ("Final Verdict", "Hire"),
    (
        "Structured Report",
        "Amina demonstrates strong frontend foundations in HTML and CSS with a solid understanding of React hooks. She presented clear communication and eagerness to improve, though she needs more practice with async data handling.",
    ),
]

for title, content in sections:
    story.append(Paragraph(f"<b>{title}</b>", styles["Heading3"]))
    story.append(Paragraph(content, styles["BodyText"]))
    story.append(Spacer(1, 12))

score_rows = [
    ["Category", "Score"],
    ["Communication", "8/10"],
    ["Technical", "7/10"],
    ["Problem Solving", "6/10"],
]

table = Table(score_rows, colWidths=[240, 120])

table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#d1d5db")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#9ca3af")),
        ]
    )
)

story.append(table)
story.append(Spacer(1, 16))
story.append(Paragraph("Generated on: %s" % datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"), styles["Italic"]))

doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
doc.build(story)
print(f"Generated PDF sample: {os.path.abspath(filename)}")
