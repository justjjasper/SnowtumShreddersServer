from django.http import JsonResponse
from .models import *
from django.db import DatabaseError #
from rest_framework.decorators import api_view
from datetime import datetime

def custom_title_case(text):
        # Split the text by spaces
        words = text.split(' ')

        # List of words to keep in uppercase
        uppercase_words = ['sb', 'mfg', 'mars1']  # Add other words as needed

        # Apply title case, but keep specific words in uppercase
        title_case_words = [word.title() if word not in uppercase_words else word.upper() for word in words]

        # Join the words back together with spaces
        return ' '.join(title_case_words)

def mega_snowboards(request):
    snowboards = Snowboard.objects.all()

    formatted_snowboards = []
    for snowboard in snowboards:
        snowboard_data = {
            'snowboard_id': snowboard.snowboard_id,
            'snowboard_name': snowboard.snowboard_name,
            'snowboard_price': float(snowboard.snowboard_price),  # Convert to float if needed
            'header_image': snowboard.header_image,
            'header_description': snowboard.header_description,
            'shape': snowboard.shape,
            'sidecut': snowboard.sidecut,
            'flex': snowboard.flex,
            'rider_type': snowboard.rider_type,
            'tech_story': snowboard.tech_story,
            'camber_type': snowboard.camber_type,
            'camber_description': snowboard.camber_description,
            'camber_image': snowboard.camber_image,
            'snowboard_images': [img.snowboard_image for img in SnowboardImage.objects.filter(snowboard=snowboard)],
            'snowboard_sku': float(SnowboardSKU.objects.filter(snowboard=snowboard).latest('snowboard_sku').snowboard_sku),  # Get the latest SKU and convert to float if needed
            'snowboard_reviews': [
                {
                    'snowboard_review_title': review.snowboard_review_title,
                    'snowboard_review_author': review.snowboard_review_author,
                    'snowboard_review_date': review.snowboard_review_date.strftime('%Y-%m-%d'),  # Format as YYYY-MM-DD
                    'snowboard_review_rating': review.snowboard_review_rating,
                    'snowboard_review_body': review.snowboard_review_body,
                }
                for review in SnowboardReview.objects.filter(snowboard=snowboard)
            ],
        }
        formatted_snowboards.append(snowboard_data)

    return JsonResponse(formatted_snowboards, safe=False)

def get_product_collections(request):
    snowboards = Snowboard.objects.all()
    product_data = []

    try:
        for snowboard in snowboards:
            # Get the first image for each snowboard
            snowboard_image = SnowboardImage.objects.filter(snowboard=snowboard).first()

            # Create an object with the desired format
            snowboard_obj = {
                'id': snowboard.snowboard_id,
                'name': snowboard.snowboard_name,
                'image': snowboard_image.snowboard_image if snowboard_image else '',  # Use the image URL or an empty string if no image found
                'description': snowboard.header_description,
                'category': 'snowboard'
            }

            product_data.append(snowboard_obj)

        # Create a list of the other products and format the data
        tshirts = list(TShirt.objects.values('tshirt_id', 'tshirt_name', 'tshirt_image', 'tshirt_description'))
        tshirt_data = [{'id': tshirt['tshirt_id'], 'name': tshirt['tshirt_name'], 'image': tshirt['tshirt_image'], 'description': tshirt['tshirt_description'], 'category': 'tshirt'} for tshirt in tshirts]

        hoodies = list(Hoodie.objects.values('hoodie_id', 'hoodie_name', 'hoodie_image', 'hoodie_description'))
        hoodie_data = [{'id': hoodie['hoodie_id'], 'name': hoodie['hoodie_name'], 'image': hoodie['hoodie_image'], 'description': hoodie['hoodie_description'], 'category': 'hoodie'} for hoodie in hoodies]

        headgear = list(Headgear.objects.values('headgear_id', 'headgear_name', 'headgear_image', 'headgear_description'))
        headgear_data = [{'id': item['headgear_id'], 'name': item['headgear_name'], 'image': item['headgear_image'], 'description': item['headgear_description'], 'category': 'headgear'} for item in headgear]

        # Retrieve the first image for each boardbag
        boardbag_data = []
        for boardbag in Boardbag.objects.all():
            boardbag_images = BoardbagImage.objects.filter(boardbag=boardbag)
        if boardbag_images.exists():
            first_image = boardbag_images.first().boardbag_image
        else:
            first_image = ""

        boardbag_data.append({
            'id': boardbag.boardbag_id,
            'name': boardbag.boardbag_name,
            'image': first_image,
            'price': boardbag.boardbag_price,
            'category': 'boardbag'
        })

        # Append individual product lists to the product_data list
        product_data.extend(tshirt_data)
        product_data.extend(hoodie_data)
        product_data.extend(headgear_data)
        product_data.extend(boardbag_data)

        return JsonResponse(product_data, safe=False)
    except DatabaseError as e:
      # Handle database-related errors
      return JsonResponse({'error': 'Error retrieving product collections from database'}, status=500)
    except Exception as e:
      # Handle other exceptions or errors
      return JsonResponse({'error': 'An error occurred'}, status=500)

def get_snowboard_collection(request):
  # Fetch all snowboards and their corresponding images
  snowboards = Snowboard.objects.all()
  snowboard_data = []

  try:
    for snowboard in snowboards:
        # Get the first image for each snowboard
        snowboard_image = SnowboardImage.objects.filter(snowboard=snowboard).first()

        # Fetch related snowboard sizes and SKUs
        snowboard_skus = SnowboardSKU.objects.filter(snowboard=snowboard)

         # Create an array of objects with snowboard Size and SKU
        snowboard_meta_data = [{'size': sku.snowboard_size, 'sku': sku.snowboard_sku} for sku in snowboard_skus]

        # Create an object with the desired format
        snowboard_obj = {
            'snowboard_id': snowboard.snowboard_id,
            'snowboard_name': snowboard.snowboard_name,
            'snowboard_price': float(snowboard.snowboard_price),  # Convert Decimal to float if needed
            'snowboard_image': snowboard_image.snowboard_image if snowboard_image else '',  # Use the image URL or an empty string if no image found
            'header_description': snowboard.header_description,
            'snowboard_meta_data': snowboard_meta_data
        }

        snowboard_data.append(snowboard_obj)

    # Return the formatted data as JSON response
    return JsonResponse(snowboard_data, safe=False)
  except DatabaseError as e:
      # Handle database-related errors
      return JsonResponse({'error': 'Database error occurred'}, status=500)

  except Exception as e:
      # Handle other exceptions or errors
      return JsonResponse({'error': 'An error occurred'}, status=500)

def get_accessory_collection(request):
  try:
    # Create a list of the other products and format the data
    tshirts = list(TShirt.objects.values('tshirt_id', 'tshirt_name', 'tshirt_price', 'tshirt_image', 'tshirt_description'))
    tshirt_data = [{'id': tshirt['tshirt_id'], 'name': tshirt['tshirt_name'], 'price': tshirt['tshirt_price'], 'image': tshirt['tshirt_image'], 'description': tshirt['tshirt_description'], 'category': 'tshirt'} for tshirt in tshirts]

     # Add the meta_data to tshirt_data
    for tshirt in tshirt_data:
        tshirt['meta_data'] = [{'size': sku['tshirt_size'], 'sku': sku['tshirt_sku']} for sku in TShirtSKU.objects.filter(tshirt_id=tshirt['id']).values('tshirt_size', 'tshirt_sku')]

    hoodies = list(Hoodie.objects.values('hoodie_id', 'hoodie_name', 'hoodie_price', 'hoodie_image', 'hoodie_description'))
    hoodie_data = [{'id': hoodie['hoodie_id'], 'name': hoodie['hoodie_name'], 'price': hoodie['hoodie_price'], 'image': hoodie['hoodie_image'], 'description': hoodie['hoodie_description'], 'category': 'hoodie'} for hoodie in hoodies]

    # Add the meta_data to hoodie_data
    for hoodie in hoodie_data:
        hoodie['meta_data'] = [{'size': sku['hoodie_size'], 'sku': sku['hoodie_sku']} for sku in HoodieSKU.objects.filter(hoodie_id=hoodie['id']).values('hoodie_size', 'hoodie_sku')]

    headgear = list(Headgear.objects.values('headgear_id', 'headgear_name', 'headgear_price', 'headgear_image', 'headgear_description', 'headgear_sku'))
    headgear_data = [{'id': item['headgear_id'], 'name': item['headgear_name'], 'price': item['headgear_price'], 'image': item['headgear_image'], 'description': item['headgear_description'], 'category': 'headgear', 'meta_data': [{'size': 'One Size', 'sku': item['headgear_sku']}]} for item in headgear]


    # Retrieve the first image for each boardbag
    boardbag_data = []
    for boardbag in Boardbag.objects.all():
        boardbag_images = BoardbagImage.objects.filter(boardbag=boardbag)
        if boardbag_images.exists():
            first_image = boardbag_images.first().boardbag_image
        else:
            first_image = ""

        boardbag_data.append({
            'id': boardbag.boardbag_id,
            'name': boardbag.boardbag_name,
            'image': first_image,
            'price': boardbag.boardbag_price,
            'category': 'boardbag',
            'meta_data': [{'size': boardbag.boardbag_size, 'sku': boardbag.boardbag_sku}]
        })

    accessories_data = {
        'tshirts': tshirt_data,
        'hoodies': hoodie_data,
        'headgear': headgear_data,
        'boardbag': boardbag_data,
    }

    response_data = accessories_data

    return JsonResponse(response_data, safe=False)
  except DatabaseError as e:
        # Handle database-related errors
        return JsonResponse({'error': 'Database error occurred'}, status=500)

  except Exception as e:
      # Handle other exceptions or errors
      return JsonResponse({'error': 'An error occurred'}, status=500)

def get_snowboard_product(request, snowboard_name):
    try:
        # # Retrieve the snowboard name from the request object
        # snowboard_name = request.GET.get('snowboard_name')

        # if not snowboard_name:
        #     # Handle the case where snowboard_name is not provided in the request
        #     return JsonResponse({'error': 'Snowboard name is required'}, status=400)

        # Convert the provided snowboard name to the format stored in the database
        formatted_snowboard_name = snowboard_name.replace('-', ' ').upper()

        # Query the database to retrieve the snowboard product data
        snowboard = Snowboard.objects.get(snowboard_name=formatted_snowboard_name)

        # Query related data (images, reviews, sizes, skus)
        snowboard_images = list(SnowboardImage.objects.filter(snowboard=snowboard).values_list('snowboard_image', flat=True))
        snowboard_reviews = SnowboardReview.objects.filter(snowboard=snowboard).values(
            'review_id',
            'snowboard_review_title',
            'snowboard_review_author',
            'snowboard_review_email',
            'snowboard_review_date',
            'snowboard_review_body',
            'snowboard_review_rating'
        )
        # Query and Create a list of objects of the "filterd" snowboard with property snowboard_size & snowboard_sku
        snowboard_meta_datas = list(SnowboardSKU.objects.filter(snowboard=snowboard).values('snowboard_size', 'snowboard_sku'))
        # Renames each iteration of the object to 'size' and 'sku' for the array within snowboard_meta_datas
        formatted_meta_data = [{'size':snowboard_meta_data['snowboard_size'], 'sku':snowboard_meta_data['snowboard_sku']} for snowboard_meta_data in snowboard_meta_datas]

        # Serialize the data into the desired format
        snowboard_data = {
            'id': snowboard.snowboard_id,
            'name': snowboard.snowboard_name,
            'image': snowboard.header_image,
            'header_description': snowboard.header_description,
            'price': str(snowboard.snowboard_price),  # Convert to string if needed
            'shape': snowboard.shape,
            'sidecut': snowboard.sidecut,
            'flex': snowboard.flex,
            'rider_type': snowboard.rider_type,
            'tech_story': snowboard.tech_story,
            'camber_type': snowboard.camber_type,
            'camber_description': snowboard.camber_description,
            'camber_image': snowboard.camber_image,
            'images': snowboard_images,
            'reviews': list(snowboard_reviews),
            'meta_data': formatted_meta_data,
            'video': snowboard.video
        }

        return JsonResponse(snowboard_data, safe=False)

    except Snowboard.DoesNotExist:
        # Handle the case where the snowboard with the provided name does not exist
        return JsonResponse({'error': 'Snowboard not found'}, status=404)

def get_tshirt_product(request, tshirt_name):
  try:
    # Format queried product name to db product name
    formatted_tshirt_name = custom_title_case(tshirt_name.replace('-', ' '))

    # Query from database to get product data
    tshirt = TShirt.objects.get(tshirt_name = formatted_tshirt_name)

    # Query and create list of filtered tshirt objects with property of 'tshirt_size' and 'tshirt_sku'
    tshirt_meta_datas = list(TShirtSKU.objects.filter(tshirt=tshirt).values('tshirt_size','tshirt_sku'))
    # Iterate through tshirt_meta_datas and rename each object to 'size' and 'sku'
    formatted_tshirt_meta_data = [{'size': tshirt_meta_data['tshirt_size'], 'sku': tshirt_meta_data['tshirt_sku']} for tshirt_meta_data in tshirt_meta_datas]

    # Format data into desired object
    tshirt_data = {
      'id': tshirt.tshirt_id,
      'name': tshirt.tshirt_name,
      'price': tshirt.tshirt_price,
      'description' : tshirt.tshirt_description,
      'images': [tshirt.tshirt_image],
      'meta_data': formatted_tshirt_meta_data
    }

    return JsonResponse(tshirt_data, safe=False)

  except TShirt.DoesNotExist:
    # Handle the case where the snowboard with the provided name does not exist
    return JsonResponse({'error': 'Tshirt not found'}, status=404)

def get_hoodie_product(request, hoodie_name):
    try:
        #Reformat provided hoodie name
        formatted_hoodie_name = custom_title_case(hoodie_name.replace('-', ' '))

        # Query the filtered hoodie
        hoodie = Hoodie.objects.get(hoodie_name = formatted_hoodie_name)

        # Create a list of the filtered hoodie with an object of 'hoodie_size' and 'hoodie_sku'
        hoodie_meta_datas = list(HoodieSKU.objects.filter(hoodie=hoodie).values('hoodie_size', 'hoodie_sku'))
        # Format the list of hoodie_meta_datas
        formatted_hoodie_meta_data = [{'size': hoodie_meta_data['hoodie_size'], 'sku': hoodie_meta_data['hoodie_sku']} for hoodie_meta_data in hoodie_meta_datas]

        hoodie_data = {
            'id': hoodie.hoodie_id,
            'name': hoodie.hoodie_name,
            'price': hoodie.hoodie_price,
            'description': hoodie.hoodie_description,
            'images': [hoodie.hoodie_image],
            'meta_data': formatted_hoodie_meta_data
        }

        return JsonResponse(hoodie_data)
    except Hoodie.DoesNotExist:
    # Handle the case where the snowboard with the provided name does not exist
        return JsonResponse({'error': 'Hoodie not found'}, status=404)

def get_headgear_product(request, headgear_name):
    try:
        formatted_headgear_name = custom_title_case(headgear_name.replace('-', ' '))

        headgear = Headgear.objects.get(headgear_name = formatted_headgear_name)

        headgear_meta_data = [{'size': 'One Size', 'sku': headgear.headgear_sku}]

        headgear_data = {
            'id': headgear.headgear_id,
            'name': headgear.headgear_name,
            'price': headgear.headgear_price,
            'description': headgear.headgear_description,
            'images': [headgear.headgear_image],
            'meta_data': headgear_meta_data
        }

        return JsonResponse(headgear_data, safe=False)
    except Headgear.DoesNotExist:
    # Handle the case where the snowboard with the provided name does not exist
        return JsonResponse({'error': 'Headgear not found'}, status=404)

def get_boardbag_product(request, boardbag_name):
    try:
        formatted_boardbag_name = custom_title_case(boardbag_name.replace('-', ' '))

        boardbag = Boardbag.objects.get(boardbag_name = formatted_boardbag_name)

        boardbag_images = list(BoardbagImage.objects.filter(boardbag=boardbag).values_list('boardbag_image', flat=True))

        boardbag_meta_data = [{'size': boardbag.boardbag_size, 'sku': boardbag.boardbag_sku}]
        boardbag_data = {
            'id': boardbag.boardbag_id,
            'name': boardbag.boardbag_name,
            'price': boardbag.boardbag_price,
            'description': boardbag.boardbag_description,
            'images': boardbag_images,
            'meta_data': boardbag_meta_data
        }

        return JsonResponse(boardbag_data, safe=False)
    except Boardbag.DoesNotExist:
    # Handle the case where the snowboard with the provided name does not exist
        return JsonResponse({'error': 'Boardbag not found'}, status=404)

@api_view(['POST'])
def post_review(request):
    if request.method == 'POST':
        body = request.data

        # Get snowboard_id
        snowboard_id = body.get('snowboard_id')

        # Change body['date'] to proper Model Format
        date_string = body['date']
        parsed_date = datetime.strptime(date_string, "%b %d, %Y").date()

        # Check if corresponding snowboard exist
        try:
            snowboard = Snowboard.objects.get(pk=snowboard_id)
        except Snowboard.DoesNotExist:
            return JsonResponse({'message': 'Snowboard not found while posting review'}, status=404)

        # Create new snowboard review instance
        new_review = SnowboardReview(
            snowboard=snowboard,
            snowboard_review_title=body['title'],
            snowboard_review_author=body['author'],
            snowboard_review_email=body['email'],
            snowboard_review_date=parsed_date,
            snowboard_review_body=body['body'],
            snowboard_review_rating=body['rating']
        )

         # Save new SnowboardReview Instance to database
        try:
            new_review.save()
            print('Review saved successfully')
        except Exception as e:
            print(f'Error saving review: {e}')

        return JsonResponse({ 'data': body}, status=201)