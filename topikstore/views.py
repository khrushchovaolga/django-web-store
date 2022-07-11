from django import views
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import *

from cart.forms import CartAddProductForm
from netstore.settings import CART_SESSION_ID

from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

from .forms import FeedbackForm, QuestionForm
from .models import *
from .utils import *
from .serializers import *

from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination


'''class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(available = True).select_related('category', 'subcategory')
    serializer_class = ProductSerializer'''

class CategoryAPIView(APIView):
    #request method get
    def get(self, request):
        cats = Categories.objects.filter(available = True)
        return Response({'cats': CategorySerializer(cats, many=True).data})
        #many - обрабатывает список всех записей 

    #request method post
    def post(self, request):
        #Проверка правильности введенных данных
        serializer = CategorySerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #category_new = Categories.objects.create(category=request.data['category'])
        return Response({'post': serializer.data})

    #Получение и изменение
    def put(self, request, *args, **kwargs):
        slug = kwargs.get("cat_slug", None)
        if not slug:
            return Response({'error': 'Method PUT is not allowed'})
        
        try:
            instance = Categories.objects.get(slug = slug)
        except:
            return Response({'error': 'Object does not exists'})

        serializer = CategorySerializer(data=request.data, instance = instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'cats': serializer.data})

    #Получение и изменение
    def delete(self, request, *args, **kwargs):
        slug = kwargs.get("cat_slug", None)
        if not slug:
            return Response({'error': 'Method DELETE is not allowed'})
        
        try:
            instance = Categories.objects.get(slug = slug)
            instance.delete()
        except:
            return Response({'error': 'Object does not exists'})

        return Response({'post': 'delete post ' + str(slug)}, status=204) 

class CategoryAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

#реализация 2-х методов get и post + форма добавления
class CategoryAPIList(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = CategoryAPIListPagination

#реализация метода put 
class CategoryAPIUpdate(generics.UpdateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    lookup_url_kwarg = "cat_slug"
    permission_classes = (IsAdminOrReadOnly, )
    #доступ по токенам, доступ по сессиям недоступен
    #authentication_classes = (TokenAuthentication, )

class CategoryAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    lookup_url_kwarg = "cat_slug"
    permission_classes = (IsAdminOrReadOnly, )

#GET, POST
class ProductAPIList(generics.ListCreateAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    #доступ к чтению для всех, добавление только для админа
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = ProductAPIListPagination

#GET, PUT, DELETE
class ProductAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'pk'
    lookup_url_kwarg = 'product_pk'

#функционал который содержит в себе все запросы
#viewsets.ReadOnlyModelViewSet только для чтения записи (без формы)
'''class CategoryViewSet(viewsets.ModelViewSet):
    #queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    lookup_url_kwarg = "cat_slug"

    def get_queryset(self):
        slug = self.kwargs.get('cat_slug')
        if not slug:
            return Categories.objects.all()[:3]
        return Categories.objects.filter(available=True)

    @action(methods=['get'], detail=True)
    def names_category(self, request, cat_slug=None):
        names = Categories.objects.get(slug = cat_slug)
        return Response({'names': names.category})'''

def home(request):
    
    products = Product.objects.select_related('category', 'subcategory').filter(available = True)
    
    #Pagination for category.catproducts
    paginator_product = Paginator(products, 10)
    page_product = request.GET.get('page')
    products = paginator_product.get_page(page_product)

    context = get_user_context(
        title = 'Topikstore',
        products = products,
        paginator = paginator_product,
    )

    return render(request, 'topikstore/index.html', context)


def get_category(request, cat_slug):

    category = get_object_or_404(Categories, slug=cat_slug)

    #Pagination for category.catproducts
    category_list = category.catproducts.select_related('subcategory').filter(available = True)
    paginator_category = Paginator(category_list, 10)
    page_category = request.GET.get('page')
    catproducts = paginator_category.get_page(page_category)

    context = get_user_context(
        title = 'Topikstore',
        products = catproducts,
        paginator = paginator_category,
    )

    return render(request, 'topikstore/index.html', context)

def get_subcategory(request, cat_slug, subcat_slug):

    subcategory = get_object_or_404(Subcategories.objects.filter(category__slug=cat_slug, available=True), slug=subcat_slug)
    
    #Pagination for subcategory.subcatproducts
    subcategory_list = subcategory.subcatproducts.select_related('category').filter(available = True)
    paginator_subcategory = Paginator(subcategory_list, 5)
    page_subcategory = request.GET.get('page')
    subcatproducts = paginator_subcategory.get_page(page_subcategory)

    context = get_user_context(
        title = subcategory,
        products = subcatproducts,
        paginator = paginator_subcategory,
    )

    return render(request, 'topikstore/index.html', context)


def product(request, cat_slug, subcat_slug, product_pk):

    product = get_object_or_404(Product.objects.select_related('category', 'subcategory').prefetch_related('images').filter(available=True, category__slug=cat_slug, subcategory__slug=subcat_slug), pk=product_pk)
    
    #Pagination for product.feedbacks
    feedback_list = product.feedbacks.filter(display = True)
    paginator_feedback = Paginator(feedback_list, 4)
    page_feedback = request.GET.get('page')
    feedbacks = paginator_feedback.get_page(page_feedback)

    #Pagination for product.questions
    question_list = product.questions.filter(display = True).prefetch_related("answer")
    paginator_question = Paginator(question_list, 4)
    page_question = request.GET.get('page')
    questions = paginator_question.get_page(page_question)

    recently_viewed_products = None

    #Resently viewed products (session)
    if 'recently_viewed' in request.session:
        if product_pk in request.session['recently_viewed']:

            #Для отображения продуктов в том порядке, в котором они были просмотрены
            request.session['recently_viewed'].remove(product_pk)

        products = Product.objects.filter(pk__in=request.session['recently_viewed'])[:5]
        recently_viewed_products = sorted(products, key=lambda x: request.session['recently_viewed'].index(x.pk))
        request.session['recently_viewed'].insert(0, product_pk)

        #Если в сеансе больше 6 продуктов, удаляется последний методом pop()
        if len(request.session['recently_viewed']) > 6:
            request.session['recently_viewed'].pop()

        #Для сохранения сессии вместе со списком и со ссылками внутри
        request.session.modified = True    
    else:
        request.session['recently_viewed'] = [product_pk]

    is_like = None
    if 'favorites_products' in request.session and product_pk in request.session['favorites_products']:
        is_like = True
    else:
        is_like = False
        

    context = get_user_context(
        product = product,
        images = product.images.all(),
        feedbacks = feedbacks,
        questions = questions,
        form_question = QuestionForm,
        form_feedback = FeedbackForm,
        paginator_feedback = paginator_feedback,
        paginator_question = paginator_question,
        recently_viewed = recently_viewed_products,
        is_like = is_like,
        is_available = Product.objects.filter(product=product.product).exclude(pk=product_pk).order_by('volume'),
    )

    return render(request, 'topikstore/product.html', context)


def get_feedback(request, cat_slug, subcat_slug, product_pk):
    if request.POST:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.product = Product.objects.get(pk = product_pk)
            form.save()
            return redirect(feedback.product.get_absolute_url())

def get_question(request, cat_slug, subcat_slug, product_pk):
    if request.POST:
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.product = Product.objects.get(pk = product_pk)
            form.save()
            return redirect(question.product.get_absolute_url())