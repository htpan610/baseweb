from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=255,verbose_name="分类")
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=255,verbose_name="商品名称")
    price=models.DecimalField(max_digits=10,decimal_places=2,verbose_name="商品价格")
    category=models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="商品分类")
    stock=models.IntegerField(default=0,verbose_name="商品库存")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name="商品"
        verbose_name_plural="商品列表"

