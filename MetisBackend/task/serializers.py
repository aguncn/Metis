from rest_framework import serializers
from MetisModels.models import TrainTask


class TrainTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainTask
        
        fields = ['id', 'task_id',
                  'sample_num', 'positive_sample_num', 'negative_sample_num',
                  'window', 'model_name', 'source',
                  'start_date', 'end_date', 'create_date',
                  'task_status', 'create_user', 'username']
        # fields = '__all__'
        extra_kwargs = {
            'username': {
                'read_only': True,
            },
            'create_user': {
                'write_only': True,
            },
        }



