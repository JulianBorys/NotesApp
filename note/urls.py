from django.urls import path
from . import views
from .views import ToggleFavoriteView

app_name = 'note'

urlpatterns = [
    # Notes
    #? GET
    path('notes/<int:pk>/<slug:slug>', views.NoteDetailView.as_view(), name='note_detail'),
    path('notes/', views.NoteListView.as_view(), name='note_list'),
    path('notes/user/<int:pk>/', views.NoteUserListView.as_view(), name='note_user_list'),
    path('notes/course/<int:pk>/<slug:slug>', views.NoteCourseListView.as_view(), name='note_course_list'),
    path('notes/course/', views.CourseListView.as_view(), name='course_list'),
    #? POST
    path('notes/add/', views.NoteCreateView.as_view(), name='note_add'),
    path('notes/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_edit'),
    path('notes/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    path('notes/<int:note_id>/toggle_favorite/', ToggleFavoriteView.as_view(), name='toggle_favorite'),

    # Courses
    #? GET
    path('courses/<int:pk>/<slug:slug>/', views.CourseUniversityListView.as_view(), name='course_university_list'),
    #? POST
    path('courses/add/', views.AddCourse.as_view(), name='add_course'),
    #? UPDATE
    path('courses/update/<int:pk>', views.UpdateCourse.as_view(), name='update_course'),
    #? DELETE
    
    # Universities
    path('ajax/load-courses/', views.load_courses, name='ajax_load_courses'),
]