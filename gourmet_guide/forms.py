from django import forms  # Djangoのフォーム機能を使用するためのモジュール

from django.core.exceptions import ValidationError  # バリデーションエラーを扱うためのモジュール

from hashlib import sha256  # ハッシュ化のためのモジュール

from .models import Shop  # Shopモデルをインポート

import time  # 現在のタイムスタンプを取得するために使用


import time


class ShopCreateForm(forms.ModelForm):

    class Meta:

        model = Shop

        fields = ["name", "address", "category", "image"]


    # 画像ファイルのバリデーションを行うためのclean_imageメソッド

    def clean_image(self):

        image = self.cleaned_data.get('image')

        if image:

            # 1. 画像ファイルの拡張子を確認

            allowed_extensions = ['jpg','jpeg','png']

  # ファイル名から拡張子を取得し小文字に変換

            file_extension = image.name.lower().split('.')[-1]

            print("file_extension",file_extension)

            if not any(file_extension.endswith(ext) for ext in allowed_extensions):

                raise ValidationError("JPEGまたはPNGフォーマットの画像ファイルをアップロードしてください。")


            # 2. ファイル名をハッシュ化

            time_int = int(time.time())

            hashed_filename = sha256(image.name.encode()).hexdigest()[:10] # ファイル名をハッシュ化して10文字までにする

            image.name = f"{hashed_filename}{str(time_int)}.{file_extension}" # 新しいファイル名をハッシュ値 + タイムスタンプ + 拡張子に設定


        return image