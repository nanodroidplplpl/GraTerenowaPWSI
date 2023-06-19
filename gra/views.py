import string

from django.shortcuts import render, redirect
from django.shortcuts import Http404
from gra.models import Sesje, Gracze, Gry, Zadania, Punktowi, Hosty, Ekipy
import datetime, random, secrets
from django.utils import timezone
from django.http import HttpResponseRedirect
from .forms import CreateNewSession

import matplotlib.pyplot as plt
import io
import base64

# from game.models import Sesje, Gracze
# from game.forms import PostScoreForm
# Create your views here.

def game_index(request):
    return render(request, 'gra/game_index.html')


def check_session_exists(ses_id):
    session_exists = Sesje.objects.filter(ses_number=ses_id).exists()
    return session_exists


def choose_group(request):
    ses_num = request.POST.get('join_code')
    if check_session_exists(ses_num):
        request.session['ses_number'] = str(ses_num)
        ekipy = Ekipy.objects.filter(sesje_ses_number=ses_num) if ses_num else Ekipy.objects.all()

        context = {
            'ekipy': ekipy,
        }
        return render(request, 'gra/choose_group.html', context)


def group_screen(request, ekipy_id=None):
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(f"Klucz: {key}, Wartość: {value}")

        nick = request.POST['nick_hidden']
        ses_number = request.session.get('ses_number')
        group_identifier = request.POST['grupa']

        if group_identifier.isdigit():
            # Dodawanie gracza do istniejącej grupy
            ekipa = Ekipy.objects.get(ekipy_id=group_identifier)
        else:
            # Tworzenie nowej grupy
            ekipa = Ekipy.objects.create(ekipy_id=random.randint(1, 10000), nazwa_ekipy=group_identifier,
                                         sesje_ses_number=ses_number)

        Gracze.objects.create(g_nick=nick, score=0, ekipy_ekipy_id=ekipa)
        czlonkowie = Gracze.objects.filter(ekipy_ekipy_id=ekipa)

        context = {
            'inni_czlonkowie': czlonkowie,
            'tytul': ekipa.nazwa_ekipy,
            'twój_nick': nick
        }
        return render(request, 'gra/group_screen.html', context)  # Przekierowanie do strony powodzenia
    else:
        return render(request, 'gra/group_screen.html')


def game_filed(request):
    return render(request, 'gra/game_filed.html')


def host_game_create(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(f'Klucz: {key}, Wartość: {value}')

    dostepne_gry = Gry.objects.all()

    request.session['host_nick'] = request.POST.get('host_id')
    request.session['host_pswd'] = request.POST.get('host_password')
    request.session['im_on'] = False

    context = {
        'dostepne_gry': dostepne_gry,
    }
    return render(request, 'gra/host_game_create.html', context)


def game_creation(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(f"{key}: {value}")
    return render(request, 'gra/game_creation.html')


def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(alphabet) for _ in range(length))
    return random_string


def host_game_filed(request):
    if not request.session.get('im_on'):
        if request.method == 'POST' and not (request.POST.get('index_gry') is not None):
            nazwa_hosta = request.POST.get('nazwa_hosta')
            haslo_hosta = request.POST.get('haslo_hosta')

            # Zapisz dane hosta
            host = Hosty(h_nick=nazwa_hosta, sesje_ses_number="")
            host.save()

            # Utwórz grę
            gra = Gry(nr_gry=generate_random_string(200), nazwa_gry=request.POST.get('nazwa_gry'),
                      czas_trwania=request.POST
                      .get('czas_trwania'), lokalizacja=request.POST.get('localisation'))
            gra.save()

            # Utwórz sesję
            sesja = Sesje(ses_number=generate_random_string(200), game_name="",
                          end_time=timezone.now() + datetime.timedelta(hours=1),
                          password=haslo_hosta, gry_nr_gry=gra)
            sesja.save()

            # Powiąż sesję z hostem
            host.sesje_ses_number = sesja.ses_number
            host.save()

            for key, value in request.POST.items():
                if key.startswith('nazwa_zadania_'):
                    indeks = key.split('_')[-1]
                    nazwa_zadania = value
                    opis_zadania = request.POST.get(f'opis_zadania_{indeks}')
                    haslo_zadania = request.POST.get(f'haslo_zadania_{indeks}')
                    lat_zadania = request.POST.get(f'lat_zadania_{indeks}')
                    lon_zadania = request.POST.get(f'lon_zadania_{indeks}')

                    # Zapisz zadanie
                    zadanie = Zadania(id_zadania=generate_random_string(200), nazwa_zadania=nazwa_zadania,
                                      opis_zadania=opis_zadania, lat=lat_zadania, lon=lon_zadania,
                                      password=haslo_zadania, gry_nr_gry=gra)
                    zadanie.save()

                    # Powiąż zadanie z punktem
                    punkt = Punktowi(p_nick=f"punkt_{indeks}", ses_num=sesja.ses_number,
                                     sesje_ses_number=sesja.ses_number)
                    punkt.save()

            ses_number = request.session['ses_number']
            nazwa_hosta = request.session['host_nick']
            request.session['im_on'] = True

            # Pobranie listy ekip
            sesja = Sesje.objects.get(ses_number=ses_number)
            ekipy = Ekipy.objects.filter(sesje_ses_number=sesja.ses_number)

            points_data = {
                'labels': [],
                'points': []
            }
            visited_points_data = {
                'labels': [],
                'visitedPoints': []
            }

            for ekipa in ekipy:
                points_data['labels'].append(ekipa.nazwa_ekipy)
                points_data['points'].append(ekipa.ilosc_punktow)
                visited_points_data['labels'].append(ekipa.nazwa_ekipy)
                visited_points_data['visitedPoints'].append(ekipa.ilosc_punkow_odwiedzonych)

            context = {
                'ses': str(ses_number),
                'h_nick': str(nazwa_hosta),
                'points_data': points_data,
                'visited_points_data': visited_points_data
            }

            return render(request, 'gra/host_game_filed.html', context)
        elif request.method == 'POST':
            host_nick = request.session.get('host_nick')

            try:
                gra = Gry.objects.get(nr_gry=request.POST.get('index_gry'))
            except Gry.DoesNotExist:
                return redirect('/')

            host = Hosty(h_nick=host_nick, sesje_ses_number="")
            host.save()

            sesja = Sesje(ses_number=generate_random_string(200), game_name="",
                          end_time=timezone.now() + datetime.timedelta(hours=1),
                          password=request.session.get('host_pswd'), gry_nr_gry=gra)
            sesja.save()
            request.session['ses_number'] = sesja.ses_number

            host.sesje_ses_number = sesja.ses_number
            host.save()

            ses_number = request.session['ses_number']
            nazwa_hosta = request.session['host_nick']
            request.session['im_on'] = True

            # Pobranie listy ekip
            sesja = Sesje.objects.get(ses_number=ses_number)
            ekipy = Ekipy.objects.filter(sesje_ses_number=sesja.ses_number)

            points_data = {
                'labels': [],
                'points': []
            }
            visited_points_data = {
                'labels': [],
                'visitedPoints': []
            }

            for ekipa in ekipy:
                points_data['labels'].append(ekipa.nazwa_ekipy)
                points_data['points'].append(ekipa.ilosc_punktow)
                visited_points_data['labels'].append(ekipa.nazwa_ekipy)
                visited_points_data['visitedPoints'].append(ekipa.ilosc_punkow_odwiedzonych)

            context = {
                'ses': str(ses_number),
                'h_nick': str(nazwa_hosta),
                'points_data': points_data,
                'visited_points_data': visited_points_data
            }

            return render(request, 'gra/host_game_filed.html', context)

        # request.session['ses_number'] = sesja.ses_number
        # request.session['host_nick'] = nazwa_hosta

        ses_number = request.session['ses_number']
        nazwa_hosta = request.session['host_nick']
        request.session['im_on'] = True

        # Pobranie listy ekip
        sesja = Sesje.objects.get(ses_number=ses_number)
        ekipy = Ekipy.objects.filter(sesje_ses_number=sesja.ses_number)

        points_data = {
            'labels': [],
            'points': []
        }
        visited_points_data = {
            'labels': [],
            'visitedPoints': []
        }

        for ekipa in ekipy:
            points_data['labels'].append(ekipa.nazwa_ekipy)
            points_data['points'].append(ekipa.ilosc_punktow)
            visited_points_data['labels'].append(ekipa.nazwa_ekipy)
            visited_points_data['visitedPoints'].append(ekipa.ilosc_punkow_odwiedzonych)

        context = {
            'ses': str(ses_number),
            'h_nick': str(nazwa_hosta),
            'points_data': points_data,
            'visited_points_data': visited_points_data
        }

        return render(request, 'gra/host_game_filed.html', context)
    else:
        ses_number = request.session['ses_number']
        nazwa_hosta = request.session['host_nick']
        request.session['im_on'] = True

        # Pobranie listy ekip
        sesja = Sesje.objects.get(ses_number=ses_number)
        ekipy = Ekipy.objects.filter(sesje_ses_number=sesja.ses_number)

        points_data = {
            'labels': [],
            'points': []
        }
        visited_points_data = {
            'labels': [],
            'visitedPoints': []
        }

        for ekipa in ekipy:
            points_data['labels'].append(ekipa.nazwa_ekipy)
            points_data['points'].append(ekipa.ilosc_punktow)
            visited_points_data['labels'].append(ekipa.nazwa_ekipy)
            visited_points_data['visitedPoints'].append(ekipa.ilosc_punkow_odwiedzonych)

        context = {
            'ses': str(ses_number),
            'h_nick': str(nazwa_hosta),
            'points_data': points_data,
            'visited_points_data': visited_points_data
        }

        return render(request, 'gra/host_game_filed.html', context)




def zaslepka(request):
    pass


def index(request):
    if request.method == 'POST':
        data_ses = request.POST.get("sesnr")
        data_pass = request.POST.get("pass")

        try:
            sss = Sesje.objects.get(ses_number=data_ses)
            if data_pass == sss.password:
                return render(request, 'gra/room.html', {'sesja': sss})
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
        return render(request, 'gra/room.html', {'sesja': sss})
    elif request.method == 'POST':
        data = Sesje.objects.get(ses_number=ses_id)
        # s = request.POST.get("score")
        # s = int(s)
        # if s < 10:
        data.gracze_set.create(g_nick=request.POST.get("g_nickk"), score=request.POST.get("scoree"))
        print(type(request.POST.get("score")))

        try:
            ses_id = str(ses_id)
            sss = Sesje.objects.get(ses_number=ses_id)
        except Sesje.DoesNotExist:
            raise Http404("Nie ma takiej sesji sory...")
        return render(request, 'gra/room.html', {'sesja': sss})


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
                    s = Sesje(ses_number=num, game_name=game_name, end_time=timezone.now() + datetime.timedelta(days=7))
                    s.save()
                    # return HttpResponseRedirect("/%i" % num)
                    return HttpResponseRedirect("creator/%i" % num)
    else:
        form = CreateNewSession()

    return render(request, 'gra/createSession.html', {"form": form})


def creator_room(request):
    return render(request, 'gra/creator_map.html')


def test_photo(request):
    return render(request, 'gra/tesserac_ex.html')