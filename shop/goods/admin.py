from django.contrib import admin

from .models import Product, Brand, ProductSizeLink, Size


class SizeInline(admin.TabularInline):
    model = ProductSizeLink
    extra = 1
    min_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'brand', 'images', 'price', 'display_sizes',)
    # list_editable = ('name', 'description', 'brand', 'images', 'price',),
    empty_value_display = '-пусто-'
    inlines = [
        SizeInline,
    ]
    @admin.display(description='Размеры')
    def display_sizes(self, obj):
        sizes_list = ', '.join(
            [
                size.size.name
                for size in obj.sizes.all()
                if size.size.name
            ]
        )
        return sizes_list



@admin.register(Brand)
class BrandRegister(admin.ModelAdmin):
    pass
    # list_display = ('__all__',)
    # list_editable = ('__all__',)


@admin.register(Size)
class SizeRegister(admin.ModelAdmin):
    pass
    # list_display = ('__all__',)
    # list_editable = ('__all__',)


@admin.register(ProductSizeLink)
class ProductSizeLinkRegister(admin.ModelAdmin):
    pass
    # list_display = ('__all__',)
    # list_editable = ('__all__',)