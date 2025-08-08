from django.urls import path
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView, \
    test_email_view

app_name = 'blog'

urlpatterns = [
    path('', BlogPostListView.as_view(), name='list'),
    path('create/', BlogPostCreateView.as_view(), name='create'),
    path('<int:pk>/', BlogPostDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', BlogPostUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='delete'),
    path('test-email/', test_email_view, name='test_email'),
]