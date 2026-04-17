from django.db import models
from academics.models import Student


class Deliberation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    total_credits = models.IntegerField(default=0)
    moyenne_generale = models.FloatField(null=True, blank=True)

    decision = models.CharField(
        max_length=20,
        choices=[
            ('ADMIS', 'Admis'),
            ('AJOURNE', 'Ajourné'),
            ('DETTE', 'Dette'),
        ]
    )

    def __str__(self):
        return f"{self.student} - {self.decision}"