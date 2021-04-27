from typing import Union, List

from django.db import models
from django.utils.translation import gettext_lazy as _

from enumfields import EnumIntegerField

from .constants import DEFAULT_ENERGY_RECOVERY, DEFAULT_BASE_ENERGY
from .enum import PlayerState


class PlayerEnergy(models.Model):
    # The recovery time of the energy described in the "energy_recovery" method
    default_energy_recovery_time = 1  # 1 sec

    _energy_recovery = models.IntegerField(
        blank=True, null=True, verbose_name=_('Energy recovery'), db_column='energy_recovery'
    )
    _base_energy = models.IntegerField(
        blank=True, null=True, verbose_name=_('Base energy'), db_column='base_energy'
    )
    stop_at = models.DateTimeField(
        blank=True, null=True, editable=False, verbose_name=_('Stop at')
    )
    start_at = models.DateTimeField(
        blank=True, null=True, editable=False, verbose_name=_('Start at')
    )
    state = EnumIntegerField(
        PlayerState, default=PlayerState.IN_MENU, help_text=_(
            'Player game status.'
        ), verbose_name=_('State'), db_index=True
    )

    # and some fields...

    @staticmethod
    def get_paused_state() -> List[PlayerState]:
        # Method can be overridden.

        return [PlayerState.IN_PAUSE, PlayerState.IN_MENU]

    def _validated_energy_recovery_time(self) -> Union[int, float]:
        energy_recovery_time = self.get_energy_recovery_time()

        assert energy_recovery_time, (
            '"energy_recovery_time" must be implemented.'
        )
        if isinstance(energy_recovery_time, (int, float)):
            return energy_recovery_time
        raise TypeError(
            '"energy_recovery_time" must be integer or float.'
        )

    def get_energy_recovery_time(self) -> Union[int, float]:
        # Method can be overridden.

        return self.default_energy_recovery_time

    @property
    def energy_recovery(self) -> int:
        # some logic or this ->

        return self._energy_recovery if self._energy_recovery else DEFAULT_ENERGY_RECOVERY

    @property
    def base_energy(self) -> int:
        # some logic or this ->

        return self._base_energy if self._base_energy else DEFAULT_BASE_ENERGY

    @base_energy.setter
    def base_energy(self, value: int) -> None:
        self._base_energy = value

    @energy_recovery.setter
    def energy_recovery(self, value: int) -> None:
        self._energy_recovery = value

    class Meta:
        abstract = True
