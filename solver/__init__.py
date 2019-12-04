from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
        try:
            return str(value._id)
        except AttributeError:
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

def model_validate(self, data):
    data = self.original_validate(data)
    if self.instance is None:
        return data
    for key, value in self.get_fields().items():
        if (isinstance(value, MongoArrayReferenceField) and key in data):
            model = getattr(self.instance,key).model
            if 'add' in data[key]:
                list_to_validate = data[key]['add']
                if not all(isinstance(item, model) for item in list_to_validate):
                    raise ValidationError("All items in '{:s}.add' must have type '{:s}'. This error may happen because the request is unauthorized for this action."
                    .format(key, str(model)))
            if 'remove' in data[key]:
                list_to_validate = data[key]['remove']
                if not all(isinstance(item, model) for item in list_to_validate):
                    raise ValidationError("All items in '{:s}.remove' must have type '{:s}'. This error may happen because the request is unauthorized for this action."
                    .format(key, str(model)))
    return data

# validated_data: has to be dict with either 'add' or 'remove' specified
# Each 'add' or 'remove' is an array of child objects, not str
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
serializers.ModelSerializer.original_validate = serializers.ModelSerializer.validate
serializers.ModelSerializer.validate = model_validate