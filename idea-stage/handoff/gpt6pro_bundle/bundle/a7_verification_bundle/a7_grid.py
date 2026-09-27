from pathlib import Path
OUT_DIR = Path(__file__).resolve().parent
"""Independent audit grid: not a reproduction of the user's unspecified 528 cases."""
import a7_reference as ref
import a7_audit as a
import numpy as np,itertools,json,time,sys
M,N=24,8;xs=ref.aligned_sites(M);Aref=abs(ref.z(xs[8:16],0,0).sum())**2/N
allS=np.array(list(itertools.combinations(range(M),N)),dtype=np.int16)
matched=allS[(allS[:,0]==0)&(allS[:,-1]==23)]
settings=[(20,.03),(20,.05),(30,.03),(30,.05)]
# First argument selects 11 geometries at one y coordinate.
iy=int(sys.argv[1]); y=[0.,2.,4.][iy]
rows=[];t0=time.perf_counter()
for x in np.arange(-5.,6.):
    P=(float(x),y);Tnom=a.tables(xs,0,P)
    nomfree=abs(Tnom['zD'][allS].sum(1))**2/N;ipfree=abs(Tnom['zP'][allS].sum(1))**2/N
    nommat=abs(Tnom['zD'][matched].sum(1))**2/N;ipmat=abs(Tnom['zP'][matched].sum(1))**2/N
    for snr,ee in settings:
        eps=ee*ref.LAM;s2=Aref/10**(snr/10);T=a.tables(xs,eps,P)
        for fam,SS,dd,pp,forced in [('free',allS,nomfree,ipfree,()),('matched',matched,nommat,ipmat,(0,23))]:
            SN=SS[np.argmax(dd/(s2+pp))]
            SR,LR=a.search(T,N,s2,SS,SN,seed=20260926,restarts=8,forced=forced)
            UN,_=a.witnesses(xs,SN,eps,P,N,s2)
            UR,_=a.witnesses(xs,SR,eps,P,N,s2)
            rows.append(dict(xP=x,yP=y,snr_db=snr,eps_lambda=ee,family=fam,SN=SN.tolist(),SR=SR.tolist(),LR=LR,UN=UN,UR=UR,gain=LR/UN-1,bracket=UR/LR))
    print('completed P',P, 'elapsed',round(time.perf_counter()-t0,2),flush=True)
open(OUT_DIR / ('a7_grid_part%d.json'%iy),'w').write(json.dumps(rows,indent=2))
for snr,ee in settings:
    for fam in ['free','matched']:
        rr=[r for r in rows if r['family']==fam and r['snr_db']==snr and r['eps_lambda']==ee]
        g=np.array([r['gain'] for r in rr]);print(snr,ee,fam,'positive',sum(g>1e-10),'>5%',sum(g>.05),'median',np.median(g))
