from django.utils.translation import gettext_lazy as _

from enumfields import Enum

__all__ = ('PlayerState',)


class PlayerState(Enum):
    IN_PAUSE = 1
    IN_MENU = 2

    IN_GAME = 0

    class Labels:
        IN_MENU = _('In menu')
        IN_PAUSE = _('In pause')
        IN_GAME = _('In game')
