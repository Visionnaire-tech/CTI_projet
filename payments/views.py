import pandas as pd
from django.shortcuts import render, redirect
from academics.models import Student, Promotion, Department


def import_payments(request):

    if request.method == "POST":

        file = request.FILES.get("file")

        promotion_id = request.POST.get("promotion")
        department_id = request.POST.get("department")
        vacation = request.POST.get("vacation")

        promotion = Promotion.objects.get(id=promotion_id)
        department = Department.objects.get(id=department_id)

        # 📌 Lecture Excel
        df = pd.read_excel(file)

        # 🔥 NORMALISATION ULTRA ROBUSTE DES COLONNES
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
        )

        # 🔥 CORRECTION ACCENTS (prénom → prenom)
        df = df.rename(columns={
            "prénom": "prenom",
            "prenom ": "prenom",
            "matricule ": "matricule",
            "nom ": "nom",
            "postnom ": "postnom",
            "genre ": "genre"
        })

        print("COLONNES DETECTÉES:", df.columns)
        print(df.head())

        # 📌 Colonnes obligatoires
        required_cols = ["matricule", "nom", "postnom", "prenom", "genre"]

        # ❌ Vérification sécurité
        missing = [col for col in required_cols if col not in df.columns]

        if missing:
            return render(request, "payments/import.html", {
                "error": f"Colonnes manquantes : {missing}",
                "promotions": Promotion.objects.all(),
                "departments": Department.objects.all()
            })

        df = df[required_cols]

        created_count = 0

        # 📌 IMPORT
        for _, row in df.iterrows():

            student, created = Student.objects.update_or_create(
                matricule=row["matricule"],
                defaults={
                    "nom": row["nom"],
                    "postnom": row["postnom"],
                    "prenom": row["prenom"],
                    "genre": row["genre"],
                    "promotion": promotion,
                    "department": department,
                    "vacation": vacation,
                    "is_active": True
                }
            )

            if created:
                created_count += 1

        return render(request, "payments/import.html", {
            "success": f"{created_count} étudiants importés avec succès",
            "promotions": Promotion.objects.all(),
            "departments": Department.objects.all()
        })

    return render(request, "payments/import.html", {
        "promotions": Promotion.objects.all(),
        "departments": Department.objects.all()
    })