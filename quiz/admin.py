from django.contrib import admin
from .models import Quiz, Question, Option, UserAnswer


class OptionInline(admin.TabularInline):
    model = Option
    extra = 2  


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('title',)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'quiz')
    list_filter = ('quiz',)
    search_fields = ('text',)
    inlines = [OptionInline]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text',)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'selected_option', 'submitted_at')
    list_filter = ('user', 'submitted_at')
    search_fields = ('user',)
