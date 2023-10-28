from rest_framework import serializers
from rest_framework.fields import empty
from .models import Student


class Capitalizer(serializers.CharField):
    def run_validation(self, data):
        return data.capitalize()


class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = Capitalizer(max_length=50)
    roll = serializers.CharField(max_length=50)

    def create(self, validated_data):
        # Implement the create method to create a new Student instance
        instance = Student.objects.create(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.roll = validated_data["roll"]
        instance.save()
        return instance

    ############################### MODEL Serializer #################################################################


# Validators
def characters_less_than(value):
    print("validators")
    if len(value) > 10:
        raise serializers.ValidationError("Value must be less than 10 characters")


class StudentModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False,
        allow_null=False,
        #default="John Doe",
        validators=[characters_less_than],
        error_messages={
            'required': 'The name field is required.',
            'max_length': 'Name is too long.',
        },
        label='Full Name',
        help_text='Enter the full name of the person.',
        style={'placeholder': 'Full Name'},
        trim_whitespace=True
    )
    roll = serializers.CharField(max_length=100, validators=[characters_less_than])
    
    class Meta:
        model = Student
        fields = "__all__"
        # exclude = ('id',)  # Exclude the 'id' field
        # read_only_fields = ('name',)  # Specify read-only fields
        # extra_kwargs = {
            # 'name': {'help_text': 'The student\'s name'},
            # 'roll': {'validators': [characters_less_than]},
        # }
        
     # Field Level validation
    def validate_name(self, value):
        print('field level validator')
        if value[0] != "D":
            raise serializers.ValidationError("Value should be start with D")
        return value
    
    # Object Level validation
    def validate(self, attrs):
        print('object level validator')
        name = attrs.get("name")
        if name:
            attrs['name'] = name.upper()
        return attrs
    
    
    #The to_internal_value() method is called before validation on a Django REST Framework serializer. 
    # It is used to convert the received data (which is in its non-serialized form) to the internal Python representation
    def to_internal_value(self, data): # received data (non-serialized) # is_valid()
        print("to_internal_value" ,data)
        # Convert the date string to a datetime object.
        #date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
        return super().to_internal_value(data)
    
    def create(self, validated_data): # serializer.save() 
        print("in_create" , validated_data)
        instance= Student.objects.create(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        print("in_update" , instance,validated_data)
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        print('Pre-save operations')
        # Call the superclass's save method to perform the actual save operation
        instance = super().save(**kwargs)
        # Perform post-save operations here
        # For example, you can trigger signals or update related objects
        print('Post-save operations')
        return instance
    
    def to_representation(self, instance):
        obj = super(StudentModelSerializer, self).to_representation(instance)
        print("inside to_representation", obj)
        return obj

    
    
    
    ##### is_valid() ####
    #-> to_internal_method()
        #-> validators
        #-> field level validation
        # -> object level validation
    
    #### is_save() ####
    #-> create
    #->update
    #-> to_representation    
    
    
    
    