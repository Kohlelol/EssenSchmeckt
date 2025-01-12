from django.db import models
from django.contrib.auth.models import User
import uuid
import qrcode
from datetime import datetime

# Create your models here.

class person(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='person', null=True, blank=True, default=None)
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True, default=None)
    group_id = models.ForeignKey('group', on_delete=models.SET_NULL, related_name='persons', null=True, blank=True, default=None)

    class Meta:
        verbose_name = "person"
        verbose_name_plural = "People"

    def __str__(self):
        return f"{self.last_name}, {self.first_name} | {self.date_of_birth} | {self.group_id.group_name} ------ {self.id}"
    
    def generate_uuids(self):
        new_uuid = uuid.uuid4()
        if new_uuid in person.objects.values_list('id', flat=True):
            self.generate_uuids()
        return new_uuid  
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_uuids()
        super(person, self).save(*args, **kwargs)


    def regenerate_UUID(self):
        self.id = self.generate_uuids()
        self.save()
        self.generate_QR()
        return self.id
    
    def generate_QR(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(self.id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        return img

    def get_food_for_today(self):
        current_date = datetime.now().date()
        return food.objects.filter(person=self, date=current_date).first()


class food(models.Model):
    person = models.ForeignKey(person, on_delete=models.SET_NULL, related_name='food', null=True)
    food = models.IntegerField(null=True, blank=True, default=1)
    date = models.DateField()
    locked = models.BooleanField(default=False)
    served = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('person', 'date')
        verbose_name = "Food order"
        verbose_name_plural = "Food orders"
    
    def __str__(self):
        return f"{self.date} | {self.person.last_name}, {self.person.first_name} -- {self.food} Served:{self.served}"
    

class group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=30)
    task = models.CharField(max_length=100)
    facility_id = models.ForeignKey('facility', on_delete=models.SET_NULL, related_name='groups', null=True)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return f"{self.group_id} {self.group_name} {self.task} {self.facility_id}"



class groupleader(models.Model):
    group = models.ForeignKey(group, on_delete=models.SET_NULL, related_name='group_leader', null=True)
    person = models.ForeignKey(person, on_delete=models.SET_NULL, related_name='group_leaderships', null=True)
    expires = models.DateField(null=True, blank=True, default=None)
    
    class Meta:
        unique_together = ('group_id', 'person_id')
        verbose_name = "Group leader"
        verbose_name_plural = "Group leaders"
    
    def __str__(self):
        return f"{self.group} - {self.person}, {self.person}"


class facility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=30)
    facility_location = models.CharField(max_length=30)
    
    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

    def __str__(self):
        return f"{self.facility_name}"


class facility_manager(models.Model):
    facility = models.ForeignKey(facility, on_delete=models.SET_NULL, related_name='facility_manager', null=True)
    person = models.ForeignKey(person, on_delete=models.SET_NULL, related_name='facility_managements', null=True)
    
    class Meta:
        unique_together = ('facility_id', 'person_id')
        verbose_name = "Facility manager"
        verbose_name_plural = "Facility managers"
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.person.last_name}, {self.person.first_name}"
        

class PDFDocument(models.Model):
    file = models.FileField(upload_to='menu/')
    expire_date = models.DateField()
    from_date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    