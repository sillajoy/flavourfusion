from django.db import models

# Admin table
class AdminModel(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_username = models.CharField(max_length=50)
    admin_password = models.CharField(max_length=50)
     
    class Meta():
        db_table = 'admin_table'

# admin add ads
class AdsModel(models.Model):
    ads_id = models.AutoField(primary_key=True)
    ads_name = models.CharField(max_length=50)
    ads_product_description = models.CharField(max_length=150)
    ads_image = models.ImageField(upload_to='images/ads_img/')
    ads_link = models.URLField(max_length=200)
    ads_start_date = models.DateField()
    ads_end_date = models.DateField()
    ads_create_at = models.DateTimeField(auto_now_add=True)
    admin_id = models.ForeignKey(AdminModel,  on_delete=models.CASCADE)

    class Meta():
        db_table = 'ads_table'