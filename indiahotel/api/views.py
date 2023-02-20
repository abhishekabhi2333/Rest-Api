from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import menu_items
# Create your views here.
class MenuItems(APIView):
    def get(self,request,*args,**kwargs):
        all_items=menu_items
        if "category" in request.query_params:
            cat=request.query_params.get("category")
            all_items=[i for i in all_items if i["category"]==cat]
            # return Response(data=items)
        if "limit" in request.query_params:
            lmt=request.query_params.get("limit")
            print(lmt)
            all_items=all_items[0:int(lmt)]
            # return Response(data=items)
        return Response(data=all_items)    
    def post(self,request,*args,**kwargs):
        data=request.data
        menu_items.append(data)
        return Response(data=menu_items)


class SpecificItems(APIView):
    def get(self,request,*args,**kwargs):
        item_code=kwargs.get('mid')
        item=[i for i in menu_items if i["code"]==item_code].pop()
        return Response(data=item)
    def delete(self,request,*args,**kwargs):
        item_code=kwargs.get('mid')
        item=[i for i in menu_items if i["code"]==item_code].pop()
        menu_items.remove(item)
        return Response(data=menu_items)
    def put(self,request,*args,**kwargs):
        item_code=kwargs.get('mid')
        data=request.data
        item=[i for i in menu_items if i["code"]==item_code].pop()
        index=menu_items.index(item)
        menu_items[index]=data
        return Response(data=menu_items)
        
