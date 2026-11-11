import unittest,json,copy,random
from fractions import Fraction
from itertools import product
from subgamelab import solve,verify
from subgamelab.verify import reconstruct
from subgamelab.schema import loads
from tools.make_cases import controls,corpus,move,leaf,flatten
class Checks(unittest.TestCase):
 def test_full_corpus(self):
  for n,x in corpus():self.assertEqual(solve(x),reconstruct(x),n)
 def test_threat(self):
  r=solve(controls()[0][1]);self.assertEqual(r['nash_ids'],[0,3]);self.assertEqual(r['subgame_perfect_ids'],[3]);self.assertEqual(r['profiles'][0]['local'][1]['continuation_gain'],'2');self.assertEqual(r['profiles'][0]['local'][1]['root_gain'],'0')
 def test_joint_deviation(self):
  r=solve(controls()[1][1]);p=r['profiles'][0];self.assertTrue(p['root_one_node_stable']);self.assertFalse(p['nash']);self.assertEqual(p['audits'][0]['gain'],'2')
 def test_chance_zero(self):
  r=solve(controls()[2][1]);self.assertEqual(r['nash_ids'],[0,1]);self.assertEqual(r['subgame_perfect_ids'],[1]);self.assertEqual(r['profiles'][0]['reach'][2],'0')
 def test_ties(self):
  r=solve(controls()[3][1]);self.assertEqual(r['subgame_perfect_ids'],[0,3]);self.assertEqual(len(solve(controls()[4][1])['subgame_perfect_ids']),8)
 def test_terminal(self):
  r=solve(controls()[6][1]);self.assertEqual(r['profiles'][0]['values'],[['-2','3']]);self.assertTrue(verify(r))
 def test_exhaustive_two_decisions(self):
  count=0
  for ps in product(range(2),repeat=2):
   for vals in product((-1,0,1),repeat=6):
    x=flatten(move(ps[0],leaf(*vals[:2]),move(ps[1],leaf(*vals[2:4]),leaf(*vals[4:]))));self.assertEqual(solve(x),reconstruct(x));count+=1
  self.assertEqual(count,2916)
 def test_positive_affine_payoffs(self):
  for _,x in corpus():
   y=copy.deepcopy(x)
   for n in y['nodes']:
    if 'payoff'in n:n['payoff']=[str(2*Fraction(n['payoff'][0])+3),str(3*Fraction(n['payoff'][1])-2)]
   a,b=solve(x),solve(y)
   for key in ['nash_ids','subgame_perfect_ids','root_one_node_stable_ids']:self.assertEqual(a[key],b[key])
 def test_player_swap(self):
  for _,x in controls():
   y=copy.deepcopy(x)
   for n in y['nodes']:
    if 'payoff'in n:n['payoff'].reverse()
    if 'player'in n:n['player']=1-n['player']
   a,b=solve(x),solve(y)
   for key in ['nash_ids','subgame_perfect_ids','root_one_node_stable_ids']:self.assertEqual(a[key],b[key])
 def test_no_mutation(self):
  x=controls()[0][1];y=copy.deepcopy(x);r=solve(x);verify(r);self.assertEqual(x,y)
 def test_input_validation(self):
  for x in [{},{'nodes':[]},{'nodes':[{'payoff':[True,'0']}]},{'nodes':[{'payoff':['-0','0']}]},{'nodes':[{'payoff':['2/4','0']}]},{'nodes':[{'chance':['1/2','1/3'],'children':[1,2]},{'payoff':['0','0']},{'payoff':['0','0']}]},{'nodes':[{'player':True,'children':[1,2]},{'payoff':['0','0']},{'payoff':['0','0']}]},{'nodes':[{'player':0,'children':[1,1]},{'payoff':['0','0']}]},{'nodes':[{'payoff':['0','0']},{'payoff':['0','0']}]}]:
   with self.assertRaises(ValueError):solve(x)
 def test_duplicate_json(self):
  with self.assertRaises(ValueError):loads('{"nodes":[],"nodes":[]}')
 def test_certificate_type_and_shape(self):
  r=solve(controls()[0][1]);r['nash_ids'][0]=False
  with self.assertRaises(ValueError):verify(r)
  for edit in [lambda r:r.update(extra=0),lambda r:r['profiles'].reverse(),lambda r:r['profiles'].pop(),lambda r:r['backward_induction'][0]['plans'].append([0,0])]:
   r=solve(controls()[0][1]);edit(r)
   with self.assertRaises(ValueError):verify(r)
 def test_primitive_tampering(self):
  r=solve(controls()[0][1]);count=0
  def visit(x,path):
   nonlocal count
   if isinstance(x,dict):
    for k,v in x.items():
     if path or k!='input':visit(v,path+[k])
   elif isinstance(x,list):
    for i,v in enumerate(x):visit(v,path+[i])
   else:
    f=copy.deepcopy(r);t=f
    for k in path[:-1]:t=t[k]
    t[path[-1]]=not x if type(x)==bool else x+1 if type(x)==int else x+'!'
    with self.assertRaises(ValueError):verify(f)
    count+=1
  visit(r,[]);print('primitive forgeries:',count);self.assertGreater(count,200)
if __name__=='__main__':unittest.main()
