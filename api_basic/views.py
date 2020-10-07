from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404



#  modelviewsets inherits from modelviewsets
class Article2Viewsets(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()




# generic viewsets

class Article1ViewSet(viewsets.GenericViewSet,
 mixins.ListModelMixin,
 mixins.CreateModelMixin,
 mixins.UpdateModelMixin, 
 mixins.RetrieveModelMixin,
 mixins.DestroyModelMixin
):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    


# viewsets and routers

class ArticleViewSet(viewsets.ViewSet):
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset,pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self,request,pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        # delete

#  generic views and mixins

class GenericAPIView(generics.GenericAPIView,
mixins.ListModelMixin,
mixins.CreateModelMixin,
mixins.UpdateModelMixin,
mixins.RetrieveModelMixin,
mixins.DestroyModelMixin
):
    serializer_class = ArticleSerializer
    queryset =Article.objects.all()
    lookup_field ='id'
    # authentication_classes=[SessionAuthentication,BasicAuthentication]
    # first checks session then basic
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request,id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)
 
    def patch(self, request,id=None):
        return self.update(request,id)

    def put(self, request,id=None):
        return self.update(request,id)

    def delete(self, request,id=None):
        return self.destroy(request,id)



# class based views 

class ArticleAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    

class ArticleDetails(APIView):

        def get_object(self,id):
            try:
                    return Article.objects.get(id=id)
            except Article.DoesNotExist:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
       
        def  get(self,request,id):
                article=self.get_object(id)
                serializer = ArticleSerializer(article)
                return Response(serializer.data)

        def put(self,request,id):
                article= self.get_object(id)
                serializer = ArticleSerializer(article,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request,id):
            article=self.get_object(id)
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)






# fn based views
# @csrf_exempt
@api_view(['GET','POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)
        # return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = ArticleSerializer(
            # data=data
            data=request.data
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
            # return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
         serializer = ArticleSerializer(article)
     # serializer only one instance    
         return Response(serializer.data)
        #  return JsonResponse(serializer.data)


    elif request.method == 'PUT':
        #   data = JSONParser().parse(request)
          serializer = ArticleSerializer(article,
        #   data=data
          data=request.data
          )

          if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
                # return JsonResponse(serializer.data)
        #   return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'DELETE':
           article.delete()
        #    return HttpResponse(status=status.HTTP_204_NO_CONTENT)
           return Response(status=status.HTTP_204_NO_CONTENT)

# DRF has two main systems for handling views:

# APIView: This provides methods handler for http verbs: get, post, put, patch, and delete.
# ViewSet: This is an abstraction over APIView, which provides actions as methods:
# list: read only, returns multiple resources (http verb: get). Returns a list of dicts.
# retrieve: read only, single resource (http verb: get, but will expect an id in the url). Returns a single dict.
# create: creates a new resource (http verb: post)
# update/partial_update: edits a resource (http verbs: put/patch)
# destroy: removes a resource (http verb: delete)
# Both can be used with normal django urls.

# Because of the conventions established with the actions, the ViewSet has also the ability to be mapped into a router, which is really helpful.

# Now, both of this Views, have shortcuts, these shortcuts give you a simple implementation ready to be used.

# GenericAPIView: for APIView, this gives you shortcuts that map closely to your database models. Adds commonly required behavior for standard list and detail views. Gives you some attributes like, the serializer_class, also gives pagination_class, filter_backend, etc

# GenericViewSet: There are many GenericViewSet, the most common being ModelViewSet. They inherit from GenericAPIView and have a full implementation of all of the actions: list, retrieve, destroy, updated, etc. Of course, you can also pick some of them, read the docs.

