from rest_framework import serializers
from .models import User, Service, Bill, Payment, ResidentFamily, AccessCard, TuDo, Package, Feedback, SurveyForm, \
    SurveyQuestion, SurveyResponse


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar', 'role', 'is_active']
        extra_kwargs = {
            'password': {
                'write_only': 'true'
            }
        }


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        # để hiển thị dường dân tuyệt đối của ảnh trên swagger
        rep = super().to_representation(instance)
        image = instance.image
        if image:
            rep['image'] = image.url
        return rep


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'nameService', 'priceService']


class BillSerializer(ItemSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'name', 'bill_date', 'created_date', 'service', 'user']


class PaymentSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # services = ServiceSerializer(many=True)
    class Meta:
        model = Payment
        fields = ['id', 'bill', 'status', 'amount', 'payment_image', 'created_date', 'transaction_id', 'user']


class ResidentFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentFamily
        fields = ['id', 'name', 'cccd', 'sdt', 'created_date', 'updated_date', 'active', 'user_id', 'status']


class TuDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuDo
        fields = ['id', 'name', 'created_date', 'active']


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['id', 'name', 'tuDo', 'status']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'subject', 'message', 'user']


class SurveyFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyForm
        fields = ['id', 'user', 'title', 'description', 'is_active']


class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = ['surveyForm', 'text']


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ['id', 'answer']
