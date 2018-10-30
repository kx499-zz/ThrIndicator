import json
import os
from app.utils import _add_indicators, _valid_json
from app import app
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

FEED_CONFIG = app.config.get('SOURCES')


def _dynamic_load(class_name):
    if '.' not in class_name:
        raise ValueError('invalid absolute classname %s' % class_name)

    modname, class_name = class_name.rsplit('.', 1)
    t = __import__(modname, globals(), locals(), [class_name])
    cls = getattr(t, class_name)
    return cls


class Feed:

    def __init__(self):
        try:
            self.configs = FEED_CONFIG
        except Exception, e:
            app.logger.warn('Error Loading File: %s' % e)

    def process_all(self, config_to_process=None, force_run=False):
        results = {}
        fields = ['frequency', 'modules', 'ttl', 'direction']
        date_hour = datetime.datetime.now().hour
        for name, config in self.configs.iteritems():
            if not _valid_json(fields, config):
                app.logger.warn('Bad config from feed.json')
                continue
            if config_to_process:
                if not name == config_to_process:
                    continue
            app.logger.info('Processing Feed: %s' % name)
            modules = config.get('modules')
            if force_run:
                freq = '*'
            else:
                freq = config.get('frequency').split(',')
            if not ('*' in freq or str(date_hour) in freq):
                continue

            if 'parse' in modules.keys() and 'collect' in modules.keys():
                try:
                    coll_cls = _dynamic_load(modules['collect'].get('name'))
                    parse_cls = _dynamic_load(modules['parse'].get('name'))
                except Exception, e:
                    app.logger.warn('error loading classes: %s' % e)
                    continue

                collect_config = modules['collect'].get('config')
                parse_config = modules['parse'].get('config')
                if not collect_config and not parse_config:
                    app.logger.warn('error loading module configs')
                    continue

                collector = coll_cls(collect_config)
                data = collector.get()

                if not data:
                    app.logger.warn('error loading data from collector')
                    continue

                parser = parse_cls(parse_config, data)
                logs = parser.run()
                #results[config.get('name', 'n/a')] = logs
                results[name] = _add_indicators(logs, name, config.get('ttl'), config.get('direction'))
            elif 'custom' in modules.keys():
                pass
            else:
                app.logger.warn('Bad config from feed.json in modules')
                continue
        app.logger.info('Processing Results: %s' % results)
        return results











