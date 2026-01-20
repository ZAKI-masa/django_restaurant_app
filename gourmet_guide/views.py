from django.shortcuts import render

# Create your views here.
from django.views import generic
#genericとは

from .models import Category, Shop
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import requests
import urllib
from django.core.exceptions import PermissionDenied
from .forms import ShopCreateForm 




class IndexView(generic.ListView):
#Listview=一覧表示でmodel=Shopで指定
    model = Shop


class DetailView(generic.DetailView):
    template_name='gourmet_guide/wonderful_shop_detail.html'

    model=Shop
    # #modelを指定  shopと関係のないデータを渡したい時
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        shop_instance=self.get_object()
        print("shop_instance:",shop_instance)
        address=shop_instance.address
        make_Url="https://msearch.gsi.go.jp/address-search/AddressSearch?q="

        # 住所をURLエンコード（日本語や特殊文字をURL安全な形式に変換）
        # 例: "東京都" → "%E6%9D%B1%E4%BA%AC%E9%83%BD"

        s_quote=urllib.parse.quote(address)

        # 国土地理院APIにリクエストを送信
        # レスポンスはJSON形式で座標情報などを含む

        response=requests.get(make_Url+s_quote)
        print("response:",response)
        print("response_text:",response.text)
            # response.json()[0] = 最初の検索結果

          # ['geometry']['coordinates'] = [経度, 緯度] の配列

        coordinates = response.json()[0]["geometry"]["coordinates"]

        print("coordinates", coordinates)
        reversed_coordinates=reversed(coordinates)
        context["coordinates"]=",".join(map(str,reversed_coordinates))
        print("context['coordinates']", context['coordinates'])



        return context


class CreateView(LoginRequiredMixin,generic.edit.CreateView):
    model=Shop
    form_class = ShopCreateForm # fieldsをこれに変更
    # フォームデータを取得し、データベースに保存するなどの操作を行う
    def form_valid(self,form):
        # authorに今ログインしてきたユーザー名を代入
        form.instance.author = self.request.user

        # .form_valid()で保存し、success_urlで指定した場所へリダイレクトする super()で親クラスのform_validメソッドを呼び出す 親クラス＝generic.edit.CreateView
        return super(CreateView, self).form_valid(form)
     



class UpdateView(LoginRequiredMixin,generic.edit.UpdateView):
    model=Shop
    fields = ['name', 'address', 'category','image'] 
    def dispatch(self,request,*args,**kwargs):
        # 現在の表示データのデータを取得
        obj=self.get_object() # ページ取得
        if obj.author != self.request.user:
            # エラーの場合、以下メッセージを表示
            raise permissionDenied("You do not have permission to edit.")
        # 親クラスのdispatchが呼ばれ、リクエスト（getとか）に応じて処理がされる
        return super(UpdateView,self).dispatch(request,*args,**kwargs) # 親クラス(UpdateView)のdispatchメソッドを呼び出す



class DeleteView(LoginRequiredMixin,generic.DeleteView):
    model=Shop
    # reverse_lazyの引数に表示したいページのnameを指定
    success_url=reverse_lazy("gourmet_guide:index")
