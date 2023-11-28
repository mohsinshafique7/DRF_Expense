import datetime
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Expenses
from .permissions import IsOwner
from .serializers import ExpenseSerializer


# Create your views here.
class ExpenseListAPIView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expenses.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        print('Userssssssssss', self.request.user)
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expenses.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseSummaryStats(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0
        for expense in expenses:
            amount += expense.amount
        return {'amount': str(amount)}

    def get_categories(self, expense):
        return expense.category

    def get(self, request):
        today_date = datetime.date.today()
        a_year_ago = today_date - datetime.timedelta(days=30 * 12)
        expenses = Expenses.objects.filter(owner=request.user, date__gte=a_year_ago, date__lte=today_date)
        final = {}
        categories = list(set(map(self.get_categories, expenses)))
        for expense in expenses:
            for category in categories:
                final[category] = self.get_amount_for_category(expense, category)
        return Response({'category_data': final}, status=status.HTTP_200_OK)
