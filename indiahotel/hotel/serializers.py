from rest_framework import serializers
from .models import*
from django.contrib.auth.models import User

class DishSerializer(serializers.Serializer):
    name=serializers.CharField()
    category=serializers.CharField()
    price=serializers.IntegerField()


class DishModelSer(serializers.ModelSerializer):
    class Meta:
        model=Dish
        fields="__all__"
    def validate(self,data):
        cost=data.get("price")
        if cost<0:
            raise serializers.ValidationError
        return data


class UserModelSerializer(serializers.ModelSerializer):
            class Meta:
                model=User
                fields=["username","password","email"]
            def create(self, validated_data):
                print(validated_data)
                return User.objects.create_user(**validated_data)    

class ReviewSerializer(serializers.ModelSerializer):
    # dish=DishModelSer(many=False,read_only=True)
    class Meta:
        model=Review
        fields=[
            
            "review",
            "rating",
            "date",
            
        ] 
    def create(self,validated_data):
        user=self.context.get("user")
        dish=self.context.get("dish")
        return Review.objects.create(user=user,dish=dish,**validated_data)    
