from django.shortcuts import render
from rest_framework.views import APIView,Response
from .serializers import DishSerializer,DishModelSer,UserModelSerializer,ReviewSerializer
from .models import Dish,Review
from rest_framework import status
# Create your views here.
class DishView(APIView):
    def post(self,request,*args,**kwargs):
        dish=DishSerializer(data=request.data)
        if dish.is_valid():
            name=dish.validated_data.get("name")
            cat=dish.validated_data.get("category")
            prc=dish.validated_data.get("price")
            Dish.objects.create(name=name,category=cat,price=prc)
            return Response({"msg":"Ok"})
        return Response({"msg":"failed"})   
    def get(self,request,*args,**kwargs):
        if "category" in request.query_params:
            cat=request.query_params.get("category")
            dish=Dish.objects.filter(category=cat)
            dis_dish=DishSerializer(dish,many=True)
            return Response(data=dis_dish.data)
        dishes=Dish.objects.all()
        dis_dish=DishSerializer(dishes,many=True)
        return Response(data=dis_dish.data)


class DishItem(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        dish=Dish.objects.get(id=id)
        des_dish=DishSerializer(dish)
        return Response(data=des_dish.data)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        dish=Dish.objects.get(id=id)
        dish.delete()
        return Response({"msg":"ok"})
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        new_dish=DishSerializer(data=request.data)
        if new_dish.is_valid():
            old_dish=Dish.objects.get(id=id)
            old_dish.name=new_dish.validated_data.get("name")
            old_dish.category=new_dish.validated_data.get("category")
            old_dish.price=new_dish.validated_data.get("price")
            old_dish.save()
            return Response({"msg":"ok"})
        return Response({"msg":"failed"})    
            

class DishMView(APIView):
    def post(self,request,*args,**kwargs):
        dish=DishModelSer(data=request.data)
        if dish.is_valid():
            dish.save()
            return Response({"msg":"ok"})
        return Response({"msg":dish.errors},status=status.HTTP_404_NOT_FOUND)
    def get(self,request,*args,**kwargs):
        dishes=Dish.objects.all()
        dis_dish=DishSerializer(dishes,many=True)
        return Response(data=dis_dish.data)


class DishMItem(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            dish=Dish.objects.get(id=id)
            des_dish=DishModelSer(dish)
            return Response(data=des_dish.data)
        except:
          return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)    
    # return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)
    def delete(self,request,*args,**kwargs):
        try:
          id=kwargs.get("id")
          dish=Dish.objects.get(id=id)
          dish.delete()
          return Response({"msg":"ok"})
        except:
          return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,*args,**kwargs):
        try:
            id=kwargs.get("id")
            old_dish=Dish.objects.get(id=id)
            new_dish=DishModelSer(data=request.data,instance=old_dish)
            if new_dish.is_valid():
                new_dish.save()
                return Response({"msg":"ok"})
            else:
                return Response({"msg":new_dish.errors},status=status.HTTP_404_NOT_FOUND)  
        except:
            return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)      
                
class UserView(APIView):
    def post(self,request,*args,**kwargs):
        try:
            new_user=UserModelSerializer(data=request.data)
            if new_user.is_valid():
                new_user.save()
                return Response({"msg":"ok"})
            else:
                return Response({"msg":new_user.errors},status=status.HTTP_404_NOT_FOUND)  
        except:
            return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)    

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework import permissions,authentication
from rest_framework.decorators import action

class DishViewViewset(ViewSet):
    def create(self,request,*args,**kwargs):
        dish=DishModelSer(data=request.data)
        if dish.is_valid():
            dish.save()
            return Response({"msg":"ok"})
        return Response({"msg":dish.errors},status=status.HTTP_404_NOT_FOUND)
    def list(self,request,*args,**kwargs):
        dish=Dish.objects.all()
        if "category" in request.query_params:
            cat=request.query_params.get("category")
            dish=dish.filter(category=cat)
        if "price_lt" in request.query_params:
            pl=request.query_params.get("price_lt")
            dish=dish.filter(price__lt=pl)    
        dis_dish=DishSerializer(dish,many=True)
        return Response(data=dis_dish.data)
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            dish=Dish.objects.get(id=id)
            des_dish=DishModelSer(dish)
            return Response(data=des_dish.data)
        except:
          return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)
    def update(self,request,*args,**kwargs):
        try:
            id=kwargs.get("pk")
            old_dish=Dish.objects.get(id=id)
            new_dish=DishModelSer(data=request.data,instance=old_dish)
            if new_dish.is_valid():
                new_dish.save()
                return Response({"msg":"ok"})
            else:
                return Response({"msg":new_dish.errors},status=status.HTTP_404_NOT_FOUND)  
        except:
            return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)

    def destroy(self,request,*args,**kwargs):
        try:
          id=kwargs.get("pk")
          dish=Dish.objects.get(id=id)
          dish.delete()
          return Response({"msg":"ok"})
        except:
          return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)


class DishModelViewViewset(ModelViewSet):
    serializer_class=DishModelSer
    queryset=Dish.objects.all()
    model=Dish
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    @action(detail=True,methods=['get'])
    def get_review(request,*args,**kwargs):
        did=kwargs.get("pk")
        dish=Dish.objects.get(id=did)
        qs=Review.objects.filter(dish=dish)
        ser=ReviewSerializer(qs,many=True)
        return Response(data=ser.data)

    @action(detail=True,methods=['post'])    
    def add_review(request,*args,**kwargs):
        did=kwargs.get("pk")
        dish=Dish.objects.get(id=did)
        user=request.user
        ser=ReviewSerializer(data=request.data,context={"user":user,"dish":dish})
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data)
        else:
            return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)



    





