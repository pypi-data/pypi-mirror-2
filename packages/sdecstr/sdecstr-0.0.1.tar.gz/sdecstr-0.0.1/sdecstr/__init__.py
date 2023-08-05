# coding=utf-8
""" Base clases for DecimalString type """

version = ('0', '0', '1', None)


from decimal import Decimal

def sdstr2dec(sdstr):
    """ Convert decimal string to long long integer """
    # Do some basic checks if value is provided as sdecstr
    if sdstr[0] not in ('0', '1'):
        raise ValueError("Wrong format of signed decimal string")
    # Calculate length of szahl:
    l = len(sdstr)
    # Calculate digits after comma:
    ci = sdstr.find('.')
    if ci == -1:
        comma = 0
        ci = 0 # length of digits after comma
    else:
        comma = 1
        ci = l - ci - 1 # -1 due to comma

    # Convert szahl to decimal
    dec = Decimal(sdstr)

    # Create Mask, "-1" due to 10^, -3 due to digits after comma + comma
    i = 10**(l - 1 - ci - comma)

    return dec-i

def decexpand(dec):
    """ Expand Decimal to a notation without exponents,
    e.g. 1000000 instead of 1E6 """
    if not isinstance(dec, Decimal):
        raise TypeError("Argument must be decimal but is : %s, %s" % \
                        (type(dec), dec))
    idec = int(dec)
    post = dec - idec
    sdec = Decimal("%s" % (idec + post))
    if 'E' in str(sdec).upper():
        raise NotImplementedError("Expand function not working for this kind"\
                                  " of number!!!")
    return sdec

    

def dec2sdstr(dec, length, precision):
    # check that no data is lost
    # Make dec again unnormalized, to maximum form
    dec = decexpand(dec)
    if precision == 0:
        comma = 0
    else:
        comma = 1
    s, d, p = dec.as_tuple()
    if precision < abs(p):
        raise ValueError("Invalid precision: Decimal digits truncated!")
    #print length, len(d), p, precision
    if length < len(d)+p+precision+comma+1: # +1 == +Sign
        raise ValueError("Invalid length: Number too big for given length!")
    
    # Create Mask, "-1" due to 10^, (precision+1)
    # due to digits after comma + comma
    i = 10**(length-1-(precision+comma))
    z = str(dec + i)
    # Drop preceding '0' in case of 0.123, resulting in .123
    if z[:2] == '0.':
        z = z[1:]
    # If no fractions, then append comma
    if precision != 0 and abs(p) == 0:
        z = z+'.'
    
    # If smaller than zero, prepend '0'
    if dec < 0:
        z = '0'+z
    # Append '0' for precision if necessary
    z = z.ljust(length, '0')

    return z

class SDecStr(Decimal):
    """ Signed Decimal String type """

    length = None
    precision = None

    def __new__(cls, value="0", length=None, precision=None):
        """ Initialize class either via a Decimal or a
        Signed Decimal String """
        
        params={}
        if length != None or precision != None:
            if length != None:
                params['length'] = length
            if precision != None:
                params['precision'] = precision
        if isinstance(value, basestring):
            # Given as a Signed Decimal String
            # If length/precision is given, then try to convert it to
            # that and if it works, set length/precision object attributes
            if params:
                # Try to change the value
                value = dec2sdstr(sdstr2dec(value).normalize(), **params)
            # Build the resulting decimal value
            value = sdstr2dec(value)
        else:
            if params:
                # Test if it is possible
                sdstr2dec(dec2sdstr(value, **params))
                
        obj = Decimal.__new__(cls, value)
        # Check if length/precision is missing in params and if yes,
        # calculate them:
        s, t, p = obj.as_tuple()
        if not 'length' in params:
            if p == 0:
                params['length'] = len(t) + 1 # No comma
            else:
                params['length'] = len(t) + 1 + 1 # Comma
        if not 'precision' in params:
            params['precision'] = abs(p)
        
        # Store length/precision if given
        for key, value in params.items():
            setattr(obj, key, value)
        return obj
        

    def __repr__(self):
        return 'SDecStr("%s")' % (self.sdstr())

    def quantize(self, *kd, **kw):
        return SDecStr(super(SDecStr,self).quantize(*kd, **kw))

    def sdstr(self, length=None, precision=None):
        """ Return the Signed Decimal String """
        # The highest precedence has the function parameters,
        # The second the class attributes and if both are absent,
        # default values are used
        if length == None:
            length = self.length
        if precision == None:
            precision = self.precision
        return dec2sdstr(self.normalize(),length, precision)


if __name__ == "__main__":
    import sys
    print "############### Testing module dbszahl #####################"
    print "Converting to dbszahl and back and comparing afterwards:"
    slen = 16
    print "Length of dbszahl: %d" % slen
    tcase = ['1','-1','2','-2','99','-99','100','-100','1827598','-2837395']
    for item in tcase:
        i = "%.2f" % float(item)
        s = str2szahl(i,slen)
        b = szahl2str(s)
        if i != b:
            print "Wrong conversion:",i,s,b,i==b
            sys.exit(1)
    print "All Tests succeeded"
