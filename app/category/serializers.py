from rest_framework import serializers

from app.category.models import Category


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name',)

    def validate_name(self, value):
        name = value.strip()

        if Category.objects.filter(name__iexact=name, is_active=True).exists():
            raise serializers.ValidationError("Category already in use")

        return name.capitalize()


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

    def validate_name(self, value):
        name = value.strip()

        if Category.objects.filter(name__iexact=name, is_active=True).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Category already in use")

        return name.capitalize()


class CategoryDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class CategoryListFilterDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name',)
