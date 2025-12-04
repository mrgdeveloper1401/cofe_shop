from django.db import models
import uuid
from django.utils.text import slugify
from django.core.validators import MinValueValidator,MaxValueValidator

from apps.core_app.models import ActiveMixin, CreateMixin, UpdateMixin



class Country(ActiveMixin, UpdateMixin, CreateMixin):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(allow_unicode=True, null=True, blank=True)
    flag = models.ImageField(upload_to="product/country/",null=True,blank=True)

    class Meta:
        db_table = "country"


    def get_most_brands(self,count=5):
        return Country.objects.annotate(
            country_brands=models.Count("brand")
        ).order_by("-country_brands")[:count]


    def save(self,**kwarges) : 
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(**kwarges)


class Brand(models.Model):
    is_own = models.BooleanField(default=False, help_text="is brand is for this company ?")
    country = models.ForeignKey(
        to=Country,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    logo = models.ImageField(upload_to="product/brand/")
    name = models.CharField(max_length=256)
    slug = models.SlugField(allow_unicode=True, max_length=256)
    
    def save(self,**kwargs) : 
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(**kwargs)
    
    class Meta:
        db_table = "brand"


class ProductCategory(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(allow_unicode=True, max_length=256)
    image = models.ImageField(upload_to="media/product/product-category/")

    def save(self,**kwargs) : 
        self.slug = slugify(self.title,allow_unicode=True)
        return super().save(**kwargs)

    class Meta:
        db_table = "product_category"


class Product(models.Model):
    category = models.ForeignKey(
        to=ProductCategory,
        on_delete=models.PROTECT,
        related_name="products",
    )
    title = models.CharField(max_length=256)
    slug = models.SlugField(allow_unicode=True, max_length=256)
    technical_code = models.CharField(max_length=256,null=True,blank=True)
    commercial_code = models.CharField(max_length=256,null=True,blank=True)
    main_image = models.CharField(max_length=256)
    country = models.ForeignKey(
        to=Country,
        on_delete=models.PROTECT,
        related_name="products"
    )
    price = models.PositiveIntegerField()
    discount_percent = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    brand = models.ForeignKey(
        to=Brand,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products"
    )
    short_description = models.TextField(null=True,blank=True)
    time_added = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    similar_products = models.ManyToManyField(
        "self",
        symmetrical=True,
    )
    
    def save(self,**kwargs) : 
        self.slug = slugify(self.title,allow_unicode=True)
        return super().save(**kwargs)
    
    class Meta:
        db_table = "product"


class ProductImage(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.PROTECT,
        related_name="images"
    )
    image = models.CharField(max_length=256)

    class Meta:
        db_table = "product_image"


class ProductFeature(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.PROTECT,
        related_name="product_features",
    )
    key = models.CharField(max_length=128)
    value = models.CharField(max_length=512)

    class Meta:
        db_table = "product_feature"
