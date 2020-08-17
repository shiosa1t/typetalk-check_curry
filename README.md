# typetalk-check_curry

![image](https://github.com/shio-salt/typetalk-check_curry/blob/master/readme.jpg?raw=true)

# 概要
このリポジトリは、Typetalkのボットのソースコードです。このボットは、トピックに投稿された画像がカレーかどうかを判定します。

# 使用方法

## 環境

Python 3.8.5での動作を確認しています。不足しているライブラリは、インストールして下さい。

## 記述

```
url = "" #メッセージURL(ボット設定ページよりコピー可能)
token = "" #ボットトークン(同上)
bot = "" #ボットID (ボットの名前に+を付け足したもの)

cloudinary.config( #Cloudnary
  cloud_name = "",
  api_key = "",
  api_secret = ""
)

```

上記にそれぞれ必要な情報を記入して下さい。このソースコードは、Cloudinaryを使用しています。

# 処理

以下の処理が毎分実行されています。  

① 直近20件の投稿を取得。  
② 画像が添付されているかを判定。(されていたら③)  
③ ボット自身が「いいね」を付けているか判定。(されていなかったら④)  
④ 画像をダウンロードして、Cloudinaryにアップロードする。(画像URLを取得)  
⑤ 取得した画像URLを用いて、Google画像検索を行う。  
⑥ 検索ワードを取得し、"curry"または「カレー」が含まれているか判定。  
⑦ 判定結果をリプライする。  

# ライセンス

[MIT](https://choosealicense.com/licenses/mit/)
