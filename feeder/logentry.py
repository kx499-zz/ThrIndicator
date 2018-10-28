#!/usr/bin/env python
import datetime


class ResultsDict:

    def __init__(self, control):
        self.control = control
        self.data_types = dict()
        # data_types dict looks like
        # {'ipv4':{'1.1.1.1':{'date':datetime_obj, 'description':'blah'}, '2.2.2.2':{... }, 'domain':{.....

    def new_ind(self, data_type, indicator, date, description):
        if not data_type in self.data_types.keys():
            self.data_types[data_type] = dict()
        dt_obj = self.data_types.get(data_type)
        ioc = dt_obj.get(indicator)
        if ioc:
            ioc['date'] = date or ioc['date']
            if description and ioc['description'] and len(ioc['description']) > 0:
                ioc['description'] += '; %s' % description
            else:
                ioc['description'] = None
        else:
            dt_obj[indicator] = dict(date=date or datetime.datetime.utcnow(),description = description)

    def as_dict(self):
        return dict(control=self.control, data_types=self.data_types)


