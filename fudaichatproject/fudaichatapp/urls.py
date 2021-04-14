from django.urls import path
from .views import TopPage, CommentListview, CommentCreateView, CreateUser, UserCreateDone, UserCreateComplete, ProfileView, DeleteUserComfirmView, DeleteUserCompleteView
from django.contrib.auth import views as auth_views

app_name  = 'fudaichat'

urlpatterns = [
    path('', TopPage.as_view(), name='top_page'),
    path('signup/', CreateUser.as_view(), name='signup'),
    path('signup/done', UserCreateDone.as_view(), name='signup_done'),
    path('signup/complete/<token>/', UserCreateComplete.as_view(), name='signup_complete'),
    # path('account/login/', CustomLoginView.as_view(), name='login'),
    path('list/', CommentListview.as_view(), name='list'),
    path('create/', CommentCreateView.as_view(), name='comment_create'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Built-inにより削除
    # path('password_change/', auth_views.PasswordChangeView.as_view, template_name='password_change.html', name='password_change'),
    # path('password_change/done/', PasswordChangeDone.as_view(), name='password_change_done'),

    # path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    # path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    # path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    # path('password_reset/complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),

    # Built-inにより削除
    # path('logout/', logoutview, name='logout'),

    path('delete_confirm', DeleteUserComfirmView.as_view(template_name='registration/delete_confirm.html'), name='delete_confirm'),
    path('delete_complete', DeleteUserCompleteView.as_view(), name='delete_complete'),
]
