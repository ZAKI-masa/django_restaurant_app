from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=255)

    

    author = models.ForeignKey(

        'auth.User',  # Djangoのデフォルトのユーザーモデルを指定

        on_delete=models.CASCADE,  # ユーザーが削除された場合、関連するカテゴリも削除

    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):

        return self.name
        



class Shop(models.Model):

    name = models.CharField(max_length=255)

    address = models.CharField(max_length=255)
    # 画像pathを保存するためのフィールド
    image = models.ImageField(upload_to='images', null=True)
    

    author = models.ForeignKey(

        'auth.User',  

        on_delete=models.CASCADE, 

    )

    

    category = models.ForeignKey(

        Category,  

        on_delete=models.PROTECT,  

    )

    

    created_at = models.DateTimeField(auto_now_add=True)    

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
         # 飲食店の名前を文字列として返す（管理画面などで表示される）
        return self.name
        

    def get_absolute_url(self):
        # 新規作成したら詳細ページにリダイレクト
        return reverse('gourmet_guide:detail', kwargs={'pk': self.pk})


