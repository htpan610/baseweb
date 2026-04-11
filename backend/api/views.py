from rest_framework.views import APIView
from .models import Category
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


class ProductFilterSchemaView(APIView):
    def get(self,request):
        return Response({
            "table_key":"product",
            "filters":[
                {"field":"name","lookup":"icontains","label":"商品名称","type":"text","placeholder":"请输入商品名称"},
                {"field":"price","lookup":"range","label":"商品价格","type":"range","placeholder":"请输入商品价格范围"},
                {"field":"category","lookup":"exact","label":"商品分类","type":"select","placeholder":"请选择商品分类","options":[{"label": c.name, "value": c.id} for c in Category.objects.all()]},
            ],
            "columns":[
                {"field":"name","title":"商品名称","width":"200px","sortable":True},
                {"field":"price","title":"商品价格","width":"100px","sortable":True},
                {"field":"category","title":"商品分类","width":"100px","sortable":True},
                {"field":"stock","title":"商品库存","width":"100px","sortable":True},
                {"field":"created_at","title":"创建时间","width":"200px","sortable":True},
            ]
        })

class ProductListView(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_fields={
        "name": ["icontains"],
        "price": ["gte", "lte", "exact"],
        "category": ["exact"],
    }
    ordering=["-created_at"]