from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class UserLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
  
class QuizUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE, related_name='quizuser',default=None)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE, related_name='questionuser',default=None)

    def __str__(self):
        return self.text
        
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE, related_name='answeruser',default=None)

    def __str__(self):
        return self.text

class UserQuizResponse(models.Model):
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE, related_name='responseuser',default=None)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,default=None)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,default=None)
    response = models.ForeignKey(Answer, on_delete=models.CASCADE,default=None)

class QuizScore(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,default=None)
    score = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE, related_name='scoreuser',default=None)



   
