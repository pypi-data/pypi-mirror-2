# coding=utf-8
""" Specific SQLAlchemy Datatypes """

from decimal import Decimal, InvalidOperation
import sqlalchemy.types as types
from sdecstr import SDecStr, decexpand

class DecimalVarchar(types.TypeEngine):
    """ Base Decimal Varchar Class """
    def __init__(self, length, precision):
        """ Store length and precision """
        self.length = length
        self.precision = precision
    def get_col_spec(self):
        return "VARCHAR(%s)" % self.length

class SDecVarchar(DecimalVarchar):
    """ Signed Decimal Varchar Data Type """
    def bind_processor(self, dialect):
        def process(value):
            """ From Application to Database """
            sdstr = SDecStr(value, self.length, self.precision)
            return sdstr.sdstr()
        return process
    def result_processor(self, dialect):
        def process(value):
            """ From Database to Application """
            if value == None:
                return None
            else:
                return Decimal(SDecStr(value, self.length, self.precision))
        return process
    
class StrDecimal(DecimalVarchar):
    """ Store Decimal as String and regard length/comma places"""
    def bind_processor(self, dialect):
        def process(value):
            """ From Application to Database """
            # First expand the decimal
            value = str(decexpand(value))
            # Check if the decimal fits into varchar
            if len(value) > self.length:
                raise ValueError("Invalid length: Number too big " \
                                 "for given length!")
            if '.' in value:
                # Check precision
                if len(value.split('.')[1]) > self.precision:
                    raise ValueError("Invalid precision: "\
                                     "Decimal digits truncated!")
            return value
        return process
    def result_processor(self, dialect):
        def process(value):
            """ From Database to Application """
            if value == None:
                return None
            else:
                try:
                    return Decimal(value)
                except InvalidOperation:
                    raise ValueError("InvalidOperation raised for value |%s| "
                                     "during DB-Read conversion" % value)
        return process

class InvStrDecimal(StrDecimal):
    """Same as StrDecimal, but store the inverted (minus) decimal"""
    def bind_processor(self, dialect):
        def process(value):
            return super(InvStrDecimal, self).bind_processor(dialect)(-value)
            # SA 43
            #return super(InvStrDecimal, self).convert_bind_param(
            #    -value, engine)
        return process

    def result_processor(self, dialect):
        def process(value):
            result = super(InvStrDecimal, self).result_processor(dialect)(value)
            # SA 43
            #result = (super(InvStrDecimal, self).convert_result_value(
            #        value, engine))
            if isinstance(result, Decimal):
                return -result
            else:
                return result
        return process

class PStrDecimal(StrDecimal):
    """ Same as StrDecimal but pad string with zero """
    def bind_processor(self, dialect):
        def process(value):
            """ From Application to Database """
            value = super(PStrDecimal, self).bind_processor(dialect)(value)
            # SA 43
            #value = super(PStrDecimal, self).convert_bind_param(value, engine)
            # Correct Precision
            if self.precision > 0:
                if '.' not in value:
                    value += '.'
                pre, post = value.split('.')
                post = post.ljust(self.precision, '0')
                # Now prepend with zeros
                value = (pre+'.'+post).zfill(self.length)
            else:
                value = value.zfill(self.length)
            # Check if the decimal still fits into varchar
            if len(value) > self.length:
                raise ValueError("Invalid length: Number too big " \
                                 "for given length!")
            return value
        return process
        
    
# SA 43 - For SA 5.3 there's no such method as convert_...    
#class SDecVarchar(DecimalVarchar):
    #""" Signed Decimal Varchar Data Type """
    #def convert_bind_param(self, value, engine):
        #""" From Application to Database """
        #sdstr = SDecStr(value, self.length, self.precision)
        #return sdstr.sdstr()
    #def convert_result_value(self, value, engine):
        #""" From Database to Application """
        #if value == None:
            #return None
        #else:
            #return Decimal(SDecStr(value, self.length, self.precision))

#class StrDecimal(DecimalVarchar):
    #""" Store Decimal as String and regard length/comma places"""
    #def convert_bind_param(self, value, engine):
        #""" From Application to Database """
        ## First expand the decimal
        #value = str(decexpand(value))
        ## Check if the decimal fits into varchar
        #if len(value) > self.length:
            #raise ValueError("Invalid length: Number too big " \
                             #"for given length!")
        #if '.' in value:
            ## Check precision
            #if len(value.split('.')[1]) > self.precision:
                #raise ValueError("Invalid precision: "\
                                 #"Decimal digits truncated!")
        #return value
    #def convert_result_value(self, value, engine):
        #""" From Database to Application """
        #if value == None:
            #return None
        #else:
            #return Decimal(value)

#class InvStrDecimal(StrDecimal):
    #"""Same as StrDecimal, but store the inverted (minus) decimal"""
    #def convert_bind_param(self, value, engine):
        #return super(InvStrDecimal, self).convert_bind_param(
            #-value, engine)

    #def convert_result_value(self, value, engine):
        #result = (super(InvStrDecimal, self).convert_result_value(
                #value, engine))
        #if isinstance(result, Decimal):
            #return -result
        #else:
            #return result

#class PStrDecimal(StrDecimal):
    #""" Same as StrDecimal but pad string with zero """
    #def convert_bind_param(self, value, engine):
        #""" From Application to Database """
        #value = super(PStrDecimal, self).convert_bind_param(value, engine)
        ## Correct Precision
        #if self.precision > 0:
            #if '.' not in value:
                #value += '.'
            #pre, post = value.split('.')
            #post = post.ljust(self.precision, '0')
            ## Now prepend with zeros
            #value = (pre+'.'+post).zfill(self.length)
        #else:
            #value = value.zfill(self.length)
        ## Check if the decimal still fits into varchar
        #if len(value) > self.length:
            #raise ValueError("Invalid length: Number too big " \
                             #"for given length!")
        #return value
        
