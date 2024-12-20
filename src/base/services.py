from django.core.exceptions import ValidationError


def get_path_upload_avatar(instance, file):
    """ Построение пути к файлу, format: (media)/avatar/user_id/photo.jpg
    """
    return f'avatar/user_{instance.id}/{file}'


def get_path_upload_cover_album(instance, file):
    """ Построение пути к файлу, format: (media)/album/user_id/photo.jpg
    """
    return f'album/user_{instance.user.id}/{file}'


def get_path_upload_cover_playlist(instance, file):
    """ Построение пути к файлу, format: (media)/playlist/user_id/photo.jpg
    """
    return f'playlist/user_{instance.user.id}/{file}'


def get_path_upload_track(instance, file):
    """ Построение пути к файлу, format: (media)/track/user_id/audio.pm3
    """
    return f'track/user_{instance.user.id}/{file}'


def get_path_upload_cover_track(instance, file):
    """ Построение пути к файлу, format: (media)/track/cover/user_id/photo.jpg
    """
    return f'track/cover/user_{instance.user.id}/{file}'


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
