from django.urls import path
from .views import TopPage, logoutview, CommentListview, CommentCreateView, CreateUser, CustomLoginView, UserCreateDone, UserCreateComplete, ProfileView, PasswordChange, PasswordChangeDone, PasswordReset, PasswordResetDone, PasswordResetConfirm, PasswordResetComplete
app_name  = 'fudaichat'

urlpatterns = [
    path('', TopPage.as_view(), name='top_page'),
    path('signup/', CreateUser.as_view(), name='signup'),
    path('signup/done', UserCreateDone.as_view(), name='signup_done'),
    path('signup/complete/<token>/', UserCreateComplete.as_view(), name='signup_complete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('list/', CommentListview.as_view(), name='list'),
    path('create/', CommentCreateView.as_view(), name='comment_create'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('logout/', logoutview, name='logout'),
]
