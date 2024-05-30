from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.permissions import IsAuthenticated

from . import serializers, paginators, perms
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Service, ResidentFamily, Feedback, Bill, SurveyForm, SurveyResponse, TuDo, Package, \
    SurveyQuestion


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['get_current_user', 'set_active', 'delete_user']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()
        return Response(serializers.UserSerializer(user).data)

    @action(methods=['delete'], url_path='delete-user', detail=True)
    def delete_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except User.DoesNotExist:
            return Response({"detail": "Không có người dùng nào khớp với truy vấn đã cho."}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='register-access-card', permission_classes=[IsAuthenticated])
    def register_access_card(self, request):
        user = request.user
        serializer = ResidentFamily(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializers.ResidentFamilySerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], url_path='set-active', detail=True)
    def set_active(self, request, pk):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        return Response(serializers.UserSerializer(instance).data)


class ServiceViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class PaymentViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Bill.objects.filter(active=True)
    serializer_class = serializers.BillSerializer
    pagination_class = paginators.PaymentPaginator
    permission_classes = [perms.PaymentOwner]

    def get_queryset(self):
        queryset = self.queryset
        q = self.request.query_params.get('status')
        if q:
            queryset = queryset.filter(status=q)

        return queryset

    @action(methods=['get'], url_path='services', detail=True)
    def get_services(self, request, pk=None):
        services = self.get_object().service.filter(active=True)
        serializer = serializers.ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['patch'], url_path='upuynhiemchi', detail=True)
    def up_uynhiemchi(self, request, pk=None):
        payment = self.get_object()
        payment_image = request.data.get('payment_image')

        if payment_image:
            payment.payment_image = payment_image
            payment.status = 'pass'
            payment.save()
            return Response(serializers.PaymentSerializer(payment).data)
        else:
            return Response({'error': 'Không tìm thấy hình ảnh thanh toán.'}, status=status.HTTP_400_BAD_REQUEST)


class TuDoViewSet(viewsets.ViewSet, generics.ListAPIView, generics.DestroyAPIView, generics.CreateAPIView):
    queryset = TuDo.objects.all()
    serializer_class = serializers.TuDoSerializer

    def get_permissions(self):
        if self.action == 'add_package':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='packages', detail=True)
    def get_packages(self, request, pk):
        packages = self.get_object().hanghoa_set.filter(status='received')
        return Response(serializers.PackageSerializer(packages, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='packages', detail=True)
    def add_package(self, request, pk):
        # hang_hoa là trong related_name ben model
        c = self.get_object().package.create(name=request.data.get('name'))
        return Response(serializers.PackageSerializer(c).data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        user_id = request.data.get('user')
        TuDo.objects.create(name=name, user_id=user_id)

        return Response(status=status.HTTP_201_CREATED)


class PackageViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Package.objects.filter(active=True)
    serializer_class = serializers.PackageSerializer
    pagination_class = paginators.PackagePaginator

    def get_queryset(self):
        queryset = self.queryset
        q = self.request.query_params.get('q')
        tudo_id = self.request.query_params.get('tuDo')
        if q:
            queryset = queryset.filter(name__icontains=q)
        if tudo_id:
            queryset = queryset.filter(tuDo=tudo_id)
        return queryset


class FeedbackViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = serializers.FeedbackSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class SurveyFormViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = SurveyForm.objects.all()
    serializer_class = serializers.SurveyFormSerializer

    @action(methods=['post'], detail=True, url_path='add-question-with-answers')
    def add_question_with_answers(self, request, pk=None):
        survey_form = self.get_object()
        question_text = request.data.get('text')
        answers = request.data.get('answers')

        if not question_text or not answers:
            return Response({'error': 'Cả nội dung câu hỏi và câu trả lời đều được yêu cầu.'},
                            status=status.HTTP_400_BAD_REQUEST)
        question = SurveyQuestion.objects.create(surveyForm=survey_form, text=question_text)
        for answer in answers:
            SurveyResponse.objects.create(surveyForm=survey_form, surveyQuestion=question, answer=answer['text'])
        return Response(serializers.SurveyQuestionSerializer(question).data, status=status.HTTP_201_CREATED)


class SurveyResponseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = SurveyResponse.objects.all()
    serializer_class = serializers.SurveyResponseSerializer
