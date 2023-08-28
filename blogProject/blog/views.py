from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from blog import models
from blog.utils.Form import BlogModelForm, RegisterModelForm, LoginForm
from blog.utils.Pagination import Pagination
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):
    """用户注册"""
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    # 非空验证，输入不为空则将数据存入数据库，并返回主页
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    """用户登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    # 非空验证
    if form.is_valid():
        row = models.UserInfo.objects.filter(**form.cleaned_data).first()
        # 注册验证
        if not row:
            form.add_error("password", "用户名或密码错误，未注册请先注册。")
            return render(request, 'login.html', {'form': form})
        # 用户认证成功，在session中存数据
        request.session["info"] = {'id': row.id, 'username': row.username, 'status': row.status}
        return redirect('/blog/')
    return render(request, 'login.html', {'form': form})


def logout(request):
    """用户注销"""
    # 清空session中该用户的数据
    request.session.clear()
    return redirect('/blog/')


def blog(request):
    """博客全部文章展示"""
    if request.method == 'GET':
        search_data = request.GET.get('search')
        if search_data:
            search_data = models.Blog.objects.filter(Q(title=search_data) | Q(context__contains=search_data))
            page = Pagination(request, search_data)
            queryset = page.page_queryset
            page_string = page.html()
            context = {
                'data': queryset,
                'page_string': page_string
            }
            return render(request, 'blog.html', context)
        # 没有搜索值执行
        queryset = models.Blog.objects.all().order_by("-id")
        page = Pagination(request, queryset)
        queryset = page.page_queryset
        page_string = page.html()
        context = {
            'data': queryset,
            'page_string': page_string
        }
        return render(request, 'blog.html', context)


@csrf_exempt
def create(request):
    """写博客"""
    if request.method == "GET":
        form = BlogModelForm()
        return render(request, 'create.html', {'form': form})
    form = BlogModelForm(data=request.POST)
    if form.is_valid():
        # 添加用户UID
        form.instance.user_id = request.session['info']['id']
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def show(request, nid):
    """展示博客"""
    blog_data = models.Blog.objects.filter(id=nid).first()
    return render(request, 'show.html', {'blog': blog_data})


def user(request):
    """用户管理"""
    userinfo = models.UserInfo.objects.all().order_by("-id")
    page = Pagination(request, userinfo)
    queryset = page.page_queryset
    page_string = page.html()
    form = RegisterModelForm()
    context = {
        'form': form,
        'queryset': queryset,
        'page_string': page_string
    }
    return render(request, 'userlist.html', context)
