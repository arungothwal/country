# from rest_framework.fields import SerializerMethodField
from .models import *
from rest_framework import serializers

class Country_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Country

        fields='__all__'

class State_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model=State
        fields='__all__'

class City_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model=City
        fields='__all__'

class Town_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = '__all__'

class Person_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


""" nested serializer"""

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model=City
        fields=['id','description','population','gdp','pincode']


class StateSerializer(serializers.ModelSerializer):
    city_data=CitySerializer(many=True)

    class Meta:
        model=State
        fields=['id','name','description','population','gdp','city_data']

class CountrySerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True)

    class Meta:
        model=Country
        fields=['id','name','description','population','gdp','states']


    def create(self, validated_data):
        states_data = validated_data.pop('states')
        country = Country.objects.create(**validated_data)
        for state_data in states_data:
            get_city_data=state_data.pop('city_data')
            states=State.objects.create(country=country, **state_data)
            for city_items in get_city_data:
                City.objects.create(state=states,country=country, **city_items)
        return country

    def update(self, instance1, validated_data):

        states_data = validated_data.pop('states')
        states = (instance1.states).all()
        print(states,'states')
        states = list(states)
        instance1.name = validated_data.get('name', instance1.name)
        instance1.description = validated_data.get('description', instance1.description)
        instance1.population = validated_data.get('population', instance1.population)
        instance1.gdp = validated_data.get('gdp', instance1.gdp)
        instance1.save()

        for state_data in states_data:
            city_data = state_data.pop('city_data')
            city = instance1.states.get().city_data.all()
            city=list(city)
            for city_items in city_data:
                cities=city.pop(0)
                cities.description =city_items.get('description',cities.description)
                cities.population =city_items.get('population',cities.population)
                cities.gdp =city_items.get('gdp',cities.gdp)
                cities.pincode =city_items.get('pincode',cities.pincode)
                cities.save()
            state = states.pop(0)
            state.name = state_data.get('name', state.name)
            state.description = state_data.get('description', state.description)
            state.population = state_data.get('population', state.population)
            state.gdp = state_data.get('gdp', state.gdp)
            state.save()
        return instance1

"""nested serializer for list of person along with city,state,country and town data"""

class Personlist_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Person
        fields=['id','name']

class Townlist_Serializer(serializers.ModelSerializer):
    person_data=Personlist_Serializer(many=True)
    class Meta:
        model=Town
        fields=['id','description','population','gdp','pincode','person_data']

#
class Citylist_Serializer(serializers.ModelSerializer):
    class Meta:
        model=City
        fields=['id','description','population','gdp','pincode']


class Statelist_Serializer(serializers.ModelSerializer):
    town_data=Townlist_Serializer(many=True)
    city_data=Citylist_Serializer(many=True)

    class Meta:
        model=State
        fields=['id','name','description','population','gdp','city_data','town_data']

class Countrylist_Serializer(serializers.ModelSerializer):
    states = Statelist_Serializer(many=True)

    class Meta:
        model=Country
        fields=['id','name','description','population','gdp','states']

