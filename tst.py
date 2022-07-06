#!/usr/bin/python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    if r is None:
        r = n
    if r > n:
        return
    indices = range(n)
    cycles = range(n, n-r, -1)
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class cCL:

    def __init__(self, CL = ''):
        self.CL = CL
        self.root = -1
        self.fin_states = ''
        self.disc = 0
        self.length = len(CL)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __str__(self):
        return self.CL

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __repr__(self):
        return self.CL

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __len__(self):
        return self.length

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_next_candidate_label_by_permuting(CLW):

    CL = list(CLW.CL)

    hit = -1
    for i in range(len(CL) - 1, 0, -1):
        if CL[i] > CL[i - 1]:
            hit = i - 1
            break
    if hit == -1:
        return None

    idx_of_min = hit + 1

    for i in range(hit + 1, len(CL)):
        if CL[i] < CL[idx_of_min] and CL[i] > CL[hit]:
            idx_of_min = i

    CL[hit], CL[idx_of_min] = CL[idx_of_min], CL[hit]
    CL = CL[:hit + 1] + sorted(CL[hit + 1:])

    CLW.CL = ''.join(CL)
    return CLW

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_next_candidate_label_by_padding(CLW, size):

    CL = list(CLW.CL)
    d = {}

    for c in CL:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1

    numlst = []

    keys = sorted(d)
    for e in keys:
        numlst.append(d[e])

    hit  = -1
    for i in range(len(numlst) - 2, -1, -1):
        if numlst[i] > 1:
            hit = i
            break

    if hit == -1:
        if size > len(CL):
            numlst[0] = numlst[-1] + 1
            if len(numlst) > 1:
                numlst[-1] = 1
        else:
            return None
    else:
        numlst[hit] -= 1
        numlst[hit + 1] += 1
        for i in range(hit + 2, len(numlst)):
            if numlst[i] > 1:
                numlst[hit + 1] += numlst[i] - 1
                numlst[i] = 1

    CL = []
    for i in range(0, len(numlst)):
        for j in range(0, numlst[i]):
            CL.append(keys[i])

    CLW.CL = ''.join(CL)
    return CLW

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_next_candidate_label_by_discriminator(CLW, dis_bits):

    if CLW.disc + 1 >= 2**dis_bits:
        return None
    else:
        CLW = get_basic_form_of_CL(CLW)
        CLW.disc += 1
        return CLW


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_next_candidate_label(CLW, disc_bits):

    tmp = get_next_candidate_label_by_permuting(CLW)

    if tmp == None:
        tmp = get_next_candidate_label_by_padding(CLW, 3)

    if tmp == None:
        tmp = get_next_candidate_label_by_discriminator(CLW, disc_bits)

    return tmp

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_basic_form_of_CL(CLW):

    CL_lst = sorted(CLW.CL)

    i = 0
    length = len(CL_lst)
    while i < length - 1:
        if CL_lst[i] == CL_lst[i + 1]:
            CL_lst.pop(i + 1)
            length -= 1
        else:
            i += 1

    CLW.CL = ''.join(CL_lst)
    return CLW





myCL = cCL()
myCL.CL = 'ab'
cnt = 0

while myCL != None:
    print myCL.CL, ' (%d)' % myCL.disc
    myCL = get_next_candidate_label(myCL, 2)
    cnt += 1




