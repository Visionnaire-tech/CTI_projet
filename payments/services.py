import pandas as pd
from academics.models import Student
from .models import Payment


def import_payments(file):

    df = pd.read_excel(file)

    for _, row in df.iterrows():

        matricule = str(row.get('matricule')).strip()
        amount = float(row.get('montant', 0))
        name = str(row.get('nom', ''))

        try:
            student = Student.objects.get(matricule=matricule)

            # 🔁 éviter doublon (optionnel)
            if Payment.objects.filter(student=student, amount=amount).exists():
                continue

            Payment.objects.create(
                student=student,
                amount=amount,
                raw_name=name,
                status='VALID'
            )

            # 🔥 ACTIVER ETUDIANT
            total_paid = sum(p.amount for p in Payment.objects.filter(student=student))

            if total_paid > 0:
                student.is_active = True
                student.save()

        except Student.DoesNotExist:
            # ❌ erreur (nom différent ou matricule absent)
            Payment.objects.create(
                student=None,
                amount=amount,
                raw_name=name,
                status='ERROR'
            )