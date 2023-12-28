from django.http import JsonResponse
from django.db import DatabaseError, transaction
from django.conf import settings
from products.models import Snowboard, SnowboardSKU
import stripe
from rest_framework.decorators import api_view

@api_view(['POST'])
def stripe_payment(request):
    if request.method == 'POST':
        body = request.data
        print('stripe-payment what is body', body)

        try:
            stripe.api_key = settings.STRIPE_PRIVATE_KEY

            line_items = []

            with transaction.atomic():  # Use atomic transaction to ensure consistency
                for cart_item in body.get('cartItems', []):
                    # Query the database to get the product based on product information
                    product = Snowboard.objects.get(snowboard_id=cart_item['id'])
                    price = float(product.snowboard_price)

                    # Update the SKU in the database (adjust the logic based on your model structure)
                    product_sku = SnowboardSKU.objects.get(snowboard_id=cart_item['id'], snowboard_size=cart_item['size'])

                    # Check if subtracting the quantity will result in a negative value
                    if product_sku.snowboard_sku - cart_item['quantity'] < 0:
                        raise ValueError('Insufficient stock')

                    product_sku.snowboard_sku -= cart_item['quantity']
                    product_sku.save()

                    line_items.append({
                        'price_data': {
                            'product_data': {
                                'name': cart_item['name']
                            },
                            'currency': 'usd',
                            'unit_amount': int(price * 100),  # Convert price to cents
                        },
                        'quantity': cart_item['quantity'],
                    })

                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    mode='payment',
                    line_items=line_items,
                    success_url='http://localhost:80/info/success',
                    cancel_url='http://localhost:80/info/cancel'
                )

            print('what is checkoutid stripe payment', session.id)
            return JsonResponse({'url': session.url}, status=201)
        except ValueError as ve:
            print(f'Error creating Stripe session: {str(ve)}')
            return JsonResponse({'message': 'Insufficient stock'}, status=400)
        except Exception as e:
            print(f'Error creating Stripe session: {str(e)}')
            return JsonResponse({'message': 'Stripe Payment failed from backend'}, status=500)
