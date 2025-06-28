from rest_framework import serializers

from app.tag.models import Tag


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('pk', 'name',)

    def validate_name(self, value):
        name = value.strip()

        if Tag.objects.filter(name__iexact=name, is_active=True).exists():
            raise serializers.ValidationError("Tag already in use")

        return name.capitalize()


class TagDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('pk', 'name',)

class TagUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('pk', 'name',)

    def validate_name(self, value):
        name = value.strip()

        if Tag.objects.filter(name__iexact=name, is_active=True).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Tag already in use")

        return name.capitalize()