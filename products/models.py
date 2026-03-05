from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from shared.models import BaseModel


class ProductCategory(BaseModel):
    icon = models.CharField(
        max_length=255,
        verbose_name=_("Icon"),
        help_text=_("CSS icon class, e.g. 'fa fa-couch'")
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        null=True,
        blank=True,
        verbose_name=_("Parent category")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active")
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_category"
        verbose_name = _("Product category")
        verbose_name_plural = _("Product categories")


class ProductTag(BaseModel):
    name = models.CharField(
        max_length=128,
        verbose_name=_("Name")
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_tag"
        verbose_name = _("Product tag")
        verbose_name_plural = _("Product tags")


class ProductColor(BaseModel):
    name = models.CharField(
        max_length=64,
        verbose_name=_("Name"),
        help_text=_("e.g. Walnut Brown, Oak Natural")
    )
    hex_code = models.CharField(
        max_length=7,
        verbose_name=_("HEX code"),
        help_text=_("e.g. #8B4513")
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_color"
        verbose_name = _("Product color")
        verbose_name_plural = _("Product colors")


class Manufacture(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    logo = models.ImageField(
        upload_to="manufacturers/",
        null=True,
        blank=True,
        verbose_name=_("Logo")
    )
    country = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_("Country"),
        help_text=_("Country of origin")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    website = models.URLField(
        blank=True,
        verbose_name=_("Website")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active")
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "manufacture"
        verbose_name = _("Manufacture")
        verbose_name_plural = _("Manufactures")


class ProductStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", _("Available")
    OUT_OF_STOCK = "OUT_OF_STOCK", _("Out of stock")
    DISCONTINUED = "DISCONTINUED", _("Discontinued")
    COMING_SOON = "COMING_SOON", _("Coming soon")


class Product(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    sku = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_("SKU"),
        help_text=_("Stock Keeping Unit — unique product code")
    )
    description = models.TextField(
        verbose_name=_("Description")
    )
    short_description = models.CharField(
        max_length=512,
        blank=True,
        verbose_name=_("Short description")
    )
    image = models.ImageField(
        upload_to="product_images/",
        verbose_name=_("Main image")
    )

    price_uzs = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Price (UZS)"),
        help_text=_("Price in Uzbek sum")
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Price (USD)"),
        help_text=_("Price in US dollar")
    )
    price_rub = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Price (RUB)"),
        help_text=_("Price in Russian ruble")
    )

    discount_price_uzs = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name=_("Discount price (UZS)")
    )
    discount_price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name=_("Discount price (USD)")
    )
    discount_price_rub = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name=_("Discount price (RUB)")
    )

    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.AVAILABLE,
        verbose_name=_("Status")
    )

    manufacture = models.ForeignKey(
        Manufacture,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name=_("Manufacture")
    )
    categories = models.ManyToManyField(
        ProductCategory,
        related_name='products',
        verbose_name=_("Categories")
    )
    tags = models.ManyToManyField(
        ProductTag,
        related_name='products',
        blank=True,
        verbose_name=_("Tags")
    )
    colors = models.ManyToManyField(
        ProductColor,
        through='ProductColorQuantity',
        related_name='products',
        blank=True,
        verbose_name=_("Colors")
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Is featured")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active")
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
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['-created_at']


class ProductColorQuantity(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='color_quantities',
        verbose_name=_("Product")
    )
    color = models.ForeignKey(
        ProductColor,
        on_delete=models.CASCADE,
        related_name='product_quantities',
        verbose_name=_("Color")
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantity"),
        help_text=_("Stock quantity for this color")
    )

    def __str__(self):
        return f"{self.product.name} — {self.color.name}: {self.quantity}"

    class Meta:
        db_table = "product_color_quantity"
        verbose_name = _("Product color quantity")
        verbose_name_plural = _("Product color quantities")
        unique_together = ('product', 'color')


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Product")
    )
    image = models.ImageField(
        upload_to="product_images/",
        verbose_name=_("Image")
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Is primary"),
        help_text=_("Mark as primary gallery image")
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Alt text")
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Order")
    )

    def __str__(self):
        return f"Image {self.order} for {self.product.name}"

    class Meta:
        db_table = "product_image"
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")
        ordering = ['order']