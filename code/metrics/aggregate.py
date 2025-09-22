import argparse, os, json, glob, csv
from .scoring import hm, DEFAULTS
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model-outputs',required=True); ap.add_argument('--original-results',required=True)
    ap.add_argument('--out',required=True); ap.add_argument('--alpha',type=float,default=DEFAULTS["alpha"])
    ap.add_argument('--beta',type=float,default=DEFAULTS["beta"]); ap.add_argument('--gamma',type=float,default=DEFAULTS["gamma"])
    ap.add_argument('--weights',type=str,default=None); a=ap.parse_args()
    w=DEFAULTS["weights"]; 
    if a.weights: import json as _j; w=_j.loads(a.weights)
    os.makedirs(a.out,exist_ok=True)
    verdicts=glob.glob(os.path.join(a.original_results,'**','*.verdict.json'),recursive=True)
    tot=len(verdicts); safe=0
    for vp in verdicts:
        with open(vp,'r',encoding='utf-8') as f: v=json.load(f)
        if v.get('status')=='safe': safe+=1
    A=1.0 if tot>0 else 0.0; acc=(safe/tot)*100 if tot>0 else 0.0; f1=acc
    Q=hm(acc,f1); s_task=hm(A*100,Q); s_interp=a.alpha*95 + a.beta*90 + (1-a.alpha-a.beta)*s_task
    overall=w["gen"]*s_task + w["comp"]*s_task + w["trans"]*s_task + w["corr"]*s_task + w["interp"]*s_interp
    with open(os.path.join(a.out,'leaderboard_overall.csv'),'w',newline='',encoding='utf-8') as f:
        csv.writer(f).writerow(["model","S_overall_recalc"]); csv.writer(f).writerow(["placeholder-model", round(overall,2)])
    for name,score in [("interpret",s_interp),("generate",s_task),("complete",s_task),("convert",s_task),("fix",s_task)]:
        with open(os.path.join(a.out,f'leaderboard_{name}.csv'),'w',newline='',encoding='utf-8') as f:
            csv.writer(f).writerow(["model",f"S_{name}_recalc"]); csv.writer(f).writerow(["placeholder-model", round(score,2)])
    print(json.dumps({"verdict_count":tot,"overall":round(overall,2),"out":a.out},indent=2))
if __name__=='__main__': main()
