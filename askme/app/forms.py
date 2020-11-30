from django import forms
from django.utils import timezone
from .models import User, Profile, Question, Answer, Tag
from .models import ProfileManager, QuestionManager, AnswerManager, TagManager

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        login = self.cleaned_data['login']
        if login.strip() == '':
            raise forms.ValidationError('Login is empty', code='validation_error')

        return login

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password is empty', code='validation_error')
        if ' ' in password:
            raise forms.ValidationError('Password contains space.', code='space in password')

        return password

class ProfileForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    nickname = forms.CharField()
    avatar = forms.ImageField(required=False)

    def clean(self):
        data = self.cleaned_data
        if data['login'].strip() == '':
            raise forms.ValidationError('Login is empty', code='validation_error')
        elif data['password'].strip() == '':
            raise forms.ValidationError('Password is empty', code='validation_error')
        elif data['password_check'].strip() == '' or data['password'] != data['password_check']:
            raise forms.ValidationError('Password and repeat password must be same', code='validation_error')
        elif data['email'].strip() == '':
            raise forms.ValidationError('Email is empty', code='validation_error')
        elif data['nickname'].strip() == '':
            raise forms.ValidationError('Nickname is empty', code='validation_error')
        return data

    def save_changes(self, uid):
        u = User.objects.get(id=uid)
        p = u.profile
        u.username = self.cleaned_data['login']
        u.set_password(self.cleaned_data['password'])
        u.email = self.cleaned_data['email']
        u.save()
        p.nick = self.cleaned_data['nickname']
        p.avatar = self.cleaned_data['avatar']
        p.save()

    def save(self):
        user = User(username=self.cleaned_data['login'], email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password'])
        user.save()
        Profile.objects.create(nick=self.cleaned_data['nickname'], 
                               avatar=str(user.pk) + self.cleaned_data['avatar'], 
                               user=user)
        return user

class AskForm(forms.Form):
    title = forms.CharField()
    tags = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        data = self.cleaned_data
        if data['title'].strip() == '':
            raise forms.ValidationError('Title of question is empty', code='validation_error')
        elif data['text'].strip() == '':
            raise forms.ValidationError('Text of question is empty', code='validation_error')

        return data

    def save(self, pid):
        tags = self.cleaned_data['tags'].split(' ')
        titles = Tag.objects.values_list('title', flat=True)
        q = Question.objects.create(title=self.cleaned_data['title'], 
                                    text=self.cleaned_data['text'],
                                    q_date=timezone.now(), profile_id=pid)
        for tag in tags:
            if tag in titles:
                tag = Tag.objects.get(title=tag)
            else:
                tag = Tag.objects.create(title=tag)
            q.tags.add(tag)
        
        q.save()
        return q

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        if self.cleaned_data['text'].strip() == '':
            raise forms.ValidationError('Text of answer is empty', code='validation_error')
        return self.cleaned_data

    def save(self, qid, pid):
        a = Answer.objects.create(text=self.cleaned_data['text'],
                                  a_date=timezone.now(), profile_id=pid, question_id=qid)
