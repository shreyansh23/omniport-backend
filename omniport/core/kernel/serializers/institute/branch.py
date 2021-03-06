import swapper

from kernel.serializers.institute.degree import DegreeSerializer
from kernel.serializers.institute.department import DepartmentSerializer
from kernel.serializers.root import ModelSerializer


class BranchSerializer(ModelSerializer):
    """
    Serializer for Branch objects
    """

    degree = DegreeSerializer(
        read_only=True,
    )
    department = DepartmentSerializer(
        read_only=True,
    )

    class Meta:
        """
        Meta class for BranchSerializer
        """

        model = swapper.load_model('kernel', 'Branch')

        fields = [
            'id',
            'code',
            'name',
            'degree',
            'department',
        ]
