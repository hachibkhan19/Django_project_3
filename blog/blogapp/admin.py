from django.contrib import admin
from .models import Author, Category, Article, Comment


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["__str__", "details"]
    list_display = ["__str__"]
    list_per_page = 3

    class Meta:
        model = Author


admin.site.register(Author, AuthorAdmin)


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["__str__"]
    list_per_page = 3

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ["__str__"]
    list_display = ["__str__", "posted_on"]
    list_filter = ["category", "posted_on"]
    list_per_page = 4

    class Meta:
        model = Article


admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)
