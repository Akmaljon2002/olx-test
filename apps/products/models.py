from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Product Title")
    description = models.TextField(verbose_name="Product Description", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Product Price")
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Product Category"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
