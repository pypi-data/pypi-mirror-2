from stdnet import orm
from stdnet.utils import date2timestamp, timestamp2date
from stdnet.contrib.timeserie.utils import default_parse_interval


class TimeSerieField(orm.HashField):
    
    def __init__(self, converter = date2timestamp,
                 inverse = timestamp2date, **kwargs):
        super(TimeSerieField,self).__init__(converter=converter,
                                            inverse=inverse,
                                            **kwargs)


class TimeSerie(orm.StdModel):
    data  = TimeSerieField()
    
    def fromto(self):
        if self.start:
            return '%s - %s' % (self.start.strftime('%Y %m %d'),self.end.strftime('%Y %m %d'))
        else:
            return ''
        
    def __str__(self):
        return self.fromto()
    
    def converter(self, key):
        return date2timestamp(key)
    
    def inverse(self, key):
        return timestamp2date(key)
    
    def __init__(self, start = None, end = None, **kwargs):
        super(TimeSerie,self).__init__(**kwargs)
        self.start = start
        self.end   = end

    def storestartend(self):
        '''Store the start/end date of the timeseries'''
        dates = self.data.keys()
        if dates:
            dates.sort()
            self.start = self.inverse(dates[0])
            self.end   = self.inverse(dates[-1])
        else:
            self.start = None
            self.end   = None
        return self.save()
    
    def intervals(self, startdate, enddate, parseinterval = default_parse_interval):
        '''Given a *start* and an *end* date, evaluate the date intervals
from which data is not available. It return a list of two-dimensional tuples
containing start and end date for the interval. The list could countain 0,1 or 2
tuples.'''
        start     = self.start
        end       = self.end
        startdate = parseinterval(startdate,0)
        enddate   = max(startdate,parseinterval(enddate,0))

        calc_intervals = []
        # we have some history already
        if start:
            # the startdate is already in the database
            if startdate < start:
                calc_start = startdate
                calc_end = parseinterval(start, -1)
                if calc_end >= calc_start:
                    calc_intervals.append((calc_start, calc_end))

            if enddate > end:
                calc_start = parseinterval(end, 1)
                calc_end = enddate
                if calc_end >= calc_start:
                    calc_intervals.append((calc_start, calc_end))
        else:
            start = startdate
            end = enddate
            calc_intervals.append((startdate, enddate))

        if calc_intervals:
            # There are calculation intervals, which means the
            # start and aned date have changed
            N = len(calc_intervals)
            start1 = calc_intervals[0][0]
            end1 = calc_intervals[N - 1][1]
            if start:
                start = min(start, start1)
                end = max(end, end1)
            else:
                start = start1
                end = end1

        # Set values in the cache in order to avoid duplicate calculations
        self.start = start
        self.end   = end
        self.save()
        return calc_intervals 

