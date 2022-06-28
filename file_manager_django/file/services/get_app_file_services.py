from app.models import App
from django.conf import settings
from django.core.files.storage import default_storage
from file.models import File
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

class GetAppFileServices:
    
    def __init__(self, domain, protocol, app_id, page, limit, keyword, order):
        self.domain = domain
        self.protocol = protocol
        self.app_id = app_id
        self.page = page
        self.limit = limit
        self.keyword = keyword
        self.order = order

    def get_files(self):
        query = File.objects.filter(app_id = self.app_id, hidden=False)
        if self.keyword is not None:
            query = query.filter(path__contains = self.keyword)
        if self.order is not None:
            query = query.order_by(self.order)  
        pagesPagination = Paginator(query, int(self.limit))
        files = list(pagesPagination.page(self.page).object_list.values()) 
        for file in files:
            file["path"] = "%s://%s/file/%s"%(
                self.protocol,
                self.domain,
                file["path"])

        return_data = {
            "total": pagesPagination.count,
            "total_page": pagesPagination.num_pages, 
            "data": files
        }
        return return_data
    
    def is_valid(self):
        if (self.limit.isdigit()) and (self.page.isdigit()) and (self.app_id.isdigit()):
            return True
        return False