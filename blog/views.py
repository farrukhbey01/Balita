from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
import requests

BOT_TOKEN = '6235320770:AAEG9jfSuctcyNQEPrr_IjdZLWoIVM0NYhk'
CHAT_ID = '5046341911'

def home(request):
    data = request.GET
    cat = data.get('cat', None)
    page = data.get('page', 1)
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True)
    popular_posts = posts.order_by('-view_count')[:3]
    new_posts = posts.order_by('-created_at')[:3]
    page_obj = Paginator(posts, 2)
    tag = Tag.objects.all()
    latest_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    top_posts = Post.objects.filter(is_published=True).order_by('-view_count')[:3]

    d = {
        # 'posts': posts,
        'blog': 'active',
        'new_posts': new_posts,
        'popular_posts': popular_posts,
        'posts': page_obj.get_page(page),
        "categories": categories,
        'tags': tag,
        'latest_posts': latest_posts,
        'popular_posts': popular_posts,
        'top_posts': top_posts,
        'home': 'active',
        'paginator': 'active'

    }

    return render(request, 'index.html', context=d)


def about(request):
    data = request.GET
    posts = Post.objects.filter(is_published=True)
    latest_posts = Post.objects.filter(is_published=True).order_by('-created_at')
    tags = Tag.objects.all()
    categories = Category.objects.all()
    page = data.get('page', 1)
    page_obj = Paginator(latest_posts, 4)
    popular_posts = posts.order_by('-view_count')[:3]
    return render(request, 'about.html',
                  context={'paginator': 'active', 'posts': page_obj.get_page(page), 'about': 'active',
                           'latest_posts': latest_posts,
                           'categories': categories,
                           'popular_posts': popular_posts, 'tags': tags})


def blog_detail(request, pk):
    tags = Tag.objects.all()
    posts = Post.objects.all()
    categories = Category.objects.all()
    latest_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    top_posts = Post.objects.filter(is_published=True).order_by('-view_count')[3:8]
    popular_posts = Post.objects.order_by('-view_count')[:3]
    if request.method == 'POST':
        data = request.POST

        comment = Comment.objects.create(post_id=pk, name=data["name"], email=data["email"], message=data["message"])
        comment.save()
        post = Post.objects.filter(id=pk).first()
        post.comments_count += 1
        post.save(update_fields=['comments_count'])
        return redirect(f'/blog/{pk}/')
    blog = Post.objects.filter(id=pk).first()
    blog.view_count += 1
    blog.save(update_fields=['view_count'])
    comments = Comment.objects.filter(post_id=pk)
    d = {'tags': tags, 'posts': posts, 'top_posts': top_posts, 'latest_posts': latest_posts,
         'popular_posts': popular_posts, 'blog': blog, 'comments': comments, 'comments_count': len(comments),
         'categories': categories}
    return render(request, 'blog-single.html', context=d)


def tags(request, pk):
    tags = Tag.objects.all()

    categories = Category.objects.all()
    tag = Tag.objects.get(pk=pk)

    tag_posts = Post.objects.filter(tags=tag)
    return render(request, 'index.html', {'tag': tag, 'posts': tag_posts,
                                          'categories': categories, 'tags': tags,
                                          })


def about(request):
    data = request.GET
    posts = Post.objects.filter(is_published=True)
    latest_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:2]
    tags = Tag.objects.all()
    categories = Category.objects.all()
    page = data.get('page', 1)
    page_obj = Paginator(posts, 2)
    posts = Post.objects.filter(is_published=True)
    popular_posts = posts.order_by('-view_count')[:3]
    return render(request, 'about.html',
                  context={'posts': page_obj.get_page(page), 'about': 'active', 'latest_posts': latest_posts,
                           'categories': categories,
                           'popular_posts': popular_posts, 'tags': tags})


def contact(request):
    tags = Tag.objects.all()
    categories = Category.objects.all()
    latest_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    popular_posts = Post.objects.order_by('-view_count')[:3]
    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(full_name=data['name'], email=data['email'], phone=data['phone'],
                                     message=data['message'])
        obj.save()
        text = f"""
        project: BALITA
        id: {obj.id}
        name:{obj.full_name} 
        phone:{obj.phone}        
        message:{obj.message}  
        """
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}'
        response = requests.get(url)
        print(response)
        return redirect('/contact')
    return render(request, 'contact.html', context={'tags': tags, 'contact': 'active', 'popular_posts': popular_posts,
                                                    'latest_posts': latest_posts, 'categories': categories})


def category(request):
    tags = Tag.objects.all()
    categories = Category.objects.all()
    latest_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    data = request.GET
    cat = data.get('cat', None)
    popular_posts = Post.objects.order_by('-view_count')[:3]

    if cat:
        cat_name = categories.filter(id=cat).first()
        posts = Post.objects.filter(is_published=True, category_id=cat)
        d = {
            'cat_name': cat_name,
            'posts': posts,
            'blog': 'active',
            'categories': categories,
            'popular_posts': popular_posts,
            'latest_posts': latest_posts,
            'category': 'active',
            'tags': tags

        }
        return render(request, 'category.html', context=d)

    posts = Post.objects.filter(is_published=True)
    view = Category.objects.filter(post_id=pk)

    page_obj = Paginator(posts, 2)
    d = {
        'posts': posts,
        'blog': 'active',
        'posts': page_obj.get_page(page),
        'view': len(view),
        'latest_posts': latest_posts,
        'category': 'active',
    }

    return render(request, 'category.html', context=d)

    page_obj = Paginator(posts, 2)
    d = {
        # 'posts': posts,
        'blog': 'active',
        'posts': page_obj.get_page(page_number),
        'view': len(view)
    }

    return render(request, 'category.html', context=d)


#
# def tag_view(request):
#
#     return render(request, 'category.html', context=d)

def search(request):
    categories = Category.objects.all()
    popular_posts = Post.objects.order_by('-view_count')[:3]
    tags = Tag.objects.all()
    d = {'categories': categories, 'popular_posts': popular_posts, 'tags': tags}
    if request.method == 'POST':
        data = request.POST
        query = data['query']
        posts = Post.objects.filter(is_published=True, name__icontains=query)
        # result = list(filter(lambda x:query in x.title,posts))

        d['posts'] = posts

    return render(request, 'category.html', context=d)
