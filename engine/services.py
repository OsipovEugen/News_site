# likes/services.py
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Like
User = get_user_model()
def add_like(obj, user):
    """Лайкает `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    return like