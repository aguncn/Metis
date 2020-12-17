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
        fields = ['id', 'attr_id', 'attr_name', 'description',
                  'view_set_id', 'view_set_name', 'model_id', 'model_name',
                  'security_token', 'check_security', 'url',
                  'update_date', 'create_user', 'username']
        extra_kwargs = {
            'username': {
                'read_only': True,
            },
            'attr_count': {
                'read_only': True,
            },
            'view_set_name': {
                'read_only': True,
            },
            'model_name': {
                'read_only': True,
            }
        }


# 依据不同的功能，建立不同的序列化类。新建指标和更新指标时，字段不同，就可以分列出来
class AttrCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attr
        # fields = '__all__'
        fields = ['attr_id', 'attr_name', 'description', 'view_set', 'model',
                  'security_token', 'check_security', 'url',
                  'create_user']


class AttrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attr
        # fields = '__all__'
        fields = ['attr_id', 'attr_name', 'description', 'view_set_id', 'model_id',
                  'security_token', 'check_security', 'url']
