import os

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.utils import timezone

class ProfileManager(models.Manager):
    pass

class Profile(models.Model):
    def avatar_filename(self, filename):
        return os.path.join(filename)

    nick = models.CharField(max_length=30, verbose_name='Nickname')
    avatar = models.ImageField(upload_to=avatar_filename, 
                               null=True, verbose_name='Avatar')

    user = models.OneToOneField(User, related_name="profile", 
                                on_delete=models.CASCADE)

    objects = ProfileManager()

    def __str__(self):
        return self.nick
    
    def get_avatar_url(self):
        return self.avatar.url

class TagManager(models.Manager):
    def by_tag(self, tag_title):
        tag = self.get(title=tag_title)
        return tag.question.all() if tag else None

class Tag(models.Model):
    title = models.CharField(max_length=30, verbose_name='Title of tag', 
                             unique=True, db_index=True)

    objects = TagManager()

    def __str__(self):
        return self.title

class VoteManager(models.Manager):
    use_for_related_fields = True

    def add_vote(self, vote, pid, oid, flag):
        if flag == 0:
            obj = Question.objects.get(id=oid)
        elif flag == 1:
            obj = Answer.objects.get(id=oid)
        self.create(value=vote, profile_id=pid, content_object=obj)
        obj.rating += vote
        #obj.save()
        return obj.rating
    

class Vote(models.Model):
    value = models.SmallIntegerField(default=0, verbose_name='Like or not', 
                                     db_index=True)

    profile = models.ForeignKey(Profile, related_name='vote', 
                                on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = VoteManager()

class QuestionManager(models.Manager):
    def new(self):
        return self.all().order_by('-q_date').select_related('profile')

    def hot(self):
        return self.all().order_by('-rating').select_related('profile')

    def by_id(self, id):
        return self.get(id=id)

class Question(models.Model):
    title = models.CharField(max_length=80, verbose_name='Title of question')
    text = models.TextField(verbose_name='Text of question')
    q_date = models.DateTimeField(default=timezone.now, 
                                  verbose_name='Date of question creating')
    rating = models.IntegerField(default=0)

    profile = models.ForeignKey(Profile, related_name='question', null=True,
                                on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name='question', blank=True)
    votes = GenericRelation(to=Vote, related_query_name='question')

    objects = QuestionManager()

    def __str__(self):
        return self.title

class AnswerManager(models.Manager):
    pass

class Answer(models.Model):
    text = models.TextField(verbose_name='Text of answer')
    a_date = models.DateTimeField(default=timezone.now,
                                  verbose_name='Date of answer creating')
    is_correct = models.BooleanField(default=False, 
                                     verbose_name='Check of correct')
    rating = models.IntegerField(default=0)

    profile = models.ForeignKey(Profile, related_name='answer', null=True,
                                on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, related_name='answer',
                                 on_delete=models.CASCADE)
    votes = GenericRelation(to=Vote, related_query_name='answer')

    objects = AnswerManager()

    def __str__(self):
        return self.text
