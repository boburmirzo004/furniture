from django.shortcuts import render

from products.models import ProductColor, ProductTag, ProductCategory, ProductImage, Product, ProductStatus


def checkout_page_view(request):
    return render(request, 'products/checkout.html')


def cart_page_view(request):
    return render(request, 'products/cart.html')


def product_detail_page_view(request):
    return render(request, 'products/product-detail.html')


def product_list_page_view(request):
    context = {
        'product_colors':ProductColor.objects.all(),
        'product_tags':ProductTag.objects.all(),
        'product_categories':ProductCategory.objects.all(),
        'product_images':ProductImage.objects.all(),
        'products':Product.objects.filter(status=ProductStatus.AVAILABLE)
    }
    return render(request, 'products/products-list.html',context=context)


def wishlist_page_view(request):
    return render(request, 'products/wishlist.html')
