from typing import Union

from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from . import Player
from ..base import PlayerEnergy

__all__ = ('PlayerLevelSettings',)


class PlayerLevelSettings(PlayerEnergy):
    """
    Player level description.
    """

    player = models.OneToOneField(
        Player, on_delete=models.CASCADE, related_name='energy_state', verbose_name=_('Player'), editable=False,
    )

    def get_recovered_energy(self) -> Union[int, float]:
        # Basic energy recover logic
        # Method can be overridden.

        if self.start_at > self.stop_at:
            # current_time = timezone.now()

            energy_recovery_time = self._validated_energy_recovery_time()

            # doesn't work ->
            seconds_count = (
                                    self.player.last_energy_update - self.start_at
                            ).total_seconds() - (
                                    self.start_at - self.stop_at
                            ).total_seconds()
            total_recover_energy = energy_recovery_time * seconds_count + self.player.energy
            # <---------------

            if total_recover_energy > self.base_energy:
                return self.base_energy

            return total_recover_energy

        return self.player.energy

    @transaction.atomic
    def save(self, *args, **kwargs):
        save_time = timezone.now()

        if self.state in self.get_paused_state():
            self.stop_at = save_time
        else:
            self.start_at = save_time
            player_energy = self.get_recovered_energy()
            self.player.energy = player_energy
            self.player.save()

        return super().save()

    def __str__(self):
        some_player_level = 10  # or some logic, for example method or property

        return 'Player %s | Level %s' % (self.player.username, some_player_level)

    class Meta:
        verbose_name = _('Player level settings')
        verbose_name_plural = _('Players level settings')
        ordering = ('id',)


@receiver(post_save, sender=Player, dispatch_uid="create_player_level_settings")
def create_player_level_settings(sender, instance, created, **kwargs):
    if created:
        PlayerLevelSettings.objects.create(player=instance)
