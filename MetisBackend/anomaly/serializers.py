from rest_framework import serializers
from MetisModels.anomaly_models import Anomaly


class AnomalySerializer(serializers.ModelSerializer):
    class Meta:
        model = Anomaly
        # fields = '__all__'
        fields = ['id', 'attr', 'mark_flag', 'anomaly_time',
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