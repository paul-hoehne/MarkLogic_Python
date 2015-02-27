class ValidationError(Exception):
    def __init__(self, message, original_value):
        self._message = message
        self._original_value = original_value

    def __repr__(self):
        "Validation Error('{0}', {1})".format(self._message, self._original_value)


def validate_boolean(raw_val):
    if type(raw_val) != bool:
        raise ValidationError('Value passed is not a boolean', repr(raw_val))


def validate_index_type(raw_val):
    valid_index_types = {"int", "unsignedInt", "long", "unsignedLong", "float", "double", "decimal", "dateTime",
                         "time", "date",  "gYearMonth", "gYear", "gMonth", "gDay", "yearMonthDuration",
                         "dayTimeDuration", "string", "anyURI"}
    if raw_val not in valid_index_types:
        raise ValidationError('Value is not a valid index type', repr(raw_val))


def validate_index_invalid_value_actions(raw_val):
    valid_actions = {'ignore', 'reject'}

    if raw_val not in valid_actions:
        raise ValidationError("Value is not a valid action for invalid index values", repr(raw_val))