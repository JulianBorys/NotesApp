from django import forms

from .models import Note, Course, University

class NoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if 'university' in self.data:
            try:
                university_id = int(self.data.get('university'))
                # Filtrowanie kursów na podstawie wybranej uczelni
                self.fields['course'].queryset = Course.objects.filter(university_id=university_id)
            except (ValueError, TypeError):
                pass  # Jeśli nie ma poprawnego ID uczelni w danych, nie filtruj kursów
        elif self.instance.pk:
            print("TU")
            # Przy edytowaniu notatki, przypisz kursy z powiązanej uczelni
            self.fields['course'].queryset = self.instance.course.university.courses.all()

    
    
    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    #TODO: Wybierz kursy z wybranej uczelni
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = Note
        fields = ['title', 'body', 'course']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
class CourseForm(forms.ModelForm):
    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = Course
        fields = ['name', 'university']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        