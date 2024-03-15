from django.contrib import admin
from django.urls import path
from app.views import MarkdownView, PlainView, GPTView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/view/md/', MarkdownView.as_view(), name='content'),
    path('api/view/md/gpt/', GPTView.as_view(), name='content'),
    path('api/view/plain/', PlainView.as_view(), name='content'),
]
