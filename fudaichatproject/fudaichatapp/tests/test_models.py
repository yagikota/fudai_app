from django.contrib.auth import get_user_model
from django.test import TestCase

'''
ユーザー1がサイトのトップページに訪問
会員登録ボタン押す
    (会員登録していない場合)
    会員登録formに遷移
    メールアドレス(必須)、ユーザー名(3文字以上, 必須)、パスワード(必須)入力
    (正しく入力された場合)
        メール受信
        メールのurlクリック(期限)
        メールアドレスの確認画面に遷移
        確認ボタン押す(期限ない?,  押さないと確認済みにならない, 押すと確認済みになり、ログインできる)
        ログインformに遷移
        ログインボタン押す
        トップページに遷移
    (正しく入力されなかった場合)
        ユーザー登録できない
    (会員登録していて,ログインしている場合)
    トップページに遷移
    (会員登録していて、ログインしていない場合)
    会員登録formに遷移
ログインボタン押す
    (会員登録していない場合)
    ログインformに遷移
    (会員登録していて,ログインしている場合)
    トップページに遷移
    (会員登録していて、ログインしていない場合)
    ログインformに遷移
    ユーザー名(必須)、パスワード(必須)入力
    (正しく入力された場合)
        トップページに遷移
    (正しく入力されなかった場合)
        トップページに遷移できない
        
'''