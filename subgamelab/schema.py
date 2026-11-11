import json,re
from fractions import Fraction
from itertools import product

def q(x):
    if not isinstance(x,str) or not re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?",x): raise ValueError("canonical rational strings required")
    f=Fraction(x)
    if str(f)!=x or abs(f.numerator)>1000 or f.denominator>1000: raise ValueError("noncanonical or unbounded rational")
    return f

def validate(x):
    if type(x)!=dict or set(x)!={'nodes'} or type(x['nodes'])!=list or not 1<=len(x['nodes'])<=17: raise ValueError("expected 1..17 nodes")
    ns=x['nodes']; parents=[0]*len(ns); dec=[];chance=[]
    for k,n in enumerate(ns):
        if type(n)!=dict: raise ValueError("node object required")
        if set(n)=={'payoff'}:
            if type(n['payoff'])!=list or len(n['payoff'])!=2:raise ValueError("two payoffs required")
            for v in n['payoff']:q(v)
        elif set(n) in ({'player','children'},{'chance','children'}):
            cs=n['children']
            if type(cs)!=list or len(cs)!=2 or any(type(c)!=int or not k<c<len(ns) for c in cs):raise ValueError("two distinct later child indices required")
            for c in cs:parents[c]+=1
            if 'player' in n:
                if type(n['player'])!=int or n['player'] not in (0,1):raise ValueError("player must be 0 or 1")
                dec.append(k)
            else:
                if type(n['chance'])!=list or len(n['chance'])!=2:raise ValueError("two chance probabilities required")
                fs=list(map(q,n['chance']))
                if any(v<0 for v in fs) or sum(fs)!=1:raise ValueError("chance must sum to one")
                chance.append(k)
        else:raise ValueError("invalid node keys")
    if parents!=[0]+[1]*(len(ns)-1) or len(dec)>6 or len(chance)>2:raise ValueError("rooted binary tree, <=6 decisions and <=2 chance nodes required")
    return ns,dec

def plans(keys):return [dict(zip(keys,a)) for a in product(range(2),repeat=len(keys))]
def same(a,b):
    if type(a)!=type(b):return False
    if type(a)==dict:return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if type(a)==list:return len(a)==len(b) and all(same(u,v) for u,v in zip(a,b))
    return a==b

def loads(s):
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise ValueError("duplicate keys")
            d[k]=v
        return d
    if len(s.encode())>8*1024*1024:raise ValueError("input too large")
    return json.loads(s,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError("nonfinite")))
