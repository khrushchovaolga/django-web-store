from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import Categories, Products

class CategoryModel:
    def __init__(self, category):
        self.category = category

'''class CategorySerializer(serializers.Serializer):
    #представление даных в виде обычной строки
    category = serializers.CharField(max_length = 250)
    slug = serializers.SlugField(max_length=255)
    available = serializers.BooleanField(default=True)
    #для полей с типом полей ForeingKey
    #cat_id = serializers.IntegerField()

    #новая запись в категорию
    def create(self, validated_data):
        return Categories.objects.create(**validated_data)

    #обновление записи
    def update(self, instance, validated_data):
        instance.category = validated_data.get("category", instance.category)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.available = validated_data.get("available", instance.available)
        instance.save()
        return instance'''

#для модели Category, аналогично записи выше, только оптимизированнее 
class CategorySerializer(serializers.ModelSerializer):
    #скрытое поле
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Categories
        fields = ('category', 'slug', 'available', 'user', )

#для модели Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        #fields = ('id', 'category', 'subcategory', 'product', 'available', )
        fields = '__all__'

'''def encode():
    model = CategoryModel('Milk')
    model_sr = CategorySerializer(model)
    print(model_sr.data, type(model_sr.data), sep = '\n')
    #преобразование в json format
    json = JSONRenderer().render(model_sr.data)
    print(json)

def decode():
    stream = io.BytesIO(b'{"category": "Milk"}')
    data = JSONParser().parse(stream)
    serializer = CategorySerializer(data = data)
    serializer.is_valid()
    print(serializer.validated_data)'''