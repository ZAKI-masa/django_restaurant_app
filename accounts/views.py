from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
# Create your views here.

class SignUpView(generic.CreateView):
    # 使用するフォームクラスを指定
    # UserCreationFormはusername、password1、password2フィールドを持つ
    form_class = UserCreationForm

    # 登録成功後のリダイレクト先（ログインページ）
    succsess_url = reverse_lazy('login')
    template_name = "accounts/signup.html"
    

 