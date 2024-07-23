from allauth.account.adapter import DefaultAccountAdapter
import re
from django.forms import ValidationError


class CustomAccountAdapter(DefaultAccountAdapter):
    def clean_password(self, password, user=None):
        # 8~20 자, 영문 숫자 특수기호 조합
        if re.match(r'^(?=.*[a-zA-Z])(?=.*[@$!%*#?&])(?=.*[0-9]).{8,20}$', password):
            return password
        else:
            raise ValidationError(
                "비밀번호는 8~20자로 영문과 숫자, 특수문자를 반드시 포함해야 합니다.")
