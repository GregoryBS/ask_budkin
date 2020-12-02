from django import forms
from django.utils import timezone
from .models import User, Profile, Question, Answer, Tag
from .models import ProfileManager, QuestionManager, AnswerManager, TagManager

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        login = self.cleaned_data.get('login', '')
        if login == '':
            raise forms.ValidationError('Login is empty', code='validation_error')

        return login

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if password == '':
            raise forms.ValidationError('Password is empty', code='validation_error')
        elif ' ' in password:
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
        l = data.get('login', '')
        p = data.get('password', '')
        pc = data.get('password_check', '')
        e = data.get('email', '')
        n = data.get('nickname', '')
        if l == '':
            raise forms.ValidationError('Login is empty', code='validation_error')
        elif p == '':
            raise forms.ValidationError('Password is empty', code='validation_error')
        elif pc == '' or pc != p:
            raise forms.ValidationError('Password and repeat password must be same', code='validation_error')
        elif e == '':
            raise forms.ValidationError('Email is empty', code='validation_error')
        elif n == '':
            raise forms.ValidationError('Nickname is empty', code='validation_error')
        return data

    def save(self):
        user = User(username=self.cleaned_data['login'], email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password'])
        user.save()
        Profile.objects.create(nick=self.cleaned_data['nickname'], 
                               avatar=str(user.pk) + self.cleaned_data['avatar'], 
                               user=user)
        return user

class SettingsForm(forms.Form):
    nickname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    avatar = forms.ImageField(required=False)

    def clean(self):
        data = self.cleaned_data
        p = data.get('password', '')
        e = data.get('email', '')
        n = data.get('nickname', '')
        if p == '':
            raise forms.ValidationError('Password is empty', code='validation_error')
        elif e == '':
            raise forms.ValidationError('Email is empty', code='validation_error')
        elif n == '':
            raise forms.ValidationError('Nickname is empty', code='validation_error')
        return data

    def save(self, uid):
        u = User.objects.get(id=uid)
        p = u.profile
        u.set_password(self.cleaned_data['password'])
        u.email = self.cleaned_data['email']
        u.save()
        p.nick = self.cleaned_data['nickname']
        p.avatar = self.cleaned_data['avatar']
        p.save()

class AskForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(required=False)

    def clean(self):
        title = self.cleaned_data.get('title', '')
        text = self.cleaned_data.get('text', '')
        if title == '':
            raise forms.ValidationError('Title of question is empty', code='validation_error')
        elif text == '':
            raise forms.ValidationError('Text of question is empty', code='validation_error')

        return self.cleaned_data

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
    answer = forms.CharField(widget=forms.Textarea)

    def clean(self):
        data = self.cleaned_data.get('answer', '')
        if data == '':
            raise forms.ValidationError('Text of answer is empty', code='validation_error')
        return self.cleaned_data

    def save(self, qid, pid):
        a = Answer.objects.create(text=self.cleaned_data['answer'],
                                  a_date=timezone.now(), profile_id=pid, question_id=qid)
