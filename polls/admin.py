from django.contrib import admin

from .models import Question, Choice


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    list_per_page = 10


admin.site.register(Question, QuestionAdmin)
admin.AdminSite.site_header = 'Polls Administration'
