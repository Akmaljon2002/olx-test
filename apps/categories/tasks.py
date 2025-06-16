from celery import shared_task
from apps.categories.models import Category
from apps.categories.utils import add_category_fast
from utils.exceptions import send_me


@shared_task
def create_category_task(name: str, parent_id: int = None) -> int:
    parent = Category.objects.get(id=parent_id) if parent_id else None
    category = add_category_fast(name, parent)
    send_me(
        f"Category created: {category.name} (ID: {category.id})\nCategory Creation Notification",
    )
    return category.id
