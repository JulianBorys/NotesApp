from django.core.exceptions import ValidationError

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError("Hasło musi zawierać co najmniej jedną cyfrę.")
        if not any(char.isupper() for char in password):
            raise ValidationError("Hasło musi zawierać co najmniej jedną wielką literę.")
        if not any(char.islower() for char in password):
            raise ValidationError("Hasło musi zawierać co najmniej jedną małą literę.")
        if len(password) < 8:
            raise ValidationError("Hasło musi mieć co najmniej 8 znaków.")

    def get_help_text(self):
        return (
            "Hasło musi zawierać co najmniej jedną cyfrę, jedną wielką literę, "
            "jedną małą literę i składać się z co najmniej 8 znaków."
        )
