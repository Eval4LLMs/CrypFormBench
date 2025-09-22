def hm(a,b): 
    if a<=0 or b<=0: return 0.0
    return 2*a*b/(a+b)
DEFAULTS={"alpha":0.3,"beta":0.3,"gamma":1.0,"weights":{"gen":0.25,"comp":0.20,"trans":0.25,"corr":0.15,"interp":0.15}}
