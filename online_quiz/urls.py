from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.urls import path, include

router = routers.DefaultRouter()

urlpatterns = router.urls
urlpatterns = [
 
    path("quizzes/",views.QuizViewSet.as_view(),),
    path('login/', obtain_auth_token, name='api_login'),
    path('logoutuser/', views.LogoutUser.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='api_register'),
    path(
        "user/<int:pk>/edit/",
        views.UserUpdateView.as_view(),
    ),
    path(
        "user/<int:pk>/delete/",
        views.UserDeleteView.as_view(),
    ),
 
    path("userlist/",views.UserListView.as_view(),),
    

    path(
        "userdetail/<int:pk>/",
        views.UserDetail.as_view()
        ),
    path(
        "userquizattend/<int:pk>/",
        views.QuizAttendView.as_view()
        ),
    path("questionlist/",views.QuestionListView.as_view(),
        ),
    path(
        "quizscore/calculate/<str:quiz_id>/",
        views.QuizResultView.as_view()
        ),
    path("quizscore/",views.QuizScoreListView.as_view(),),
 
]