from django.db import models

class Country(models.Model):
    name=models.CharField(max_length=25,unique=True)
    description=models.TextField()
    population=models.IntegerField()
    gdp=models.FloatField()

    def __str__(self):
        return "country is " +'' + str(self.name)

class State(models.Model):
    country=models.ForeignKey(Country,related_name='states',on_delete=models.CASCADE)
    name=models.CharField(max_length=20,unique=True)
    description = models.TextField()
    population = models.IntegerField()
    gdp = models.FloatField()

    def __str__(self):
        return "state is " +' ' + str(self.name)

class City(models.Model):
    state=models.ForeignKey(State,on_delete=models.CASCADE,related_name="city_data")
    country=models.ForeignKey(Country,on_delete=models.CASCADE)
    description = models.TextField()
    population = models.IntegerField()
    gdp = models.FloatField()
    pincode=models.CharField(max_length=10,blank=True)

    def __str__(self):
        return  str(self.state)+' '+str(self.country)

class Town(models.Model):
    state = models.ForeignKey(State,related_name='town_data', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField()
    population = models.IntegerField()
    gdp = models.FloatField()
    pincode = models.CharField(max_length=10,blank=True)

    def __str__(self):
        return str(self.state) + ' ' + str(self.country)

class Person(models.Model):
    name=models.CharField(max_length=20)
    town=models.OneToOneField(Town,on_delete=models.CASCADE,related_name='person_data')

    def __str__(self):
        return "person is "+ ' ' + str(self.name)



