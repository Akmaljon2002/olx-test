from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Parent Category"
    )
    lft = models.PositiveIntegerField(verbose_name="Left Value")
    rgt = models.PositiveIntegerField(verbose_name="Right Value")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        indexes = [
            models.Index(fields=['lft', 'rgt'])
        ]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['lft', 'rgt']

    def __str__(self):
        return self.name
