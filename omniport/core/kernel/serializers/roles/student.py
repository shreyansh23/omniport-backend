import swapper

from kernel.serializers.institute.branch import BranchSerializer
from kernel.serializers.person import AvatarSerializer
from kernel.serializers.root import ModelSerializer


class StudentSerializer(ModelSerializer):
    """
    Serializer for Student objects
    """

    person = AvatarSerializer(
        read_only=True,
    )
    branch = BranchSerializer(
        read_only=True,
    )

    class Meta:
        """
        Meta class for StudentSerializer
        """

        model = swapper.load_model('kernel', 'Student')

        fields = [
            'id',
            'person',
            'branch',
            'current_year',
            'current_semester',
        ]
