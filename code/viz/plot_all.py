import argparse, os, glob
def main():
  ap=argparse.ArgumentParser(); ap.add_argument('--in',dest='indir',required=True); ap.add_argument('--out',dest='outdir',required=True); a=ap.parse_args()
  os.makedirs(a.outdir,exist_ok=True)
  csvs=glob.glob(os.path.join(a.indir,'**','leaderboard_*.csv'),recursive=True)
  with open(os.path.join(a.outdir,'SUMMARY.txt'),'w',encoding='utf-8') as f:
    for p in csvs: f.write(p+'\n')
  print("Wrote SUMMARY.txt")
if __name__=='__main__': main()
