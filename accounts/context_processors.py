# accounts/context_processors.py
def user_roles(request):
    """Ajoute des booléens pour les rôles dans le template"""
    user = request.user
    return {
        'is_teacher': user.is_authenticated and user.groups.filter(name='Enseignant').exists(),
        'is_student': user.is_authenticated and user.groups.filter(name='Étudiant').exists(),
        'is_admin': user.is_authenticated and user.is_staff,
    }