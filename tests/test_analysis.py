import pandas as pd
def test_clean_dataset():
    df=pd.read_csv('data/processed/nyc_school_results_clean.csv')
    assert len(df)>=350
    assert df[['math_score','reading_score','writing_score','attendance_rate_pct']].notna().all().all()
    assert df['composite_score'].between(250,800).all()
def test_all_boroughs_present():
    df=pd.read_csv('data/processed/borough_mi_summary.csv')
    assert set(df.borough)=={'Bronx','Brooklyn','Manhattan','Queens','Staten Island'}
