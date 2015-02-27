__author__ = 'phoehne'

import requests
import json
from .forest import Forest
from .utilities import files
from .index import RangeElementAttribute, ElementRange

class Database:
    def __init__(self, name):
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

    def set_database_name(self, name):
        self.config[u'database-name'] = name
        return self

    def set_enabled(self, enabled=True):
        self.config[u'enabled'] = enabled
        return self

    def set_security_database(self, db=u'Security'):
        self.config[u'security-database'] = db
        return self

    def set_triggers_database(self, db=u'Triggers'):
        self.config[u'triggers-database'] = db
        return self

    def add_forest(self, forest):
        if not self.config[u'forest']:
            self.config[u'forest'] = []

        self.config[u'forest'].append(forest)

        return self

    def set_language(self, language):
        self.config[u'language'] = language
        return self

    def set_stemmed_searches(self, which=u'basic'):
        self.config[u'stemmed-searches'] = which
        return self

    def set_word_searches(self, enabled=False):
        self.config[u'word-searches'] = enabled
        return self

    def set_word_positions(self, enabled=False):
        self.config[u'word-positions'] = enabled
        return self

    def set_fast_phrase_searches(self, enabled=True):
        self.config[u'fast-phrase-searches'] = enabled
        return self

    def set_fast_reverse_searches(self, enabled=True):
        self.config[u'fast-reverse-searches'] = enabled
        return self

    def set_triple_index(self, enabled=False):
        self.config[u'triple-index'] = enabled
        return self

    def set_triple_positions(self, enabled=False):
        self.config[u'triple-positions'] = enabled
        return self

    def set_fast_case_senstive_searches(self, enabled=True):
        self.config[u'fast-case-sensitive-searches'] = enabled
        return self

    def set_fast_diacritic_sensitive_searches(self, enabled=True):
        self.config[u'fast-diacritic-sensitive-searches'] = enabled
        return self

    def set_fast_element_word_searches(self, enabled=True):
        self.config[u'fast-element-word-searches'] = enabled
        return self

    def set_element_word_positions(self, enabled=False):
        self.config[u'element-word-positions'] = enabled
        return self

    def set_fast_element_phrase_searches(self, enabled=True):
        self.config[u'fast-element-phrase-searches'] = enabled
        return self

    def set_element_value_positions(self, enabled=False):
        self.config[u'element-value-positions'] = enabled
        return self

    def set_attribute_value_positions(self, enabled=False):
        self.config[u'attribute-value-positions'] = enabled
        return self

    def set_field_value_searches(self, enabled=False):
        self.config[u'field-value-searches'] = enabled
        return self

    def set_field_value_positions(self, enabled=False):
        self.config[u'field-value-positions'] = enabled
        return self

    def set_three_character_searches(self, enabled=False):
        self.config[u'three-character-searches'] = enabled
        return self

    def set_three_character_word_positions(self, enabled=False):
        self.config[u'three-character-word-positions'] = enabled
        return self

    def set_fast_element_character_searches(self, enabled=False):
        self.config[u'fast-element-character-searches'] = enabled
        return self

    def set_trailing_wildcard_searches(self, enabled=False):
        self.config[u'trailing-wildcard-searches'] = enabled
        return self

    def set_trailing_wildcard_word_positions(self, enabled=False):
        self.config[u'trailing-wildcard-word-positions'] = enabled
        return self

    def set_fast_element_trailing_wildcard_searches(self, enabled=False):
        self.config[u'fast-element-trailing-wildcard-searches'] = enabled
        return self

    def set_two_character_searches(self, enabled=False):
        self.config[u'two-character-searches'] = enabled
        return self

    def set_one_character_searches(self, enabled=False):
        self.config[u'one-character-searches'] = enabled
        return self

    def set_uri_lexicon(self, enabled=True):
        self.config[u'uri-lexicon'] = enabled
        return self

    def set_collection_lexicon(self, enabled=False):
        self.config[u'collection-lexicon'] = enabled
        return self

    def set_reindexer_enable(self, enabled=True):
        self.config[u'reindexer-enable'] = enabled
        return self

    def set_reindexer_throtel(self, limit=5):
        self.config[u'reindexer-throttle'] = limit
        return self

    def set_reindexer_timestamp(self, limit=0):
        self.config[u'reindexer-timestamp'] = limit
        return self

    def set_directory_creation(self, which=u'manual'):
        self.config[u'directory-creation'] = which
        return self

    def set_maintain_last_modified(self, enabled=False):
        self.config[u'maintain-last-modified'] = enabled
        return self

    def set_maintain_directory_last_modified(self, enabled=False):
        self.config[u'maintain-directory-last-modified'] = enabled
        return self

    def set_inherit_permissions(self, enabled=False):
        self.config[u'inherit-permissions'] = enabled
        return self

    def set_inherit_collections(self, enabled=False):
        self.config[u'inherit-collections'] = enabled
        return self

    def set_inherit_quality(self, enabled=False):
        self.config[u'inherit-quality'] = enabled
        return self

    def set_in_memory_limit(self, limit=262144):
        self.config[u'in-memory-limit'] = limit
        return self

    def set_in_memory_list_size(self, limit=512):
        self.config[u'in-memory-list-size'] = limit
        return self

    def set_in_memory_tree_size(self, limit=128):
        self.config[u'in-memory-tree-size'] = limit
        return self

    def set_in_memory_range_index_size(self, limit=16):
        self.config[u'in-memory-range-index-size'] = limit
        return self

    def set_in_memory_reverse_index_size(self, limit=16):
        self.config[u'in-memory-reverse-index-size'] = limit
        return self

    def set_in_memory_triple_index_size(self, limit=64):
        self.config[u'in-memory-triple-index-size'] = limit
        return self

    def set_large_size_threshold(self, limit=1024):
        self.config[u'large-size-threshold'] = limit
        return self

    def set_locking(self, which=u'fast'):
        self.config[u'locking'] = which
        return self

    def set_journaling(self, which=u'fast'):
        self.config[u'journaling'] = which
        return self

    def set_journal_size(self, limit=1365):
        self.config[u'journal-size'] = limit
        return self

    def set_journal_count(self, limit=2):
        self.config[u'journal-count'] = limit
        return self

    def set_preallocate_journal(self, enabled=False):
        self.config[u'preallocate-journals'] = enabled
        return self

    def set_preload_mapped_data(self, enabled=False):
        self.config[u'preload-mapped-data'] = enabled
        return self

    def set_preload_replica_mapped_data(self, enabled=False):
        self.config[u'preload-replica-mapped-data'] = enabled
        return self

    def set_range_index_optimize(self, which=u'facet-time'):
        self.config[u'range-index-optimize'] = which
        return self

    def set_position_list_max_size(self, limit=256):
        self.config[u'positions-list-max-size'] = limit
        return self

    def set_format_compatibility(self, which=u'automatic'):
        self.config[u'format-compatibility'] = which
        return self

    def set_index_detection(self, which=u'automatic'):
        self.config[u'index-detection'] = which
        return self

    def set_expunge_locks(self, which=u'none'):
        self.config[u'expunge-locks'] = which
        return self

    def set_if_normalization(self, which=u'scaled-log'):
        self.config[u'tf-normalization'] = which
        return self

    def set_merge_priority(self, which=u'lower'):
        self.config[u'merge-priority'] = which
        return self

    def set_merge_max_size(self, limit=32768):
        self.config[u'merge-max-size'] = limit
        return self

    def set_merge_min_size(self, limit=1024):
        self.config[u'merge-min-size'] = limit
        return self

    def set_merge_min_ratio(self, limit=2):
        self.config[u'merge-min-ratio'] = limit
        return self

    def set_merge_timestamp(self, limit=0):
        self.config[u'merge-timestamp'] = limit
        return self

    def set_retain_until_backup(self, enabled=False):
        self.config[u'retain-until-backup'] = enabled
        return self

    def set_rebalancer_enable(self, enabled=True):
        self.config[u'rebalancer-enable'] = enabled
        return self

    def set_rebalancer_throttle(self, limit=5):
        self.config[u'rebalancer-throttle'] = limit
        return self

    def set_assignemnt_policy(self, which=u'bucket'):
        self.config[u'assignment-policy'] = {"assignment-policy-name": which}
        return self

    def create(self, connection):
        uri = "http://{0}:{1}/manage/v2/databases".format(connection.host, connection.management_port)

        for forest_name in self.config[u'forest']:
            new_forest = Forest(forest_name)
            new_forest.create(connection)

        response = requests.post(uri, json=self.config, auth=connection.auth)
        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def save(self, connection):
        uri = "http://{0}:{1}/manage/v2/databases/{2}/properties".format(connection.host, connection.management_port,
                                                              self.config[u'database-name'])
        response = requests.put(uri, json=self.config, auth=connection.auth)

        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def remove(self, connection):
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

    def load_file(self, connection, path, uri, collections=[], content_type="application/json"):
        doc_url = "http://{0}:{1}/v1/documents?uri={2}&database={3}".format(connection.host, connection.port, uri,
                                                                                self.config[u'database-name'])
        for collection in collections:
            doc_url += ("&collection=" + collection)

        with open(path) as data_file:
            file_data = data_file.read()
            response = requests.put(doc_url, data=file_data, auth=connection.auth,
                                    headers={'content-type': content_type})
            if response.status_code > 299:
                raise Exception(response.text)

        return self

    def load_directory_files(self, connection, path, prefix="/", collections=[], content_type="application/json"):
        file_list = files.walk_directories(path)
        for result in file_list:
            self.load_file(connection, result['partial-directory'], prefix + result['filename'],
                           collections=collections, content_type=content_type)
        return self

    def load_directory(self, connection, path, prefix="/", collections=[], content_type="application/json"):
        file_list = files.walk_directories(path)
        for result in file_list:
            self.load_file(connection, result['partial-directory'], prefix + result['partial-directory'],
                           collections=collections, content_type=content_type)
        return self

    @classmethod
    def lookup(cls, name, connection):
        uri = "http://{0}:{1}/manage/v2/databases/{2}/properties".format(connection.host, connection.management_port, name)
        response = requests.get(uri, auth=connection.auth, headers={u'accept': u'application/json'})
        if response.status_code > 299:
            raise response
        result = Database("temp")
        result.config = json.loads(response.text)

        return result

    def add_index(self, index_def):
        index_name = "range-element-index"
        if type(index_def) is index.ElementRange:
            index_name = u'range-element-index'
        elif type(index_def) is index.RangeElementAttribute:
            index_name = u'range-element-attribute-index'

        if not index_name in self.config:
            self.config[index_name] = []

        self.config[index_name].append(index_def.config)
        return self