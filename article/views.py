from rest_framework import viewsets
from article.serializers import ArticleSerializer, CategorySerializer, CategoryDetailSerializer, TagSerializer, \
    ArticleDetailSerializer
from .models import Article, Category, Tag
from .permissions import IsAdminUserOrReadOnly
from rest_framework import filters
from article.models import Avatar
# 这个 AvatarSerializer 最后来写
from article.serializers import AvatarSerializer


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer

    pagination_class = None


# 第八次：使用视图集
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer


# def list(self, request, *args, **kwargs):
#     print(self.request.query_params.get('username', None))
#     return super().list(request, *args, **kwargs)

# def get_queryset(self):
#     queryset = self.queryset
#     username = self.request.query_params.get('username', None)
#     if username is not None:
#         queryset = queryset.filter(author__username=username)
#     return queryset


# from django.shortcuts import render
# 第一次写视图函数
# from django.http import JsonResponse
# from .models import Article
# from .serializers import ArticleListSerializer
#
#
# def article_list(request):
#     articles = Article.objects.all()
#     serializers = ArticleListSerializer(articles, many=True)
#     return JsonResponse(serializers.data, safe=False)

# 第二次：使用rest_framework框架
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Article
# from .serializers import ArticleListSerializer, ArticleDetailSerializer

# 第四次：使用混合类
from rest_framework import mixins
from rest_framework import generics

# 第六次：增加权限控制
# from rest_framework.permissions import IsAdminUser

# 第七次：完善权限控制
# from .permissions import IsAdminUserOrReadOnly


# 第五次：继承 generics.RetrieveUpdateDestroyAPIView 类
# class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleDetailSerializer
#     permission_classes = [IsAdminUserOrReadOnly]


# class ArticleDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleDetailSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# 第三次：定义类视图
from rest_framework.views import APIView
from django.http import Http404

# class ArticleDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Article.objects.get(pk=pk)
#         except:
#             raise Http404
#
#     def get(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleDetailSerializer(article)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleDetailSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         article = self.get_object(pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def article_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializers = ArticleListSerializer(articles, many=True)
#         return Response(serializers.data)
#     elif request.method == 'POST':
#         serializer = ArticleListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ArticleList(generics.ListCreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleListSerializer
#     # 仅允许管理员查看和发表文章
#     permission_classes = [IsAdminUserOrReadOnly]
#
#     # 新增代码，让文章作者等于写文章的人
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
