from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
import datetime


class User(AbstractUser):
    DoesNotExist = None
    STATUS_CHOICES = (
        ('admin', 'quan tri vien'),
        ('resident', 'dan cu')
    )
    avatar = CloudinaryField(null=True)
    role = models.CharField(max_length=20, choices=STATUS_CHOICES, default='resident')
    tuDo = models.OneToOneField('TuDo', on_delete=models.CASCADE, related_name='users', null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        elif self.role == 'admin' and not self.is_superuser:
            self.role = 'resident'
        super().save(*args, **kwargs)


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    update_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Service(BaseModel):
    objects = None
    name = models.CharField(max_length=50, null=True)
    nameService = RichTextField()
    priceService = models.FloatField()

    def __str__(self):
        return self.name


# Hóa đơn
class Bill(BaseModel):
    objects = None
    STATUS_CHOICES = (
        ('momo', 'Momo pay'),
        ('vnpay', 'vn pay')
    )
    name = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='bills')
    bill_date = models.DateField(default=datetime.date.today)
    payment_method = models.CharField(max_length=20, choices=STATUS_CHOICES, default='momo')
    service = models.ManyToManyField(Service, related_name='hoa_don')

    def __str__(self):
        return self.name

    def get_total_amount(self):
        total_amount = 0
        for service in self.service.all():
            total_amount += service.priceService
        return total_amount


class Payment(BaseModel):
    objects = None
    STATUS_CHOICES = (
        ('pending', 'Chua thanh toan'),
        ('pass', 'Da thanh toan')
    )
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_image = CloudinaryField(null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.transaction_id


# ý 5
class ResidentFamily(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Cho xu ly'),
        ('pass', 'Xu ly thanh cong')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resident_families')
    name = models.CharField(max_length=50, null=True)
    cccd = models.CharField(max_length=50, unique=True)
    sdt = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.errors = None
        self.data = None

    def __str__(self):
        return f'{self.name} - nguoi than cua: {self.user.username}'

    def is_valid(self):
        pass


class AccessCard(BaseModel):
    resident_family = models.OneToOneField(ResidentFamily, on_delete=models.CASCADE, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None

    def __str__(self):
        return f'{self.id} - the giu xe cua: {self.resident_family}'


# ý 6
class Apartment(BaseModel):
    objects = None
    STATUS_CHOICES = (
        ('1', 'Căn hộ cao cấp'),
        ('2', 'Căn hộ trung cấp'),
        ('3', 'Căn hộ thông thường'),
        ('4', 'Căn hộ studio'),
        ('5', 'Căn hộ officetel')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tang = RichTextField()
    soNha = models.CharField(max_length=255, default='default_value')
    type = models.CharField(max_length=20, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return self.user.username


class Contract(BaseModel):
    name = models.CharField(max_length=50, null=True)
    nameContract = RichTextField()
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='hop_dong')
    # Tiền đặt cọc
    deposits = models.FloatField(null=True)

    def __str__(self):
        return self.user.username


# ý 7
class TuDo(BaseModel):
    objects = None
    name = models.CharField(max_length=50, null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tudos')

    def __str__(self):
        return self.name


class Package(BaseModel):
    objects = None
    STATUS_CHOICES = (
        ('waiting', 'Cho nhan hang'),
        ('received', 'Da nhan hang'),
    )
    name = models.CharField(max_length=50, null=True)
    tuDo = models.ForeignKey(TuDo, on_delete=models.CASCADE, related_name='package')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')

    def __str__(self):
        return self.name


# ý 8
class Feedback(BaseModel):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


# Ý 9
class SurveyForm(BaseModel):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='surveyForm')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class SurveyQuestion(BaseModel):
    objects = None
    surveyForm = models.ForeignKey(SurveyForm, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text


class SurveyResponse(BaseModel):
    objects = None
    surveyForm = models.ForeignKey(SurveyForm, on_delete=models.CASCADE, related_name='survey_responses')
    surveyQuestion = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return f'{self.surveyQuestion.text} - {self.answer}'



