from django.urls import path
from .views import Home, CreateUserView, LoginView, VerifyUserView, Post, PostDetails, CommentListCreate, CommentDetails

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
    path('posts/', Post.as_view(), name='post-it'),
    path('post/<int:id>/', PostDetails.as_view(), name='post-detail'),
    path('interest/<int:interest_id>/comment/', CommentListCreate.as_view(), name='comment-list'),
    path('interest/<int:interest_id>/comment/<int:comment_id>/', CommentDetails.as_view(), name='comment-details'),
]