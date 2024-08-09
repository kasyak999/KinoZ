from django.core.exceptions import ValidationError
from .models import FilmsdModel


def erorr_id_kp(value) -> None:
    result = FilmsdModel.objects.filter(id_kp=value).count()
    print(result)
    # if result:
    #     raise ValidationError(
    #         'Уже есть в базе'
    #     )
