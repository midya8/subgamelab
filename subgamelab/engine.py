from fractions import Fraction
from itertools import product
from .schema import validate,q,plans

def solve(data):
    ns,ds=validate(data); positions={k:i for i,k in enumerate(ds)}
    descendants={}
    for k in reversed(range(len(ns))):descendants[k]=[k]+sum((descendants[c] for c in ns[k].get('children',[])),[])
    def values(plan):
        vs={}
        for k in reversed(range(len(ns))):
            n=ns[k]
            if 'payoff'in n:vs[k]=list(map(q,n['payoff']))
            elif 'player'in n:vs[k]=vs[n['children'][plan[k]]]
            else:vs[k]=[sum(q(p)*vs[c][i] for p,c in zip(n['chance'],n['children'])) for i in range(2)]
        return vs
    # Backward-induction correspondence: Cartesian product of complete child plans,
    # then every maximizing root action, not separate coordinatewise payoff maxima.
    bi={}
    for k in reversed(range(len(ns))):
        n=ns[k]
        if 'payoff'in n:bi[k]=[{}];continue
        out=[]
        for parts in product(*(bi[c] for c in n['children'])):
            base={a:b for part in parts for a,b in part.items()}
            if 'chance'in n:out.append(base);continue
            vals=[]
            for a in range(2):vals.append(values({**{d:0 for d in ds},**base,k:a})[k][n['player']])
            out.extend({**base,k:a} for a,v in enumerate(vals) if v==max(vals))
        bi[k]=out
    rows=[]
    for index,plan in enumerate(plans(ds)):
        vs=values(plan);reach=[Fraction(0) for _ in ns];reach[0]=Fraction(1)
        for k,n in enumerate(ns):
            if 'player'in n:reach[n['children'][plan[k]]]+=reach[k]
            elif 'chance'in n:
                for p,c in zip(n['chance'],n['children']):reach[c]+=reach[k]*q(p)
        local=[]
        for k in ds:
            a=1-plan[k];i=ns[k]['player'];alt=values({**plan,k:a})
            local.append({'node':k,'player':i,'chosen':plan[k],'alternative':a,'continuation_gain':str(alt[k][i]-vs[k][i]),'root_gain':str(alt[0][i]-vs[0][i]),'reach':str(reach[k])})
        audits=[]
        for k,n in enumerate(ns):
            if 'payoff'in n:continue
            for i in range(2):
                keys=[d for d in ds if d in descendants[k] and ns[d]['player']==i]
                candidates=[]
                for alt in plans(keys):
                    val=values({**plan,**alt})[k][i]
                    candidates.append({'actions':[alt[d] for d in keys],'payoff':str(val)})
                best=max(q(c['payoff']) for c in candidates)
                audits.append({'node':k,'player':i,'decision_nodes':keys,'current':str(vs[k][i]),'best':str(best),'gain':str(best-vs[k][i]),'alternatives':candidates,'maximizers':[c['actions'] for c in candidates if q(c['payoff'])==best]})
        root=[a for a in audits if a['node']==0]
        # A terminal-root game has no deviations.
        rows.append({'id':index,'actions':[plan[d] for d in ds],'values':[[str(v) for v in vs[k]] for k in range(len(ns))],'reach':[str(r) for r in reach],'local':local,'audits':audits,'root_one_node_stable':all(q(a['root_gain'])<=0 for a in local),'nash':all(q(a['gain'])==0 for a in root),'subgame_perfect':all(q(a['gain'])==0 for a in audits)})
    sp=[r['id'] for r in rows if r['subgame_perfect']]
    bid=sorted(sum(p[d]*2**(len(ds)-1-j) for j,d in enumerate(ds)) for p in bi[0])
    assert sp==bid
    return {'schema':'subgamelab/1','input':data,'decision_nodes':ds,'profiles':rows,'nash_ids':[r['id'] for r in rows if r['nash']],'root_one_node_stable_ids':[r['id'] for r in rows if r['root_one_node_stable']],'subgame_perfect_ids':sp,'backward_induction':[{'node':k,'decision_nodes':[d for d in ds if d in descendants[k]],'plans':sorted([[p[d] for d in ds if d in descendants[k]] for p in bi[k]])} for k in range(len(ns))]}
