from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'view_count', 'publish_date')
    search_fields = ('title',)

admin.site.register(Article, ArticleAdmin)
