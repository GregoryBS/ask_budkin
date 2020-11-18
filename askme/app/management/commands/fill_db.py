from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
from app.models import *

from faker import Faker
from random import randint, sample

fake = Faker()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--users', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--votes', type=int)
    
    def handle(self, *args, **options):
        users_cnt = options['users']
        tags_cnt = options['tags']
        questions_cnt = options['questions']
        answers_cnt = options['answers']
        votes_cnt = options['votes']

        if users_cnt is not None:
            self.generate_users(users_cnt)

        if tags_cnt is not None:
            self.generate_tags(tags_cnt)

        if questions_cnt is not None:
            self.generate_questions(questions_cnt)
            
        if answers_cnt is not None:
            self.generate_answers(answers_cnt)

        if votes_cnt is not None:
            self.generate_votes(votes_cnt)

    def generate_users(self, users_cnt):
        dels = ['', ' ', '_', '-']
        for i in range(users_cnt):
            d1 = dels[randint(0, 3)]
            d2 = dels[randint(0, 3)]
            username = (fake.name().split(' ')[randint(0, 1)] + d1 + \
                       fake.word() + d2 + fake.sentence()[:7])[:30]
            u = User(username=username, password=fake.password(), email=fake.email())
            u.save()
            p = Profile(user=u, nick=u.username, avatar="../../../static/img/avatar.png")
            p.save()

    def generate_tags(self, tags_cnt):
        dels = ['', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '-']
        for i in range(tags_cnt):
            title = fake.word()
            d = dels[randint(0, 12)]
            t = Tag(title=title + d + fake.word())
            t.save()
    
    def generate_questions(self, questions_cnt):
        p_ids = Profile.objects.values_list('id', flat=True)
        tag_ids = Tag.objects.values_list('id', flat=True)
        for i in range(questions_cnt):
            q = Question(title=fake.sentence()[:30], text=fake.text(), 
                         q_date=timezone.now(),
                         profile_id=p_ids[randint(0, p_ids.count() - 1)])
            q.save()

            question_tags_cnt = randint(0, 3)
            for j in range(question_tags_cnt):
                q.tags.add(tag_ids[randint(0, tag_ids.count() - 1)])
            q.save()
    
    def generate_answers(self, answers_cnt):
        p_ids = Profile.objects.values_list('id', flat=True)
        q_ids = Question.objects.values_list('id', flat=True)
        answers = []
        for i in q_ids:
            answers_cnt = randint(4, 12)
            for j in range(answers_cnt):
                answers.append(Answer(profile_id=p_ids[randint(0, p_ids.count() - 1)],
                               question_id=i, a_date=timezone.now(), text=fake.text()))
            if len(answers) > 5000:
                Answer.objects.bulk_create(answers)
                answers.clear()
                print("inserted 5000")

    def generate_votes(self, votes_cnt):
        q_ids = list(Question.objects.values_list('id', flat=True))
        a_ids = list(Answer.objects.values_list('id', flat=True))
        p_ids = list(Profile.objects.values_list('id', flat=True))
        votes = []

        for i in p_ids:
            q_likes = sample(q_ids, randint(5, 15))
            for j in q_likes:
                q = Question.objects.get(id=j)
                votes.append(Vote(content_object=q,
                                  value=1, profile_id=i))
            q_dislikes = sample(q_ids, randint(5, 15))
            for j in q_dislikes:
                if j not in q_likes:
                    q = Question.objects.get(id=j)
                    votes.append(Vote(content_object=q,
                                      value=-1, profile_id=i))
            a_likes = sample(a_ids, randint(85, 100))
            for j in a_likes:
                a = Answer.objects.get(id=j)
                votes.append(Vote(content_object=a,
                                  value=1, profile_id=i))
            a_dislikes = sample(a_ids, randint(85, 100))
            for j in a_dislikes:
                if j not in a_likes:
                    a = Answer.objects.get(id=j)
                    votes.append(Vote(content_object=a,
                                      value=-1, profile_id=i))

            Vote.objects.bulk_create(votes)
            votes.clear()
            print(i)