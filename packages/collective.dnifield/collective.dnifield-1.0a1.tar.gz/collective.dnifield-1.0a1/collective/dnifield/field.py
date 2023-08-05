import re

from zope.schema import TextLine
from zope.schema.interfaces import ValidationError

from collective.dnifield import _

KEY = 'TRWAGMYFPDXBNJZSQVHLCKE'


class WrongFormat(ValidationError):
    __doc__ = _("The entered value has a wrong format.")

class WrongLetter(ValidationError):
    __doc__ = _("The entered control letter doesn't match.")

class DNI(TextLine):
    """A field to enter a Spanish DNI.

    If an ending letter is provided, it will be validated against the
    entered number.
    """

    max_length = 9  # 8 digits + 1 letter = 9 chars

    def validate(self, value):
        """
        >>> dni = DNI()

        DNIs with a wrong format don't validate:
        >>> bad_formed = 'h4x0r'
        >>> dni.validate(bad_formed)
        Traceback (most recent call last):
        ...
        WrongFormat

        DNIs with the wrong letter don't validate:
        >>> bad_letter = '5892138Y'
        >>> dni.validate(bad_letter)
        Traceback (most recent call last):
        ...
        WrongLetter

        DNIs with the correct letter do validate:
        >>> good_w_letter = '0000000T'
        >>> dni.validate(good_w_letter)

        DNIs without letter but with a correct format do validate:
        >>> good_wo_letter = '0000000'
        >>> dni.validate(good_wo_letter)
        """
        match = re.match('^(\d{7,8})([A-z])?$', value) 
        if not match:
            raise WrongFormat

        number = int(match.group(1))
        letter = match.group(2)
        if letter and not KEY[number%23] == letter:
                raise WrongLetter
