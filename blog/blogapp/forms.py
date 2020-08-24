from django import forms
from .models import Article, Author, Comment, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewPostCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'body',
            'image',
            'category'
        ]


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]


class CreateAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'image',
            'details'
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'post_comment'
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name'
        ]
