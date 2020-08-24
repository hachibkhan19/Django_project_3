from django.shortcuts import render, get_object_or_404, redirect, Http404
from .models import Article, Category, Author, Comment
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import NewPostCreateForm, RegisterForm, CreateAuthorForm, CommentForm, CategoryForm
from django.contrib import messages
from django.views import View


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        post = Article.objects.all()
        search = request.GET.get('q')
        if search:
            post = post.filter(Q(title__icontains=search) | Q(body__icontains=search)
                               )
        paginator = Paginator(post, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "post": page_obj
        }
        return render(request, self.template_name, context)


class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request, name):
        post_author = get_object_or_404(User, username=name)
        auth = get_object_or_404(Author, name=post_author.id)
        post = Article.objects.filter(article_author=auth.id)
        context = {
            "auth": auth,
            "post": post
        }
        return render(request, self.template_name, context)


class SingleView(View):
    template_name = 'single.html'
    def get(self, request, id):
        post = get_object_or_404(Article, pk=id)
        first = Article.objects.first()
        last = Article.objects.last()
        comment = Comment.objects.filter(post=id)
        related_post = Article.objects.filter(category=post.category).exclude(id=id)[:4]
        form = CommentForm
        context = {
            "post": post,
            "first": first,
            "last": last,
            "related": related_post,
            "form": form,
            "comment": comment
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        post = get_object_or_404(Article, pk=id)
        form = CommentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.save()
            return redirect("blog:single", id=id)


class CategoryView(View):
    def get(self, request, name):
        cat = get_object_or_404(Category, name=name)
        post = Article.objects.filter(category=cat.id)
        context = {
            "post": post,
            "cat": cat
        }
        return render(request, 'category.html', context)


class RegistrationView(View):
    def get(self, request):
        form = RegisterForm
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('blog:login')
        return render(request, 'register.html', {"form": form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:index')
        else:
            return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('user')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog:index')
        else:
            messages.add_message(request, messages.WARNING, 'Your username or password mismatch.')
            return redirect('blog:login')


def create_new_post_view(request):
    if request.user.is_authenticated:
        u = get_object_or_404(Author, name=request.user.id)
        form = NewPostCreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.article_author = u
            new_post.save()
            return redirect('blog:index')
        context = {
            "form": form
        }
        return render(request, 'create_new_post.html', context)
    else:
        return redirect('blog:login')


def update_post_view(request, id):
    if request.user.is_authenticated:
        u = get_object_or_404(Author, name=request.user.id)
        post = get_object_or_404(Article, id=id)
        form = NewPostCreateForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request, "Your article is updated successfully.")
            return redirect('blog:article_auhtor_profile')
        context = {
            "form": form
        }
        return render(request, 'create_new_post.html', context)

    else:
        return redirect('blog:login')


def delete_post_view(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Article, id=id)
        post.delete()
        messages.warning(request, "Your article is deleted successfully.")
        return redirect('blog:article_auhtor_profile')
    else:
        return redirect('blog:login')


def article_auhtor_profile_view(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = Author.objects.filter(name=user.id)
        if author_profile:
            auhtorUser = get_object_or_404(Author, name=request.user.id)
            post = Article.objects.filter(article_author=auhtorUser.id)
            context = {
                "post": post,
                "auth": auhtorUser
            }
            return render(request, 'article_auhtor_profile.html', context)
        else:
            form = CreateAuthorForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save()
                return redirect('blog:article_auhtor_profile')
            return render(request, 'author.html', {"form": form})
    else:
        return render('blog:login')


class TopicView(View):
    def get(self, request):
        query = Category.objects.all()
        context = {
            "query": query
        }
        return render(request, 'topics.html', context)


def create_new_topic_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form = CategoryForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'Topic is created.')
                return redirect("blog:topics")
            return render(request, 'create_new_topic.html', {"form": form})
        else:
            raise Http404("You are not authorized access this page.")
    else:
        return redirect('blog:login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('blog:index')

