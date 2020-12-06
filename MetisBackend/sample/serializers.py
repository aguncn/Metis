from rest_framework import serializers
from MetisModels.models import SampleSet


class SampleSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleSet
        # fields = '__all__'
        fields = ['id', 'attr', 'source', 'anomaly_time',
                  'train_or_test', 'positive_or_negative', 'window',
                  'data_a', 'data_b', 'data_c',
                  'attr_name', 'view_set_name',
                  'create_user', 'username']
        extra_kwargs = {
            'username': {
                'read_only': True,
            },
            'attr_name': {
                'read_only': True,
            },
            'view_set_name': {
                'read_only': True,
            },
            'create_user': {
                'write_only': True,
            },
        }

