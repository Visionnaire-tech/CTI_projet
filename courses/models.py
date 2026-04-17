from django.db import models
from academics.models import Promotion, UE, Department

from django.contrib.auth.models import User
from accounts.models import Teacher
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.nom
# -----------------------------
# COURS (MODULE)
# -----------------------------
class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

    credit = models.IntegerField()

    # règles académiques
    compensable = models.BooleanField(default=True)
    elimination_strict = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.promotion})"


# -----------------------------
# ASSIGNATION ENSEIGNANT
# -----------------------------
class CourseAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    groupe = models.CharField(
        max_length=10,
        choices=[('A', 'A'), ('B', 'B')],
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.teacher} → {self.course} ({self.groupe})"