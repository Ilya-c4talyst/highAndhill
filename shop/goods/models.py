from django.db import models


"""Модель категории"""
class Type(models.Model):
    name = models.CharField(max_length=150, verbose_name="Тип")

    class Meta:
        verbose_name = 'Тип (категория)'
        verbose_name_plural = 'Типы (категории)'

    def __str__(self) -> str:
        return self.name


"""Модель баннера"""
class Banner(models.Model):
    name = models.CharField(max_length=150)
    url = models.URLField(max_length=200)
    image = models.ImageField(upload_to='banners/')
    category = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name='Категория', related_name='banners')

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self) -> str:
        return self.name    


"""Модель бренда"""
class Brand(models.Model):
    name = models.CharField(max_length = 150, verbose_name = 'Название бренда')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self) -> str:
        return self.name


"""Модель размера"""
class Size(models.Model):
    size = models.CharField(max_length=150, verbose_name='Размер')

    class Meta:
        verbose_name = 'Размер обуви'
        verbose_name_plural = 'Размеры обуви'

    def __str__(self) -> str:
        return f'{self.size}'


"""Модель изображения для пары"""
class Image(models.Model):
    img = models.ImageField(upload_to='products/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


"""Модель для обуви"""
class Product(models.Model):
    name = models.CharField(max_length = 150, verbose_name = 'Название')
    price = models.PositiveIntegerField(default=0, verbose_name = 'Цена')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='Бренд', blank=True)
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип", blank=True)
    most_liked = models.BooleanField(default=False)
    on_sale = models.BooleanField(default=False)
    images = models.ImageField(upload_to='products/')
    show_images = models.ManyToManyField(
        Image,
        through='ImageProductLink'
    )
    sizes = models.ManyToManyField(
        Size,
        through='ProductSizeLink',
    )

    class Meta:
        verbose_name = 'Обувь'
        verbose_name_plural = 'Обувь'

    def __str__(self) -> str:
        return self.name


"""Связь изображений и кроссовок"""
class ImageProductLink(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='positions_p')
    img = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='images_p')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['product', 'img'], name='unique_product_img'
        )]
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return (
            f'{self.product}: {self.img}'
        )


"""Связь размера и кроссовок"""
class ProductSizeLink(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='sizes')


    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['product', 'size'], name='unique_product_size'
        )]
        verbose_name = 'Предложенные размеры'
        verbose_name_plural = 'Предложенные размеры'

    def __str__(self):
        return (
            f'{self.product}: {self.size}'
        )


"""Связь одежды и размера"""
class ClothSize(models.Model):
    size = models.CharField(max_length=150, verbose_name='Размер')

    class Meta:
        verbose_name = 'Размер одежды'
        verbose_name_plural = 'Размеры одежды'

    def __str__(self) -> str:
        return f'{self.size}'


"""Модель одежды"""
class Cloth(models.Model):
    name = models.CharField(max_length = 150, verbose_name = 'Название')
    price = models.PositiveIntegerField(default=0, verbose_name = 'Цена')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='Бренд', blank=True)
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип", blank=True)
    images = models.ImageField(upload_to='products/', blank=True)
    on_sale = models.BooleanField(default=False)
    show_images = models.ManyToManyField(
        Image,
        through='ImageClothLink'
    )
    sizes = models.ManyToManyField(
        ClothSize,
        through='ClothSizeLink',
    )

    class Meta:
        verbose_name = 'Одежда'
        verbose_name_plural = 'Одежда'

    def __str__(self) -> str:
        return self.name


"""Связь одежды и размера"""
class ClothSizeLink(models.Model):
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE, related_name='clothes')
    size = models.ForeignKey(ClothSize, on_delete=models.CASCADE, related_name='cloth_sizes')


    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['cloth', 'size'], name='unique_cloth_size'
        )]
        verbose_name = 'Предложенные размеры'
        verbose_name_plural = 'Предложенные размеры'

    def __str__(self):
        return (
            f'{self.cloth}: {self.size}'
        )


"""Связь изображений и кроссовок"""
class ImageClothLink(models.Model):
    product = models.ForeignKey(Cloth, on_delete=models.CASCADE, related_name='positions_c')
    img = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='images_c')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['product', 'img'], name='unique_cloth_img'
        )]
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return (
            f'{self.product}: {self.img}'
        )


class Order(models.Model):
    code = models.CharField(max_length=200)
    cart = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        return self.code