import json,random
from pathlib import Path

def leaf(a,b):return {'payoff':[str(a),str(b)]}
def move(p,a,b):return {'player':p,'branches':[a,b]}
def chance(q,a,b):return {'chance':q,'branches':[a,b]}
def flatten(root):
    nodes=[]
    def walk(n):
        k=len(nodes);nodes.append({})
        if 'payoff'in n:nodes[k]=n.copy()
        else:
            cs=[walk(c) for c in n['branches']];nodes[k]={a:b for a,b in n.items() if a!='branches'};nodes[k]['children']=cs
        return k
    walk(root);return {'nodes':nodes}

def controls():
    return [(name,flatten(tree)) for name,tree in [
      ('Empty threat',move(0,leaf(1,4),move(1,leaf(-1,0),leaf(3,2)))),
      ('Joint deviation escapes one-node trap',move(0,leaf(1,0),move(0,leaf(0,0),leaf(3,0)))),
      ('Chance-zero still has a subgame',chance(['1','0'],leaf(2,2),move(1,leaf(0,0),leaf(0,5)))),
      ('Tie changes earlier incentives',move(0,leaf(2,0),move(1,leaf(1,3),leaf(4,3)))),
      ('All ties',move(0,move(1,leaf(0,0),leaf(0,0)),move(1,leaf(0,0),leaf(0,0)))),
      ('Rational chance',chance(['1/3','2/3'],move(0,leaf('-1/2','3/4'),leaf('1/2','-3/4')),move(1,leaf(2,-1),leaf(-2,1)))),
      ('Terminal only',leaf(-2,3)),
      ('One player only',move(1,leaf(2,2),leaf(1,3))),
      ('Boundary six decisions',move(0,move(1,move(0,leaf(1,2),leaf(3,0)),move(1,leaf(4,-1),leaf(-2,4))),move(0,move(1,leaf(5,5),leaf(0,6)),leaf(2,3)))),
      ('Zero and unit chances',chance(['0','1'],move(0,leaf(5,1),leaf(1,5)),chance(['1','0'],move(1,leaf(3,2),leaf(2,3)),leaf(0,0))))
    ]]
def corpus():
    rng=random.Random(4281);out=controls()
    for t in range(55):
        budget=1+t%6
        def tree(b):
            if not b:return leaf(rng.randrange(-3,4),rng.randrange(-3,4))
            left=rng.randrange(b);return move(rng.randrange(2),tree(left),tree(b-1-left))
        r=tree(budget)
        if t%3==0:r=chance(['1/2','1/2'],r,leaf(rng.randrange(-2,3),rng.randrange(-2,3)))
        out.append((f'Seeded {t}',flatten(r)))
    return out
if __name__=='__main__':
    from subgamelab import solve
    Path('docs/cases.json').write_text(json.dumps([{'name':n,'input':x} for n,x in controls()],indent=2)+'\n')
