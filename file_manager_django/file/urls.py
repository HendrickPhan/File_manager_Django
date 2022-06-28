from django.urls import path

from file.views import PostFileView, GetFileView, GetAppFilesView, DeleteFileView

urlpatterns = [
    path('', PostFileView.as_view()),
    path('app-files', GetAppFilesView.as_view()),
    path('del-files', DeleteFileView.as_view()),
    path('<str:file_type>/<str:folder_name>/<str:extension>', GetFileView.as_view()),
]