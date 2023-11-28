import datetime
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Income
from .permissions import IsOwner
from .serializers import IncomeSerializer


# Create your views here.
class IncomeListAPIView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class IncomeDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class IncomeSummaryStats(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_amount_for_source(self, income_list, source):
        income = income_list.filter(source=source)
        amount = 0
        for i in income:
            amount += i.amount
        return {'amount': str(amount)}

    def get_sources(self, income_list):
        return income_list.source

    def get(self, request):
        today_date = datetime.date.today()
        a_year_ago = today_date - datetime.timedelta(days=30 * 12)
        income = Income.objects.filter(owner=request.user, date__gte=a_year_ago, date__lte=today_date)
        final = {}
        sources = list(set(map(self.get_sources, income)))
        for i in income:
            for source in sources:
                final[source] = self.get_amount_for_source(i, source)
        return Response({'income_data': final}, status=status.HTTP_200_OK)
