# Generated to migrate legacy users to django-allauth email model.

from django.db import migrations
from django.db.models import Count


def forwards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    EmailAddress = apps.get_model('account', 'EmailAddress')

    dupes = (
        User.objects.exclude(email__isnull=True)
        .exclude(email__exact='')
        .values('email')
        .annotate(c=Count('id'))
        .filter(c__gt=1)
    )
    if dupes.exists():
        examples = list(dupes[:20])
        raise RuntimeError(
            'Duplicate emails found in auth_user; cannot safely migrate to allauth. '
            f'Examples (up to 20): {examples}'
        )

    qs = User.objects.exclude(email__isnull=True).exclude(email__exact='')

    for user in qs.iterator():
        email = (user.email or '').strip()
        if not email:
            continue

        obj, created = EmailAddress.objects.get_or_create(
            user_id=user.pk,
            email=email,
            defaults={
                'primary': True,
                'verified': bool(getattr(user, 'is_active', True)),
            },
        )

        if not created:
            update_fields = []
            if not obj.primary:
                obj.primary = True
                update_fields.append('primary')
            if getattr(user, 'is_active', True) and not obj.verified:
                obj.verified = True
                update_fields.append('verified')
            if update_fields:
                obj.save(update_fields=update_fields)


def backwards(apps, schema_editor):
    # Intentionally irreversible.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_delete_actionevent'),
        # django-allauth 65.14.1
        ('account', '0009_emailaddress_unique_primary_email'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
