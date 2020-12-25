from django.contrib import admin

from myboard.models import Profile, Task


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Task)
