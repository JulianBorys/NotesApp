from django import forms

from .models import Note, Course, University

#TODO: Dodać, żeby author był automatycznie dodawany po zalogowanym użytkowniku
class NoteForm(forms.ModelForm):
    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = Note
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
        