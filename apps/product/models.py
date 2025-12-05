from django.db import models
from django.utils.text import gettext_lazy as _, slugify
from mptt.models import MPTTModel, TreeForeignKey
from apps.core_app.models import ActiveMixin, CreateMixin, UpdateMixin, Image



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


class ProductCategory(MPTTModel, CreateMixin, UpdateMixin, ActiveMixin):
    title = models.CharField(max_length=256)
    # slug = models.SlugField(allow_unicode=True, max_length=256, blank=True)
    category_image = models.ForeignKey(
        Image,
        related_name="category_images",
        on_delete=models.PROTECT,
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
        verbose_name=_("زیر دسته بندی")
    )

    # def save(self,**kwargs) : 
    #     self.slug = slugify(self.title,allow_unicode=True)
    #     return super().save(**kwargs)

    class Meta:
        db_table = "product_category"


class Product(CreateMixin, UpdateMixin, ActiveMixin):
    category = models.ForeignKey(
        to=ProductCategory,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("دسته بندی")
    )
    title = models.CharField(_("عنوان محصول"), max_length=256)
    slug = models.SlugField(_("اسلاگ"), allow_unicode=True, max_length=256)
    # technical_code = models.CharField(max_length=256,null=True,blank=True)
    commercial_code = models.CharField(max_length=256,null=True,blank=True)
    # main_image = models.CharField(max_length=256)
    # country = models.ForeignKey(
    #     to=Country,
    #     on_delete=models.PROTECT,
    #     related_name="products"
    # )
    price = models.PositiveIntegerField(_("قیمت"))
    discount_percent = models.IntegerField(_("قیمت تخفیف"), default=0)
    brand = models.ForeignKey(
        to=Brand,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="product_brands",
        verbose_name=_("برند")
    )
    short_description = models.TextField(_("توضیح کوتاه محصول"), null=True,blank=True)
    # time_added = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(_("محصول در دسترس هست"), default=True)
    similar_products = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="related_to",
        verbose_name=_("محصولات مشابه")
    )
    stock = models.PositiveIntegerField(_("موجودی"), default=1)
    meta_title = models.CharField(_("متا تایتل"), max_length=70, null=True, blank=True)
    meta_description = models.CharField(_("متا دیسکریپشن"), max_length=320, null=True, blank=True)

    class Meta:
        ordering = ("id",)
        db_table = "product"

    def final_price(self):
        if self.discount_percent:
            price = self.price - self.discount_percent
            return max(price, 0)
        return self.price


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
