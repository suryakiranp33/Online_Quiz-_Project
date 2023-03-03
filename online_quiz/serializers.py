from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizScore, QuizUser, UserQuizResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.serializers import (
    SerializerMethodField,
)
import logging
logger = logging.getLogger(__name__)

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct','question']

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'text','quiz']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizUser
        # fields = '__all__'
        exclude = ["email","user"]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')        

class UserQuizResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserQuizResponse
        fields = "__all__"

class QuestionListSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    quiz = SerializerMethodField(read_only=True)
    choices = SerializerMethodField(read_only=True)    
    def get_choices(self, obj):
        try:
            if obj:
                owner_item=[]
                answer_obj = Answer.objects.filter(question=obj.id)
                for items in answer_obj:
                    owner_item.append(
                        {
                            "id": items.id,
                            "text": items.text,
                          
                        }
                    )
                return owner_item
            else:
                return None
        except Exception as exception:
            logger.exception("Getting Exception while Fetching choices  as %s", exception)
        return None

    def get_quiz(self,obj):
        try:
            if obj.quiz.title:
                data={
                    "name":obj.quiz.title,
                    "id":obj.quiz.id,
                }
                return data
            else:
                return None
        except Exception as exception:
            logger.exception(
                "Getting Exception while Fetching Quiz tittle as %s", exception
            )
            return None

    class Meta:
        model = Question
        fields = ['id', 'text','quiz','choices']

class QuizResultSerializer(serializers.ModelSerializer):
    quiz = SerializerMethodField(read_only=True)
    user = SerializerMethodField(read_only=True)

    def get_user(self,obj):
        try:
            if obj.user.username:
                data={
                    "name":obj.user.username,
                    "id":obj.user.id,
                }
                return data
            else:
                return None
        except Exception as exception:
            logger.exception(
                "Getting Exception while Fetching user as %s", exception
            )
            return None
        
    def get_quiz(self,obj):
        try:
            if obj.quiz.title:
                data={
                    "name":obj.quiz.title,
                    "id":obj.quiz.id,
                }
                return data
            else:
                return None
        except Exception as exception:
            logger.exception(
                "Getting Exception while Fetching quiz as %s", exception
            )
            return None
        
    class Meta:
        model = QuizScore
        fields = ('id', 'user', 'quiz', 'score')