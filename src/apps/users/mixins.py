from django.contrib.auth.mixins import AccessMixin
from django.http import HttpRequest
from django.db.models import Model, ForeignKey

from .models import User


class UpdatePermissionMixin(AccessMixin):
    error_message_403 = "You doesn't have permissions for the operation"

    def get_permission_denied_message(self):
        """
        Override this method to override the permission_denied_message attribute.
        """
        return self.error_message_403

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        current_user: User = request.user
        obj: Model = self.get_object()

        # obj is instance User class
        if isinstance(obj, User):
            if current_user.slug != obj.slug:
                self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)

        # search related user model
        user_related_model = (
            user[0]
            if (
                user := [
                    related
                    for related in obj._meta.fields
                    if isinstance(related, ForeignKey) and related.related_model == User
                ]
            )
            else None
        )

        # if obj from requet doesn't relate with User - return
        if not user_related_model:
            return

        user_field_name = user_related_model.name

        # get user pk of user that related to obj from request
        user_pk = (
            obj.__class__.objects.filter(**{user_field_name: current_user})
            .values_list(user_field_name + "__pk")
            .first()
        )

        if not user_pk:
            self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
