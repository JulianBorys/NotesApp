from django.urls import path
from . import views
 
app_name = 'blog'
urlpatterns = [
    # POST views
    path('', views.note_list, name='note_list'),
    path('<int:id>/', views.note_detail, name='note_detail'),
 ]