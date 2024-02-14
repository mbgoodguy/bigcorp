from django.core.management import BaseCommand
from faker import Faker

from shop.models import Product, Category

fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fake = Faker()

        # create 20 products
        for _ in range(20):
            product_title = fake.company()
            product_brand = fake.company()
            product_description = fake.paragraph(nb_sentences=2)
            product_price = fake.pydecimal(
                left_digits=3, right_digits=2, min_value=1, max_value=999.99
            )
            slug = f"{product_title.lower().replace(' ', '_').replace(',', '')}_product"
            product = Product(
                category=Category.objects.first(),
                title=product_title,
                brand=product_brand,
                description=product_description,
                slug=slug,
                price=product_price,
                available=True,
                created_at=fake.date_time(),
                updated_at=fake.date_time(),
                discount=fake.pyint(min_value=0, max_value=20),
            )
            product.save()

        self.stdout.write(f'Products in DB: {Product.objects.count()}')
