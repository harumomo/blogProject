import datetime as datetime
from django.db import models
from datetime import datetime


class UserInfo(models.Model):
    username = models.CharField("用户名", max_length=32)
    password = models.CharField("密码", max_length=16)
    telephone = models.CharField("电话号码", max_length=11, default='')
    choice = ((1, '男'), (2, '女'), (3, '保密'))
    sex = models.IntegerField("性别", choices=choice, default=3)
    age = models.IntegerField("年龄", default=0)
    choice2 = ((1, '是'), (2, '否'))
    status = models.IntegerField("是否为管理员", choices=choice2, default=2)

    def __str__(self):
        return self.username


class Blog(models.Model):
    title = models.CharField("标题", max_length=64)
    context = models.TextField("内容")
    user = models.ForeignKey(verbose_name="作者", to=UserInfo, on_delete=models.CASCADE)
    datetime = models.DateTimeField("发布时间", default=datetime.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(verbose_name="博客", to=Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="作者", to=UserInfo, on_delete=models.CASCADE)
    comment = models.TextField("评论")
    datetime = models.DateTimeField("评论时间", default=datetime.now)

    def __str__(self):
        return self.comment
