from django.contrib.auth.models import Group


def save_group(backend, user, response, *args, **kwargs):
    """Map keycloak groups to django groups and add the user to them."""
    if backend.name == "keycloak":
        keycloak_groups = response.get("keycloak_groups")
        if not keycloak_groups:
            return

        if not isinstance(keycloak_groups, list):
            return

        current_groups = user.groups.all()
        current_groups_name = [group.name for group in current_groups]
        for keycloak_group in keycloak_groups:
            if keycloak_group.lower() in current_groups_name:
                continue
            group = Group.objects.create(name=keycloak_group.lower())
            user.groups.add(group)
            user.save()
