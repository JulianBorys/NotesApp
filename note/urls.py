from django.urls import path
from . import views
 
app_name = 'note'

urlpatterns = [
    # GET views
    
    # Notes
    path('notes/<int:pk>/<slug:slug>', views.NoteDetailView.as_view(), name='note_detail'),
    path('notes/', views.NoteListView.as_view(), name='note_list'),
    path('notes/user/<int:pk>/', views.NoteUserListView.as_view(), name='note_user_list'),
    path('notes/course/<int:pk>/<slug:slug>', views.NoteCourseListView.as_view(), name='note_course_list'),
    
    path('notes/add/', views.AddNote.as_view(), name='add_note'),
    # Courses
    path('courses/<int:pk>/<slug:slug>/', views.CourseUniversityListView.as_view(), name='course_university_list'),
    
    # Universities
]