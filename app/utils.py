from app import db
from app import app
from .models import Indicator
from feeder.logentry import ResultsDict
#from whois import whois
#from ipwhois import IPWhois
#import pprint
import re


# def _enrich_data(data_type, data, pend=True):
#     results = 'Not implemented yet'
#     full = 'Not implemented yet'
#     if pend:
#         if data_type == 'ipv4':
#             obj = IPWhois(data)
#             q = obj.lookup_rdap(depth=1)
#             net = q.get('network', {})
#             results = '%s|%s' % (net.get('name'), net.get('cidr'))
#             full = pprint.pformat(q)
#         elif data_type == 'domain':
#             q = whois(data)
#             results = '%s|%s|%s' % (q.get('registrar'), q.get('name'), q.get('emails'))
#             full = q.text
#
#     return results, full

def _valid_json(fields, data_dict):
    if all(k in data_dict for k in fields):
        for field in fields:
            if re.search('_id$', field):
                try:
                    int(data_dict[field])
                except Exception:
                    return False
        return True

    return False


def _add_indicators(results, source, ttl, direction, enrich_it=False):
    #need to add a fix for ttl and direction from feed config
    reasons = []
    inserted_indicators = []
    failed_indicators = []
    updated_indicators = []
    if not isinstance(results, ResultsDict):
        app.logger.warn('Bad object passed to _add_indicators')
        reasons.append('Bad object passed to _add_indicators')
        return {'success':len(inserted_indicators), 'failed':len(failed_indicators), 'reason':';'.join(reasons)}

    for data_type in results.data_types.keys():
        indicators = results.data_types.get(data_type)
        for i in indicators.keys():
            val = i
            dt = indicators[i]['date']
            desc = indicators[i]['description']
            ind = Indicator.query.filter(Indicator.source == source, Indicator.data_type == data_type,
                                         Indicator.value == i).first()
            if ind:
                ind.last_seen = dt
                updated_indicators.append([ind.id, source, val])
            else:
                try:
                    ind = Indicator(value=val,
                                    source=source,
                                    ttl=ttl,
                                    data_type=data_type,
                                    direction=direction,
                                    details=desc)
                except:
                    print 'except in try'
                    reasons.append('Validation Failed')
                    failed_indicators.append([0, source, val])
                    continue
            db.session.add(ind)
            db.session.flush()
            ind_id = ind.id
            inserted_indicators.append([ind_id, source, val])

    # commit
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        app.logger.warn('Error committing indicators: %s' % e)
        reasons.append('Commit Failed')
        failed_indicators += inserted_indicators
        inserted_indicators = []

    return {'success':len(inserted_indicators) + len(updated_indicators), 'failed':len(failed_indicators), 'reason':';'.join(reasons)}
