from django.core.validators import MinValueValidator
from django.db import models

from shared.models import BaseModel


class ProductCategory(BaseModel):
    icon = models.CharField(
        max_length=255,
        verbose_name="Icon",
        help_text="CSS icon class, e.g. 'fa fa-couch'"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Name"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        null=True,
        blank=True,
        verbose_name="Parent category"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is active"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_category"
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class ProductTag(BaseModel):
    name = models.CharField(
        max_length=128,
        verbose_name="Name"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_tag"
        verbose_name = "Product Tag"
        verbose_name_plural = "Product Tags"


class ProductColor(BaseModel):
    name = models.CharField(
        max_length=64,
        verbose_name="Name",
        help_text="e.g. Walnut Brown, Oak Natural"
    )
    hex_code = models.CharField(
        max_length=7,
        verbose_name="HEX Code",
        help_text="e.g. #8B4513"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_color"
        verbose_name = "Product Color"
        verbose_name_plural = "Product Colors"


class Manufacture(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name="Name"
    )
    logo = models.ImageField(
        upload_to="manufacturers/",
        null=True,
        blank=True,
        verbose_name="Logo"
    )
    country = models.CharField(
        max_length=128,
        verbose_name="Country",
        null=True, blank=True,
        help_text="Country of origin"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    website = models.URLField(
        blank=True,
        verbose_name="Website"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is active"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "manufacture"
        verbose_name = "Manufacture"
        verbose_name_plural = "Manufactures"


class ProductStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    OUT_OF_STOCK = "OUT_OF_STOCK", "Out of Stock"
    DISCONTINUED = "DISCONTINUED", "Discontinued"
    COMING_SOON = "COMING_SOON", "Coming Soon"


class Product(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name="Name"
    )
    sku = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="SKU",
        help_text="Stock Keeping Unit — unique product code"
    )
    description = models.TextField(
        verbose_name="Description"
    )
    short_description = models.CharField(
        max_length=512,
        blank=True,
        verbose_name="Short description"
    )
    image = models.ImageField(
        upload_to="product_images/",
        verbose_name="Main Image"
    )

    price_uzs = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Price (UZS)",
        help_text="Price in Uzbek Sum"
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Price (USD)",
        help_text="Price in US Dollar"
    )
    price_rub = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Price (RUB)",
        help_text="Price in Russian Ruble"
    )

    discount_price_uzs = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name="Discount Price (UZS)"
    )
    discount_price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name="Discount Price (USD)"
    )
    discount_price_rub = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name="Discount Price (RUB)"
    )

    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.AVAILABLE,
        verbose_name="Status"
    )

    manufacture = models.ForeignKey(
        Manufacture,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Manufacture"
    )
    categories = models.ManyToManyField(
        ProductCategory,
        related_name='products',
        verbose_name="Categories"
    )
    tags = models.ManyToManyField(
        ProductTag,
        related_name='products',
        blank=True,
        verbose_name="Tags"
    )
    colors = models.ManyToManyField(
        ProductColor,
        through='ProductColorQuantity',
        related_name='products',
        blank=True,
        verbose_name="Colors"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Is featured"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is active"
    )

    def __str__(self):
        return self.name

    @property
    def has_discount(self):
        return any([self.discount_price_uzs, self.discount_price_usd, self.discount_price_rub])

    @property
    def total_stock(self):
        return self.color_quantities.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

    class Meta:
        db_table = "product"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']


class ProductColorQuantity(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='color_quantities',
        verbose_name="Product"
    )
    color = models.ForeignKey(
        ProductColor,
        on_delete=models.CASCADE,
        related_name='product_quantities',
        verbose_name="Color"
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantity",
        help_text="Stock quantity for this color"
    )

    def __str__(self):
        return f"{self.product.name} — {self.color.name}: {self.quantity}"

    class Meta:
        db_table = "product_color_quantity"
        verbose_name = "Product Color Quantity"
        verbose_name_plural = "Product Color Quantities"
        unique_together = ('product', 'color')


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Product"
    )
    image = models.ImageField(
        upload_to="product_images/",
        verbose_name="Image"
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name="Is primary",
        help_text="Mark as primary gallery image"
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Alt text"
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Order"
    )

    def __str__(self):
        return f"Image {self.order} for {self.product.name}"

    class Meta:
        db_table = "product_image"
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['order']