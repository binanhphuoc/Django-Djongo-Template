from rest_framework import serializers
from djongo.models.fields import ArrayReferenceManagerMixin

# ArrayReferenceField won't be able to fetch so it returns an empty array
# Expected to return an array of ObjectID values
# Fix this by overriding ArrayReferenceManagerMixin.__str__
# Issue raised on GitHub at: https://github.com/nesdis/djongo/issues/270

def patch_str(self):
    return ("\n".join(set([str(item) for item in self.all()])))

ArrayReferenceManagerMixin.__str__ = patch_str

# CUSTOM FIELDS

class MongoIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)
    
    def to_internal_value(self, data):
        return data

class MongoArrayReferenceField(serializers.ListField):

    class DefaultSerializer(serializers.Serializer):
        _id = MongoIdField()

    child = MongoIdField()

    def __init__(self, *args, **kwargs):
        if 'serializer' not in kwargs:
            self.serializer = self.DefaultSerializer
        else:
            self.serializer = kwargs['serializer']
        kwargs.pop('serializer', None)
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        array = [self.serializer(obj).data for obj in value.get_queryset()]
        return array
    
    def to_internal_value(self, data):
        return data

serializers.MongoIdField = MongoIdField
serializers.MongoArrayReferenceField = MongoArrayReferenceField

def model_update(self, instance, validated_data):
    for key, value in self.get_fields().items():
        if (isinstance(value, MongoArrayReferenceField) and key in validated_data):
            if 'add' in validated_data[key]:
                getattr(instance,key).add(*validated_data[key]['add'])
            if 'remove' in validated_data[key]:
                getattr(instance,key).remove(*validated_data[key]['remove'])
            validated_data.pop(key, None)
    return self.original_update(instance, validated_data)

serializers.ModelSerializer.original_update = serializers.ModelSerializer.update
serializers.ModelSerializer.update = model_update