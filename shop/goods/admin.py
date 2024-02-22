from django.contrib import admin

from .models import (
    Product, Brand, ProductSizeLink,
    Size, Banner, Type, ClothSize, Cloth,
    ClothSizeLink, ImageClothLink,
    ImageProductLink, Image
)


class SizeInline(admin.TabularInline):
    model = ProductSizeLink
    extra = 1
    min_num = 1


class ClothSizeInline(admin.TabularInline):
    model = ClothSizeLink
    extra = 1
    min_num = 1


class ShoesImagesInLine(admin.TabularInline):
    model = ImageProductLink
    extra = 1
    min_num = 1


class ClothesImagesInLine(admin.TabularInline):
    model = ImageClothLink
    extra = 1
    min_num = 1


@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'type', 'description', 'brand', 'images', 'price', 'display_sizes', 'display_images')
    empty_value_display = '-пусто-'
    inlines = [
        ClothSizeInline,
        ClothesImagesInLine,
    ]

    @admin.display(description='Фото')
    def display_images(self, obj):
        images_list = ', '.join(
            [
                str(img.img)
                for img in obj.show_images.all()
                if str(img.img)
            ]
        )
        return images_list

    @admin.display(description='Размеры')
    def display_sizes(self, obj):
        sizes_list = ', '.join(
            [
                str(size.size)
                for size in obj.sizes.all()
                if str(size.size)
            ]
        )
        return sizes_list


@admin.register(ClothSize)
class ClothSizeRegister(admin.ModelAdmin):
    pass
    # list_display = ('__all__',)
    # list_editable = ('__all__',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'type', 'description', 'brand', 'images', 'price', 'display_sizes', 'display_images')
    # list_editable = ('name', 'description', 'brand', 'images', 'price',),
    empty_value_display = '-пусто-'
    inlines = [
        SizeInline,
        ShoesImagesInLine,
    ]
    @admin.display(description='Фото')
    def display_images(self, obj):
        images_list = ', '.join(
            [
                str(img.img)
                for img in obj.show_images.all()
                if str(img.img)
            ]
        )
        return images_list

    @admin.display(description='Размеры')
    def display_sizes(self, obj):
        sizes_list = ', '.join(
            [
                str(size.size)
                for size in obj.sizes.all()
                if str(size.size)
            ]
        )
        return sizes_list


@admin.register(Type)
class TypeRegister(admin.ModelAdmin):
    pass


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


# @admin.register(ProductSizeLink)
# class ProductSizeLinkRegister(admin.ModelAdmin):
#     pass
#     # list_display = ('__all__',)
#     # list_editable = ('__all__',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


# @admin.register(ImageClothLink)
# class ImageClothAdmin(admin.ModelAdmin):
#     pass


# @admin.register(ImageProductLink)
# class ImageShoeAdmin(admin.ModelAdmin):
#     pass