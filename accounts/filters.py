import django_filters
from .models import *

class OrderFilter(django_filters.filterSet):
    class Meta:
        model : Order
        fields = '__all__'
