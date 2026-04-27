from django import forms
from .models import Grade

class GradeUpdateForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['tp', 'interro', 'examen', 'statut']

    def clean(self):
        cleaned = super().clean()

        tp = cleaned.get("tp")
        interro = cleaned.get("interro")
        examen = cleaned.get("examen")

        if tp is not None and tp > 5:
            raise forms.ValidationError("TP max = 5")

        if interro is not None and interro > 5:
            raise forms.ValidationError("Interro max = 5")

        if examen is not None and examen > 10:
            raise forms.ValidationError("Examen max = 10")

        return cleaned

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['tp', 'interro', 'examen', 'statut']