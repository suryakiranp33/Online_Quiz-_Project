
from rest_framework import viewsets
from .models import Quiz, QuizScore,QuizUser, Question, Answer, UserQuizResponse
from .serializers import QuestionListSerializer, QuizResultSerializer, QuizSerializer, QuestionSerializer, ChoiceSerializer, UserCreateSerializer, UserQuizResponseSerializer, UserSerializer
import logging
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, 
                                     RetrieveUpdateAPIView)
logger = logging.getLogger(__name__)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist


class QuizViewSet(CreateAPIView):

   

    queryset = Quiz.objects.order_by('id').all()
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
 


    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                  
                  q_title = self.request.data.get('title')
                  user=self.request.user
                  userobj=QuizUser.objects.get(user=user)
                  q_row = {}
                  q_row.update(
                        {
                            'title': q_title,
                        }
                    )
                  quiz_serializer = QuizSerializer(data=q_row)
                  quiz_serializer.is_valid(raise_exception=True)
                  quiz_datas = quiz_serializer.save(user=userobj)
                  question_data = self.request.data.get('questions')
                  for question_dt in question_data:
                   
                    quiz_dic = {}
                
                    quiz_dic.update(
                        {
                            'quiz': quiz_datas.id,
                            'text': question_dt["text"],
                           
                        }
                    )
                    if question_dt["text"]:
                        question_serializer = QuestionSerializer(data=quiz_dic)
                     
                        question_serializer.is_valid(raise_exception=True)
                        question_obj = question_serializer.save(user=userobj)
                    choices = question_dt["choices"]
                    for i in choices:
                        choice_row = {}
            
          
                        choice_row.update(
                            {
                                'question': question_obj.id,
                                'text': i["text"],
                                'is_correct':i["is_correct"],
                               
                            }
                        )
                        if question_dt["choices"]:
                            ans_serializer = ChoiceSerializer(data=choice_row)
                            # Validation check
                            ans_serializer.is_valid(raise_exception=True)
                            ans_datas = ans_serializer.save(user=userobj)
                  data['status'] = 'success'
                  data['message'] = 'created'
                  data["code"]=200
            else:
                data['message'] = 'create_failed'             
                data['status'] = 'failed'
                data["code"]=422
            return data

        except Exception as exception:
            logger.exception(
                "Exception occuring while fetching  %s", exception
            )
            data["status"] = "failed"
            data["message"] = 'something_went_wrong'
            data['code'] = 500
        return data      

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)

        if data['status'] == True:
            return Response(data=data, status=201)
        elif data['status'] == False:
            return Response(data=data, status=400)
        else:
            return Response(data=data, status=500)
                                           
class UserDetail(RetrieveUpdateAPIView):
    queryset = QuizUser.objects.order_by('id').all()
    serializer_class = UserCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"

    def perform_update(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                
                object_id = self.kwargs.get("pk")
                emp_obj = QuizUser.objects.get(id=object_id)
                data["message"] = "User detail"
                data["status"] = "success"
                data["code"] = 200

            else:
                data["message"] = "Failed"
                data["status"] = "failed"
                data['code'] = 422

        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] ='something_went_wrong'
            data['code'] = 500
        return data

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        data={}
        data["message"] ="enter_valid_inputs"
        data["status"] = "failed"
        return Response(data=data,status=406)          

class UserUpdateView(RetrieveUpdateAPIView):
    queryset = QuizUser.objects.order_by('id').all()
    serializer_class = UserCreateSerializer  
    lookup_field = "pk"
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_update(self, serializer):
        try:
            data = {}
            
            if serializer.is_valid():
                serializer.save()
                data['message'] = 'User updated'
                data['status'] = 'Success'
                return data
            else:
                data['message'] = 'update_failed'
                data['details'] = serializer.errors
                data['status'] = 'Failed'
            return data
        except Exception as exception:
            logger.exception(
                "Exception occuring while updating User %s", exception
            )
            return {
                'status': 'Failed',
                'message': 'something_went_wrong'
            }

    def update(self, request, *args, **kwargs):
        instance = self.get_object()   
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial) 
        data = self.perform_update(serializer)
        if data['status'] == 'Success':
            return Response(data=data, status=200)
        elif data['status'] == 'Failed':
            return Response(data=data, status=400)
        else:
            return Response(data=data, status=500)

class UserDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = QuizUser.objects.order_by('id').all()
    serializer_class = UserCreateSerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        try:
            data = {}
            instance.delete()
            data['status'] = "success"
            data['message'] = 'User_deleted'
            return data
        except Exception as exception:
            logger.exception(
                "Exception occuring while deleting User %s", exception
            )
            data['message'] = 'something_went_wrong'
            data['status'] = 'failed'
            return data

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        if data['status'] == 'success':
            return Response(data=data, status=200)
        elif data['status'] == 'failed':
            return Response(data=data, status=400)
        else:
            return Response(data=data, status=500)

class UserListView(ListAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get_queryset(self, *args, **kwargs):

        try:
           
            obj = QuizUser.objects.all()

            return obj
        except Exception as exception:
            logger.exception(
                "Exception occuring while fetching User %s ", exception
            )
            
class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            QuizUser.objects.create(user=user,email=user.email,username=user.username)
            token = Token.objects.create(user=user)
            data = {
                'token': token.key,
                'user': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutUser(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Logout successfull"}, status=status.HTTP_200_OK)

class QuizAttendView(CreateAPIView):
    queryset = UserQuizResponse.objects.order_by('id').all()
    serializer_class = UserQuizResponseSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                  object_id = self.kwargs.get("pk") 
                  quiz = Quiz.objects.get(id=object_id)           
                  user=self.request.user
                  user_obj=QuizUser.objects.get(user=user)
                  items = self.request.data.get('items')
                                  
                  for item_obj in items:                  
                    obj=UserQuizResponse.objects.filter(question=item_obj["question"])
                    if obj:
                        data['status'] = 'failed'
                        data['message'] = 'already Quiz is taken'
                        data["code"]=200
                    else:
                        tab_row = {}                                  
                        tab_row.update(
                            {   'quiz':quiz.id,
                                'question': item_obj["question"],
                                'response': item_obj["response"],
                                'user': user_obj.id,                           
                            }
                        )
                        if item_obj["response"]:                       
                            quiz_response_serializer = UserQuizResponseSerializer(data=tab_row)                           
                            quiz_response_serializer.is_valid(raise_exception=True)
                            quiz_datas = quiz_response_serializer.save()                         
                            data['status'] = 'success'
                            data['message'] = 'created'
                            data["code"]=200
                        else:
                            data['status'] = 'failed'
                            data['message'] = 'failed'
                            data["code"]=422
              
            else:
                    
                data['message'] = 'create_failed'
                data['status'] = 'failed'
                data["code"]=422
        
            return data

        except Exception as exception:
            logger.exception(
                "Exception occuring while fetching  %s", exception
            )
            data["status"] = "failed"
            data["message"] = 'something_went_wrong'
            data['code'] = 500

        print(data)
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)
        if data['status'] == True:
            return Response(data=data, status=201)
        elif data['status'] == False:
            return Response(data=data, status=400)
        else:
            return Response(data=data, status=500)

class QuestionListView(ListAPIView):
    serializer_class = QuestionListSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get_queryset(self, *args, **kwargs):

        try:
           
            obj = Question.objects.all()

            return obj
        except Exception as exception:
            logger.exception(
                "Exception occuring while fetching Question%s", exception
            )


class QuizResultView(generics.ListCreateAPIView):
    queryset = QuizScore.objects.all()
    serializer_class = QuizResultSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        data = {}
        quiz_id = kwargs['quiz_id']
        user=self.request.user
        user_obj=QuizUser.objects.get(user=user)
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.questions.all()
        scorecheck_obj=QuizScore.objects.filter(quiz=quiz_id)
        respose_obj=UserQuizResponse.objects.filter(quiz=quiz_id)
        if scorecheck_obj:
           data['status'] = "Failed"
           data['message'] = 'Cannot Submit Again'
        else:
            count=0
            for i in respose_obj:
                if(i.response.is_correct==True):
                    count=count+1
            sum=(count/questions.count())*100
            score_obj = QuizScore.objects.create(user=user_obj,score=sum,quiz=quiz)
            data['status'] = "Success"
            data['message'] = 'Score percentage calculated'
        return Response(data=data)

class QuizScoreListView(ListAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get_queryset(self, *args, **kwargs):
        try:         
            obj = QuizScore.objects.all()
            return obj
        except Exception as exception:
            logger.exception(
                "Exception occuring while fetching Score %s", exception
            )