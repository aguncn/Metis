from rest_framework import serializers
from MetisModels.view_set_models import ViewSet
from MetisModels.attr_models import Attr


class ViewSetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewSet
        # fields = '__all__'
        fields = ['id', 'view_set_id', 'view_set_name', 'description', 'attr_count',
                  'update_date', 'create_user', 'username']
        extra_kwargs = {
            'username': {
                'read_only': True,
            },
            'attr_count': {
                'read_only': True,
            }
        }


class ViewSetCreateSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewSet
        # fields = '__all__'
        fields = ['view_set_id', 'view_set_name', 'description', 'create_user']


class ViewSetUpdateSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewSet
        # fields = '__all__'
        fields = ['view_set_id', 'view_set_name', 'description']


class AttrListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attr
        # fields = '__all__'
        fields = ['id', 'attr_id', 'attr_name', 'description', 'model_id', 'model_name',
                  'security_token', 'check_security', 'url',
                  'update_date', 'create_user', 'username']
        extra_kwargs = {
            'username': {
                'read_only': True,
            },
            'attr_count': {
                'read_only': True,
            },
            'model_name': {
                'read_only': True,
            }
        }


class AttrCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attr
        # fields = '__all__'
        fields = ['attr_id', 'attr_name', 'description', 'model',
                  'security_token', 'check_security', 'url',
                  'create_user']


class AttrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attr
        # fields = '__all__'
        fields = ['attr_id', 'attr_name', 'description', 'model_id',
                  'security_token', 'check_security', 'url']
