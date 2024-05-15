from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from web.models import User, Expense, Income
from time import gmtime, strftime

from django.views.decorators.http import require_POST

from web.models import Expense, Income
from django.core import serializers

from django.db.models import Count, Sum

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

# return General Status of a user as Json (income,expense)

@csrf_exempt
@require_POST
def query_expenses(request):
    this_token = request.POST['token']
    num = request.POST.get('num', 10)
    this_user = get_object_or_404(User, token__token=this_token)
    expenses = Expense.objects.filter(user=this_user).order_by('-date')[:num]
    expenses_serialized = serializers.serialize("json", expenses)

    return JsonResponse(expenses_serialized, encoder=JSONEncoder, safe=False)

@csrf_exempt
@require_POST
def query_incomes(request):
    this_token = request.POST['token']
    num = request.POST.get('num', 10)
    this_user = get_object_or_404(User, token__token=this_token)
    expenses = Income.objects.filter(user=this_user).order_by('-date')[:num]
    expenses_serialized = serializers.serialize("json", expenses)

    return JsonResponse(expenses_serialized, encoder=JSONEncoder, safe=False)


@csrf_exempt
@require_POST
def generalstat(request):
    # TODO: should get a valid duration (from - to), if not, use 1 month
    # TODO: is the token valid?
    this_token = request.POST['token']
    this_user = get_object_or_404(User, token__token=this_token)
    income = Income.objects.filter(user=this_user).aggregate(
        Count('amount'), Sum('amount'))
    expense = Expense.objects.filter(user=this_user).aggregate(
        Count('amount'), Sum('amount'))
    context = {}
    context['expense'] = expense
    context['income'] = income

    return JsonResponse(context, encoder=JSONEncoder)

