from django.db import connection
from django.db import transaction, models
from apps.categories.models import Category

def add_category(name, parent=None):

    with transaction.atomic():
        if parent:
            Category.objects.filter(lft__gt=parent.rgt - 1).update(lft=models.F('lft') + 2)
            Category.objects.filter(rgt__gte=parent.rgt).update(rgt=models.F('rgt') + 2)
            category = Category.objects.create(
                name=name,
                parent=parent,
                lft=parent.rgt,
                rgt=parent.rgt + 1
            )
        else:
            max_rgt = Category.objects.aggregate(models.Max('rgt'))['rgt__max'] or 0
            category = Category.objects.create(
                name=name,
                parent=None,
                lft=max_rgt + 1,
                rgt=max_rgt + 2
            )
        return category


def add_category_fast(name: str, parent: Category = None) -> Category:
    with transaction.atomic():
        with connection.cursor() as cursor:
            if parent:
                cursor.execute("SELECT rgt FROM categories_category WHERE id = %s FOR UPDATE", [parent.id])
                row = cursor.fetchone()
                if not row:
                    raise ValueError("Parent category does not exist.")
                parent_rgt = row[0]

                cursor.execute("UPDATE categories_category SET lft = lft + 2 WHERE lft > %s", [parent_rgt - 1])
                cursor.execute("UPDATE categories_category SET rgt = rgt + 2 WHERE rgt >= %s", [parent_rgt])

                cursor.execute("""
                    INSERT INTO categories_category (name, parent_id, lft, rgt, created_at)
                    VALUES (%s, %s, %s, %s, NOW())
                    RETURNING id
                """, [name, parent.id, parent_rgt, parent_rgt + 1])
            else:
                cursor.execute("SELECT COALESCE(MAX(rgt), 0) FROM categories_category")
                max_rgt = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO categories_category (name, parent_id, lft, rgt, created_at)
                    VALUES (%s, NULL, %s, %s, NOW())
                    RETURNING id
                """, [name, max_rgt + 1, max_rgt + 2])

            new_id = cursor.fetchone()[0]
            return Category.objects.get(id=new_id)


"""DO $$
DECLARE
    v_parent_id INTEGER := 1;
    parent_rgt INTEGER;
    new_name TEXT := 'Child kategoriya';
BEGIN
    SELECT rgt INTO parent_rgt FROM categories_category WHERE id = v_parent_id;

    UPDATE categories_category SET lft = lft + 2 WHERE lft > parent_rgt - 1;
    UPDATE categories_category SET rgt = rgt + 2 WHERE rgt >= parent_rgt;

    INSERT INTO categories_category (name, parent_id, lft, rgt, created_at)
    VALUES ('test', v_parent_id, parent_rgt, parent_rgt + 1, now());
END$$;
DO
"""