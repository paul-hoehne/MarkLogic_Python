#
# Copyright 2015 MarkLogic Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0#
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# File History
# ------------
#
# Paul Hoehne       03/01/2015     Initial development
# Paul Hoehne       03/08/2014     Added support for field indexes


import requests
import json
from .forest import Forest
from .utilities import files
from .utilities.validators import *

from .index import ElementAttributeRange, ElementRange, FieldRange

"""
Database related classes for manipulating MarkLogic databases
"""

class Database:
    """
    The Database class encapsulates a MarkLogic database.  It provides
    methods to set/get database attributes.  The use of methods will
    allow IDEs with tooling to provide auto-completion hints.
    """
    def __init__(self, name, hostname=None):
        """
        Initialize the database object to either create a database or
        lookup the existing database information

        :param name: The database name
        :return: The database object with default data
        """
        self.config = {
            u'database-name': name,
            u'forest': [
                name + u'-Forest-001'
            ],
            u'security-database': u'Security',
            u'schema-database': u'Schemas',
            u'enabled': True,
            u'language': u'en'
        }

        if hostname is not None:
            self.hostname = hostname

    def set_database_name(self, name):
        """
        Sets the database name

        :param name: A valid database name
        :return: The database object
        """
        self.config[u'database-name'] = name
        return self

    def database_name(self):
        """
        Returns the database name

        :return: The database object
        """
        return self.config[u'database-name']

    def set_enabled(self, enabled=True):
        """
        Set the flag to enable or disable a database.

        :param enabled: The enable status
        :return: the database object
        """
        validate_boolean(enabled)
        self.config[u'enabled'] = enabled
        return self

    def enabled(self):
        """
        Returns the enable status

        :return: The database enable status
        """
        return self.config[u'enabled']

    def set_security_database(self, db=u'Security'):
        """
        Set the name of the security database for this database

        :param db: The name of the security database
        :return: The database object
        """
        self.config[u'security-database'] = db
        return self

    def security_database(self):
        """
        Returns the name of the security database for this database

        :return: The security database name
        """
        return self.config[u'security-database']

    def set_triggers_database(self, db=u'Triggers'):
        """
        Set the name of the triggers database associated with this database

        :param db: The name of the triggers database
        :return: The database object
        """
        self.config[u'triggers-database'] = db
        return self

    def triggers_database(self):
        """
        Return the name of the triggers database associted with this database.

        :return: The name of the triggers database
        """
        return self.config[u'triggers-database']

    def add_forest(self, forest):
        """
        Add a new forest name to the database.  The forest with that name
        will be created when the database is created.

        :param forest: The forest name
        :return: The database object
        """
        if not self.config[u'forest']:
            self.config[u'forest'] = []

        self.config[u'forest'].append(forest)

        return self

    def forests(self):
        """
        Return the forests associated with this database

        :return: The associated forests
        """
        return self.config[u'forest']

    def set_language(self, language):
        """
        Set the default language for the database.  By default the default language is
        'en.'

        :param language: The language abbreviation
        :return: The database object
        """
        self.config[u'language'] = language
        return self

    def language(self):
        """
        Returns the default language for the database.

        :return: The default language for the database.
        """
        return self.config[u'language']

    def set_stemmed_searches(self, which=u'basic'):
        """
        Set the stemmed search option for the database.  Valid values are 'off',
        'basic', 'advanced' and 'decompounding'.

        :param which: The stemmed search option
        :return: The database object
        """
        validate_stemmed_searches_type(which)
        self.config[u'stemmed-searches'] = which
        return self

    def stemmed_searches(self):
        """
        Returns the stemmed search option

        :return: The type of stemmed search
        """
        return self.config[u'stemmed-searches']

    def set_word_searches(self, enabled=False):
        """
        Enables stemmed word searches

        :param enabled: Enable stemmed word searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'word-searches'] = enabled
        return self

    def word_searches(self):
        """
        Returns if stemmed word searches are enabled

        :return: Stemmed word searches enabled
        """
        return self.config[u'word-searches']

    def set_word_positions(self, enabled=False):
        """
        Enable word positions for faster phrase or 'near' searching

        :param enabled: Enable searching on word positions
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'word-positions'] = enabled
        return self

    def word_positions(self):
        """
        Returns if word positions are enabled.

        :return: Word positions are enabled
        """
        return self.config[u'word-positions']

    def set_fast_phrase_searches(self, enabled=True):
        """
        Enable fast phrase searching.

        :param enabled:  Enable faster phrase searching
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'fast-phrase-searches'] = enabled
        return self

    def fast_phrase_searches(self):
        """
        Returns if fast phrase searches are enabled.

        :return: Fast phrase searches enabled
        """
        return self.config[u'fast-phrase-searches']

    def set_fast_reverse_searches(self, enabled=True):
        """
        Enable fast revrese searches

        :param enabled: Faster reverse searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'fast-reverse-searches'] = enabled
        return self

    def fast_reverse_searches(self):
        """
        Returns if fast reverse searches are enabled

        :return: Fast reverse searches enabled
        """
        return self.config[u'fast-reverse-searches']

    def set_triple_index(self, enabled=False):
        """
        Enables the triple index for semantic queries

        :param enabled: Enable the triple index
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'triple-index'] = enabled
        return self

    def triple_index(self):
        """
        Returns if the triple index is enabled

        :return: The triple index enabled
        """
        return self.config[u'triple-index']

    def set_triple_positions(self, enabled=False):
        """
        Enable triple positions for faster near searches with triple range queries

        :param enabled: Enable triple positions
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'triple-positions'] = enabled
        return self

    def triple_positions(self):
        """
        The status of triple positions

        :return: Triple positions enabled
        """
        return self.config[u'triple-positions']

    def set_fast_case_senstive_searches(self, enabled=True):
        """
        Enable faster case sensitive searches

        :param enabled: Enable faster case sensitive searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'fast-case-sensitive-searches'] = enabled
        return self

    def fast_cast_sensitive_searches(self):
        """
        The status of case sensitive searches

        :return: Fast case sensitive searches enabled
        """
        return self.config[u'fast-case-sensitive-searches']

    def set_fast_diacritic_sensitive_searches(self, enabled=True):
        """
        Enable fast diacritic sensitive searches

        :param enabled: Fast diacritic sensitive searches enabled.
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'fast-diacritic-sensitive-searches'] = enabled
        return self

    def fast_diacritic_sensitive_searches(self):
        """
        The status of fast diacritic sensitive searches

        :return: Fast diacritic sensitive searches enabled
        """
        return self.config[u'fast-diacritic-sensitive-searches']

    def set_fast_element_word_searches(self, enabled=True):
        """
        Enable faster element word searches

        :param enabled: Enable fast element word searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'fast-element-word-searches'] = enabled
        return self

    def fast_element_word_searches(self):
        """
        Status of fast element word searches

        :return: Fast element word searches enabled
        """
        return self.config[u'fast-element-word-searches']

    def set_element_word_positions(self, enabled=False):
        """
        Enable faster element phrase searches and near searches.

        :param enabled: Enable element word positions
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'element-word-positions'] = enabled
        return self

    def element_word_positions(self):
        """
        Status of element word positions

        :return: Fast element word searches enabled
        """
        return self.config[u'element-word-positions']

    def set_fast_element_phrase_searches(self, enabled=True):
        """
        Enable faster phrase searches

        :param enabled: Enable fast element phrase searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'fast-element-phrase-searches'] = enabled
        return self

    def fast_element_phrase_searches(self):
        """
        Status of fast element phrase searches

        :return: Fast element phrase searches enabled
        """
        return self.config[u'fast-element-phrase-searches']

    def set_element_value_positions(self, enabled=False):
        """
        Enable element faster searches for faster near searches with element values

        :param enabled: Enable element value positions
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'element-value-positions'] = enabled
        return self

    def element_value_positions(self):
        """
        Status of element value positions

        :return: Element value positions enabled
        """
        return self.config[u'element-value-positions']

    def set_attribute_value_positions(self, enabled=False):
        """
        Index attribute value positions for faster near searches involving element-attribute-value-query

        :param enabled: Attribute value positions
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'attribute-value-positions'] = enabled
        return self

    def attribute_value_positions(self):
        """
        Status of attribute value positions

        :return: Attribute value positions enabled
        """
        return self.config[u'attribute-value-positions']

    def set_field_value_searches(self, enabled=False):
        """
        Index field values for faster searches involving field-value-query

        :param enabled: Field value searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'field-value-searches'] = enabled
        return self

    def field_value_searches(self):
        """
        Status of field value searches

        :return: Field value searches enabled
        """
        return self.config[u'field-value-searches']

    def set_field_value_positions(self, enabled=False):
        """
        Index field value positions for faster near searches involving field-value-query

        :param enabled: Field value positions
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'field-value-positions'] = enabled
        return self

    def field_value_positions(self):
        """
        Status of field value positions

        :return: Field value positions enabled
        """
        return self.config[u'field-value-positions']

    def set_three_character_searches(self, enabled=False):
        """
        Enable wildcard searches and faster character-based XQuery predicates using three or more characters

        :param enabled: Three character wildcard searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'three-character-searches'] = enabled
        return self

    def three_character_searches(self):
        """
        Status of three character wildcard searches

        :return: Three character searches enabled
        """
        return self.config[u'three-character-searches']

    def set_three_character_word_positions(self, enabled=False):
        """
        Index word positions for three-character searches only when three-character-searches are enabled

        :param enabled: Three character word positions
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'three-character-word-positions'] = enabled
        return self

    def three_character_word_positions(self):
        """
        Status of word positions where three character searches are enabled

        :return: Three character word positions enabled
        """
        return self.config[u'three-character-word-positions']

    def set_fast_element_character_searches(self, enabled=False):
        """
        Enable element wildcard searches and element-character-based XQuery predicates

        :param enabled: Fast element character searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'fast-element-character-searches'] = enabled
        return self

    def fast_element_character_searches(self):
        """
        Status of fast element character searches

        :return: Fast element character searches
        """
        return self.config[u'fast-element-character-searches']

    def set_trailing_wildcard_searches(self, enabled=False):
        """
        Enable trailing wildcard searches

        :param enabled: Wild card searches enabled
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'trailing-wildcard-searches'] = enabled
        return self

    def trailing_wildcard_searches(self):
        """
        Status of trailing wildcard searches

        :return: Trailing wild card searches enabled
        """
        return self.config[u'trailing-wildcard-searches']

    def set_trailing_wildcard_word_positions(self, enabled=False):
        """
        Index word positions for trailing-wildcard searches only when trailing-wildcard-searches are enabled

        :param enabled: Index word positions for trailing wildcard searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'trailing-wildcard-word-positions'] = enabled
        return self

    def trailing_wildcard_word_positions(self):
        """
        Index word positions for trailing-wildcard searches

        :return: Index word positions enabled
        """
        return self.config[u'trailing-wildcard-word-positions']

    def set_fast_element_trailing_wildcard_searches(self, enabled=False):
        """
        Enable element trailing wildcard searches

        :param enabled: Enable trailing wildcard searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'fast-element-trailing-wildcard-searches'] = enabled
        return self

    def fast_element_trailing_wildcard_searches(self):
        """
        Fast element trailing wildcard searches

        :return: Fast element trailing wildcard searches enabled
        """
        return self.config[u'fast-element-trailing-wildcard-searches']

    def set_two_character_searches(self, enabled=False):
        """
        Enable wildcard searches and faster character-based XQuery predicates using two character

        :param enabled: Enable two character wildcard searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'two-character-searches'] = enabled
        return self

    def two_character_searches(self):
        """
        Two character wild card searches

        :return: Two character wildcard searches enabled
        """
        return self.config[u'two-character-searches']

    def set_one_character_searches(self, enabled=False):
        """
        Enable wildcard searches and faster character-based XQuery predicates using one character

        :param enabled: Enable one character wildcard searches
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'one-character-searches'] = enabled
        return self

    def one_character_searches(self):
        """
        One character wildcard searches

        :return: One character wildcard searches enabled
        """
        return self.config[u'one-character-searches']

    def set_uri_lexicon(self, enabled=True):
        """
        Maintain a lexicon of document URIs

        :param enabled: Enable URI lexicon
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'uri-lexicon'] = enabled
        return self

    def uri_lexicon(self):
        """
        URI lexicon enabled

        :return: URI lexicon enabled
        """
        return self.config[u'uri-lexicon']

    def set_collection_lexicon(self, enabled=False):
        """
        Maintain a lexicon of collection URIs

        :param enabled: Enable collection URI lexicon
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'collection-lexicon'] = enabled
        return self

    def collection_lexicon(self):
        """
        Collection lexicon enabled

        :return: Collection lexicon enabled
        """
        return self.config[u'collection-lexicon']

    def set_reindexer_enable(self, enabled=True):
        """
        Enable automatic reindexing after configuration changes.

        :param enabled:
        :return:
        """
        validate_boolean(enabled)
        self.config[u'reindexer-enable'] = enabled
        return self

    def reindexer_enable(self):
        """
        Automatic reindexing after configuration changes enabled

        :return: Automatic reindexing enabled
        """
        return self.config[u'reindexer-enable']

    def set_reindexer_throttle(self, limit=5):
        """
        Set the level of system resources allocated to reindexing

        :param limit: The level of system resources
        :return: The database object
        """
        validate_integer_range(limit, 1, 5)
        self.config[u'reindexer-throttle'] = limit
        return self

    def reindexer_throttle(self):
        """
        The level of system resources for indexing

        :return: The level of system resources
        """
        return self.config[u'reindexer-throttle']

    def set_reindexer_timestamp(self, limit=0):
        """
        Set the timestamp above which document fragments will be re-indexed in milliseconds

        :param limit: Reindexer timestamp
        :return: The document object
        """
        self.config[u'reindexer-timestamp'] = limit
        return self

    def reindexer_timestamp(self):
        """
        The current reindexer timestamp

        :return: Reindexer timestamp in milliseconds
        """
        return self.config[u'reindexer-timestamp']

    def set_directory_creation(self, which=u'manual'):
        """
        Directory creation method

        :param which: The method of directory configuration
        :return: The database object
        """
        validate_directory_creation(which)
        self.config[u'directory-creation'] = which
        return self

    def directory_creation(self):
        """
        The directory creation method

        :return: Directory creation method
        """
        return self.config[u'directory-creation']

    def set_maintain_last_modified(self, enabled=False):
        """
        Maintain last-modified properties of documents

        :param enabled: Maintain last-modified
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'maintain-last-modified'] = enabled
        return self

    def maintain_last_modified(self):
        """
        Maintain last-modified properties of documents

        :return: Maintain last modified
        """
        return self.config[u'maintain-last-modified']

    def set_maintain_directory_last_modified(self, enabled=False):
        """
        Maintain last-modified properties of directories

        :param enabled: Maintain last-modified
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'maintain-directory-last-modified'] = enabled
        return self

    def maintain_directory_last_modified(self):
        """
        Maintain last modified properties of directories

        :return: Maintain directory last modified property enabled
        """
        return self.config[u'maintain-directory-last-modified']

    def set_inherit_permissions(self, enabled=False):
        """
        New document default permissions include parent directory

        :param enabled: Inherit document permissions from parent
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'inherit-permissions'] = enabled
        return self

    def inherit_permissions(self):
        """
        New document default permissions include parent directory

        :return: Inherit document permissions from parent enabled
        """
        return self.config[u'inherit-permissions']

    def set_inherit_collections(self, enabled=False):
        """
        New document default collections include parent directory collections.

        :param enabled: Inherit collection from parent directory
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'inherit-collections'] = enabled
        return self

    def inherit_collections(self):
        """
        New document default collections include parent directory collections.

        :return: Inherit default collections enabled
        """
        return self.config[u'inherit-collections']

    def set_inherit_quality(self, enabled=False):
        """
        New document default quality is inherited parent directory quality.

        :param enabled: Inherit parent directory quality
        :return: The database object
        """
        validate_boolean(enabled)
        self.config[u'inherit-quality'] = enabled
        return self

    def inherit_quality(self):
        """
        New document default quality is inherited parent directory quality.

        :return: Inherity document quality
        """
        return self.config[u'inherit-quality']

    def set_in_memory_limit(self, limit=262144):
        """
        The maximum number of fragments in an in-memory stand.

        :param limit: In memory fragment limit
        :return: The database object
        """
        self.config[u'in-memory-limit'] = limit
        return self

    def in_memory_limit(self):
        """
        The maximum number of fragments in an in-memory stand.

        :return: In memory fragment limit
        """
        return self.config[u'in-memory-limit']

    def set_in_memory_list_size(self, limit=512):
        """
        Size of the in-memory list storage, in megabytes.

        :param limit: The in memory list storage in megabytes
        :return: The database object
        """
        self.config[u'in-memory-list-size'] = limit
        return self

    def in_memory_list_size(self):
        """
        Size of the in-memory list storage, in megabytes.

        :return: The in memory list storage size in megabytes
        """
        return self.config[u'in-memory-list-size']

    def set_in_memory_tree_size(self, limit=128):
        """
        Size of the in-memory tree storage, in megabytes.

        :param limit: In memory tree storage size
        :return: The database object
        """
        self.config[u'in-memory-tree-size'] = limit
        return self

    def in_memory_tree_size(self):
        """
        Size of the in-memory tree storage, in megabytes.

        :return: In memory tree storage size
        """
        return self.config[u'in-memory-tree-size']

    def set_in_memory_range_index_size(self, limit=16):
        """
        Size of the in-memory range index storage, in megabytes.

        :param limit: The in memory range index size
        :return: The database object
        """
        self.config[u'in-memory-range-index-size'] = limit
        return self

    def in_memory_range_index_size(self):
        """
        Size of the in-memory range index storage, in megabytes.

        :return: The in-memory range index size
        """
        return self.config[u'in-memory-range-index-size']

    def set_in_memory_reverse_index_size(self, limit=16):
        """
        Size of the in-memory reverse index storage, in megabytes.

        :param limit: In memory reverse index size
        :return: The database object
        """
        self.config[u'in-memory-reverse-index-size'] = limit
        return self

    def in_memory_reverse_index_size(self):
        """
        Size of the in-memory reverse index storage, in megabytes.

        :return: In memory reverse index size
        """
        return self.config[u'in-memory-reverse-index-size']

    def set_in_memory_triple_index_size(self, limit=64):
        """
        Size of the in-memory triple index storage, in megabytes.

        :param limit: The in memory triple index size
        :return: The database object
        """
        self.config[u'in-memory-triple-index-size'] = limit
        return self

    def in_memory_triple_index_size(self):
        """
        Size of the in-memory triple index storage, in megabytes.

        :return: In memory triple index size
        """
        return self.config[u'in-memory-triple-index-size']

    def set_large_size_threshold(self, limit=1024):
        """
        Size threshold for large objects, in kilobytes.

        :param limit: Size limit for large objects
        :return: The database object
        """
        self.config[u'large-size-threshold'] = limit
        return self

    def large_size_threshold(self):
        """
        Size threshold for large objects, in kilobytes.

        :return: The large size threshold
        """
        return self.config[u'large-size-threshold']

    def set_locking(self, which=u'fast'):
        """
        Specifies how robust transaction locking should be.

        :param which: The type of transaction logging
        :return: The database object
        """
        validate_locking_type(which)
        self.config[u'locking'] = which
        return self

    def locking(self):
        """
        Specifies how robust transaction locking should be.

        :return: The transaction locking
        """
        return self.config[u'locking']

    def set_journaling(self, which=u'fast'):
        """
        Specifies how robust transaction journaling should be.

        :param which:The type of journaling
        :return:The database object
        """
        validate_locking_type(which)
        self.config[u'journaling'] = which
        return self

    def journaling(self):
        """
        Specifies how robust transaction journaling should be.

        :return:The journaling
        """
        return self.config[u'journaling']

    def set_journal_size(self, limit=682):
        """
        Size of each journal file, in megabytes.

        :param limit: The journal size
        :return:The database object
        """
        self.config[u'journal-size'] = limit
        return self

    def journal_size(self):
        """
        The size of the journal, in megabytes.
        :return:The journal size
        """
        return self.config[u'journal-size']

    def set_journal_count(self, limit=2):
        """
        The journal count

        :param limit:The journal count
        :return:The database object
        """
        self.config[u'journal-count'] = limit
        return self

    def journal_count(self):
        """
        The journal count

        :return:The journal count
        """
        return self.config[u'journal-count']

    def set_preallocate_journal(self, enabled=False):
        """
        Allocate journal files before executing transactions.

        :param enabled:Pre-allocate journal files
        :return:The database object
        """
        validate_boolean(enabled)
        self.config[u'preallocate-journals'] = enabled
        return self

    def preallocate_journal(self):
        """
        Allocate journal files before executing transactions.

        :return:Pre-allocate journal files
        """
        return self.config[u'preallocate-journals']

    def set_preload_mapped_data(self, enabled=False):
        """
        Preload memory mapped forest information while mounting forest.

        :param enabled: Preload memory mapped forest information
        :return:The database object
        """
        validate_boolean(enabled)
        self.config[u'preload-mapped-data'] = enabled
        return self

    def preload_mapped_data(self):
        """
        Preload memory mapped forest information while mounting forest.

        :return:Preload memory mapped forest information
        """
        return self.config[u'preload-mapped-data']

    def set_preload_replica_mapped_data(self, enabled=False):
        """
        Preload memory mapped forest information while mounting replica forest.

        :param enabled:Preload mapped replica forest information
        :return:The database object
        """
        validate_boolean(enabled)
        self.config[u'preload-replica-mapped-data'] = enabled
        return self

    def preload_replica_mapped_data(self):
        """
        Preload memory mapped forest information while mounting replica forest.

        :return:Preload mapped replica forest information
        """
        return self.config[u'preload-replica-mapped-data']

    def set_range_index_optimize(self, which=u'facet-time'):
        """
        Specifies how to optimize range indexes

        :param which:Range index optimization option
        :return:The database object
        """
        validate_range_index_optimize_options(which)
        self.config[u'range-index-optimize'] = which
        return self

    def range_index_optimize(self):
        """
        Specifies how to optimize range indexes

        :return:Range index optimization type
        """
        return self.config[u'range-index-optimize']

    def set_position_list_max_size(self, limit=256):
        """
        Maximum size of a positions-containing list, in megabytes. Lists longer than this have positions discarded

        :param limit:Max position containing list size
        :return:The database object
        """
        self.config[u'positions-list-max-size'] = limit
        return self

    def position_list_max_size(self):
        """
        Maximum size of a positions-containing list, in megabytes. Lists longer than this have positions discarded

        :return:The maximum position containing list size
        """
        return self.config[u'positions-list-max-size']

    def set_format_compatibility(self, which=u'automatic'):
        """
        Version of on-disk forest format.

        :param which:On disk forest format
        :return:The database object
        """
        validate_format_compatibility_options(which)
        self.config[u'format-compatibility'] = which
        return self

    def format_compatibility(self):
        """
        The on-disk forest format

        :return:The on-disk forest format
        """
        return self.config[u'format-compatibility']

    def set_index_detection(self, which=u'automatic'):
        """
        Handling of differences between the current configuration of database indexes and on-disk settings.

        :param which:How to handle differences in configuration settings
        :return:The database object
        """
        validate_index_detection_options(which)
        self.config[u'index-detection'] = which
        return self

    def index_detection(self):
        """
        Handling of differences between the current configuration of database indexes and on-disk settings.

        :return:How to handle differences in configuration settings
        """
        return self.config[u'index-detection']

    def set_expunge_locks(self, which=u'none'):
        """
        Garbage collection of timed locks that have expired.

        :param which:Garbage collect timed locks
        :return:The database object
        """
        validate_expunge_locks_options(which)
        self.config[u'expunge-locks'] = which
        return self

    def expunge_locks(self):
        """
        Garbage collection of timed locks that have expired.

        :return:How to garbage collect timed locks
        """
        return self.config[u'expunge-locks']

    def set_if_normalization(self, which=u'scaled-log'):
        """
        What kind of term frequency normalization to apply.

        :param which: The term frequency normalization
        :return:The database object
        """
        validate_term_frequency_normalization_options(which)
        self.config[u'tf-normalization'] = which
        return self

    def if_normalization(self):
        """
        The kind of term frequency normalization to apply

        :return:The term frequency normalization option
        """
        return self.config[u'tf-normalization']

    def set_merge_priority(self, which=u'lower'):
        """
        The CPU scheduler priority for merges.

        :param which:CPU scheduling hint for merges
        :return:The database object
        """
        validate_merge_priority_options(which)
        self.config[u'merge-priority'] = which
        return self

    def merge_priority(self):
        """
        The CPU scheduler priority for merges.

        :return:CPU scheduling hint for merges
        """
        return self.config[u'merge-priority']

    def set_merge_max_size(self, limit=32768):
        """
        Maximum allowable size (in megabytes) for merges, or 0 for no limit.

        :param limit:Size in megabytes
        :return:The database object
        """
        self.config[u'merge-max-size'] = limit
        return self

    def merge_max_size(self):
        return self.config[u'merge-max-size']

    def set_merge_min_size(self, limit=1024):
        """
        Stands with fewer than this number of fragments are merged together.

        :param limit:Minimum stand count for merge
        :return:The database object
        """
        self.config[u'merge-min-size'] = limit
        return self

    def merge_min_size(self):
        """
        Stands with fewer than this number of fragments are merged together.

        :return:Minimum stand count for merge
        """
        return self.config[u'merge-min-size']

    def set_merge_min_ratio(self, limit=2):
        """
        Larger ratios trigger more merges.

        :param limit: The marge min ratio
        :return:The database object
        """
        self.config[u'merge-min-ratio'] = limit
        return self

    def merge_min_ratio(self):
        """
        Larger ratios trigger more merges.

        :return:The marge min ratio
        """
        return self.config[u'merge-min-ratio']

    def set_merge_timestamp(self, limit=0):
        """
        Set the minimum timestamp for merging

        :param limit:Minimum value
        :return:The database object
        """
        self.config[u'merge-timestamp'] = limit
        return self

    def merge_timestamp(self):
        """
        Set the minimum timestamp for merging

        :return:Minimum value
        """
        return self.config[u'merge-timestamp']

    def set_retain_until_backup(self, enabled=False):
        self.config[u'retain-until-backup'] = enabled
        return self

    def set_rebalancer_enable(self, enabled=True):
        """
        Indicate if automatic rebalancing is enabled after configuration changes

        :param enabled: Enable automatic rebalancing
        :return:The database object
        """
        validate_boolean(enabled)
        self.config[u'rebalancer-enable'] = enabled
        return self

    def rebalancer_enable(self):
        """
        Indicate if automatic rebalancing is enabled after configuration changes

        :return:Enable automatic rebalancing
        """
        return self.config[u'rebalancer-enable']

    def set_rebalancer_throttle(self, limit=5):
        """
        Larger numbers mean work harder at rebalancing.

        :param limit:The relative amount of resources to dedicate to rebalancing
        :return:The database object
        """
        validate_integer_range(limit, 1, 5)
        self.config[u'rebalancer-throttle'] = limit
        return self

    def rebalancer_throttle(self):
        """
        Larger numbers mean work harder at rebalancing.

        :return:The relative amount of resources to dedicate to rebalancing
        """
        return self.config[u'rebalancer-throttle']

    def set_assignemnt_policy(self, which=u'bucket'):
        """
        What policy to use for assignment and rebalancing.

        :param which:The policy for assignment and rebalancing
        :return:The database object
        """
        validate_assignment_policy_options(which)
        self.config[u'assignment-policy'] = {"assignment-policy-name": which}
        return self

    def assignment_policy(self):
        """
        What policy to use for assignment and rebalancing.

        :return:The policy for assignment and rebalancing
        """
        return self.config[u'assignment-policy']

    def add_path_namespace(self, prefix, namespace):
        """
        Add a path namespace for use by field paths.

        :param prefix: The prefix to use in field (i.e. 'foo')
        :param namespace: The namespace uri (i.e. 'http://bar.com')
        :return: The database object
        """
        if u'path-namespaces' not in self.config:
            self.config[u'path-namespaces'] = []

        self.config[u'path-namespaces'].append({
            u'prefix': prefix,
            u'namespace-uri': namespace
        })
        return self

    def path_namespaces(self):
        """
        Return the array path namespaces defined or None, if no path namespaces
        are defined.

        :return:The path namespaces or none
        """
        if u'path-namespaces' not in self.config:
            return None
        return self.config[u'path-namespaces']

    def create(self, connection):
        """
        Create a new database defined by these parameters on the given connection.

        :param connection: The server connection
        :return: The database object
        """
        uri = "http://{0}:{1}/manage/v2/databases".format(connection.host, connection.management_port)

        for forest_name in self.config[u'forest']:
            new_forest = Forest(forest_name)
            if self.hostname is not None:
                new_forest.set_host(self.hostname)
            new_forest.create(connection)

        response = requests.post(uri, json=self.config, auth=connection.auth)
        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def save(self, connection):
        """
        Save the configuration changes with the given connection.  If the database already exists on the
        given connection, then you can update the settings with this method.

        :param connection:The server connection
        :return:The database object
        """
        uri = "http://{0}:{1}/manage/v2/databases/{2}/properties".format(connection.host, connection.management_port,
                                                                         self.config[u'database-name'])
        response = requests.put(uri, json=self.config, auth=connection.auth)

        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def remove(self, connection):
        """
        Remove the given database and all its forests.

        :param connection: The server connection
        :return:The database object
        """
        uri = "http://{0}:{1}/manage/v2/databases/{2}".format(connection.host, connection.management_port,
                                                              self.config[u'database-name'])
        response = requests.delete(uri, auth=connection.auth)

        if response.status_code > 299 and not response.status_code == 404:
            raise Exception(response.text)

        for forest_name in self.config[u'forest']:
            forest_uri = uri = "http://{0}:{1}/manage/v2/forests/{2}?level=full".format(connection.host,
                                                                                        connection.management_port,
                                                                                        forest_name)
            response = requests.delete(forest_uri, auth=connection.auth)
            if response.status_code > 299 and not response.status_code == 404:
                raise Exception(response.text)

        return self

    def load_file(self, connection, path, uri, collections=None, content_type="application/json"):
        """
        Load a given file into a given database.

        :param connection: The server connection
        :param path: The path to the file
        :param uri: The uri for the file contents in the database
        :param collections: A list of collections
        :param content_type: The content type of the data
        :return:The database object
        """
        doc_url = "http://{0}:{1}/v1/documents?uri={2}&database={3}".format(connection.host, connection.port, uri,
                                                                            self.config[u'database-name'])

        if collections is not None:
            for collection in collections:
                doc_url += ("&collection=" + collection)

        with open(path) as data_file:
            file_data = data_file.read()
            response = requests.put(doc_url, data=file_data, auth=connection.auth,
                                    headers={'content-type': content_type})
            if response.status_code > 299:
                raise Exception(response.text)

        return self

    def load_directory_files(self, connection, path, prefix="/", collections=None, content_type="application/json"):
        """
        Load all the given files in a directory.  It will combine the prefix with the filename to generate
        a uri for the file on the server.

        :param connection: The server connection
        :param path: The path to the directory
        :param prefix: The prefix to the individuals files
        :param collections: A list of collections to use for the files
        :param content_type: The content type of the files
        :return:The database object
        """
        file_list = files.walk_directories(path)
        for result in file_list:
            self.load_file(connection, result['partial-directory'], prefix + result['filename'],
                           collections=collections, content_type=content_type)
        return self

    def load_directory(self, connection, path, prefix="/", collections=None, content_type="application/json"):
        """
        Load all the file in a directory, preserving the partial path between the directory root and the
        file.  So a file located at /data/files/myfile.xml, with a prefix parameter of '/data' will be
        loaded as /files/myfile.xml.  (Using the default prefix).

        :param connection: The server connection
        :param path: The path to the directory root
        :param prefix: The prefix to use when constructing the server URI for the file
        :param collections: The collections to use for the files
        :param content_type: The content type of the files
        :return:
        """
        file_list = files.walk_directories(path)
        for result in file_list:
            self.load_file(connection, result['partial-directory'], prefix + result['partial-directory'],
                           collections=collections, content_type=content_type)
        return self

    @classmethod
    def lookup(cls, name, connection):
        """
        Lookup a database configuration by name.

        :param name:The name of the database
        :param connection:The server connection
        :return:The database configuration
        """
        uri = "http://{0}:{1}/manage/v2/databases/{2}/properties".format(connection.host, connection.management_port,
                                                                         name)
        response = requests.get(uri, auth=connection.auth, headers={u'accept': u'application/json'})
        if response.status_code > 299:
            raise response
        result = Database("temp")
        result.config = json.loads(response.text)

        return result

    def add_index(self, index_def):
        """
        Add a new index to the database configuration.  The index isn't actually created on the server until
        the server configuration is saved.

        :param index_def: The index definition
        :return:The database configuration.
        """
        index_name = "range-element-index"
        if index_def.__class__ == ElementRange:
            index_name = u'range-element-index'
        elif index_def.__class__ == ElementAttributeRange:
            index_name = u'range-element-attribute-index'
        elif index_def.__class__ == FieldRange:
            index_name = u'range-field-index'

        if index_name not in self.config:
            self.config[index_name] = []

        self.config[index_name].append(index_def.config)
        return self

    def field_range_index(self, index=None):
        if index is None and u'range-field-index' in self.config:
            result = []
            for field in self.config[u'range-field-index']:
                temp = FieldRange("", "")
                temp.config = field
                result.append(temp)
            return result
        elif u'range-field-index' in self.config and len(self.config[u'range-field-index']) > index:
            temp = FieldRange("", "")
            temp.config = self.config[u'range-field-index'][index]
            return temp
        return None

    def add_field(self, field):
        if u'field' not in self.config:
            self.config[u'field'] = []

        self.config[u'field'].append(field.config)

        return self

    def fields(self, field_idx):
        if u'fields' not in self.config:
            return None
        if field_idx >= len(self.config[u'fields']):
            return None
        return self.config[u'fields'][field_idx]