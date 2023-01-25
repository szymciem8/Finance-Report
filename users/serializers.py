# from .models import User
# from django.core.serializers import serialize

# class UserRegistrationSerializer(serializers.Serializer):
#     class Meta:
#         model = User 
#         fields = ['id', 'email', 'password']
#         extra_kwargs = {
#             'password': {'write_only':True},
#         }
        
#     def create(self, validated_data:dict) -> User:
#         instance = self.Meta.model(**validated_data)
#         instance.save()
#         return instance