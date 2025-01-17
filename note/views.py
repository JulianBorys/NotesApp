from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, FormView, View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.urls import reverse
from django.db.models import Q

from .models import University, Course, Note, Favourite
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pobierz wszystkie ulubione notatki użytkownika
        favorite_notes = Favourite.objects.filter(user=self.request.user).values_list('note_id', flat=True)
        # Przekaż zestaw ID ulubionych notatek do szablonu
        context['favorite_notes'] = set(favorite_notes)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
            )
        return queryset


class NoteUserListView(ListView):
    context_object_name = 'notes'
    template_name = 'notes/notes_all.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, id=self.kwargs['pk'])
        return Note.objects.filter(author=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user_view'] = True  # Dodaj flagę do kontekstu
        return context


class NoteCourseListView(ListView):
    context_object_name = 'notes'
    template_name = 'notes/notes_all.html'

    def get_queryset(self):
        self.course = get_object_or_404(Course,
                                        id=self.kwargs['pk'],
                                        slug=self.kwargs['slug'])
        return Note.objects.filter(course=self.course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_quiz_note_view'] = True  # Dodaj flagę do kontekstu
        return context


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'

    def get_object(self, queryset=None):
        """Pobierz obiekt notatki i sprawdź, czy użytkownik jest jej autorem."""
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise Http404("Nie masz uprawnień do zmiany tej notatki.")
        return obj


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/delete_note.html'
    success_url = reverse_lazy('notes:note_list')
    def get_object(self, queryset=None):
        """Pobierz obiekt notatki i sprawdź, czy użytkownik jest jej autorem."""
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise Http404("Nie masz uprawnień do usunięcia tej notatki.")
        return obj


# Course model - Views

class CourseListView(LoginRequiredMixin, ListView):
    queryset = Course.objects.all()
    context_object_name = 'courses'
    template_name = 'courses/courses_all.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )
        return queryset


class CourseUniversityListView(ListView):
    context_object_name = 'courses'
    template_name = 'courses/courses.html'

    def get_queryset(self):
        self.university = get_object_or_404(University,
                                            id=self.kwargs['pk'],
                                            slug=self.kwargs['slug'])
        return Course.objects.filter(university=self.university)


class AddCourse(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/add_course.html"

    def form_valid(self, form):
        course = form.save(commit=False)
        course.university = form.cleaned_data['university']
        course.save()
        return redirect(reverse('note:note_course_list', args=[course.id, course.slug]))


class UpdateCourse(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template = 'courses/update_course.html'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.university = form.cleaned_data['university']
        course.save()
        return redirect(reverse('note:note_course_list', args=[course.id, course.slug]))


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=kwargs['note_id'])
        favorite, created = Favourite.objects.get_or_create(user=request.user, note=note)

        if not created:
            favorite.delete()

        return redirect('note:note_list')


def load_courses(request):
    university_id = request.GET.get('university')
    courses = Course.objects.filter(university_id=university_id).order_by('name')
    return JsonResponse(list(courses.values('id', 'name')), safe=False)
