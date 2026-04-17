from evaluations.models import Grade

ELIMINATION_NOTE = 5
PASS_MARK = 11
MIN_CREDITS = 55


def calcul_deliberation(student):
    grades = Grade.objects.filter(student=student).select_related('course', 'course__ue')

    ue_data = {}

    total_points = 0
    total_coeff = 0
    total_credits = 0

    elimination = False

    for g in grades:
        course = g.course
        ue = course.ue

        note = g.note_finale or 0
        credit = course.credit

        tnp = note * credit  # 🔥 IMPORTANT

        if ue.id not in ue_data:
            ue_data[ue.id] = {
                'ue': ue,
                'courses': [],
                'total_tnp': 0,
                'total_credit': 0,
                'credits': ue.credit
            }

        ue_data[ue.id]['courses'].append({
            'course': course,
            'note': note,
            'credit': credit,
            'tnp': tnp
        })

        ue_data[ue.id]['total_tnp'] += tnp
        ue_data[ue.id]['total_credit'] += credit

        total_points += tnp
        total_coeff += credit

    # 🎯 calcul UE
    ue_results = []

    for ue_id, data in ue_data.items():

        moyenne = data['total_tnp'] / data['total_credit'] if data['total_credit'] else 0

        valide = moyenne >= PASS_MARK

        if valide:
            total_credits += data['credits']

        ue_results.append({
            'ue': data['ue'],
            'moyenne': round(moyenne, 2),
            'valide': valide,
            'courses': data['courses']  # ✔ corrigé
        })

    # 🎯 moyenne générale
    moyenne_generale = total_points / total_coeff if total_coeff else 0

    # 🎯 décision
    if elimination:
        decision = "DEF"
    elif moyenne_generale >= PASS_MARK and total_credits >= MIN_CREDITS:
        decision = "ADM"
    elif total_credits >= (MIN_CREDITS / 2):
        decision = "AJ"
    else:
        decision = "DEF"

    return {
        'ues': ue_results,
        'moyenne': round(moyenne_generale, 2),
        'credits': total_credits,
        'decision': decision
    }