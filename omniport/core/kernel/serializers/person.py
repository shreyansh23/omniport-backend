import swapper
from rest_framework import serializers

from kernel.managers.get_role import get_all_roles
from kernel.serializers.root import ModelSerializer
from omniport.utils import switcher


def process_roles(person):
    """
    Get all the roles of a person in convenient list format
    :param person: the person whose roles are being retrieved
    :return: the roles of the person as a list
    """

    roles = get_all_roles(person)
    roles = [
        {
            'role': key,
            'activeStatus': str(roles[key]['activeStatus']),
            'data': switcher.load_serializer('kernel', key)(
                roles[key]['instance'],
                excluded_fields=['person', ]
            ).data
        }
        for key in roles
    ]
    return roles


class ProfileSerializer(ModelSerializer):
    """
    Serializer for the entire profile of a person
    """

    roles = serializers.SerializerMethodField()

    def get_roles(self, person):
        """
        Populates the roles field of the serializer
        :param person: the person being serialized
        :return: the roles of the person
        """

        return process_roles(person)

    class Meta:
        """
        Meta class for ProfileSerializer
        """

        model = swapper.load_model('kernel', 'Person')
        fields = '__all__'


class AvatarSerializer(ModelSerializer):
    """
    Serializer for minimal information of a person
    """

    roles = serializers.SerializerMethodField()

    def get_roles(self, person):
        """
        Populates the roles field of the serializer
        :param person: the person being serialized
        :return: the roles of the person
        """

        return process_roles(person)

    class Meta:
        """
        Meta class for AvatarSerializer
        """

        model = swapper.load_model('kernel', 'Person')

        fields = [
            'id',
            'short_name',
            'full_name',
            'display_picture',
            'roles',
        ]
