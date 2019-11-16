from rest_framework import serializers
from djongo.models.fields import ArrayReferenceManagerMixin
from .models import Concept, Attribute, Equation

# ArrayReferenceField won't be able to fetch and return an empty array
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

    # def to_internal_value(self, data):
    #     data = data.strip('rgb(').rstrip(')')
    #     red, green, blue = [int(col) for col in data.split(',')]
    #     return Color(red, green, blue)

class MongoArrayReferenceField(serializers.Field):

    class DefaultSerializer(serializers.Serializer):
        _id = MongoIdField()

    def __init__(self, *args, **kwargs):
        if 'serializer' not in kwargs:
            self.serializer = self.DefaultSerializer
        else:
            self.serializer = kwargs['serializer']
        kwargs.pop('serializer', None)
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        print("\nArrayReferenceField:\n")
        array = [self.serializer(obj).data for obj in value.get_queryset()]
        # value.get_queryset() will return the Python objects, so we need to serialize
        # them into JSON
        # We can see the Python objects and their data types by uncommenting the below:

        # for obj in value.get_queryset():
        #     print(obj.description)
        #     print(type(obj))
        return array

# SERIALIZERS

class AttributeSerializer(serializers.ModelSerializer):
    _id = MongoIdField()
    class Meta:
        model = Attribute
        fields = ['_id','symbol', 'description']

class EquationSerializer(serializers.ModelSerializer):
    _id = MongoIdField()
    class Meta:
        model = Equation
        fields = ['_id','syntax', 'name','description']

class ConceptSerializer(serializers.ModelSerializer):
    #     many=True
    # )
    _id = MongoIdField()
    attributes = MongoArrayReferenceField(serializer=AttributeSerializer)
    equations = MongoArrayReferenceField(serializer=EquationSerializer)
    
    class Meta:
        model = Concept
        fields = ['_id','name','attributes','equations']