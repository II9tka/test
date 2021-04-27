from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver

__all__ = ('Player',)


class Player(AbstractUser):
    """
    Player model.
    """

    energy = models.PositiveIntegerField(
        blank=True, default=0, verbose_name=_('Energy')
    )
    prev_energy = models.PositiveIntegerField(
        blank=True, default=0, verbose_name=_('Prev energy')
    )
    last_energy_update = models.DateTimeField(
        blank=True, null=True, editable=False, verbose_name=_('Last energy update')
    )
    experience = models.PositiveIntegerField(
        blank=True, default=0, verbose_name=_('Experience')
    )

    class Meta:
        verbose_name = _('Player')
        verbose_name_plural = _('Players')
        ordering = ('id',)


@receiver(post_save, sender=Player, dispatch_uid="set_player_prev_energy")
def set_player_prev_energy(sender, instance, **kwargs):
    if instance.energy != instance.prev_energy:
        instance.prev_energy = instance.energy
        instance.last_energy_update = timezone.now()
