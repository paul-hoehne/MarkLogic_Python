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


def validate_stemmed_searches_type(raw_val):
    valid_types = {'off', 'basic', 'advanced', 'decompounding'}

    if raw_val not in valid_types:
        raise ValidationError("Stemmed search type is not a valid type of stemmed search", repr(raw_val))


def validate_integer_range(raw_val, min, max):
    if raw_val not in range(min, (1 + max)):
        raise ValidationError("Integer value out of range", repr(raw_val))


def validate_directory_creation(raw_val):
    if raw_val not in ['manual', 'automatic', 'manual-enforced']:
        raise ValidationError("Invalid directory creation method", repr(raw_val))


def validate_locking_type(raw_val):
    if raw_val not in ['strict', 'fast', 'off']:
        raise ValidationError("Invalid locking option", repr(raw_val))


def validate_range_index_optimize_options(raw_val):
    if raw_val not in ['facet-time', 'memory-size']:
        raise ValidationError("Range index optimize option is not a valid value", repr(raw_val))


def validate_format_compatibility_options(raw_val):
    if raw_val not in ['5.0', '4.2', '4.1', '4.0', '3.2']:
        raise ValidationError("On disk index format comatibility objest is not a valide value", repr(raw_val))


def validate_index_detection_options(raw_val):
    if raw_val not in ['automatic', 'none']:
        raise ValidationError("Index detection options is not a valid value", repr(raw_val))


def validate_expunge_locks_options(raw_val):
    if raw_val not in ['automatic', 'none']:
        raise ValidationError("Expunge locks option is not a valid value", repr(raw_val))


def validate_term_frequency_normalization_options(raw_val):
    if raw_val not in ['unscaled-log', 'weakest-scaled-log', 'weakly-scaled-log', 'moderately-scaled-log',
                      'strongly-scaled-log', 'scaled-log']:
        raise ValidationError("Term frequency normalization option is not a valid value", repr(raw_val))


def validate_merge_priority_options(raw_val):
    if raw_val not in ['lower', 'normal']:
        raise ValidationError("Merge priority option is not a valid value", repr(raw_val))


def validate_assignment_policy_options(raw_val):
    if raw_val not in ['bucket', 'statistical', 'range', 'legacy']:
        raise ValidationError("Assignment policy option is not a valid value", repr(raw_val))