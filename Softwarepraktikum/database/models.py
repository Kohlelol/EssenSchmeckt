from django.db import models

# Create your models here.

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    qr_code = models.CharField(max_length=30)
    group_id = models.ForeignKey('group', on_delete=models.CASCADE, related_name='persons', null=True, blank=True, default=None)
    facility_id = models.ForeignKey('facility', on_delete=models.CASCADE, related_name='persons', null=True, blank=True, default=None)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    
class status(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='status')
    status = models.CharField(max_length=10)
    date = models.DateField()
    
    class Meta:
        unique_together = ('person', 'date')
    
    def __str__(self):
        return f"{self.person.id} {self.status} - {self.date}"


class food(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='food')
    food = models.IntegerField()
    date = models.DateField()
    
    class Meta:
        unique_together = ('person', 'date')
    
    def __str__(self):
        return f"{self.person.id} {self.food} - {self.date}"
    

class group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=30)
    task = models.CharField(max_length=100)
    facility_id = models.ForeignKey('facility', on_delete=models.CASCADE, related_name='groups')


class groupleader(models.Model):
    group = models.ForeignKey(group, on_delete=models.CASCADE, related_name='group_leader')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='group_leaderships')
    
    class Meta:
        unique_together = ('group_id', 'person_id')
    
    def __str__(self):
        return f"{self.group_id} {self.person_id}"


class facility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=30)
    facility_location = models.CharField(max_length=30)
    
    def __str__(self):
        return self.facility_name


class facility_manager(models.Model):
    facility = models.ForeignKey(facility, on_delete=models.CASCADE, related_name='facility_manager')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='facility_managements')
    
    class Meta:
        unique_together = ('facility_id', 'person_id')
    
    def __str__(self):
        return f"{self.facility_id} {self.person_id}"
        