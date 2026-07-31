from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
def main():
    df=pd.read_csv(ROOT/'data/processed/nyc_school_results_clean.csv'); summary=pd.read_csv(ROOT/'data/processed/borough_mi_summary.csv'); out=ROOT/'assets'
    plt.figure(figsize=(10,5)); plt.bar(summary.borough,summary.median_composite,color='#E11D48'); plt.ylabel('Median composite score'); plt.title('Borough performance ranking'); plt.tight_layout(); plt.savefig(out/'borough-ranking.png',dpi=160); plt.close()
    plt.figure(figsize=(10,5)); plt.scatter(df.attendance_rate_pct,df.composite_score,alpha=.45,color='#EC4899'); plt.xlabel('Attendance rate (%)'); plt.ylabel('Composite score'); plt.title('Attendance and performance relationship'); plt.tight_layout(); plt.savefig(out/'attendance-score.png',dpi=160); plt.close()
if __name__=='__main__': main()
