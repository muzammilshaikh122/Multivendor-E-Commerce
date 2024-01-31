from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify


# Create your models here.
class Slider(models.Model):
    DISCOUNT_DEAL = (
        ('HOT DEALS', 'HOT DEALS'),
        ('New Arraivels', 'New Arraivels'),
    )

    Image = models.ImageField(upload_to='media/Slider_imgs')
    Discount_Deal = models.CharField(choices=DISCOUNT_DEAL, max_length=100)
    SALE = models.IntegerField()
    Brand = models.CharField(max_length=200)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200)

    def __str__(self):
        return self.Brand

class banner_area(models.Model):
    image = models.ImageField(upload_to='banner_img')
    Discount_Deal = models.CharField(max_length=100)
    Quote = models.CharField(max_length=100)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.Quote



class Main_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    main_category = models.ForeignKey(Main_Category,models.CASCADE)
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name + " -- " + self.main_category.name

class Sub_Category(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.category.main_category.name + "__" + self.category.name + "__" + self.name



class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.code

class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# def pre_save_post_receiver(sender, insance, *args, **kwargs):
#     if not insance.slug:
#         insance.slug = create_slug(insance)
#
# pre_save.connect(pre_save_post_receiver, product)
#
# class Coupon_Code(models.Model):
#     code = models.CharField(max_length=100)
#     discount = models.IntegerField()
#
#     def __str__(self):
#         return self.code


class Product(models.Model):
    objects = None
    total_quantity = models.IntegerField()
    Availability = models.IntegerField()
    featured_image = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    Brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    price = models.IntegerField()
    Discount = models.IntegerField()
    tax = models.IntegerField(null=True)
    packing_cost = models.IntegerField(null=True)
    product_information = RichTextField()
    model_Name = models.CharField(max_length=100)
    Categories = models.ForeignKey(Category,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,null=True)
    Tags = models.CharField(max_length=100)
    Description = RichTextField()
    section = models.ForeignKey(Section,on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"


def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, Product)

class Coupon_Code(models.Model):
    code = models.CharField(max_length=100)
    discount = models.IntegerField()
    def __str__(self):
        return self.code

class Product_Image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Image_url = models.CharField(max_length=200)



class Additional_Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)