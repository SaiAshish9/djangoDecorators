from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields =['id', 'title','author']
        # fields = '__all__'


# class ArticleSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100)
#     author= serializers.CharField(max_length=100)
#     email= serializers.EmailField(max_length=100)
#     date= serializers.DateTimeField(auto_now_add=True)

#     def create(self,validated_data):
#         return Article.objects.create(validated_data)

#     def update(self,instance,validated_data):
#         instance.title = validated_data.get('title',instance.title)
#         instance.author = validated_data.get('author',instance.author)
#         instance.email=validated_data.get('email',instance.email)
#         instance.date=validated_data.get('date',instance.date)
#         instance.save()
#         return instance
    
    # from  api_basic.models import Article
    # from api_basic.serializers import ArticleSerializer
    # from rest_framework.serializers import JSONRenderer
    # from rest_framework.parsers import JSONParser
    # a=Article(title='a',author='a',email='b')
    # a.save()
    # serializer=ArticleSerializer(a)
    # serializer.data
    # content = JSONRenderer().render(serializer.data)
    # content
    # serializer=ArticleSerializer(Article.objects.all(),many=True)


#  In the same way django provides form and
#  modelForm
#  Rest Framework provides both Serializer 
#  and ModelSerializer
#  print(repr(ArticleSerializer()))

#  to serialize a queryset always use many=True

   