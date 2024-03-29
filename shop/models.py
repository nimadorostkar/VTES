from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.template.defaultfilters import truncatechars
from django_jalali.db import models as jmodels
from authentication.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.html import format_html
from colorfield.fields import ColorField









#------------------------------------------------------------------------------
class Province(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="نام")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان ها"


#------------------------------------------------------------------------------
class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name = "استان")
    name = models.CharField(max_length=256, unique=True, verbose_name="نام")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهر ها"













#------------------------------------------------------------------------------
class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name = "نام")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name = "والد")

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return str(self.name)

    def child(self):
        return self.get_children()






#------------------------------------------------------------------------------
class Brand(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name='برند')
    fname = models.CharField(max_length=256, unique=True, null=True, blank=True, verbose_name='برند (فارسی)')
    link = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(default='logos/default.png', upload_to='brands', null=True, blank=True , verbose_name = "لوگو ")

    def __str__(self):
        return str(self.name)

    def logo_tag(self):
        return format_html("<img width=40 src='{}'>".format(self.image.url))

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"








#------------------------------------------------------------------------------
class Unit(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="واحد اندازه گیری")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "واحد اندازه گیری"
        verbose_name_plural = "واحد اندازه گیری"







#------------------------------------------------------------------------------
class Attributes(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name='ویژگی')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی ها"







#------------------------------------------------------------------------------
class Shop(models.Model):
    slug = models.SlugField(max_length=256, null=True, blank=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile', verbose_name = "کاربر")
    name = models.CharField(max_length=70, verbose_name = "نام فروشگاه")
    logo = models.ImageField(default='logos/default.png', upload_to='logos', null=True, blank=True , verbose_name = "لوگو فروشگاه")
    cover = models.ImageField(default='covers/default.png', upload_to='covers', null=True, blank=True , verbose_name = "کاور فروشگاه")
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name = "شماره تماس")
    email = models.EmailField(max_length=50, null=True, blank=True, verbose_name = "ایمیل")
    description = models.TextField(max_length=1000,null=True, blank=True, verbose_name = "توضیحات")
    category = models.ManyToManyField(Category, related_name='shop_category', verbose_name = "دسته بند")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True, verbose_name = "استان")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name = "شهر")
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name = "آدرس")
    postal_code = models.CharField(max_length=200, null=True, blank=True, verbose_name = "کد پستی")
    lat_long = models.CharField(max_length=200, null=True, blank=True, verbose_name = "lat & long")
    shaba_number = models.CharField(max_length=120, null=True, blank=True, verbose_name = "شماره شبا")
    card_number = models.CharField(max_length=120, null=True, blank=True, verbose_name = "شماره کارت")
    bank_account_number = models.CharField(max_length=120, null=True, blank=True, verbose_name = "شماره حساب")
    instagram = models.CharField(max_length=120, null=True, blank=True)
    linkedin = models.CharField(max_length=120, null=True, blank=True)
    whatsapp = models.CharField(max_length=120, null=True, blank=True)
    telegram = models.CharField(max_length=120, null=True, blank=True)
    economic_code = models.CharField(max_length=120, null=True, blank=True, verbose_name = "کد اقتصادی")
    national_ID = models.CharField(max_length=120, null=True, blank=True, verbose_name = "شناسه ملی")
    registration_number = models.CharField(max_length=120, null=True, blank=True, verbose_name = "شماره ثبت")
    central_office_province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True, related_name='central_office_province', verbose_name = "استان دفتر مرکزی")
    central_office_city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, related_name='central_office_city', verbose_name = "شهر دفتر مرکزی")
    landline_phone_number = models.CharField(max_length=50, null=True, blank=True, verbose_name = "شماره تماس ثابت")
    invoicing = models.BooleanField(default=False, verbose_name = "امکان صدور فاکتور رسمی")
    date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ ایجاد")

    def __str__(self):
        return str(self.name)

    def logo_tag(self):
        return format_html("<img width=40 src='{}'>".format(self.logo.url))

    def user_mobile(self):
        return str(self.user.mobile)

    def city_name(self):
        return str(self.city.name)

    def province_name(self):
        return str(self.province.name)

    def owner_name(self):
        return str(self.user.first_name) +' '+ str(self.user.last_name)

    @property
    def short_description(self):
        return truncatechars(self.description, 50)

    def get_absolute_url(self):
        return reverse('shops_detail',args=[self.id])

    class Meta:
        verbose_name = "فروشگاه"
        verbose_name_plural = "فروشگاه ها"








#------------------------------------------------------------------------------
class Product(models.Model):
    approved = models.BooleanField(default=False, verbose_name = "تایید شده")
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name = "کد محصول")
    irancode = models.CharField(max_length=50, null=True, blank=True, verbose_name = "ایران کد")
    name = models.CharField(max_length=80, verbose_name = "نام محصول")
    banner = models.ImageField(default='products/default.png', upload_to='products', verbose_name = "تصویر")
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.CASCADE, related_name='product_brand', verbose_name = "برند")
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name = "لینک محصول")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, related_name='product_category', verbose_name = "دسته بند")
    description = models.TextField(max_length=1000,null=True, blank=True, verbose_name = "توضیحات")
    datasheet = models.FileField(upload_to='datasheet', null=True, blank=True, verbose_name = "فایل و Datasheet")
    date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ ایجاد")
    #CHOICES = ( ('متر','متر'), ('لیتر','لیتر'), ('کیلوگرم','کیلوگرم'), ('عدد','عدد') )
    #unit = models.CharField(max_length=256, choices=CHOICES, null=True, blank=True, verbose_name = "واحد اندازه گیری")

    def __str__(self):
        return str(self.name)

    def category_name(self):
        return str(self.category.name)

    def brand_name(self):
        return str(self.brand.name)

    def img_tag(self):
        return format_html("<img width=40 src='{}'>".format(self.banner.url))

    def get_absolute_url(self):
        return reverse('product_detail',args=[self.id])

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


#------------------------------------------------------------------------------
class ProductImgs(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productImg',  verbose_name = "محصول")
    img = models.ImageField(upload_to='products', verbose_name = "تصویر")

    def __str__(self):
        return str(self.product.name)

    def product_name(self):
        return str(self.product.name)


    class Meta:
        verbose_name = "تصاویر محصول"
        verbose_name_plural = "تصاویر محصولات"








#------------------------------------------------------------------------------
class ShopProducts(models.Model):
    available = models.BooleanField(default=True, verbose_name = "موجود")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='Shop',  verbose_name = "فروشگاه")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product',  verbose_name = "محصول")
    internal_code = models.CharField(max_length=50, null=True, blank=True, verbose_name = "کد داخلی محصول")
    qty = models.IntegerField(default=0, verbose_name = "تعداد")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, verbose_name = "واحد اندازه گیری")
    CHOICES = ( ('1','1'), ('2','2'), ('3','3') )
    price_model = models.CharField(max_length=254, choices=CHOICES, null=True, blank=True, verbose_name = "مدل قیمتی")
    one_price = models.IntegerField(default=0, verbose_name = "قیمت تکی")
    medium_volume_price = models.IntegerField(default=0, verbose_name = "قیمت حجم متوسط")
    medium_volume_qty = models.IntegerField(default=0, verbose_name = "حداقل تعداد حجم متوسط")
    wholesale_volume_price = models.IntegerField(default=0, verbose_name = "قیمت حجم عمده")
    wholesale_volume_qty = models.IntegerField(default=0, verbose_name = "حداقل تعداد حجم عمده")

    def __str__(self):
        return str(self.shop.name)

    def product_code(self):
        return str(self.product.code)

    def unit_name(self):
        return str(self.unit.name)

    class Meta:
        verbose_name = "محصول فروشگاه"
        verbose_name_plural = "محصولات فروشگاه"












#------------------------------------------------------------------------------
class ProductAttr(models.Model):
    product = models.ForeignKey(ShopProducts, on_delete=models.CASCADE, related_name='product_attr',  verbose_name = "محصول فروشگاه")
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE, verbose_name='ویژگی')
    value = models.CharField(max_length=60, verbose_name='مقدار')

    def __str__(self):
        return str(self.attribute.name)

    def attribute_name(self):
        return str(self.attribute.name)

    def product_name(self):
        return str(self.product.product.name)

    class Meta:
        verbose_name = "ویژگی محصول"
        verbose_name_plural = "ویژگی محصولات"









#------------------------------------------------------------------------------
class ProductColor(models.Model):
    product = models.ForeignKey(ShopProducts, on_delete=models.CASCADE, related_name='product_color',  verbose_name = "محصول مربوطه")
    color = ColorField(default='#BFBFBF', verbose_name='رنگ')

    def __str__(self):
        return str(self.color)


    def product_name(self):
        return str(self.product.name)

    def plate(self):
        return format_html("<div style='height:20px; width:20px; background-color:{};'> </div>".format(self.color))

    class Meta:
        verbose_name = "رنگ محصول"
        verbose_name_plural = "رنگ محصولات"














#End
