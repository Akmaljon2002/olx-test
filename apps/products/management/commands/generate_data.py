from django.core.management.base import BaseCommand
from apps.categories.models import Category
from apps.products.models import Product
from faker import Faker
import random
from tqdm import tqdm
from django.db.models import Max
from collections import deque
import time
import sys

fake = Faker()
sys.setrecursionlimit(10000)


class Command(BaseCommand):
    help = 'Generate N categories and M products (efficient version)'

    def handle(self, *args, **kwargs):
        categories_to_add = 1_000_000
        products_to_add = 5_000_000
        branch_factor = 12
        max_depth = 7

        start_id = (Category.objects.aggregate(max_id=Max('id'))['max_id'] or 0) + 1
        node_id = start_id

        self.stdout.write(self.style.WARNING(f"🚀 Generating {categories_to_add:,} categories from ID {start_id}"))

        start_time = time.time()

        categories = []
        queue = deque([(None, 1)])

        while node_id < start_id + categories_to_add and queue:
            parent, depth = queue.popleft()
            if depth > max_depth:
                continue

            category = Category(
                id=node_id,
                name=fake.word(),
                parent=parent,
                lft=0,
                rgt=0
            )
            categories.append(category)
            node_id += 1

            for _ in range(branch_factor):
                if node_id >= start_id + categories_to_add:
                    break
                queue.append((category, depth + 1))

        self.stdout.write(self.style.SUCCESS(f"✅ Tree structure ready with {len(categories):,} categories."))

        self.stdout.write("🧠 Assigning nested set values...")

        id_to_cat = {cat.id: cat for cat in categories}
        children_map = {}
        for cat in categories:
            parent_id = cat.parent.id if cat.parent else None
            children_map.setdefault(parent_id, []).append(cat)

        lft_counter = [1]

        def dfs_iterative(root):
            stack = [(root, 0)]
            visited = set()
            while stack:
                node, child_idx = stack[-1]
                if node.id in visited:
                    node.rgt = lft_counter[0]
                    lft_counter[0] += 1
                    stack.pop()
                    continue

                node.lft = lft_counter[0]
                lft_counter[0] += 1
                visited.add(node.id)
                children = children_map.get(node.id, [])
                if children:
                    for child in reversed(children):
                        stack.append((child, 0))
                else:
                    node.rgt = lft_counter[0]
                    lft_counter[0] += 1
                    stack.pop()

        for root_cat in children_map.get(None, []):
            dfs_iterative(root_cat)

        self.stdout.write(self.style.SUCCESS("✅ Nested set assigned."))

        self.stdout.write(self.style.WARNING("💾 Saving categories to DB..."))
        Category.objects.bulk_create(categories, batch_size=10_000)

        leaf_categories = [cat for cat in categories if cat.rgt == cat.lft + 1]
        self.stdout.write(self.style.SUCCESS(f"🌿 Leaf categories: {len(leaf_categories):,}"))

        self.stdout.write(self.style.WARNING(f"📦 Generating {products_to_add:,} products..."))
        products = []

        for _ in tqdm(range(products_to_add)):
            products.append(Product(
                title=fake.sentence(nb_words=4),
                description=fake.text(max_nb_chars=50),
                price=round(random.uniform(10, 10_000), 2),
                category=random.choice(leaf_categories)
            ))

            if len(products) >= 10_000:
                Product.objects.bulk_create(products, batch_size=10_000)
                products.clear()

        if products:
            Product.objects.bulk_create(products, batch_size=10_000)

        total_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f"✅ All done in {total_time:.2f} seconds!"))
