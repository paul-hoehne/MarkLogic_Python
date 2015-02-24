__author__ = 'phoehne'


class ElementRange:
    def __init__(self, localname, scalar_type=u'string', namespace_uri=None, collation=None,
                 range_value_positions=False, invalid_values=u'reject'):
        self.config = {
            u"scalar-type": scalar_type,
            u'namespace-uri': '',
            u"localname": localname,
            u'collation': u'',
            u"range-value-positions": range_value_positions,
            u"invalid-values": invalid_values
        }
        if namespace_uri:
            self.config[u'namespace-uri'] = namespace_uri
        if collation:
            self.config[u'collation'] = collation


class RangeElementAttribute:
    def __init__(self, element_name, attribute_name, scalar_type=u'string', element_namespace=None,
                 attribute_namespace=None, collation=None, range_value_positions=False, invalid_values=u'reject'):
        self.config = {
            u"scalar-type": scalar_type,
            u'collation': u'',
            u'parent-namespace-uri': u'',
            u"parent-localname": element_name,
            u'namespace-uri': u'',
            u"localname": attribute_name,
            u"range-value-positions": range_value_positions,
            u"invalid-values": invalid_values
        }

        if collation:
            self.config[u'collation'] = collation
        if element_namespace:
            self.config[u'parent-namespace-uri'] = element_namespace
        if attribute_namespace:
            self.config[u'namespace-uri'] = attribute_namespace