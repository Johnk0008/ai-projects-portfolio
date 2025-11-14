from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        # Create categories
        electronics, _ = Category.objects.get_or_create(name='Electronics')
        clothing, _ = Category.objects.get_or_create(name='Clothing')
        books, _ = Category.objects.get_or_create(name='Books')
        home, _ = Category.objects.get_or_create(name='Home & Garden')
        
        # Create sample products
        sample_products = [
            {
                'name': 'Smartphone',
                'description': 'Latest smartphone with great features, 128GB storage, 5G capable',
                'price': 699.99,
                'category': electronics,
                'stock': 50
            },
            {
                'name': 'Laptop',
                'description': 'High-performance laptop for work and gaming, 16GB RAM, 512GB SSD',
                'price': 1299.99,
                'category': electronics,
                'stock': 25
            },
            {
                'name': 'Wireless Headphones',
                'description': 'Noise-cancelling wireless headphones with 30hr battery life',
                'price': 199.99,
                'category': electronics,
                'stock': 75
            },
            {
                'name': 'Cotton T-Shirt',
                'description': 'Comfortable 100% cotton t-shirt, available in multiple colors',
                'price': 19.99,
                'category': clothing,
                'stock': 100
            },
            {
                'name': 'Jeans',
                'description': 'Classic fit jeans, durable denim material',
                'price': 49.99,
                'category': clothing,
                'stock': 60
            },
            {
                'name': 'Python Programming Book',
                'description': 'Learn Python programming from scratch with practical examples',
                'price': 39.99,
                'category': books,
                'stock': 30
            },
            {
                'name': 'Coffee Maker',
                'description': 'Automatic drip coffee maker with programmable timer',
                'price': 79.99,
                'category': home,
                'stock': 40
            },
            {
                'name': 'Desk Lamp',
                'description': 'LED desk lamp with adjustable brightness and color temperature',
                'price': 29.99,
                'category': home,
                'stock': 80
            }
        ]
        
        for product_data in sample_products:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f"Created product: {product.name}")
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))