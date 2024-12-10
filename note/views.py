from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.models import User

from .models import University, Course, Note
from .forms import NoteForm

# Note model - Views
class NoteDetailView(DetailView):
    model = Note
    context_object_name = 'note'
    template_name = 'notes/note_detail.html'
    
class NoteListView(ListView):
    queryset = Note.objects.all()
    context_object_name = 'notes'
    template_name = 'notes/notes_all.html'
    
class NoteUserListView(ListView):
    context_object_name = 'notes'
    template_name = 'notes/notes_all.html'
    
    def get_queryset(self):
        self.user = get_object_or_404(User, id=self.kwargs['pk'])
        return Note.objects.filter(author=self.user)
    
class NoteCourseListView(ListView):
    context_object_name = 'notes'
    template_name = 'notes/notes_all.html'
    
    def get_queryset(self):
        self.course = get_object_or_404(Course, 
                                        id=self.kwargs['pk'],
                                        slug=self.kwargs['slug'])
        return Note.objects.filter(course=self.course)

class AddNote(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/add_note.html'
    success_url = 'notes/'
    
# Course model - Views
class CourseUniversityListView(ListView):
    context_object_name = 'courses'
    template_name = 'courses/courses.html'
    
    def get_queryset(self):
        self.university = get_object_or_404(University,
                                            id=self.kwargs['pk'],
                                            slug=self.kwargs['slug'])
        return Course.objects.filter(university=self.university)
    