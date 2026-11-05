from urllib.parse import urlsplit

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, URLValidator

from .models import Target


def validate_web_url(value):
    URLValidator(schemes=['http', 'https'])(value)
    # https://아이디:비밀번호@주소 형태는 비밀번호가 DB에 그대로 저장되므로 막는다.
    parts = urlsplit(value)
    if parts.username or parts.password:
        raise ValidationError('주소에 아이디나 비밀번호를 넣을 수 없습니다.')


def validate_absolute_path(value):
    if not value.startswith('/') or '..' in value.split('/'):
        raise ValidationError('/로 시작하는 전체 경로를 입력하세요. ..는 쓸 수 없습니다.')


def validate_apk_path(value):
    validate_absolute_path(value)
    if not value.endswith('.apk'):
        raise ValidationError('.apk 파일 경로를 입력하세요.')


def web_url_field(label, **kwargs):
    return forms.URLField(label=label, assume_scheme='https', validators=[validate_web_url], **kwargs)


class TargetForm(forms.ModelForm):
    """모든 종류에 공통인 칸. 종류별 칸은 아래 클래스에서 추가한다."""

    config_fields = ()  # 이 이름의 칸들을 config JSON에 담는다.

    class Meta:
        model = Target
        fields = ['name', 'environment']

    def clean_name(self):
        name = self.cleaned_data['name']
        # project는 폼 칸이 아니어서 유니크 제약을 Django가 미리 검사하지 않는다.
        if Target.objects.filter(project=self.instance.project, name=name).exists():
            raise ValidationError('이 프로젝트에 같은 이름의 대상이 이미 있습니다.')
        return name

    def save(self, commit=True):
        self.instance.config = {
            field: self.cleaned_data[field]
            for field in self.config_fields
            if self.cleaned_data[field]
        }
        return super().save(commit)


class RepoTargetForm(TargetForm):
    config_fields = ('path',)

    path = forms.CharField(label='저장소 경로', max_length=500, validators=[validate_absolute_path])


class DomainTargetForm(TargetForm):
    config_fields = ('url',)

    url = web_url_field('주소')


class ApiTargetForm(TargetForm):
    config_fields = ('base_url', 'swagger_url', 'login_path', 'token_location')

    base_url = web_url_field('API 기본 주소')
    swagger_url = web_url_field('Swagger 문서 주소', required=False)
    login_path = forms.CharField(
        label='로그인 경로',
        max_length=200,
        required=False,
        validators=[RegexValidator(r'^/', '/로 시작하는 경로를 입력하세요.')],
    )
    token_location = forms.ChoiceField(
        label='토큰 위치',
        choices=[('header', 'Authorization 헤더'), ('cookie', '쿠키')],
    )


class ApkTargetForm(TargetForm):
    config_fields = ('path',)

    path = forms.CharField(label='APK 파일 경로', max_length=500, validators=[validate_apk_path])


class CloudTargetForm(TargetForm):
    config_fields = ('account_id', 'region')

    account_id = forms.CharField(
        label='AWS 계정 번호',
        validators=[RegexValidator(r'^\d{12}$', '12자리 숫자를 입력하세요.')],
    )
    region = forms.CharField(
        label='리전',
        validators=[RegexValidator(r'^[a-z]{2}(-[a-z]+)+-\d+$', '예: ap-northeast-2')],
    )


TARGET_FORMS = {
    Target.Kind.REPO: RepoTargetForm,
    Target.Kind.DOMAIN: DomainTargetForm,
    Target.Kind.API: ApiTargetForm,
    Target.Kind.APK: ApkTargetForm,
    Target.Kind.CLOUD: CloudTargetForm,
}
