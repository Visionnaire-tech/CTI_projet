from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from evaluations.models import Grade


def generate_student_pdf(student, file_path):
    # 📄 Création du document PDF
    doc = SimpleDocTemplate(file_path, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    # 🏫 Titre
    elements.append(Paragraph("HAUTE ECOLE DE COMMERCE", styles['Title']))
    elements.append(Paragraph("BULLETIN DE NOTES", styles['Heading2']))
    elements.append(Spacer(1, 10))

    # 👤 Infos étudiant
    elements.append(Paragraph(f"Nom : {student.nom}", styles['Normal']))
    elements.append(Paragraph(f"Matricule : {student.matricule}", styles['Normal']))
    elements.append(Paragraph(f"Promotion : {student.promotion}", styles['Normal']))
    elements.append(Spacer(1, 15))

    # 📊 Tableau
    data = [["Cours", "Note /20", "Crédit", "TNP"]]

    total_points = 0
    total_credit = 0

    grades = Grade.objects.filter(student=student).select_related('course', 'course__ue')

    for g in grades:
        course = g.course
        note = g.note_finale if g.note_finale else 0
        credit = course.credit

        # 🔥 Total Note Pondérée
        tnp = note * credit

        total_points += tnp
        total_credit += credit

        data.append([
            course.name,
            round(note, 2),
            credit,
            round(tnp, 2)
        ])

    # 📊 Moyenne générale
    moyenne = total_points / total_credit if total_credit else 0

    data.append(["", "", "TOTAL", round(total_points, 2)])
    data.append(["", "", "MOYENNE", round(moyenne, 2)])

    # 🎨 Style tableau
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # 🧾 Mention
    if moyenne >= 16:
        mention = "EXCELLENT"
    elif moyenne >= 14:
        mention = "TRES BIEN"
    elif moyenne >= 12:
        mention = "BIEN"
    elif moyenne >= 10:
        mention = "PASSABLE"
    else:
        mention = "ECHEC"

    elements.append(Paragraph(f"Moyenne Générale : {round(moyenne, 2)}", styles['Heading3']))
    elements.append(Paragraph(f"Mention : {mention}", styles['Heading3']))

    # 📄 Génération
    doc.build(elements)