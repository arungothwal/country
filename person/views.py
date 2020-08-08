
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CountrySerializer,State_dataSerializer,Countrylist_Serializer,Person_dataSerializer,City_dataSerializer,Town_dataSerializer,Country_dataSerializer
from .models import *
from django.db.models import Q

from rest_framework.pagination import LimitOffsetPagination

# Create your views here.

""" CRUD of country  """

class Country_data(APIView):
    def post(self,request):
        try:
            data = request.data
            name = data.get('name')
            country_name=Country.objects.filter(name=name)
            if country_name:
                return Response({"message": 'country is already exist'}, status=status.HTTP_400_BAD_REQUEST)
            if name is None:
                return Response({"message": 'please enter country name with field "name"'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = Country_dataSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
        try:
            country_obj = request.GET.get('id')
            if country_obj is not None:
                data = Country.objects.get(id=country_obj)
                serializer = Country_dataSerializer(data)
                return Response({'message': "Country Data", 'result': serializer.data}, status=status.HTTP_200_OK)
            all_country=Country.objects.all()
            print(all_country)
            serializer = Country_dataSerializer(all_country,many=True)
            return Response({'message': "All Country", 'result': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        try:
            try:
                country_id = Country.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'data does not exist'}, status=status.HTTP_404_NOT_FOUND)
            serializer = Country_dataSerializer(country_id,data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'updated successfully'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk):
        try:
            try:
                snippet = Country.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'data not exist'}, status=status.HTTP_404_NOT_FOUND)
            snippet.delete()
            return Response({'message':'successfully deleted'},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

""" CRUD of state  """

class State_data(APIView):
    def post(self,request):
        try:
            params = request.data
            name=params.get('name')
            state_name = State.objects.filter(name=name)
            if state_name:
                return Response({"message": 'State is already exist'}, status=status.HTTP_400_BAD_REQUEST)
            if not name:
                return Response({"message": 'please enter state name'}, status=status.HTTP_400_BAD_REQUEST)
            description=params.get('description')
            if not description:
                return Response({"message": 'please enter state description'}, status=status.HTTP_400_BAD_REQUEST)
            population=params.get('population')
            if not population:
                return Response({"message": 'please enter state population'}, status=status.HTTP_400_BAD_REQUEST)
            gdp=params.get('gdp')
            if not gdp:
                return Response({"message": 'please enter state gdp'}, status=status.HTTP_400_BAD_REQUEST)
            country_name= params.get('country')
            if not country_name:
                return Response({"message": 'please enter country name with field "country" '}, status=status.HTTP_400_BAD_REQUEST)
            try:
                country_obj = Country.objects.get(name=country_name)
            except Exception as e:
                print(e)
                return Response({"message": 'country not exist'}, status=status.HTTP_400_BAD_REQUEST)
            data1={'name':name,'description':description,'population':population,'gdp':gdp,'country':country_obj.id}
            serializer =State_dataSerializer(data=data1)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "successfully created", "data": serializer.data},status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        try:
            state_obj =request.GET['id']
            try:
                data= State.objects.get(id=state_obj)
            except Exception as e:
                print(e)
                return Response({"message": 'state does not exist'}, status=status.HTTP_404_NOT_FOUND)
            print(data,data)
            serializer = State_dataSerializer(data)
            return Response({'message': "success", 'result': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            try:
                state_id = State.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'state does not exist'}, status=status.HTTP_404_NOT_FOUND)
            serializer = State_dataSerializer(state_id, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk):
        try:
            try:
                snippet = State.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'data not exist'}, status=status.HTTP_404_NOT_FOUND)
            snippet.delete()
            return Response({'message': 'successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

"""CRUD of City"""
class City_data(APIView):

    def post(self,request):
        try:
            params = request.data
            state_name = params.get('state')
            if not state_name:
                return Response({"message": 'please enter state name'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                state_name = State.objects.get(name=state_name)
            except Exception as e:
                return Response({"message": 'State not existt'}, status=status.HTTP_404_NOT_FOUND)
            country_name = params.get('country')
            if not country_name:
                return Response({"message": 'please enter country name with field "country" '},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                country_obj = Country.objects.get(name=country_name)
            except Exception as e:
                print(e)
                return Response({"message": 'country not exist'}, status=status.HTTP_404_NOT_FOUND)
            description = params.get('description')
            if not description:
                return Response({"message": 'please enter state description'}, status=status.HTTP_400_BAD_REQUEST)
            population = params.get('population')
            if not population:
                return Response({"message": 'please enter state population'}, status=status.HTTP_400_BAD_REQUEST)
            gdp = params.get('gdp')
            if not gdp:
                return Response({"message": 'please enter state gdp'}, status=status.HTTP_400_BAD_REQUEST)
            pincode = params.get('pincode')
            if not pincode:
                return Response({"message": 'please enter pincode'}, status=status.HTTP_400_BAD_REQUEST)

            data1 = {'state': state_name.id, 'description': description, 'population': population, 'gdp': gdp,'pincode':pincode,
                     'country': country_obj.id}
            serializer = City_dataSerializer(data=data1)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        try:
            city_obj = request.GET['id']
            try:
                data = City.objects.get(id=city_obj)
            except Exception as e:
                return Response({"message": "city doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = City_dataSerializer(data)
            return Response({'message': "success", 'result': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            try:
                city_id = City.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'city does not exist'}, status=status.HTTP_404_NOT_FOUND)
            serializer = City_dataSerializer(city_id, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk):
        try:
            try:
                snippet = City.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'data not exist'}, status=status.HTTP_400_BAD_REQUEST)
            snippet.delete()
            return Response({'message': 'successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

"""CRUD of Town"""

class Town_data(APIView):
    def post(self,request):
        try:
            params = request.data
            state_name = params.get('state')
            if not state_name:
                return Response({"message": 'please enter state name'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                state_name = State.objects.get(name=state_name)
            except Exception as e:
                return Response({"message": 'State not existt'}, status=status.HTTP_400_BAD_REQUEST)
            country_name = params.get('country')
            if not country_name:
                return Response({"message": 'please enter country name with field "country" '},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                country_obj = Country.objects.get(name=country_name)
            except Exception as e:
                print(e)
                return Response({"message": 'country not exist'}, status=status.HTTP_400_BAD_REQUEST)
            description = params.get('description')
            if not description:
                return Response({"message": 'please enter town description'}, status=status.HTTP_400_BAD_REQUEST)
            population = params.get('population')
            if not population:
                return Response({"message": 'please enter town population'}, status=status.HTTP_400_BAD_REQUEST)
            gdp = params.get('gdp')
            if not gdp:
                return Response({"message": 'please enter town gdp'}, status=status.HTTP_400_BAD_REQUEST)
            pincode = params.get('pincode')
            if not pincode:
                return Response({"message": 'please enter pincode'}, status=status.HTTP_400_BAD_REQUEST)

            data1 = {'state': state_name.id, 'description': description, 'population': population, 'gdp': gdp,'pincode':pincode,
                     'country': country_obj.id}
            serializer = Town_dataSerializer(data=data1)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        try:
            town_obj = request.GET['id']
            try:
                data = Town.objects.get(id=town_obj)
            except Exception as e:
                return Response({"message": "Town doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = Town_dataSerializer(data)
            return Response({'message': "success", 'result': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            try:
                town_id = Town.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'town does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = City_dataSerializer(town_id, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            try:
                snippet = Town.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'data not exist'}, status=status.HTTP_400_BAD_REQUEST)
            snippet.delete()
            return Response({'message': 'successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


"""CRUD  of person"""
class Persons(APIView):
    def post(self,request):
        try:
            params=request.data
            name=params.get('name')
            if not name:
                return Response({"message": 'please enter the person name'}, status=status.HTTP_400_BAD_REQUEST)
            state_name = params.get('state')
            if not state_name:
                return Response({"message": 'please enter the state name'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                state = State.objects.get(name=state_name)
            except Exception as e:
                return Response({"message": 'state not found'}, status=status.HTTP_400_BAD_REQUEST)
            country_name = params.get('country')
            if not country_name:
                return Response({"message": 'please enter the country name'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                country =Country.objects.get(name=country_name)
            except Exception as e:
                return Response({"message": 'country not found'}, status=status.HTTP_400_BAD_REQUEST)
            dataa = Town.objects.get(Q(state=state.id) and Q(country=country.id))
            if not dataa:
                return Response({"message": 'Town not found'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                test={'name':name,'town':dataa.id}
                serializer = Person_dataSerializer(data=test)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({"message": "successfully created", "data": serializer.data},
                                        status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            data = Person.objects.all()
            serializer = Person_dataSerializer(data,many=True)
            return Response({'message': "success", 'result': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            try:
                person_id = Person.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'person does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = Person_dataSerializer(person_id, data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            try:
                snippet = Person.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'data not exist'}, status=status.HTTP_400_BAD_REQUEST)
            snippet.delete()
            return Response({'message': 'successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


"""CRUD of country,state and city"""

class Person_data(APIView):

    def post(self, request):
        try:
            data=request.data
            name=data.get('name')
            country_name = Country.objects.filter(name=name)
            if country_name:
                return Response({"message": 'country is already exist'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = CountrySerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        try:
            country_id = request.GET['id']
            try:
                data = Country.objects.get(id=country_id)
            except Exception as e:
                return Response({"message": "data doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CountrySerializer(data)
            return Response({'message': "success", 'result': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        try:
            try:
                snippet = Country.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'data not found,please enter correct id'}, status=status.HTTP_404_NOT_FOUND)
            serializer = CountrySerializer(snippet, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'updated successfully'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk):
        try:
            try:
                snippet = Country.objects.get(pk=pk)
            except Exception as e:
                return Response({"message": 'data not found'}, status=status.HTTP_404_NOT_FOUND)
            snippet.delete()
            return Response({'message':'successfully deleted'},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

'''list of person'''

class PersonListView(APIView):
    def get(self,request):
        try:
            filter_country=request.GET.get('name')
            if filter_country is not None:
                country=Country.objects.filter(name=filter_country)
                serializer=Countrylist_Serializer(country,many=True)
                return Response({'message': 'data', 'data': serializer.data}, status=status.HTTP_200_OK)
            queryset=Country.objects.all()
            paginator = LimitOffsetPagination()
            result_page = paginator.paginate_queryset(queryset, request)
            serializer=Countrylist_Serializer(result_page,many=True)
            return Response({'message': 'data','data':serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
