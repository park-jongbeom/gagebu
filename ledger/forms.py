from django import forms
from ledger.models import 내역

class 내역폼(forms.ModelForm):
    class Meta:
        model = 내역
        fields = ["날짜", "분류", "항목", "금액", "이름", "계좌"]