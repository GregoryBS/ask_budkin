from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404
from django.core.paginator import Paginator

from faker import Faker
from random import randint

fake = Faker()

tags = ['TWICE', 'Sana', 'Momo', '2YEON', 'Anime']
pop_tags = [{'title' : tags[i] } for i in range(5)]
pop_users = ['user1', 'user2', 'admin', 'me', 'whoever']
text = 'Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.'
questions = [{'id': i,
              'title' : fake.name(),
              'text' : fake.sentence(),
              'q_date' : fake.date(),
              'answers_count' : randint(0, 5),
              'rating' : randint(-20, 20),
              'profile' : {'nick' : fake.name() },
              'tag' : {'all' : [pop_tags[randint(0, 4)]] },
             } for i in range(20)]
answers = [{'text' : fake.sentence(),
            'a_date' : fake.date(),
            'rating' : randint(-20, 20),
            'profile' : {'nick' : fake.name() } 
            } for i in range(5)]

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
    new_questions = sorted(questions, key=lambda x: x['q_date'], reverse=True)
    page = paginate(request, new_questions)
    return render(request, 'src/index.html', {'pop_tags' : pop_tags,
                                              'pop_users' : pop_users,
                                              'page_objs' : page
                                              })


def hot_view(request):
    top_questions = sorted(questions, key=lambda x: x['rating'], reverse=True)
    page = paginate(request, top_questions)
    return render(request, 'src/index.html', {'pop_tags' : pop_tags,
                                              'pop_users' : pop_users,
                                              'page_objs' : page
                                              })

def questions_view(request, pk):
    page = paginate(request, answers)
    return render(request, 'src/question-detail.html', {'pop_tags' : pop_tags,
                                                        'pop_users' : pop_users,
                                                        'question' : questions[pk],
                                                        'page_objs' : page
                                                        })

def tags_view(request, slug):
    tagged = []
    for q in questions:
        for t in q['tag']['all']:
            if t['title'] == slug:
                tagged.append(q)
    page = paginate(request, tagged)
    return render(request, 'src/index.html', {'pop_tags' : pop_tags,
                                              'pop_users' : pop_users,
                                              'page_objs' : page,
                                              'tag' : {'title': slug } 
                                              })

def login_view(request):
    return render(request, 'src/login.html', {'pop_tags' : pop_tags,
                                              'pop_users' : pop_users,
                                              'errors' : ['Неверный логин или пароль']
                                              })

def signup_view(request):
    return render(request, 'src/signup.html', {'pop_tags' : pop_tags,
                                               'pop_users' : pop_users 
                                               })

def settings_view(request):
    return render(request, 'src/settings.html', {'pop_tags' : pop_tags,
                                                 'pop_users' : pop_users 
                                                 })

def ask_view(request):
    return render(request, 'src/ask.html', {'pop_tags' : pop_tags,
                                            'pop_users' : pop_users 
                                            })

def logout_view(request):
    return