from django.contrib import admin
from .models import Post,BlogComment


# Register your models here.
# admin.site.register((Post,BlogComment)) bef0re tiny editor
admin.site.register((BlogComment))
@admin.register(Post)
class postAdmin (admin.ModelAdmin):
    class Media:
        js = ('tiny.js',)