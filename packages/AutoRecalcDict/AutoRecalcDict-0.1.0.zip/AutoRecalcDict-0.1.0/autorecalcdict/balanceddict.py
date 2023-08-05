class DepDescFunc(object):
    """
    Class for creating a DEPendencyDESCriptorFUNCtion object.
    All it is is a target key, a list of dependancy keys, and a function.
    """
    def __init__(self, target, deplist, func):
        hash(target)	# This will raise TypeError if it fails.
        self.target = target
        if not isinstance(deplist, (tuple,list)):
            raise TypeError, "DepDescFunc:deplist must be iterable."
        for ii in deplist:
            hash(ii)	# Again, raise TypeError if it fails.
        self.deplist = deplist
        if not callable(func):
            raise TypeError, "DepDescFunc:func must be function"
        self.func = func

    def __repr__(self):
        return "target:%r\ndeplist:%r\nfunc:%r\n"%(self.target,
                                                   self.deplist,
                                                   self.func)
    __str__ = __repr__

    def modFunc(self, parent):
        self.func = self.func.__get__(parent, AutoRecalcDict)

    def __cmp__(self,other):
        vv = cmp( self.target, other.target )
        if vv != 0:
            return vv
        vv = cmp( self.deplist, other.deplist )
        if vv != 0:
            return vv
        vv = cmp( self.func, other.func )
        return vv

class AutoRecalcDict(dict):
    """
    Create a dict that has the ability to change values of keys based
    on dependancies on other keys.
    First arg is the dict's initial value.
    The second value dependency description described above.

    TBD:
         if we add another Bool to the tuple then we could specify whether
         the function should be bound to the instance or stay unbound.
    """

    def __init__( self, initval={}, depDesc=None ):
        dict.__init__(self)
        # __TargDepFunc is an array of DepDescFunc's.
        # All functions that come in get made into an instance method.
        self.__TargDepFunc = []
        if not isinstance(initval, dict):
            raise TypeError('Invalid type for initial value')
        dict.update(self, initval)
        # Call addDep *after* calling update. No need to have dependencies set
        # from an initial value.
        self.addDep( depDesc )

    def __setitem__(self, key, value):             # setting a keyword
        dict.__setitem__(self, key, value)
        # See if the key that was modified is dependent on anything.
        for ii, tdf in enumerate(self.__TargDepFunc):
            if key in tdf.deplist:
                self.__TargDepFunc[ii].func(self.__TargDepFunc[ii].target,
                                            self.__TargDepFunc[ii].deplist)

    def addDep(self, depDesc=None):
        """
        addDep takes either a DepDescFunc or an array of them.
        It converts the func attribute to an instance method
        and returns the DepDescFunc (or the array of them)
        """
        if isinstance(depDesc, (tuple, list)):
            ret = []
            for jj in depDesc:
                # Make the new function be an instance method.
                jj.modFunc(self)
                self.__TargDepFunc.append(jj)
                ret.append(jj)
            return ret
        if isinstance(depDesc, DepDescFunc):
            depDesc.modFunc(self)
            self.__TargDepFunc.append(depDesc)
            return depDesc
        raise TypeError, "AutoRecalcDict.addDep:depDesc is not DepDescFunc"

    def _rmOneDep(self, depDesc):
        delList = []
        for ii in range(len(self.__TargDepFunc)):
            if depDesc == self.__TargDepFunc[ii]:
                delList.append(ii)
        if len(delList) > 0:
            for ii in delList[::-1]:
                del(self.__TargDepFunc[ii])

    def removeDep(self, depDesc=None):
        if isinstance(depDesc, (tuple, list)):
            for jj in depDesc:
                self._rmOneDep(jj)
        elif isinstance(depDesc, DepDescFunc):
            self._rmOneDep(depDesc)
        else:
            raise TypeError, "AutoRecalcDict.addDep:depDesc is not DepDescFunc"

if __name__ == "__main__":
    import pprint

    def Targ_Class(op, inc):
        """
        closure to create a func that operates on lists.
        """
        def targ_calc(self, target, deplist):
            """
            Example to perform a function on each element of a list.
            In this example, deplist is unused.
            """
            self[target]= [op(ii, inc) for ii in self[target]]
            # for fun, let's give the return value a more meaningful name
            # If rr was a numpy.array then I could have said
            #opname,typename = numpy.array(repr(op).split())[[2,4]]
            rr = repr(op).split()
            opname,typename = [rr[ii] for ii in 2,4]
            targ_calc.__name__ = 'targ_calc_%s%s_%s'%(opname.strip("'_"),
                                                      typename.strip("'"),
                                                      str(inc).replace('.','P'))
        return targ_calc

    def recalc_range(self, target, deplist):
        """
        Example func that *does* ref deplist.
        """
        # Create deps to be a dict of dependencies whose values are True or None
        # If everything is True then we should run the function.
        # Note that this could be subverted by deliberatly doing
        # something like foo['start'] = False
        # because type of a bool is int.
        deps = dict([(ii,self[ii])
                     if ii in self else (ii,None) for ii in deplist])
        if all([isinstance(t, int) for t in deps.values()]):
            # All is set? and to integer values? Run it.
            self[target] = range(*(self[ii] for ii in deplist))

    targAdd_f = Targ_Class(int.__add__, 6)
    print 'targAdd_f:',targAdd_f

    targSub_f = Targ_Class(float.__sub__, .1)
    print 'targSub_f:',targSub_f

    b = {'Hello': 'Goodbye',
         'color': 'red',
         (3, 4): [3,5,7],
         (6, 7): [3.14, 2.178, 2.88] }

    pp = pprint.PrettyPrinter()
    dd = AutoRecalcDict( b, DepDescFunc((3,4), ['color'], targAdd_f) )
    print 'dd: Init'
    pp.pprint(dd)
    print
    rangeDeps = ('start','stop','step')
    rangeDepDesc = DepDescFunc('range', rangeDeps, recalc_range)
    print 'rangeDepDesc:', rangeDepDesc
    rangeDepDesc = dd.addDep( rangeDepDesc )
    dd['start'] = 10
    dd['stop'] = 40
    dd['step'] = 5
    print 'dd: After start stop and step'
    pp.pprint(dd)
    print
    dd['color'] = 'blue'
    print 'dd: color changed so apply targAdd_f to (3,4)'
    pp.pprint(dd)
    print
    fruitDepDesc = dd.addDep(DepDescFunc((6,7), ['fruit'], targSub_f))
    dd['fruit'] = 'orange'
    print 'dd: dep for fruit added and modified. (6,7) gets targSub_f'
    pp.pprint(dd)
    print
    dd.removeDep(fruitDepDesc)
    dd['fruit'] = 'blueberry'
    print 'fruitDepDesc removed. fruit set to blueberry'
    pp.pprint(dd)
    print
