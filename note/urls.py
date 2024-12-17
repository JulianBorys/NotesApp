from django.urls import path
from . import views
 
app_name = 'note'

urlpatterns = [
    # Notes
    #? GET
    path('notes/<int:pk>/<slug:slug>', views.NoteDetailView.as_view(), name='note_detail'),
    path('notes/', views.NoteListView.as_view(), name='note_list'),
    path('notes/user/<int:pk>/', views.NoteUserListView.as_view(), name='note_user_list'),
    path('notes/course/<int:pk>/<slug:slug>', views.NoteCourseListView.as_view(), name='note_course_list'),
    #? POST
    path('notes/add/', views.AddNote.as_view(), name='add_note'),
    #? UPDATE, WORKS
    path('notes/update/<int:pk>', views.UpdateNote.as_view(), name='update_note'),
    #? DELETE WORKS
    path('notes/delete/<int:pk>', views.DeleteNote.as_view(), name='delete_note'),
    
    # Courses
    #? GET
    path('courses/<int:pk>/<slug:slug>/', views.CourseUniversityListView.as_view(), name='course_university_list'),
    #? POST
    path('courses/add/', views.AddCourse.as_view(), name='add_course'),
    #? UPDATE
    #? DELETE
    
    # Universities
]