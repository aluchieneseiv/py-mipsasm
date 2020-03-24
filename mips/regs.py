class Register:
    def __init__(self, reg_id, name):
        self.reg_id = reg_id
        self.name = name

    def __str__(self):
        return f"${self.name}"

    def __repr__(self):
        return f"${self.name}({self.reg_id})"

zero = Register(0, "zero")
at = Register(1, "at")

v0 = Register(2, "v0")
v1 = Register(3, "v1")

a0 = Register(4, "a0")
a1 = Register(5, "a1")
a2 = Register(6, "a2")
a3 = Register(7, "a3")

t0 = Register(8, "t0")
t1 = Register(9, "t1")
t2 = Register(10, "t2")
t3 = Register(11, "t3")
t4 = Register(12, "t4")
t5 = Register(13, "t5")
t6 = Register(14, "t6")
t7 = Register(15, "t7")

s0 = Register(16, "s0")
s1 = Register(17, "s1")
s2 = Register(18, "s2")
s3 = Register(19, "s3")
s4 = Register(20, "s4")
s5 = Register(21, "s5")
s6 = Register(22, "s6")
s7 = Register(23, "s7")

t8 = Register(24, "t8")
t9 = Register(25, "t9")

k0 = Register(26, "k0")
k1 = Register(27, "k1")

gp = Register(28, "gp")
sp = Register(29, "sp")
fp = Register(30, "fp")
ra = Register(31, "ra")

_id_lookup = [
    zero, at, v0, v1, a0, a1, a2, a3,
    t0, t1, t2, t3, t4, t5, t6, t7,
    s0, s1, s2, s3, s4, s5, s6, s7,
    t8, t9, k0, k1, gp, sp, fp, ra
]

_name_lookup = {reg.name: reg for reg in _id_lookup}

def from_name(name):
    if name in _name_lookup:
        return _name_lookup[name]

    raise Exception(f"Unknown register: ${name}")

def from_id(reg_id):
    if reg_id in _id_lookup:
        raise Exception(f"Unknown register: ${id}")

    return _id_lookup[reg_id]