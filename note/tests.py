from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from note.models import Note, Course, University, Favourite

class NoteViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.university = University.objects.create(name='Test University')
        self.course = Course.objects.create(name='Test Course', university=self.university)
        self.note = Note.objects.create(title='Test Note', body='Some content', author=self.user, course=self.course)

    def test_note_list_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('note:note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/notes_all.html')

    def test_note_detail_view(self):
        response = self.client.get(reverse('note:note_detail', args=[self.note.id, self.note.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')

    def test_add_favorite_note(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('note:toggle_favorite', args=[self.note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Favourite.objects.filter(user=self.user, note=self.note).exists())

    def test_course_list_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('note:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/courses_all.html')
