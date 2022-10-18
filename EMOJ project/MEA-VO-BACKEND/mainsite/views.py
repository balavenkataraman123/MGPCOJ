from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import pytz
import random

from pytz import timezone
import mdtex2html
from urllib3 import HTTPResponse
from .models import SiteUser, Problem, Submission
from datetime import datetime

def index(request):
    posts = Post.objects.all()
    return render(request, "announcements.html", {'posts': [i.getinfo() for i in posts]})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

@login_required
def logout_view(request): 
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = SiteUser.objects.create_user(username, email, password)
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

def getproblem(request, problem):
    status = 'unsolved'
    if request.user.is_authenticated:
        solved = request.user.getinfo()['problemssolved']
        if str(problem) in solved:
            status = 'solved'
        print(datetime.now())
        now_toronto = datetime.now().astimezone(pytz.timezone('America/Toronto'))
        if Problem.objects.get(id=problem).release > now_toronto:
            return HttpResponse("this problem does not exist")
        if Problem.objects.get(id=problem).expiry < now_toronto:
            if status == 'solved':
                status = 'solved-archive'
            else:
                status = 'unsolved-archive'
    probmdt= mdtex2html.convert(get_entry(Problem.objects.get(id=problem).qmduuid))
    solmdt = mdtex2html.convert(get_entry(Problem.objects.get(id=problem).amduuid))
    if status != 'unsolved' or request.user.is_superuser:
        sol = Problem.objects.get(id=problem).getanswer()
        return render(request, 'problem.html', {"problem" : Problem.objects.get(id=problem).getinfo(), "probmdt" : probmdt, "solmdt":solmdt,"status":status, "solution":sol})
    else:
        return render(request, 'problem.html', {"problem" : Problem.objects.get(id=problem).getinfo(), "status":status,"probmdt" : probmdt})
def randomproblem(request, category, level):
    return HttpResponse("deez nuts")    
def problemlist(request):
    now_toronto = datetime.now().astimezone(pytz.timezone('America/Toronto'))
    if request.user.is_authenticated:
        solved = request.user.getinfo()['problemssolved']
        probleml = []
        problems = Problem.objects.all()
        for i in problems:
            if i.release < now_toronto:
                color = ''
                if str(i.id) in solved:
                    color = 'solved'
                elif i.expiry < now_toronto:
                    color = 'archived'
                else:
                    color = 'unsolved'
                prob = {}
                prob['problem'] = i.getinfo()
                prob['color'] = color
                probleml.append(prob)
            else:
                if request.user.is_superuser:
                    color = ''
                    if str(i.id) in solved:
                        color = 'solved'
                    elif i.expiry < now_toronto:
                        color = 'archived'
                    elif i.release > now_toronto:
                        color="future"
                    else:
                        color = 'black'
                    prob = {}
                    prob['problem'] = i.getinfo()
                    prob['color'] = color
                    probleml.append(prob)
        return render(request, "index.html", {"problems" : probleml})
    else:
        probleml = []
        problems = Problem.objects.all()
        for i in problems:
            color = 'black'
            prob = {}
            prob['problem'] = i.getinfo()
            prob['color'] = color
            probleml.append(prob)
        return render(request, "index.html", {"problems" : probleml})

def userleaderboard(request):
    users = SiteUser.objects.all()
    users.order_by('points')
    return render(request, 'users.html', {"users" : [i.getinfo() for i in users]})

def getuserinfo(request, user):
    return render(request, 'user.html', {"userinfo":SiteUser.objects.get(id=user).getinfo()})

@csrf_exempt
@login_required
def solveproblem(request, problem):
    if request.method == 'POST':
        now_toronto = datetime.now().astimezone(pytz.timezone('America/Toronto'))
        if not str(problem) in request.user.problemssolved.split() and not Problem.objects.get(id=problem).user.id == request.user.id:
            probdd = Problem.objects.get(id=problem).expiry
            if now_toronto > probdd:
                return HttpResponse("too late")
            answer = str(request.body).split("\"")[3].strip()
            if answer == Problem.objects.get(id=problem).answer:
                attempts = 0
                if str(problem) in request.user.problems1attempt.split():
                    things = request.user.problems1attempt.split()
                    things.pop(things.index(str(problem)))
                    user = request.user
                    user.problems1attempt = ' '.join(things)
                    user.save()
                    sub = Submission.objects.get(user=request.user, problem=problem.objects.get(id=problem))
                    attempts = sub.at1
                things = request.user.problemssolved.split()
                things.append(str(problem))
                user = request.user
                if attempts == 0:
                    user.points += Problem.objects.get(id=problem).xpvalue
                    sub = Submission.objects.create(user=request.user, problem =  Problem.objects.get(id=problem), timesubmitted = datetime.now(), correct = True, at1=attempts)
                    sub.save()
                else:
                    user.points += int(Problem.objects.get(id=problem).xpvalue - (Problem.objects.get(id=problem).wattval * attempts))
                    sub = Submission.objects.get(user=request.user, problem =  Problem.objects.get(id=problem))
                    sub.timesubmitted = datetime.now()
                    sub.correct = True
                    sub.at1 = attempts
                    sub.save()
                user.problemssolved = ' '.join(things)
                user.save()        

                return HttpResponse('correct')
            else:
                if str(problem) in request.user.problems1attempt.split():
                    sub = Submission.objects.get(user=request.user, problem=problem.objects.get(id=problem))
                    attempts = sub.at1
                    if (attempts + 1) * Problem.objects.get(id=problem).wattval >= Problem.objects.get(id=problem).xpval:
                        things = request.user.problems1attempt.split()
                        things.pop(things.index(str(problem)))
                        user = request.user
                        user.problems1attempt = ' '.join(things)
                        user.save()
                        things = request.user.problemswrong.split()
                        things.append(str(problem))
                        user = request.user
                        user.problemswrong = ' '.join(things)
                        user.save()
                        sub = Submission.objects.get(user=request.user, problem =  Problem.objects.get(id=problem))
                        sub.timesubmitted = datetime.now()
                        sub.at1 += 1                        
                        return HttpResponse('bigwrong')
                    else:
                        sub = Submission.objects.get(user=request.user, problem =  Problem.objects.get(id=problem))
                        sub.timesubmitted = datetime.now()
                        sub.at1 += 1
                        return HttpResponse('wrong')          


                else:
                    things = request.user.problems1attempt.split()
                    things.append(str(problem))
                    user = request.user
                    user.problems1attempt = ' '.join(things)
                    user.save()
                    sub = Submission.objects.create(user=request.user, problem =  Problem.objects.get(id=problem), timesubmitted = datetime.now(), correct = False, at1 = False)
                    sub.save                   

                return HttpResponse('wrong')
        else:
            return HttpResponse('no')
    

@login_required
def makeproblem(request):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return HttpResponse('403 u no authorizey')
        else:
            title = request.POST['title']
            qmduuid = request.POST['questiontext']
            amduuid = request.POST['answer']
            xpval = request.POST['XPvalue']
            answer = request.POST['answer']
            expiry = request.POST['expiry']
            release = request.POST['release']
            problem = Problem.objects.create(title=title, qmduuid=qmduuid, amduuid = amduuid, answer=answer, xpvalue=xpval, expiry=expiry, release=release)
            problem.save()
            return HttpResponseRedirect('/getproblem/' + str(problem.id))
    else:
        return render(request, 'makeproblem.html')

@login_required
def editprofile(request):
    if request.method == 'GET':
        return render(request, 'edituser.html', {'user1':request.user.getinfo()})
    elif request.method == 'POST':
        desc = request.POST['description']
        pfp = request.POST['pfp']
        request.user.description = desc
        request.user.pfpurl = pfp
        request.user.save()
        return HttpResponseRedirect('/userinfo/' + str(request.user.id))
@csrf_exempt
def storeAndProcessFile(request):
    if request.method != 'POST':
        return render(request, "fileupload.html")
    if request.user.is_superuser:
        file = request.FILES['file']
        print('yeet')
        filename = f"entries/{file.name}"
        with open('%s' % filename, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
def image(request, imgid):
    img = default_storage.open(f"entries/{imgid}")
    response = FileResponse(img)
    return response
def makepost(request):
    print('e')
def get_entry(title):
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
def save_entry(title, content):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))
def edit_entry(request, name):
    return render(request, 'editfile.html',{
    "entry": get_entry(name),
    "name": name})   
def edited(request):
    if request.user.is_superuser:
        save_entry(str(request.GET.get('name')), str(request.GET.get('q')))
        return HttpResponse('it worked uwu')   
    else:
        return HttpResponse('not authenticatey uwu')