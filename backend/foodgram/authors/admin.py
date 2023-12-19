from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class Author(UserAdmin):
    list_filter = (
        'username',
        'email',
    )


admin.site.unregister(User)
admin.site.register(User, Author)

admin.site.empty_value_display = 'Не задано'
