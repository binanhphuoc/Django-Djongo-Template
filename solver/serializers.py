from rest_framework import serializers
from .models import Concept, Attribute, Equation

# SERIALIZERS

class AttributeSerializer(serializers.ModelSerializer):
    _id = serializers.MongoIdField(read_only=True)
    parent_concept = serializers.MongoIdField()
    class Meta:
        model = Attribute
        fields = ['_id','symbol','parent_concept','description']

class EquationSerializer(serializers.ModelSerializer):
    _id = serializers.MongoIdField(read_only=True)
    parent_concept = serializers.MongoIdField()
    class Meta:
        model = Equation
        fields = ['_id','syntax', 'name','description']

class ConceptSerializer(serializers.ModelSerializer):
    _id = serializers.MongoIdField(read_only=True)
    equations = serializers.MongoArrayReferenceField(serializer=EquationSerializer,required=False)
    attributes = serializers.MongoArrayReferenceField(serializer=AttributeSerializer,required=False)

    class Meta:
        model = Concept
        fields = ['_id','name','attributes','equations']
    
    # def validate_attributes(self, value):
    #     """
    #     Check that the start is before the stop.
    #     """
    #     if ['start_date'] > data['end_date']:
    #         raise serializers.ValidationError("finish must occur after start")
    #     return data

# As we see, ArrayReferenceField requires patch_str overriding of __str__ to work!!!
# There's another way to avoid this override.
# Append "_id" to the the name of ArrayReferenceField, e.g. "attributes" -> "attributes_id"
# And provide the field with a custom serializers.Field
# The code below demonstrates this way:

# class MongoArrayReferenceFieldWithIdPostfix(serializers.Field):
#     def to_representation(self, value):
#         print(value)
#         return "hello"

# class ConceptSerializer(serializers.ModelSerializer):
#     attributes = MongoArrayReferenceFieldWithIdPostfix()
#     class Meta:
#         model = Concept
#         fields = ['attributes_id']