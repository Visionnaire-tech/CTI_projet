from django.db import models
from django.core.exceptions import ValidationError
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

    # =========================
    # 🔥 CALCUL NOTE
    # =========================
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
        else:
            self.note_finale = 0

    # =========================
    # 🔒 VALIDATION LMD
    # =========================
    def clean(self):
        if self.tp is not None and self.tp > 5:
            raise ValidationError("TP > 5 interdit")

        if self.interro is not None and self.interro > 5:
            raise ValidationError("Interro > 5 interdit")

        if self.examen is not None and self.examen > 10:
            raise ValidationError("Examen > 10 interdit")

    # =========================
    # 💾 SAVE CORRECT
    # =========================
    def save(self, *args, **kwargs):
        bypass_lock = kwargs.pop('bypass_lock', False)

        if self.is_submitted and not bypass_lock:
            raise ValueError("Note verrouillée")

        # 🔥 validation Django
        self.full_clean()

        # 🔥 recalcul automatique
        self.calculer_note()

        super().save(*args, **kwargs)

    # =========================
    # 📊 TNP
    # =========================
    def tnp(self):
        if self.note_finale is not None:
            return self.note_finale * self.course.credit
        return 0

    def __str__(self):
        return f"{self.student} - {self.course}"

    class Meta:
        unique_together = ('student', 'course')