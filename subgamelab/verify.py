# Independent replay: leaf-path enumeration and full unilateral plan census.
# Does not import the recursive generator or its backward-induction routine.
from fractions import Fraction
from itertools import product
from .schema import validate,q,plans,same

def reconstruct(data):
    ns,ds=validate(data); paths={};desc={}
    def walk(k,path):
        paths[k]=path
        for a,c in enumerate(ns[k].get('children',[])):walk(c,path+[(k,a)])
    walk(0,[])
    for k in range(len(ns)):desc[k]=[t for t in range(len(ns)) if t==k or any(v==k for v,a in paths[t])]
    def mass(path,plan):
        z=Fraction(1)
        for k,a in path:
            n=ns[k]
            z*=q(n['chance'][a]) if 'chance'in n else int(plan[k]==a)
        return z
    def ev(k,plan):
        out=[Fraction(0),Fraction(0)]
        for t in desc[k]:
            if 'payoff'not in ns[t]:continue
            path=[(v,a) for v,a in paths[t] if v in desc[k]]
            m=mass(path,plan)
            for i in range(2):out[i]+=m*q(ns[t]['payoff'][i])
        return out
    profiles=[]
    for idx,plan in enumerate(plans(ds)):
        vals=[ev(k,plan) for k in range(len(ns))];reach=[mass(paths[k],plan) for k in range(len(ns))]
        local=[];audits=[]
        for k in ds:
            i=ns[k]['player'];alt={**plan,k:1-plan[k]}
            local.append(dict(node=k,player=i,chosen=plan[k],alternative=1-plan[k],continuation_gain=str(ev(k,alt)[i]-vals[k][i]),root_gain=str(ev(0,alt)[i]-vals[0][i]),reach=str(reach[k])))
        for k,n in enumerate(ns):
            if 'payoff'in n:continue
            for i in (0,1):
                keys=[d for d in ds if d in desc[k] and ns[d]['player']==i]
                cs=[{'actions':[a[d] for d in keys],'payoff':str(ev(k,{**plan,**a})[i])} for a in plans(keys)]
                best=max(q(c['payoff']) for c in cs)
                audits.append(dict(node=k,player=i,decision_nodes=keys,current=str(vals[k][i]),best=str(best),gain=str(best-vals[k][i]),alternatives=cs,maximizers=[c['actions'] for c in cs if q(c['payoff'])==best]))
        profiles.append(dict(id=idx,actions=[plan[d] for d in ds],values=[[str(v) for v in vs] for vs in vals],reach=[str(r) for r in reach],local=local,audits=audits,root_one_node_stable=not any(q(a['root_gain'])>0 for a in local),nash=not any(a['node']==0 and q(a['gain'])>0 for a in audits),subgame_perfect=not any(q(a['gain'])>0 for a in audits)))
    # Every subgame's equilibrium plans by direct all-player deviations, no induction.
    bi=[]
    for k in range(len(ns)):
        keys=[d for d in ds if d in desc[k]];accepted=[]
        for p in plans(keys):
            full={**{d:0 for d in ds},**p};ok=True
            for t in desc[k]:
                if 'payoff'in ns[t]:continue
                for i in (0,1):
                    own=[d for d in keys if d in desc[t] and ns[d]['player']==i];cur=ev(t,full)[i]
                    if any(ev(t,{**full,**a})[i]>cur for a in plans(own)):ok=False;break
                if not ok:break
            if ok:accepted.append([p[d] for d in keys])
        bi.append(dict(node=k,decision_nodes=keys,plans=accepted))
    return dict(schema='subgamelab/1',input=data,decision_nodes=ds,profiles=profiles,nash_ids=[r['id'] for r in profiles if r['nash']],root_one_node_stable_ids=[r['id'] for r in profiles if r['root_one_node_stable']],subgame_perfect_ids=[r['id'] for r in profiles if r['subgame_perfect']],backward_induction=bi)

def verify(report):
    if type(report)!=dict or 'input'not in report:raise ValueError('certificate object required')
    expected=reconstruct(report['input'])
    if not same(report,expected):raise ValueError('certificate mismatch')
    return True
