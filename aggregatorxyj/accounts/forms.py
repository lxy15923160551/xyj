from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AggregatorUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AggregatorUser
        fields = ('real_name',) + UserCreationForm.Meta.fields


