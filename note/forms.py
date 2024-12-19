from django import forms

from .models import Note, Course, University

class NoteForm(forms.ModelForm):
    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        required=True,
        label="University"
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        required=True,
        label="Course"
    )

    class Meta:
        model = Note
        fields = ['title', 'body', 'university', 'course']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the university field for the instance
        if self.instance.pk:  # If editing an existing note
            self.fields['university'].initial = self.instance.course.university
            self.fields['course'].queryset = Course.objects.filter(university=self.instance.course.university)
        elif 'university' in self.data:  # Populate the course field dynamically when changing university
            try:
                university_id = int(self.data.get('university'))
                self.fields['course'].queryset = Course.objects.filter(university_id=university_id)
            except (ValueError, TypeError):
                pass  # Invalid input; fallback to default queryset
        else:
            self.fields['course'].queryset = Course.objects.none()
            
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
        