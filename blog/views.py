from django import template
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.views.generic.list import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from plants_app.config import pagination
from .models import Post, Category, Images
from .forms import PostForm, ImagesForm
from plants_app import settings
from main.models import NewsletterUser
from .serializers import PostSerializer


class PostListView(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        if self.request.method == 'GET' and 'orderby' in self.request.GET:
            order_by = self.request.GET.get('orderby', 'id')
            if order_by is not None and order_by != '':
                posts = Post.objects.all().order_by(order_by)
        else:
            posts = Post.objects.all().order_by('-created')

        return posts

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['orderby'] = self.request.GET.get('orderby', 'id')
        # context['all_table_fields'] = Post._meta.get_fields()
        return context


class PostDetailView(ListView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        num_likes = stuff.num_likes()
        context["num_likes"] = num_likes

        return context


# API

class FilterPostView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('created', 'updated', 'place', 'author', 'category')
    ordering = ('created',)  # default posts ordering


class SearchPostView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title', 'description')
    pagination_class = PageNumberPagination


def post_list(request):
    object_list = Post.objects.filter(status='Published')
    pages = pagination(request, object_list, 15)

    template = 'blog/post_list.html'
    context = {'post_list': object_list,
               'page_obj': pages}

    return render(request, template, context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    files = Images.objects.filter(images=Images.images)

    template = 'blog/post_detail.html'
    context = {'post': post, 'files': files}

    return render(request, template, context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    post = Post.objects.filter(category=category, status='Published')

    template = 'blog/category_detail.html'
    context = {
        'category': category,
        'post': post
    }
    return render(request, template, context)


def search(request):
    query = request.GET.get('q')
    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        results = Post.objects.filter(status='Published')

    pages = pagination(request, results, num=3)

    template = 'blog/post_list.html'
    context = {'page_obj': pages,
               'query': query,
               'object_list': pages,
               }

    return render(request, template, context)


@login_required(login_url='/authentication/login')
def new_post(request):
    form = PostForm(request.POST, request.FILES)
    img_form = ImagesForm(request.POST, request.FILES)
    image = request.FILES.getlist('images')  # field name in model
    image_list = []

    if form.is_valid() and img_form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()  # we should be updating the instance not the form, if we write: img_form.save() and form.save() this will give us an error
        for img in image:
            image_instance = Images.objects.create(images=img, post=instance)
            image_instance.save()
            image_list.append(image_instance)

        messages.success(request, 'New post has been successfully added!')
        # print(image_list)
        if form.data['status'] == 'Draft':
            form = PostForm()

        else:
            send_email_if_new_post(form)
            form = PostForm()
    else:
        form = PostForm()
        img_form = ImagesForm()

    return render(request, 'blog/new_post.html', {'form': form, 'img_form': img_form, 'image_list': image_list})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    form = PostForm(instance=post)


    if request.method == 'POST' and user.id == post.author.id:
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save()
            messages.success(request, 'The blog post has been updated!')

    elif request.method == 'POST' and user.id != post.author.id:
        messages.warning(request, 'Not your blog post, your must be login as a proper user to edit/delete')

    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    template = 'blog/new_post.html'

    return render(request, template, context)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    form = PostForm(instance=post)
    if request.method == 'POST' and user.id == post.author.id:
        post.delete()
        form = PostForm()
        messages.success(request, 'You have successfully delete the post.')

    elif request.method == 'POST' and user.id != post.author.id:
        messages.warning(request, 'Not your blog post, your must be login as a proper user to edit/delete')

    else:
        form = PostForm(instance=post)

    template = 'blog/new_post.html'
    context = {
        'form': form,
        'post': post
    }

    return render(request, template, context)


@staff_member_required
def post_list_admin(request):
    post = Post.objects.all()

    pages = pagination(request, post, 10)

    context = {
        'post_list_admin': pages,
        'page_obj': pages}
    templates = 'blog/post_list_admin.html'

    return render(request, templates, context)


def send_email_if_new_post(form):
    subscribers = NewsletterUser.objects.all()
    title = f"New post has been added to blog: {form.data['title']} "
    body = {
        'description': form.data['description'],
    }
    plaintext = template.loader.get_template('blog/new_post_form.txt')
    htmltemp = template.loader.get_template('blog/new_post_form.html')
    from_email = settings.EMAIL_HOST_USER
    text_content = plaintext.render(body)
    html_content = htmltemp.render(body)

    for sub in subscribers:
        try:
            msg = EmailMultiAlternatives(title, text_content, from_email, [sub.email],
                                         headers={'Reply-To': 'YOUR-GMAIL'})
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

        except BadHeaderError:
            return HttpResponse('Invalid header found.')

    # for sub in subscribers:
    #     send_mail(subject=f"New post has been added to blog: {title}",
    #               message=f"{body}", from_email=settings.EMAIL_HOST_USER,
    #               recipient_list=[sub.email], fail_silently=True)
    #


def like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('blog:post_detail', slug=post.slug)
