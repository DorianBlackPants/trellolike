from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from myboard.models import Profile, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True, default='NEW')
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        if task.created_by is None:
            task.created_by = self.context['request'].user
            task.save()
            return task

        raise serializers.ValidationError('Somthing went wrong!')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Profile
        fields = ('username', 'first_name',
                  'last_name', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        attrs.pop('password2')
        return attrs

    def create(self, validated_data):
        user = Profile.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
