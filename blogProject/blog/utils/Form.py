from django import forms
from django.forms import ModelForm, Form
from blog import models
from blog.utils.md5 import md5


class BootStrap:
    """显示固定样式"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中所有字段，给每个字段把样式加上
        for name, field in self.fields.items():
            # 字段中有属性，保留原来的属性，没有属性的才增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs = {"class": "form-control"}


class RegisterModelForm(BootStrap, ModelForm):
    class Meta:
        model = models.UserInfo
        # 排除是否为管理员状态
        exclude = ["status"]

    def clean(self):
        # 对用户密码进行加密
        password = self.cleaned_data["password"]
        self.cleaned_data["password"] = md5(password)
        return self.cleaned_data


class LoginForm(BootStrap, Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class BlogModelForm(BootStrap, ModelForm):
    class Meta:
        model = models.Blog
        fields = ["title", "context"]


class BlogListModelForm(BootStrap, ModelForm):
    class Meta:
        model = models.Blog
        fields = ["status"]


class UserListModelForm(BootStrap, ModelForm):
    class Meta:
        model = models.UserInfo
        exclude = ["password"]
