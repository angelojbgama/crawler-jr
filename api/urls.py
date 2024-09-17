from django.urls import path
from .views import NotebooksAPIView

urlpatterns = [
    path('lenovo-notebooks/', NotebooksAPIView.as_view(), name='lenovo-notebooks'),
]
