from django.shortcuts import render
from django.shortcuts import Http404
from gra.models import Sesje, Gracze
import datetime, random
from django.utils import timezone
from django.http import HttpResponseRedirect
from .forms import CreateNewSession

#from game.models import Sesje, Gracze
#from game.forms import PostScoreForm
# Create your views here.

def index(request):
    if request.method == 'POST':
        data_ses = request.POST.get("sesnr")
        data_pass = request.POST.get("pass")

        try:
            sss = Sesje.objects.get(ses_number=data_ses)
            if data_pass == sss.password:
                return render(request, 'gra/room.html', {'sesja':sss})
        except:
            raise Http404("Nie ma takiej sesji sory...")
    return render(request, 'gra/index.html')

def room(request, ses_id):
    if request.method == 'GET':
        try:
            ses_id = str(ses_id)
            sss = Sesje.objects.get(ses_number=ses_id)
        except Sesje.DoesNotExist:
            raise Http404("Nie ma takiej sesji sory...")
        return render(request, 'gra/room.html', {'sesja':sss})
    elif request.method == 'POST':
        data = Sesje.objects.get(ses_number = ses_id)
        #s = request.POST.get("score")
        #s = int(s)
        #if s < 10:
        data.gracze_set.create(g_nick=request.POST.get("g_nickk"),score=request.POST.get("scoree"))
        print(type(request.POST.get("score")))

        try:
            ses_id = str(ses_id)
            sss = Sesje.objects.get(ses_number=ses_id)
        except Sesje.DoesNotExist:
            raise Http404("Nie ma takiej sesji sory...")
        return render(request, 'gra/room.html', {'sesja':sss})


def newses(request):
    if request.method == "POST":
        what = True
        while what:
            num = random.randint(100000, 1000000)
            if Sesje.objects.filter(ses_number=num):
                what = True
            else:
                form = CreateNewSession(request.POST)
                what = False
                if form.is_valid():
                    game_name = form.cleaned_data["game_name"]
                    s = Sesje(ses_number=num, game_name=game_name, end_time=timezone.now()+datetime.timedelta(days=7))
                    s.save()
                    return HttpResponseRedirect("/%i" % num)
    else:
        form = CreateNewSession()

    return render(request, 'gra/createSession.html', {"form": form})

def test_photo(request):
    return render(request, 'gra/tesserac_ex.html')