# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
	
	return render(request, 'index.html')


def url_test(request, number, test):
	return HttpResponse(
		f'number: {number}\n'
		f'test: {test}'
		
	)


def test(request, number):
	
	print(type(number))
	print('=======')
	return HttpResponse(f'<h1> 逆子！逆子！ 不孝子！！！ </h1>')


def bad_request(request, exception, template_name='400.html'):
	return render(request, template_name)


def permission_denied(request, exception, template_name='403.html'):
	return render(request, template_name)


def page_not_found(request, exception, template_name='404.html'):
	return render(request, template_name)


def server_error(request, template_name='500.html'):
	return render(request, template_name)