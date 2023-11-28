from django.urls import path
from . import views

prefix = 'api/'
urlpatterns = [
    path(prefix + '', views.IncomeListAPIView.as_view(), name='income'),
    path(prefix + '<int:id>', views.IncomeDetailAPIView.as_view(), name='income'),
    path(prefix + 'income-category_data', views.IncomeSummaryStats.as_view(), name='income-category_data'),
]
