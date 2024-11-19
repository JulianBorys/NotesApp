from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Note

# Create your views here.
def note_list(request):
    notes = Note.published.all()
    return render(request,
                  'notes/list.html',
                  {'notes': notes})
    
def note_detail(request, id):
    note = get_object_or_404(Note,
                             id=id,
                             status=Note.Status.PUBLISHED)
    
    return render(request,
                  'notes/detail.html',
                  {'note': note})