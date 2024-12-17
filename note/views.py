from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .models import University, Course, Note
from .forms import NoteForm, CourseForm

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
    success_url = 'notes:note_list'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        note = form.save(commit=False)
        note.author = self.request.user
        note.save()
        return redirect(note.get_absolute_url())
    
class UpdateNote(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/update_note.html'
    success_url = '/notes/'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        note = form.save(commit=False)
        print(note.author)
        if note.author != self.request.user:
            form.add_error(None, "Nie możesz edytować tej notatki.")
            return self.form_invalid(form)
        note.save()
        return super().form_valid(form)
    
class DeleteNote(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/delete_note.html'
    success_url = '/notes/'

    def get_object(self, queryset=None):
        """Pobierz obiekt notatki i sprawdź, czy użytkownik jest jej autorem."""
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise Http404("Nie masz uprawnień do usunięcia tej notatki.")
        return obj
    
# Course model - Views
class CourseUniversityListView(ListView):
    context_object_name = 'courses'
    template_name = 'courses/courses.html'
    
    def get_queryset(self):
        self.university = get_object_or_404(University,
                                            id=self.kwargs['pk'],
                                            slug=self.kwargs['slug'])
        return Course.objects.filter(university=self.university)
     
class AddCourse(CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/add_course.html"
    
    def form_valid(self, form):
        course = form.save(commit=False)
        course.university = form.cleaned_data['university']
        course.save()
        return redirect(course.university.get_absolute_url())
