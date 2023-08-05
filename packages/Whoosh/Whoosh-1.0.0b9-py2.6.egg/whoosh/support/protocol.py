from struct import Struct

class Protoslot(object):
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def read_from(self, f):
        raise NotImplementedError
    
    def write_to(self, f):
        raise NotImplementedError


class Int(Protoslot):
    code = "i"
    
    def read_from(self, f):
        return f.read_int()
    
    def write_to(self, f, value):
        f.write_int(value)
    
class Long(Protoslot):
    code = "q"
    
    def read_from(self, f):
        return f.read_long()
    
    def write_to(self, f, value):
        f.write_long(value)

class Float(Protoslot):
    code = "f"
    
    def read_from(self, f):
        return f.read_float()
    
    def write_to(self, f, value):
        f.write_float(value)

class String(Protoslot):
    def read_from(self, f):
        f.read_string()
    
    def write_to(self, f, value):
        f.write_string(value)
        

class List(Protoslot):
    def __init__(self, slot):
        self.slot = slot
    
    def read_from(self, f):
        slot = self.slot
        length = f.read_uint()
        return [slot.read_from(f) for _ in xrange(length)]
    
    def write_to(self, f, values):
        slot = self.slot
        f.write_uint(len(f))
        for value in values:
            slot.write_to(f, value)


class Dict(Protoslot):
    def __init__(self, *slots):
        self.by_name = {}
        self.by_id = {}
        
        for slot in slots:
            if slot.name in self.by_name: raise ValueError
            self.by_name[slot.name] = slot
        for slot in slots:
            if slot.id in self.by_id: raise ValueError
            self.by_id[slot.id] = slot
        
    def read_from(self, f):
        by_id = self.by_id
        
        d = {}
        count = f.read_uint()
        for _ in xrange(count):
            id = f.read_uint()
            slot = by_id[id]
            d[slot.name] = slot.read_from(f)
        return d

    def write_to(self, f, _=None, **d):
        if _ is not None:
            d = _
        
        by_name = self.by_name
        f.write_uint(len(d))
        for key, value in d.iteritems():
            slot = by_name[key]
            f.write_uint(slot.id)
            slot.write_to(f, value)
        
            
        
    




    
    