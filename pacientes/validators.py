from django.core.validators import RegexValidator

nns_validador = RegexValidator(
    regex = '^(\d{2})(\d{2})(\d{2})\d{5}$',
    message = 'El numero de seguridad social no es valido',
    code = 'nss_invalido'
)


