from marshmallow import fields


class ValueEnum(fields.Enum):
    """Serializes an Enum member by its *name*.

    The previous marshmallow_enum based version tried to switch to by-value after
    __init__, which had no effect, so the API has always returned names (e.g. 'APPLIED').
    """
