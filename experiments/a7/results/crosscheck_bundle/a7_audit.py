from pathlib import Path
OUT_DIR = Path(__file__).resolve().parent
"""A7 numerical audit and stronger angular enclosure (CPU NumPy/SciPy)."""
import itertools, json, time, argparse
import numpy as np
from scipy.optimize import minimize
import a7_reference as ref

def tables(xs, eps, P, K=1440, asymmetric=True):
    xs = np.asarray(xs, dtype=float)
    phase0 = ref.psi(xs, 0, 0)
    if np.max(np.abs(np.angle(np.exp(1j * (phase0-phase0[0]))))) > 1e-8:
        raise ValueError('This desired certificate requires a D-aligned candidate family')
    if eps < 0 or K < 3:
        raise ValueError('Require eps >= 0 and K >= 3')
    th = np.linspace(-np.pi, np.pi, K, endpoint=False)
    pp = ref.psi(xs + eps, 0, 0); pm = ref.psi(xs - eps, 0, 0)
    p0 = ref.psi(xs, 0, 0)
    bd = np.maximum(pp-p0, p0-pm)
    if np.any(bd > np.pi/2 + 1e-12):
        raise ValueError('Desired projection certificate needs beta_D <= pi/2')
    c = ref.amp_range(xs, eps, 0, 0)[0] * np.cos(bd)
    p0=ref.psi(xs,*P); pp=ref.psi(xs+eps,*P); pm=ref.psi(xs-eps,*P)
    if asymmetric:
        phi=-(pp+pm)/2; bp=(pp-pm)/2
    else:
        phi=-p0; bp=np.maximum(pp-p0,p0-pm)
    amin,amax=ref.amp_range(xs,eps,*P)
    gap=np.maximum(np.abs(np.angle(np.exp(1j*(th[None]-phi[:,None]))))-bp[:,None],0)
    mc=np.cos(gap)
    s=np.where(mc>=0, amax[:,None]*mc,amin[:,None]*mc)
    return dict(cD=c,s=s,amax=amax,zD=ref.z(xs,0,0),zP=ref.z(xs,*P),K=K,eps=eps,valid=True,xs=xs.copy())

def cert(S,T,N,s2,mode='sec'):
    S=np.atleast_2d(S)
    c=T['cD'][S].sum(1)
    if T['eps']==0:
        B=np.abs(T['zP'][S].sum(1))
    else:
        m=T['s'][S].sum(1).max(1)
        if mode=='sec': B=m/np.cos(np.pi/T['K'])
        elif mode=='pad': B=m+T['amax'][S].sum(1)*np.pi/T['K']
        else: raise ValueError(mode)
        B=np.maximum(B,0)
    return c*c/(N*s2+B*B)

def feasible(S,xs,eps,dmin=0.5*ref.LAM):
    S=np.atleast_2d(S)
    return np.all(np.diff(xs[S],axis=1)>=dmin+2*eps-1e-14,axis=1)

def search(T,N,s2,allS,init,seed=0,restarts=8,forced=(),mode='sec'):
    rng=np.random.default_rng(seed); best=None; bestv=-np.inf
    starts=[np.sort(init)]+[allS[k] for k in rng.integers(0,len(allS),size=restarts)]
    # allS must represent cardinality, robust-clearance, and forced-site constraints.
    M=len(T['cD'])
    for S in starts:
        S=S.copy(); v=cert(S,T,N,s2,mode)[0]
        while True:
            outsiders=np.setdiff1d(np.arange(M),S)
            cand=[]
            for i in range(N):
                if int(S[i]) in forced: continue
                for j in outsiders:
                    Q=S.copy(); Q[i]=j; Q=np.sort(Q)
                    cand.append(Q)
            if not cand: break
            cand=np.asarray(cand)
            cand=cand[feasible(cand,T['xs'],T['eps'])]
            if not len(cand): break
            vv=cert(cand,T,N,s2,mode); k=np.argmax(vv)
            if vv[k] <= v+1e-12: break
            S,v=cand[k],vv[k]
        if v>bestv: best,bestv=S,v
    return best,float(bestv)

def exact_at(xs,S,delta,P,N,s2):
    D=np.atleast_2d(delta)
    hD=ref.z(xs[S][None]+D,0,0).sum(1)
    hP=ref.z(xs[S][None]+D,*P).sum(1)
    GD=np.abs(hD)**2/N; IP=np.abs(hP)**2/N
    return GD/(s2+IP),GD,IP

def witnesses(xs,S,eps,P,N,s2,refine=0):
    corners=np.array(list(itertools.product((-1.,1.),repeat=N)))
    vv,_,_=exact_at(xs,S,eps*corners,P,N,s2)
    k=np.argmin(vv); U=float(vv[k]); delta=eps*corners[k]
    if eps>0:
        for k in np.argsort(vv)[:refine]:
            # Optimize dimensionless errors to avoid scaling problems.
            result=minimize(lambda u:exact_at(xs,S,eps*u,P,N,s2)[0][0],corners[k],method='L-BFGS-B',bounds=[(-1,1)]*N,options={'maxiter':150,'ftol':1e-12})
            u=np.clip(result.x,-1,1)
            val=exact_at(xs,S,eps*u,P,N,s2)[0][0]
            if val<U: U=float(val);delta=eps*u
    return U,delta

def second_derivative_bound(x,eps,P):
    ux,uy=P; b=np.sqrt(uy*uy+ref.D_H**2)
    lo=x-eps-ux;hi=x+eps-ux
    qmin=np.maximum(np.maximum(lo,-hi),0)
    rmin=np.sqrt(qmin*qmin+b*b)
    tlo=lo/np.sqrt(lo*lo+b*b);thi=hi/np.sqrt(hi*hi+b*b)
    T=np.maximum(np.abs(tlo),np.abs(thi));v=ref.K0*(ref.NEFF+thi)
    A2=np.maximum(np.abs(3*np.minimum(tlo*tlo,thi*thi)-1),np.abs(3*T*T-1))
    # Use the globally safe A'' bound 2/rmin^3.
    return np.sqrt((2/rmin**3+v*v/rmin)**2+(2*T*v/rmin**2+ref.K0/rmin**2)**2)

def audit_one():
    M,N=24,8;xs=ref.aligned_sites(M);Aref=abs(ref.z(xs[8:16],0,0).sum())**2/N
    P=(3.,2.);eps=.05*ref.LAM;s2=Aref/1e3
    allS=np.array(list(itertools.combinations(range(M),N)),dtype=np.int16)
    T0=ref.tables(xs,eps,P);SN=ref.exhaustive_nominal(T0,M,N,s2)
    SR0=ref.swap_search(lambda S:ref.cert_L(S,T0,N,s2),M,N,SN,np.random.default_rng(0))
    T=tables(xs,eps,P)
    SR,LR=search(T,N,s2,allS,SN)
    UN,dn=witnesses(xs,SN,eps,P,N,s2,refine=8)
    UR,dr=witnesses(xs,SR,eps,P,N,s2,refine=8)
    matched=allS[(allS[:,0]==0)&(allS[:,-1]==M-1)]
    SNm=matched[np.argmax(ref.nominal(matched,T,N,s2))]
    SRm,LRm=search(T,N,s2,matched,SNm,forced=(0,23))
    UNm,_=witnesses(xs,SNm,eps,P,N,s2,refine=8)
    URm,_=witnesses(xs,SRm,eps,P,N,s2,refine=8)
    Tz=tables(xs,0,P);Tzold=ref.tables(xs,0,P)
    vnom=ref.nominal(SN[None],Tz,N,s2)[0]; vzero=cert(SN,Tz,N,s2)[0]; vold=ref.cert_L(SN[None],Tzold,N,s2)[0]
    rng=np.random.default_rng(20260926);checks=0;min_slack=np.inf
    for S in (SN,SR,SNm,SRm):
        for ee in (0,.01,.03,.05,.08):
            e=ee*ref.LAM; TT=tables(xs,e,P);L=cert(S,TT,N,s2)[0]
            DD=rng.uniform(-e,e,size=(5000,N)); vv,_,_=exact_at(xs,S,DD,P,N,s2)
            min_slack=min(min_slack,float(np.min(vv)-L));checks+=len(vv)
    # Finite-epsilon nonlinear endpoint converse and fully explicit Taylor converse.
    zp=ref.z(xs+eps,*P);zm=ref.z(xs-eps,*P);m=(zp+zm)/2;d=(zp-zm)/2
    endpoint_per_subset=np.abs(m[allS].sum(1))**2+(np.abs(d[allS])**2).sum(1)
    F=endpoint_per_subset.min()/N;bestfloor=allS[endpoint_per_subset.argmin()]
    simplefloor=np.sort(np.abs(d)**2)[:N].sum()/N
    x=xs[SN];rr=ref.R(x,*P);t=(x-P[0])/rr
    bder=np.exp(-1j*ref.psi(x,*P))*(-t/rr**2-1j*ref.K0*(ref.NEFF+t)/rr)
    rho=.5*eps*eps*second_derivative_bound(x,eps,P).sum()
    h0=ref.z(x,*P).sum();linear_converse=max(np.sqrt(abs(h0)**2+eps*eps*(abs(bder)**2).sum())-rho,0)**2/N
    corner=np.array(list(itertools.product((-1,1),repeat=N)))*eps
    _,_,Icorn=exact_at(xs,SN,corner,P,N,s2)
    out={
      'original':{'SN':SN.tolist(),'SR':SR0.tolist(),'LR':float(ref.cert_L(SR0[None],T0,N,s2)[0]),'UN_corners':ref.witness_U(xs,SN,eps,P,N,s2)},
      'sec_asymmetric':{'SR':SR.tolist(),'LR':LR,'UN_refined':UN,'UR_refined':UR,'gain':LR/UN-1},
      'matched':{'family_size':len(matched),'SN':SNm.tolist(),'SR':SRm.tolist(),'LR':LRm,'UN':UNm,'UR':URm,'gain':LRm/UNm-1},
      'epsilon_zero':{'nominal':vnom,'corrected':vzero,'original':vold,'relative_original_loss':1-vold/vnom},
      'converse':{'family_exact_endpoint_floor_power':float(F),'minimizing_subset':bestfloor.tolist(),'additive_floor_power':float(simplefloor),'SN_taylor_floor_power':float(linear_converse),'SN_endpoint_floor_power':float((abs(m[SN].sum())**2+(abs(d[SN])**2).sum())/N),'SN_max_corner_power':float(Icorn.max())},
      'random_checks':{'count':checks,'min_SLNR_minus_L':min_slack},
      'clearance':{'min_spacing_lambda':float(np.diff(xs).min()/ref.LAM),'all_subsets_valid_eps_limit_lambda':float((np.diff(xs).min()/ref.LAM-.5)/2),'feasible_at_0p1_lambda':int(feasible(allS,xs,.1*ref.LAM).sum()),'SN_valid_at_0p1':bool(feasible(SN,xs,.1*ref.LAM)[0]),'SR_valid_at_0p1':bool(feasible(SR0,xs,.1*ref.LAM)[0])},
      'grid_relative_power_gap_bound':float(1/np.cos(np.pi/1440)**2-1),
      'coefficient_ratio':float((np.sort(T['cD'])[:N].sum()/np.sort(T['cD'])[-N:].sum())**2)
    }
    print(json.dumps(out,indent=2));open(OUT_DIR / 'a7_audit_results.json','w').write(json.dumps(out,indent=2))

if __name__=='__main__':audit_one()
