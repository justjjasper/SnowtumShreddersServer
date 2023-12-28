# models.py is responsible for creating Table Schemas
from django.db import models

# Create your models here.
class Snowboard(models.Model):
    snowboard_id = models.AutoField(primary_key=True)
    snowboard_name = models.CharField(max_length=255)
    header_image = models.CharField(max_length=255)
    header_description = models.TextField()
    snowboard_price = models.DecimalField(max_digits=10, decimal_places=2)
    shape = models.CharField(max_length=255)
    sidecut = models.CharField(max_length=255)
    flex = models.CharField(max_length=255)
    rider_type = models.CharField(max_length=255)
    tech_story = models.TextField()
    camber_type = models.CharField(max_length=255)
    camber_description = models.TextField()
    camber_image = models.CharField(max_length=255)
    video = models.CharField(max_length=255)

    class Meta:
      db_table = 'snowboards'

class SnowboardImage(models.Model):
    snowboard_image_id = models.AutoField(primary_key=True)
    snowboard = models.ForeignKey(Snowboard, on_delete=models.CASCADE)
    snowboard_image = models.CharField(max_length=255)

    class Meta:
      db_table = 'snowboard_images'

class SnowboardReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    snowboard = models.ForeignKey(Snowboard, on_delete=models.CASCADE)
    snowboard_review_title = models.CharField(max_length=255)
    snowboard_review_author = models.CharField(max_length=255)
    snowboard_review_email = models.CharField(max_length=255)
    snowboard_review_date = models.DateField()
    snowboard_review_body = models.TextField()
    snowboard_review_rating = models.IntegerField()

    class Meta:
      db_table = 'snowboard_reviews'

class SnowboardSKU(models.Model):
    snowboard_sku_id = models.AutoField(primary_key=True)
    snowboard = models.ForeignKey(Snowboard, on_delete=models.CASCADE)
    snowboard_size = models.CharField(max_length=255)
    snowboard_sku = models.IntegerField()

    class Meta:
      db_table = 'snowboard_skus'

class TShirt(models.Model):
    tshirt_id = models.AutoField(primary_key=True)
    tshirt_name = models.CharField(max_length=255)
    tshirt_price = models.DecimalField(max_digits=10, decimal_places=2)
    tshirt_image = models.CharField(max_length=255)
    tshirt_description = models.TextField()

    class Meta:
      db_table = 'tshirts'

class TShirtSKU(models.Model):
    tshirt_sku_id = models.AutoField(primary_key=True)
    tshirt = models.ForeignKey(TShirt, on_delete=models.CASCADE)
    tshirt_size = models.CharField(max_length=255)
    tshirt_sku = models.IntegerField()

    class Meta:
      db_table = 'tshirt_skus'

class Hoodie(models.Model):
    hoodie_id = models.AutoField(primary_key=True)
    hoodie_name = models.CharField(max_length=255)
    hoodie_price = models.DecimalField(max_digits=10, decimal_places=2)
    hoodie_image = models.CharField(max_length=255)
    hoodie_description = models.TextField()

    class Meta:
      db_table = 'hoodies'

class HoodieSKU(models.Model):
    hoodie_sku_id = models.AutoField(primary_key=True)
    hoodie = models.ForeignKey(Hoodie, on_delete=models.CASCADE)
    hoodie_size = models.CharField(max_length=255)
    hoodie_sku = models.IntegerField()

    class Meta:
      db_table = 'hoodie_skus'

class Headgear(models.Model):
    headgear_id = models.AutoField(primary_key=True)
    headgear_name = models.CharField(max_length=255)
    headgear_image = models.CharField(max_length=255)
    headgear_price = models.DecimalField(max_digits=10, decimal_places=2)
    headgear_description = models.TextField()
    headgear_sku = models.IntegerField()

    class Meta:
      db_table = 'headgear'

class Boardbag(models.Model):
    boardbag_id = models.AutoField(primary_key=True)
    boardbag_name = models.CharField(max_length=255)
    boardbag_price = models.DecimalField(max_digits=10, decimal_places=2)
    boardbag_size = models.CharField(max_length=255)
    boardbag_description = models.TextField()
    boardbag_sku = models.IntegerField()

    class Meta:
      db_table = 'boardbag'

class BoardbagImage(models.Model):
    boardbag_image_id = models.AutoField(primary_key=True)
    boardbag = models.ForeignKey(Boardbag, on_delete=models.CASCADE)
    boardbag_image = models.CharField(max_length=255)

    class Meta:
      db_table = 'boardbag_images'
