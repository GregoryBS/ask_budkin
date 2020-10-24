from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

pop_tags = ['TWICE', 'Sana', 'Momo', '2YEON', 'Anime']
pop_users = ['user1', 'user2', 'admin', 'me', 'whoever']
questions = [i for i in range(10)]
text = 'Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.'

def index_view(request):
    return render(request, 'src/index.html', {'pop_tags' : pop_tags,
                                              'pop_users' : pop_users,
                                              'page_objs' : questions })


def hot_view(request):
    return render(request, 'src/index.html', {'pop_tags' : pop_tags,
                                              'pop_users' : pop_users,
                                              'page_objs' : questions })

def questions_view(request, pk):
    return render(request, 'src/question-detail.html', {'pop_tags' : pop_tags,
                                                        'pop_users' : pop_users,
                                                        'question' : 1,
                                                        'answers' : questions

    })

def tags_view(request, slug):
    return render(request, 'src/index.html', {'pop_tags' : pop_tags,
                                              'pop_users' : pop_users,
                                              'page_objs' : questions,
                                              'tag' : slug })

def login_view(request):
    return render(request, 'src/login.html', {'pop_tags' : pop_tags,
                                              'pop_users' : pop_users })

def signup_view(request):
    return render(request, 'src/signup.html', {'pop_tags' : pop_tags,
                                               'pop_users' : pop_users })

def settings_view(request):
    return render(request, 'src/settings.html', {'pop_tags' : pop_tags,
                                                 'pop_users' : pop_users })

def ask_view(request):
    return render(request, 'src/ask.html', {'pop_tags' : pop_tags,
                                               'pop_users' : pop_users })

def logout_view(request):
    return