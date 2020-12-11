from rest_framework import serializers

from emails.models import Email


# Class LetterSerializer extends
# django_rest_framework serializers model
# Is a serializer for Letter objects
class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'
        
