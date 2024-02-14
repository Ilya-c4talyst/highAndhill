from django.db import models


class Banner(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='banners/')

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self) -> str:
        return self.name
    


class Brand(models.Model):
    name = models.CharField(max_length = 150, verbose_name = 'Название бренда')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self) -> str:
        return self.name


class Size(models.Model):
    size = models.PositiveIntegerField(default=0, verbose_name='Размер')

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self) -> str:
        return f'{self.size}'


class Product(models.Model):
    name = models.CharField(max_length = 150, verbose_name = 'Название')
    price = models.PositiveIntegerField(default=0, verbose_name = 'Цена')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='Бренд', blank=True)
    images = models.ImageField(upload_to='products/', blank=True)
    sizes = models.ManyToManyField(
        Size,
        through='ProductSizeLink',
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return self.name


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
