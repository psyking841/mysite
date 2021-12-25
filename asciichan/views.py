from django.shortcuts import render

# Create your views here.
from asciichan.models import Art


def render_front(request, title='', art='', error='', arts=[]):
    arts = Art.objects.order_by('-created')[:10]
    context = {
        'title': title,
        'art': art,
        'error': error,
        'arts': arts
    }
    return render(request, 'asciichan/theora-front.html', context)

def front(request):
    if request.method == "GET":
        return render_front(request)
    elif request.method == "POST":
        title = request.POST['title']
        art = request.POST['art']

    if title and art:
        a = Art(title=title, art=art)
        a.save()
        return render_front(request)
    else:
        error = 'we need both a title and some artwork!'
        return render_front(request, title=title, art=art, error=error)
