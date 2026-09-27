from pathlib import Path
OUT_DIR = Path(__file__).resolve().parent
"""Extra tests of analytic curvature bounds and endpoint witness compression.
These are floating-point regression checks, not interval-arithmetic proofs.
"""
import json, itertools, numpy as np
import a7_reference as ref
from a7_global import endpoint_bank

def explicit_H(xs,eps,P):
    ux,uy=P; b=np.sqrt(uy*uy+ref.D_H**2)
    lo=xs-eps-ux;hi=xs+eps-ux
    vmin=np.maximum(np.maximum(lo,-hi),0.)
    rmin=np.sqrt(b*b+vmin*vmin)
    tl=lo/np.sqrt(lo*lo+b*b);tu=hi/np.sqrt(hi*hi+b*b)
    C=np.maximum(abs(3*tl*tl-1),abs(3*tu*tu-1))
    C=np.where((tl<=0)&(tu>=0),np.maximum(C,1.),C)
    f=lambda t:1-3*t*t-2*ref.NEFF*t
    E=np.maximum(abs(f(tl)),abs(f(tu)))
    tc=-ref.NEFF/3
    E=np.where((tl<=tc)&(tc<=tu),np.maximum(E,abs(f(tc))),E)
    V=ref.K0*(ref.NEFF+tu)
    return np.sqrt((C/rmin**3+V*V/rmin)**2+(ref.K0*E/rmin**2)**2)

def analytic_z2(x,P):
    r=ref.R(x,*P);t=(x-P[0])/r;k=ref.K0;n=ref.NEFF
    return np.exp(-1j*ref.psi(x,*P))*((3*t*t-1)/r**3-k*k*(n+t)**2/r-1j*k*(1-3*t*t-2*n*t)/r**2)

xs=ref.aligned_sites(24);rng=np.random.default_rng(9);maxratio=0.;nchecks=0;err=0.
for P in [(-5.,0.),(0.,0.),(3.,2.),(5.,4.)]:
    for e in [.01,.05,.10,.20]:
        eps=e*ref.LAM;H=explicit_H(xs,eps,P)
        xx=xs[:,None]+np.linspace(-eps,eps,1001)[None]
        maxratio=max(maxratio,float(np.max(abs(analytic_z2(xx,P))/H[:,None])))
        nchecks+=xx.size
    eps=.05*ref.LAM;_,_,ZP=endpoint_bank(xs,eps,P)
    corners=np.array(list(itertools.product([-1.,1.],repeat=8)))*eps
    for _ in range(10):
        S=np.sort(rng.choice(24,8,replace=False))
        bank=np.max(abs(ZP[S].sum(0))**2)
        full=np.max(abs(ref.z(xs[S][None]+corners,*P).sum(1))**2)
        err=max(err,abs(bank-full))
# Check the original support formula against fine brute-force phase/radius sampling,
# explicitly including cases with negative support.
maxsupporterror=0.;negative=0
for _ in range(100):
    amin=rng.uniform(.05,.5);amax=amin+rng.uniform(0,.5)
    phi=rng.uniform(-np.pi,np.pi);beta=rng.uniform(0,1.4);th=rng.uniform(-np.pi,np.pi)
    gap=max(abs(np.angle(np.exp(1j*(th-phi))))-beta,0.)
    mc=np.cos(gap);formula=(amax if mc>=0 else amin)*mc
    phases=np.linspace(phi-beta,phi+beta,2001)
    brute=max(np.max(amin*np.cos(phases-th)),np.max(amax*np.cos(phases-th)))
    maxsupporterror=max(maxsupporterror,float(brute-formula))
    negative+=formula<0
out={'curvature_grid_points':nchecks,'max_sampled_abs_z2_over_explicit_H':maxratio,'endpoint_vertex_checks':40,'max_squared_field_discrepancy':err,'sector_support_cases':100,'negative_support_cases':int(negative),'max_bruteforce_minus_support':maxsupporterror}
print(json.dumps(out,indent=2))
open(OUT_DIR / 'a7_unit_checks_results.json','w').write(json.dumps(out,indent=2))
