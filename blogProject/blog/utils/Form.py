from django import forms
from django.forms import ModelForm, Form
from blog import models


class BootStrap:
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
        fields = "__all__"


class LoginForm(BootStrap, Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput
    )


class BlogModelForm(BootStrap, ModelForm):
    class Meta:
        model = models.Blog
        fields = ["title", "context"]
