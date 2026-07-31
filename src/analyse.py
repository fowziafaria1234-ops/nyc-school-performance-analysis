from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
    raw=pd.read_csv(ROOT/'data/raw/nyc_school_results_raw.csv')
    df=raw.drop_duplicates(['school_id','year']).copy(); df['borough']=df['borough'].str.title(); df['attendance_rate_pct']=pd.to_numeric(df['attendance_rate_pct'],errors='coerce')
    for c in ['math_score','reading_score','writing_score','attendance_rate_pct']:
        df[c]=pd.to_numeric(df[c],errors='coerce'); df[c]=df[c].fillna(df.groupby(['borough','year'])[c].transform('median'))
    df['composite_score']=df[['math_score','reading_score','writing_score']].mean(axis=1)
    q1,q3=df.composite_score.quantile([.25,.75]); iqr=q3-q1; df['outlier_flag']=~df.composite_score.between(q1-1.5*iqr,q3+1.5*iqr)
    out=ROOT/'data/processed'; out.mkdir(parents=True,exist_ok=True); df.to_csv(out/'nyc_school_results_clean.csv',index=False)
    summary=df.groupby('borough').agg(schools=('school_id','nunique'),median_composite=('composite_score','median'),median_attendance=('attendance_rate_pct','median'),median_graduation=('graduation_rate_pct','median'),median_disadvantage=('economically_disadvantaged_pct','median')).sort_values('median_composite',ascending=False).reset_index(); summary.to_csv(out/'borough_mi_summary.csv',index=False)
if __name__=='__main__': main()
