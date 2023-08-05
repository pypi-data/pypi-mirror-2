import datetime
import unittest
import logging
from itertools import izip

from stdnet.stdtest import TestBase
from stdnet import orm
from stdnet.utils import populate

# Create some models for testing

class Base(orm.StdModel):
    name = orm.AtomField(unique = True)
    ccy  = orm.AtomField()
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        abstract = True

class Instrument(Base):
    type = orm.AtomField()
    
class Fund(Base):
    pass

class Position(orm.StdModel):
    instrument = orm.ForeignKey(Instrument, related_name = 'positions')
    fund       = orm.ForeignKey(Fund)
    dt         = orm.DateField()
    
    def __str__(self):
        return '%s: %s @ %s' % (self.fund,self.instrument,self.dt)
    
    def __init__(self, size = 1, price = 1, **kwargs):
        self.size  = size
        self.price = price
        super(Position,self).__init__(**kwargs)
    

orm.register(Instrument)
orm.register(Fund)
orm.register(Position)

INST_LEN    = 100
FUND_LEN    = 20
POS_LEN     = 30
NUM_DATES   = 3

ccys_types  = ['EUR','GBP','AUD','USD','CHF','JPY']
insts_types = ['equity','bond','future','cash','option']

inst_names = populate('string',INST_LEN, min_len = 5, max_len = 20)
inst_types = populate('choice',INST_LEN, choice_from = insts_types)
inst_ccys  = populate('choice',INST_LEN, choice_from = ccys_types)

fund_names = populate('string',FUND_LEN, min_len = 5, max_len = 20)
fund_ccys  = populate('choice',FUND_LEN, choice_from = ccys_types)

dates = populate('date',NUM_DATES,start=datetime.date(2009,6,1),end=datetime.date(2010,6,6))



class TestORM(TestBase):
    
    def setUp(self):
        for name,typ,ccy in izip(inst_names,inst_types,inst_ccys):
            Instrument(name = name, type = typ, ccy = ccy).save()
        for name,ccy in izip(fund_names,fund_ccys):
            Fund(name = name, ccy = ccy).save()
    
    def makePositions(self):
        '''Create Positions objects which hold foreign key to instruments and funds'''
        instruments = Instrument.objects.all()
        n = 0
        for f in Fund.objects.all():
            insts = populate('choice',POS_LEN,choice_from = instruments)
            for dt in dates:
                for inst in insts:
                    n += 1
                    Position(instrument = inst, dt = dt, fund = f).save()
        return n
        
    def testLen(self):
        '''Simply test len of objects greater than zero'''
        objs = Instrument.objects.all()
        self.assertTrue(len(objs)>0)
        
    def testObject(self):
        obj = Instrument.objects.get(id = 1)
        self.assertEqual(obj.id,1)
        self.assertTrue(obj.name)
        obj2 = Instrument.objects.get(name = obj.name)
        self.assertEqual(obj,obj2)
    
    def testFilter(self):
        '''Test filtering'''
        tot = 0
        for t in insts_types:
            fs = Instrument.objects.filter(type = t)
            count = {}
            for f in fs:
                count[f.ccy] = count.get(f.ccy,0) + 1
            for c in ccys_types:
                x = count.get(c,0)
                objs = fs.filter(ccy = c)
                y = 0
                for obj in objs:
                    y += 1
                    tot += 1
                    self.assertEqual(obj.type,t)
                    self.assertEqual(obj.ccy,c)
                self.assertEqual(x,y)
        all = Instrument.objects.all()
        self.assertEqual(tot,len(all))
        
    def testForeignKey(self):
        '''Test filtering with foreignkeys'''
        self.makePositions()
        #
        positions = Position.objects.all()
        for p in positions:
            self.assertTrue(isinstance(p.instrument,Instrument))
            self.assertTrue(isinstance(p.fund,Fund))
            pos = Position.objects.filter(instrument = p.instrument,
                                          fund = p.fund)
            found = 0
            for po in pos:
                if po == p:
                    found += 1
            self.assertEqual(found,1)
                
        # Testing 
        total_positions = len(positions)
        totp = 0
        for instrument in Instrument.objects.all():
            pos  = list(instrument.positions.all())
            for p in pos:
                self.assertTrue(isinstance(p,Position))
                self.assertEqual(p.instrument,instrument)
            totp += len(pos)
        
        self.assertEqual(total_positions,totp)
        
    def testRelatedManagerFilter(self):
        self.makePositions()
        instruments = Instrument.objects.all()
        for instrument in instruments:
            positions = instrument.positions.all()
            funds = {}
            flist = []
            for pos in positions:
                fund = pos.fund
                n    = funds.get(fund.id,0) + 1
                funds[fund.id] = n
                if n == 1:
                    flist.append(fund)
            for fund in flist:
                positions = instrument.positions.filter(fund = fund)
                self.assertEqual(len(positions),funds[fund.id])
            
        
    def testDeleteSimple(self):
        '''Test delete on models without without related models'''
        instruments = Instrument.objects.all()
        funds = Fund.objects.all()
        Ni = len(instruments)
        Nf = len(funds)
        self.assertEqual(Ni,instruments.delete())
        self.assertEqual(Nf,funds.delete())
        
    def testDelete(self):
        '''Test delete on models with related models'''
        # Create Positions which hold foreign keys to Instruments
        Np = self.makePositions()
        instruments = Instrument.objects.all()
        Ni = len(instruments)
        T = instruments.delete()
        self.assertEqual(T,Np+Ni)
        
        

