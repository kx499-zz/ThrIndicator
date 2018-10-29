import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

DATA_TYPES = ['ipv4', 'cidr', 'domain']
TTL_VALUES = [0,7,30,60,90]
DIRECTIONS = ['inbound', 'outbound', 'both']
VALIDATE = {'ipv4': '\d+\.\d+\.\d+\.\d+',
            'cidr':None,
            'domain':None
            }

SOURCES = {
    "SSL IPBL":
        {
            "frequency": "*",
            "ttl": 90,
            "direction": "both",
            "modules": {
                "collect": {
                    "name": "collect.GetHttp",
                    "config": {
                        "url": "https://sslbl.abuse.ch/blacklist/sslipblacklist.csv",
                        "ignore_regex": "^#",
                        "user_agent": "OSTIP",
                        "referer": None,
                        "timeout": 20,
                        "verify_cert": True
                    }
                },
                "parse": {
                    "name": "parse.ParseCsv",
                    "config":{
                        "fieldnames": ["indicator_ipv4", "port", "desc_1"],
                        "data_types": ["ipv4"],
                        "control": "Inbound"
                    }
                }
            }
          },
    "alienvault":
        {
            "frequency": "0,4,8,12,16,20",
            "ttl": 90,
            "direction": "both",
            "modules": {
                "collect": {
                    "name": "collect.GetHttp",
                    "config": {
                        "url": "https://reputation.alienvault.com/reputation.data",
                        "ignore_regex": "^#",
                        "user_agent": "OSTIP",
                        "referer": None,
                        "timeout": 20,
                        "verify_cert": True
                    }
                },
                "parse": {
                    "name": "parse.ParseText",
                    "config":{
                        "regex": "^(?P<indicator_ipv4>[^\#]+)\#\d\#\d\#(?P<desc_1>[^\#]+)\#",
                        "data_types": ["ipv4"],
                        "control": "Inbound"
                    }
                }
            }
          }
}


