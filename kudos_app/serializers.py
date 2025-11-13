from rest_framework import serializers
from .models import Organization, User, Kudo

# ---- Organization ----
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']

# ---- User ----
class UserSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'organization', 'kudos_left']

# --- Kudo (read) ---
class KudosSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only = True)
    receiver = UserSerializer(read_only = True)

    class Meta:
        model = Kudo
        fields = ['id', 'sender', 'receiver', 'message', 'created_at']

# --- Kudo (create) ---
class KudoCreateSerializer(serializers.ModelSerializer):
    receiver_id = serializers.UUIDField(write_only = True)
    message = serializers.CharField(allow_blank=True, required = False)
    
    class Meta:
        model = Kudo
        fields = ['receiver_id', 'message']

    def validate_receiver_id(self, value):
        try:
            receiver = User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Recevier user not found.")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        sender = request.user
        receiver = User.objects.get(pk=validated_data['receiver_id'])
        kudo = Kudo.objects.create(
            sender=sender,
            receiver=receiver,
            message=validated_data.get('message','')
        )
        return kudo