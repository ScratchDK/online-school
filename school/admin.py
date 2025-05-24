from django.contrib import admin
from school.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'preview_image')
    search_fields = ('title',)

