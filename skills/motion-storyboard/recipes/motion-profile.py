# Motion profile: per-clip motion events, still share and ease shape from frame differences.
# Usage: python3 motion-profile.py clip1.mp4 clip2.mp4 ...   (needs ffmpeg, ffprobe, numpy)
import subprocess,sys,numpy as np,json
def frames(f,w=160):
    p=subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=width,height,r_frame_rate','-of','json',f],capture_output=True,text=True)
    s=json.loads(p.stdout)['streams'][0]; W,H=s['width'],s['height']; n,d=s['r_frame_rate'].split('/'); fps=float(n)/float(d)
    h=int(H*w/W)//2*2
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',f'scale={w}:{h},format=gray','-f','rawvideo','-'],capture_output=True).stdout
    a=np.frombuffer(raw,np.uint8).reshape(-1,h,w).astype(np.float32)
    return a,fps
out={}
for f in sys.argv[1:]:
    a,fps=frames(f)
    d=np.abs(np.diff(a,axis=0)).mean(axis=(1,2))
    thr=max(0.15,np.percentile(d,30)*1.5)
    cuts=[i for i in range(1,len(d)-1) if d[i]>8 and d[i]>4*max(d[i-1],d[i+1],0.3)]
    ev=[];i=0
    while i<len(d):
        if d[i]>thr:
            j=i
            while j<len(d) and d[j]>thr: j+=1
            seg=d[i:j]
            if j-i>=3:
                pk=int(np.argmax(seg)); ev.append(((j-i)/fps, pk/max(1,(j-i-1)), i/fps))
            i=j
        else: i+=1
    still=(d<=thr).mean()
    durs=[e[0] for e in ev]; pks=[e[1] for e in ev]
    out[f]=dict(fps=fps,len=round(len(a)/fps,2),events=len(ev),med_event=round(float(np.median(durs)),2) if durs else None,
      p25=round(float(np.percentile(durs,25)),2) if durs else None,p75=round(float(np.percentile(durs,75)),2) if durs else None,
      peak_pos_med=round(float(np.median(pks)),2) if pks else None, early_peak_share=round(float(np.mean([p<0.35 for p in pks])),2) if pks else None,
      still_share=round(float(still),2),hard_cuts=len(cuts))
for k,v in out.items(): print(k,v)
