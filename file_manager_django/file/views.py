from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound
from file.services.post_file_services import PostFileServices
from file.services.get_file_services import GetFileServices
from file.services.get_app_file_services import GetAppFileServices
from file.services.delete_file_services import DeleteFileServices
from json_response import json_response_failure, json_response_success
from django.urls import Resolver404, reverse, resolve
from django.db.models.query import EmptyQuerySet

class PostFileView(View):
    def post(self, request):
        
        files = request.FILES
        data = {
            'file': files['file'] if 'file' in files else None,
            'app_id': request.POST.get('app_id'),
            'upload_time': request.POST.get('upload_time'),
            'secure_code': request.POST.get('secure_code'),
            'domain': request.get_host(),
            'hidden': request.POST.get('hidden', False),
            'protocol': request.scheme
        }

        service = PostFileServices(data)
        if(service.is_valid()):
            file_name = service.save_file()
            service.update_app_data()
            file_record = service.create_record()
            return json_response_success(file_name)
        else:
            return json_response_failure(service.error)

class GetFileView(View):
    def get(self, request, file_type, folder_name, extension):
        size = request.GET.get('size', 'default') 
        service = GetFileServices(file_type, folder_name, extension, size)
        path = service.get_file()

        if(service.is_valid()):
            response = redirect(path)
            return response
        else:
            return json_response_failure(service.error)

        return json_response_failure('Invalid')

class GetAppFilesView(View):
    def get(self, request):
        app_id = request.GET.get('app_id')
        #Default page = 1
        page = request.GET.get('page', '1')
        limit = request.GET.get('limit', '10')
        keyword = request.GET.get('keyword', '')
        order = request.GET.get('order_by')
        domain = request.get_host()
        protocol = request.scheme
        service = GetAppFileServices(domain, protocol, app_id, page, limit, keyword, order)
        
        if(not service.is_valid()):
            return json_response_failure('Invalid Syntax')
        else:
            files = service.get_files()
            return json_response_success(files)

class DeleteFileView(View):
    def delete(self, request):
        app_id = request.GET.get('app_id', '')
        id = request.GET.get('id', '')
        service = DeleteFileServices(app_id, id)
        if(service.is_valid()):
            return json_response_success(service.deleteModels())
        else:
            return json_response_failure(service.error)
