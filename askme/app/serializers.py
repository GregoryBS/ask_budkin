from rest_framework import serializers
from .models import Profile, Tag, Question, Answer, Vote

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'nick', 'avatar', 'user']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'text', 'q_date', 'rating', 'profile', 'tags']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'a_date', 'profile', 'question', 'is_correct']
