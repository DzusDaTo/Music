from django.core.exceptions import ValidationError


def get_path_upload_avatar(instance, file):
    """
    Построение пути к файлу, format: (media)/avatar/user_id/photo.jpeg
    """
    if not instance.id:
        raise ValidationError("Пользователь должен быть сохранен перед загрузкой аватара.")
    return f'avatar/{instance.id}/{file}'


def validate_size_image(file_obj):
    """
    Проверка размера файла и дополнительных условий (например, допустимые форматы).
    """
    allowed_extensions = ['.jpeg', '.jpg', '.png']
    extension = file_obj.name.split('.')[-1].lower()
    if f'.{extension}' not in allowed_extensions:
        raise ValidationError(f"Неподдерживаемый формат файла. Допустимые форматы: {', '.join(allowed_extensions)}")

    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла {megabyte_limit}MB.')
