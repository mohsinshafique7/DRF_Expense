from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExpenseListAPIView.as_view(), name='expenses'),
    path('<int:id>', views.ExpenseDetailAPIView.as_view(), name='expenses'),
    path('expense-category_data', views.ExpenseSummaryStats.as_view(), name='expenses'),
]
