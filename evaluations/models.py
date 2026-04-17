from django.db import models
from academics.models import Student
from courses.models import Course

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    tp = models.FloatField(null=True, blank=True)
    interro = models.FloatField(null=True, blank=True)
    examen = models.FloatField(null=True, blank=True)

    note_finale = models.FloatField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)

    statut = models.CharField(
        max_length=10,
        choices=[('normal', 'Normal'), ('ABS', 'Absent')],
        default='normal'
    )

    def calculer_note(self):
        if self.statut == 'ABS':
            self.note_finale = 0
            return

        if self.tp is not None and self.interro is not None and self.examen is not None:
            self.note_finale = (
                (self.tp * 0.3) +
                (self.interro * 0.2) +
                (self.examen * 0.5)
            )

    # 🔥 TNP = note * crédit (VERSION SAFE)
    def tnp(self):
        if self.note_finale is not None:
            return self.note_finale * self.course.credit
        return 0

    # 🔥 BONUS : Moyenne simple
    def moyenne(self):
        if self.tp is not None and self.interro is not None and self.examen is not None:
            return (self.tp + self.interro + self.examen) / 3
        return 0

    def __str__(self):
        return f"{self.student} - {self.course}"