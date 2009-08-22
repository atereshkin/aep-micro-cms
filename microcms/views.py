# -*- coding: utf-8 -*-
from google.appengine.ext import db

from django.http import HttpResponse
from ragendja.template import render_to_response
from ragendja.dbutils import get_object_or_404
from .models import Page

def show_page(request, path):
    slug = path.split('/')[-1] 
    #TODO: need to use full path to identify the page
    page = get_object_or_404(Page, "slug =",  slug)
    if request.method == "POST":
        setattr(page, request.POST['id'], db.Text(request.POST['value']))
        page.put()
        return HttpResponse(request.POST['value'])
    return render_to_response(request,
                              page.template.name,
                              {'page' : page })



                                  
