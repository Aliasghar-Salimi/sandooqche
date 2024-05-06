from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from web.models import User, Expense, Income
from time import gmtime, strftime


# Create your views here.




@csrf_exempt
@cache_page(60 * 15)
def submit_expense(request):

    #TODO: validate data. user might be fake. token might be fake. amount might be...
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if 'date' not in request.POST:
        date = now
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token = this_token).get()
    Expense.objects.create(user=this_user, amount=request.POST['amount'], 
                           text=request.POST['text'], date=date)
    print(request.POST)

    return JsonResponse({'status' : 'ok'}, encoder=JSONEncoder)

@csrf_exempt
@cache_page(60 * 15)
def submit_income(request):
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    Income.objects.create(text=request.POST['text'], amount=request.POST['amount'], 
                           user=this_user, date=date)
    
    print(request.POST)
    return JsonResponse({'status':'working'}, encoder=JSONEncoder)