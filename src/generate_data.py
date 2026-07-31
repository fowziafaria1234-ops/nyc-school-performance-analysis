"""Rebuild the seeded school-performance demonstration dataset."""
from pathlib import Path
import numpy as np
import pandas as pd

def main():
    rng=np.random.default_rng(202602); boroughs=['Bronx','Brooklyn','Manhattan','Queens','Staten Island']; years=range(2021,2026); rows=[]; school_no=1
    for b in boroughs:
        base={'Bronx':470,'Brooklyn':515,'Manhattan':560,'Queens':535,'Staten Island':545}[b]
        for s in range(15):
            name=f'{b} Academy {s+1:02d}'; disadvantage=np.clip(rng.normal({'Bronx':.72,'Brooklyn':.60,'Manhattan':.42,'Queens':.54,'Staten Island':.46}[b],.10),.12,.95); ratio=np.clip(rng.normal(14.5+4*disadvantage,1.7),10,25)
            for y in years:
                trend=(y-2021)*4.5; attendance=np.clip(rng.normal(.91-.08*disadvantage+.006*(y-2021),.025),.72,.99)
                scores=[np.clip(rng.normal(base+offset+trend+weight*(attendance-.88)-penalty*(disadvantage-.5),sd),250,800) for offset,weight,penalty,sd in [(0,180,80,45),(15,165,72,42),(8,150,65,40)]]
                grad=np.clip(.70+.30*(attendance-.8)-.12*(disadvantage-.5)+rng.normal(0,.035),.45,.99)
                rows.append([f'SCH-{school_no:03d}',name,b,y,int(rng.integers(280,1300)),*map(lambda x:round(x,1),scores),round(attendance*100,1),round(disadvantage*100,1),round(ratio,1),round(grad*100,1)])
            school_no+=1
    df=pd.DataFrame(rows,columns=['school_id','school_name','borough','year','enrolment','math_score','reading_score','writing_score','attendance_rate_pct','economically_disadvantaged_pct','student_teacher_ratio','graduation_rate_pct'])
    for idx in rng.choice(df.index,15,replace=False): df.loc[idx,'math_score']=np.nan
    df['attendance_rate_pct']=df['attendance_rate_pct'].astype(object)
    for idx in rng.choice(df.index,10,replace=False): df.loc[idx,'attendance_rate_pct']='unknown'
    for idx in rng.choice(df.index,8,replace=False): df.loc[idx,'borough']=df.loc[idx,'borough'].lower()
    df=pd.concat([df,df.iloc[:5]],ignore_index=True)
    out=Path(__file__).resolve().parents[1]/'data/raw/nyc_school_results_raw.csv'; out.parent.mkdir(parents=True,exist_ok=True); df.to_csv(out,index=False)
if __name__=='__main__': main()
