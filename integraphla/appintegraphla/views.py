from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello, world. \n You\'re at the appintegraphla index.')