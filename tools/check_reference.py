"""Optional input-built Nashpy normal-form reference, every proper subtree.
No generator decision is used to construct matrices. Scale exact input-built
rational matrices to integers to remove this corpus's conversion rounding.
Nashpy uses NumPy isclose; this is supplemental numerical evidence, not proof.
"""
import json,math
from fractions import Fraction as F
from itertools import product
import numpy as np,nashpy
from tools.make_cases import corpus
from subgamelab import solve

def assignments(keys):return [dict(zip(keys,a)) for a in product((0,1),repeat=len(keys))]
matrices=checks=profiles=0;maxentry=0
for name,data in corpus():
 ns=data['nodes'];ds=[k for k,n in enumerate(ns) if 'player'in n];paths={}
 def visit(k,path):
  paths[k]=path
  for a,c in enumerate(ns[k].get('children',[])):visit(c,path+[(k,a)])
 visit(0,[]);reference={};report=solve(data)
 for k in range(len(ns)):
  subtree=[j for j in range(len(ns)) if j==k or any(t==k for t,a in paths[j])]
  keys=[[d for d in ds if d in subtree and ns[d]['player']==i] for i in (0,1)]
  ss=[assignments(ks) for ks in keys];pay=[[],[]]
  for row in ss[0]:
   pp=[[],[]]
   for col in ss[1]:
    plan={**row,**col};v=[F(0),F(0)]
    for t in subtree:
     if 'payoff'not in ns[t]:continue
     weight=F(1)
     for node,a in paths[t]:
      if node not in subtree:continue
      weight*=F(ns[node]['chance'][a]) if 'chance'in ns[node] else int(plan[node]==a)
     for i in (0,1):v[i]+=weight*F(ns[t]['payoff'][i])
    for i in (0,1):pp[i].append(v[i])
   for i in (0,1):pay[i].append(pp[i])
  scale=math.lcm(*(x.denominator for a in pay for row in a for x in row));arr=[np.array([[int(x*scale) for x in row] for row in a],dtype=float) for a in pay];maxentry=max(maxentry,max(abs(float(x)) for a in arr for x in a.flat));game=nashpy.Game(*arr);accepted=set()
  for a,row in enumerate(ss[0]):
   for b,col in enumerate(ss[1]):
    sr=np.eye(len(ss[0]))[a];sc=np.eye(len(ss[1]))[b];checks+=1
    if all(game.is_best_response(sr,sc)):accepted.add(tuple(({**row,**col})[d] for d in ds if d in subtree))
  reference[k]=accepted;matrices+=1
 for p in report['profiles']:
  plan=dict(zip(ds,p['actions']));actual=[]
  for k in range(len(ns)):
   subkeys=[d for d in ds if d==k or any(t==k for t,a in paths[d])]
   actual.append(tuple(plan[d] for d in subkeys) in reference[k])
  assert p['nash']==actual[0],(name,p['id'],'root')
  assert p['subgame_perfect']==all(actual),(name,p['id'],'SP')
  profiles+=1
print(json.dumps(dict(reference='Nashpy '+nashpy.__version__,input_built_matrices=matrices,pure_pair_checks=checks,complete_profiles=profiles,max_scaled_abs_entry=maxentry)))
