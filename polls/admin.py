from django.contrib import admin
from polls.models import Poll, Choice

"""
class PollAdmin(admin.ModelAdmin):
	fields = ['pub_date', "question"]
"""

"""
class PollAdmin(admin.ModelAdmin):
	fieldsets = [
	(None,               {'fields': ['question']}),
	('Date Information', {'fields': ['pub_date']}),
    ]
"""
"""
class ChoiceInLine(admin.StackedInline):
	model = Choice
	extra = 3
"""

class ChoiceInLine(admin.TabularInline):
	model = Choice
	exitra = 3

class PollAdmin(admin.ModelAdmin):
	fieldsets = [
	(None,		{'fields': ['question']}),
	('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']})
	]
	inlines = [ChoiceInLine]
	list_display = ('question', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['question']



# Register your models here.
admin.site.register(Poll, PollAdmin)

#Inefficent way to preview Choices
#admin.site.register(Choice)