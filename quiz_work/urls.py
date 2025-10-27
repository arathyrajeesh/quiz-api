"""
URL configuration for quiz_work project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from quiz.views import QuizViewSet, QuestionViewSet, OptionViewSet, UserAnswerViewSet, SubmitQuizAPIView

router = DefaultRouter()
router.register('quizzes', QuizViewSet)
router.register('questions', QuestionViewSet)
router.register('options', OptionViewSet)
router.register('answers', UserAnswerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include(router.urls)),
    path('quiz/submit/', SubmitQuizAPIView.as_view(), name='submit-quiz'),  
]

