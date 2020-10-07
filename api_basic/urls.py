from django.urls import path,include
from .views import article_list,article_detail,
ArticleAPIView,
ArticleDetails,
GenericAPIView,
ArticleViewSet,
Article1ViewSet,
Article2ViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('article',Article2ViewSet,basename='article')
# ArticleViewSet
# Artivle2ViewSet

urlpatterns = [
   path('article/',ArticleAPIView.as_view()),
#    path('article/',article_list),
#    path('article/<int:pk>/',article_detail),
  path('viewset/',include(router.urls)),
#   path('')
  path('viewset/<int:pk>/',include(router.urls)),
  path('article/<int:id>',ArticleDetails.as_view()),
  path('generic/article/<int:id>',GenericAPIView.as_view())
]