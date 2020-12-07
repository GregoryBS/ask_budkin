from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, Http404
from django.core.paginator import Paginator
from django.utils import timezone

import json

from .models import *
from .forms import LoginForm, ProfileForm, AskForm, AnswerForm, SettingsForm

tags = ['TWICE', 'Sana', 'Momo', '2YEON', 'Anime']
pop_tags = [{'title' : tags[i] } for i in range(5)]
pop_users = ['user1', 'user2', 'admin', 'me', 'whoever']

def paginate(request, objects):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    paginator = Paginator(objects, limit)
    page = paginator.page(page)
    return page

def index_view(request):
    new_questions = Question.objects.new()
    page = paginate(request, new_questions)
    return render(request, 'src/index.html', {'pop_tags' : pop_tags,
                                              'pop_users' : pop_users,
                                              'page_objs' : page
                                              })

def hot_view(request):
    top_questions = Question.objects.hot()
    page = paginate(request, top_questions)
    return render(request, 'src/index.html', {'pop_tags' : pop_tags,
                                              'pop_users' : pop_users,
                                              'page_objs' : page
                                              })

def questions_view(request, pk):
    question = Question.objects.by_id(pk)
    answers = question.answer.all()
    page = paginate(request, answers)
    return render(request, 'src/question-detail.html', {'pop_tags' : pop_tags,
                                                        'pop_users' : pop_users,
                                                        'question' : question,
                                                        'page_objs' : page,
                                                        'form' : AnswerForm(),
                                                        })

def tags_view(request, slug):
    tagged = Tag.objects.by_tag(slug)
    page = paginate(request, tagged)
    return render(request, 'src/index.html', {'pop_tags' : pop_tags,
                                              'pop_users' : pop_users,
                                              'page_objs' : page,
                                              'tag' : {'title': slug } 
                                              })

def login_view(request):
    errors = []
    next_page = request.GET.get('next', '/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(next_page)
        errors.append('Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'src/login.html', { 'form': form, 
                                               'errors': errors, 
                                               'pop_tags' : pop_tags,
                                               'pop_users' : pop_users,
                                               'next' : next_page
                                               })

def signup_view(request):
    errors = []
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/api/v1/')

        errors = form.errors

    else:
        form = ProfileForm()

    return render(request, 'src/signup.html', { 'form': form, 
                                                'errors': errors, 
                                                'pop_tags' : pop_tags,
                                                'pop_users' : pop_users  
                                                })

@login_required
def settings_view(request):
    errors = []
    u = request.user
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(u.id)
        else:
            errors = form.errors
    else:
        form = SettingsForm({'password': u.password,
                             'email': u.email, 'nickname': u.profile.nick,
                             'avatar': u.profile.avatar })

    return render(request, 'src/settings.html', {'form': form, 'errors': errors,
                                                 'pop_tags' : pop_tags,
                                                 'pop_users' : pop_users 
                                                 })

@login_required
def ask_view(request):
    errors = []
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            q = form.save(request.user.profile.id)
            return redirect(reverse('question', kwargs={'pk': q.id}))
        
        errors = form.errors
    else:
        form = AskForm()

    return render(request, 'src/ask.html', {'form': form, 'errors': errors,
                                            'pop_tags' : pop_tags,
                                            'pop_users' : pop_users 
                                            })

@login_required
def logout_view(request):
    if not request.user.is_authenticated:
        raise Http404
    logout(request)
    next_page = request.GET.get('next')
    if next_page is None:
        next_page = '/'
    return redirect(next_page)

@login_required
def vote_view(request):
    pid = request.user.profile.id
    oid = request.POST.get('oid')
    vote = request.POST.get('event')
    flag = request.POST.get('flag')
    rating = Vote.objects.add_vote(vote, pid, oid, flag)
    return HttpResponse(json.dumps({ 'rating' : rating }), 
                        content_type='application/json')

@login_required
def answer_view(request, pk):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save(pk, request.user.profile.id)

    else:
        form = AnswerForm()
    return redirect(reverse('question', kwargs={'pk': pk}))
