from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('notes:course_university_list',
                       args=[self.id,
                             self.slug])
    
    
class Course(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    university = models.ForeignKey(University,
                                   on_delete=models.CASCADE,
                                   related_name='courses')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('notes:note_course_list',
                       args=[self.id,
                             self.slug])
    
class Note(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='notes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='notes')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('notes:note_detail',
                       args=[self.id,
                             self.slug])
    