from evaluations.models import Grade


def calculer_bulletin(student):
    grades = Grade.objects.filter(student=student)

    ue_dict = {}

    total_points = 0
    total_coeff = 0
    total_credits = 0

    for grade in grades:
        course = grade.course
        ue = course.ue

        if ue.id not in ue_dict:
            ue_dict[ue.id] = {
                'ue_code': ue.code,
                'courses': [],
                'total': 0,
                'coeff': 0,
                'credit': ue.credit
            }

        note = grade.note_finale

        # Statut
        if note is None:
            statut = "ABS"
        elif note >= 11:
            statut = "Validé"
        else:
            statut = "Échec"

        ue_dict[ue.id]['courses'].append({
            'name': course.name,
            'note': note,
            'credit': course.credit,
            'statut': statut
        })

        if note is not None:
            ue_dict[ue.id]['total'] += note * course.credit
            ue_dict[ue.id]['coeff'] += course.credit

    # Calcul par UE
    ue_list = []

    for ue_id, data in ue_dict.items():
        moyenne_ue = data['total'] / data['coeff'] if data['coeff'] else 0

        if moyenne_ue >= 11:
            total_credits += data['credit']

        total_points += data['total']
        total_coeff += data['coeff']

        ue_list.append({
            'ue_code': data['ue_code'],
            'courses': data['courses'],
            'moyenne': round(moyenne_ue, 2),
            'credit': data['credit']
        })

    moyenne_generale = total_points / total_coeff if total_coeff else 0

    # Décision
    if total_credits >= 55:
        decision = "ADMIS"
    elif total_credits >= 30:
        decision = "DETTE"
    else:
        decision = "AJOURNE"

    return {
        'ues': ue_list,
        'moyenne': round(moyenne_generale, 2),
        'credits': total_credits,
        'decision': decision
    }