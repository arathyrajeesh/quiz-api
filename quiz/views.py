from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Quiz, Question, Option, UserAnswer
from .serializers import QuizSerializer, QuestionSerializer, OptionSerializer, UserAnswerSerializer
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SubmitAnswerSerializer


class SubmitQuizAPIView(APIView):
    def post(self, request):
        serializer = SubmitAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quiz_id = serializer.validated_data['quiz_id']
        answers = serializer.validated_data['answers']

        score = 0
        results = []

        for ans in answers:
            qid = ans.get('question')
            oid = ans.get('selected_option')

            try:
                option = Option.objects.get(id=oid, question_id=qid)
                correct = option.is_correct
                if correct:
                    score += 1
                results.append({
                    "question": qid,
                    "selected_option": oid,
                    "is_correct": correct
                })
            except Option.DoesNotExist:
                results.append({
                    "question": qid,
                    "selected_option": oid,
                    "is_correct": False
                })

        return Response({
            "quiz_id": quiz_id,
            "score": score,
            "results": results
        }, status=status.HTTP_200_OK)


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    @action(detail=False, methods=['post'])
    def submit(self, request):
        user = request.data.get('user')
        answers = request.data.get('answers', [])  

        score = 0
        for ans in answers:
            q = Question.objects.get(id=ans['question'])
            selected = Option.objects.get(id=ans['selected_option'])
            UserAnswer.objects.create(user=user, question=q, selected_option=selected)
            if selected.is_correct:
                score += 1

        return Response({'user': user, 'score': score, 'total': len(answers)}, status=status.HTTP_200_OK)
