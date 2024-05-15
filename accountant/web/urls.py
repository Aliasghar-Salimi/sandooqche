from django.urls import path
from web import views

app_name = 'web'
urlpatterns = [
    path('submit/expense', views.submit_expense, name='submit_expense'),
    path('submit/income', views.submit_income, name='submit_income'),
    path('query/expenses/', views.query_expenses, name='query_expenses'),
    path('query/incomes/', views.query_incomes, name='query_incomes'),
    path('generalstat/', views.generalstat, name='generalstat'),
    
]