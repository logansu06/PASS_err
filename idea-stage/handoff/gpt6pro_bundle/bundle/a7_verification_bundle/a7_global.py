from pathlib import Path
OUT_DIR = Path(__file__).resolve().parent
"""Finite-family global audit with a shared feasible endpoint-witness bank.
All reported global bounds are exact-arithmetic statements evaluated in float64,
not machine-verified interval certificates.
"""
import numpy as np,itertools,time,json
import a7_reference as ref
import a7_audit as a

def endpoint_bank(xs,eps,P):
    zp=ref.z(xs+eps,*P);zm=ref.z(xs-eps,*P);d=(zp-zm)/2
    angles=np.mod(np.r_[np.angle(d)+np.pi/2,np.angle(d)-np.pi/2],2*np.pi)
    breaks=np.unique(angles);th=(breaks+np.r_[breaks[1:],breaks[0]+2*np.pi])/2
    signs=np.where(np.real(d[:,None]*np.exp(-1j*th[None]))>=0,1.,-1.)
    ZP=ref.z(xs[:,None]+eps*signs,*P)
    ZD=ref.z(xs[:,None]+eps*signs,0,0)
    return signs,ZD,ZP

def global_audit(P=(3.,2.),ee=.05,snr=30):
    t0=time.perf_counter();M,N=24,8;xs=ref.aligned_sites(M);eps=ee*ref.LAM
    ar=abs(ref.z(xs[8:16],0,0).sum())**2/N;s2=ar/10**(snr/10)
    allS=np.array(list(itertools.combinations(range(M),N)),dtype=np.int16)
    allS=allS[a.feasible(allS,xs,eps)]
    matched=(allS[:,0]==0)&(allS[:,-1]==23)
    signs,ZD,ZP=endpoint_bank(xs,eps,P);H=ZD.shape[1]
    UU=np.empty(len(allS));EE=np.empty(len(allS))
    for start in range(0,len(allS),4096):
        SS=allS[start:start+4096]
        hp=ZP[SS].sum(1);hd=ZD[SS].sum(1)
        pp=abs(hp)**2;dd=abs(hd)**2
        UU[start:start+len(SS)]=np.min(dd/(N*s2+pp),axis=1)
        EE[start:start+len(SS)]=np.max(pp,axis=1)/N
    witness_elapsed=time.perf_counter()-t0
    out={'P':P,'eps_lambda':ee,'snr_db':snr,'H':H,'witness_enumeration_seconds':witness_elapsed}
    T=a.tables(xs,eps,P)
    rng=np.random.default_rng(17)
    err=0.
    corners=np.array(list(itertools.product((-1.,1.),repeat=N)))*eps
    for S in allS[rng.choice(len(allS),20,replace=False)]:
        _,_,ip=a.exact_at(xs,S,corners,P,N,s2)
        ipbank=np.max(abs(ZP[S].sum(0))**2)/N
        err=max(err,abs(ip.max()-ipbank))
    out['max_endpoint_vertex_identity_error_20_subsets']=err
    for name,mask,forced in [('free',np.ones(len(allS),bool),()),('matched',matched,(0,23))]:
        SS=allS[mask];uu=UU[mask];eev=EE[mask]
        SN=SS[np.argmax(ref.nominal(SS,T,N,s2))]
        SR,inc=a.search(T,N,s2,SS,SN,forced=forced)
        initial_L=inc;initial_SR=SR.copy()
        survivors=np.flatnonzero(uu>inc)
        ts=time.perf_counter()
        # Safe pruning: all discarded layouts have W <= U <= incumbent L.
        for start in range(0,len(survivors),128):
            ii=survivors[start:start+128]
            active=ii[uu[ii]>inc]
            if not len(active):continue
            vv=a.cert(SS[active],T,N,s2)
            k=np.argmax(vv)
            if vv[k]>inc:inc=float(vv[k]);SR=SS[active[k]]
        rivals=np.any(SS!=SR,axis=1)
        rival_U=float(uu[rivals].max())
        global_U=float(uu.max());UN,_=a.witnesses(xs,SN,eps,P,N,s2,refine=4)
        UR,_=a.witnesses(xs,SR,eps,P,N,s2,refine=8)
        # Leakage achievability for the best certificate subset.
        B=T['s'][SR].sum(0).max()/np.cos(np.pi/T['K'])
        out[name]={'family_size':len(SS),'nominal_subset':SN.tolist(),'initial_subset':initial_SR.tolist(),'initial_L':initial_L,'survivors_initial':len(survivors),'certificate_optimum_subset':SR.tolist(),'certificate_optimum_L':inc,'global_robust_SLNR_upper':global_U,'global_relative_upper_gap':global_U/inc-1,'largest_other_layout_U':rival_U,'strict_global_layout_dominance_margin':inc-rival_U,'unpruned_after_search':int(np.sum(uu>inc)),'certified_gain_over_nominal':inc/UN-1,'UN_nominal':UN,'UR_robust':UR,'minimum_endpoint_worst_leakage_power':float(eev.min()),'minimum_endpoint_subset':SS[np.argmin(eev)].tolist(),'selected_leakage_upper_power':float(B*B/N),'survivor_evaluation_seconds':time.perf_counter()-ts}
    out['total_seconds']=time.perf_counter()-t0
    print(json.dumps(out,indent=2))
    open(OUT_DIR / 'a7_global_results.json','w').write(json.dumps(out,indent=2))
if __name__=='__main__':global_audit()
