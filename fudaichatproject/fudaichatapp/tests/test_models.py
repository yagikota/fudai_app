from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):

    def test_is_empty(self):
        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), 0)

    def test_is_count_one(self):
        user = User.objects.create_user(
            username='test1',
            email='test1@edu.osakafu-u.ac.jp',
            password='psst1'
        )
        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), 1)

    def assertEqualUserModel(self, actual_user, username, email, password):
        self.assertEqual(actual_user.username, username)
        self.assertEqual(actual_user.email, email)
        self.assertTrue(actual_user.check_password(password))

    def test_saving_and_retrieving_user(self):
        username, email, password = 'test1', 'test1@edu.osakafu-u.ac.jp', 'psst1'
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        saved_users = User.objects.all()
        actual_user = saved_users[0]
        self.assertEqualUserModel(actual_user, username, email, password)



'''
ユーザー1がサイトのトップページに訪問 ok
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