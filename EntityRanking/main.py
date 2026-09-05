import csv
import pandas as pd
from data_utils import data_extraction_utils
from ranking_utils import entity_ranking
# from ranking_utils_merge import entity_ranking


CLIENT = "WLN"

PATHS = {
    "Acuity": {
        "config":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Acuity Brands\ConfigBackup_Acuity Brands_T3.zip",
        "tenant":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Acuity Brands\TenantLogs.Csv",
        "adoption":  r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Acuity Brands\AdoptionData.csv",
        "psr":       r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Acuity Brands\ELKPSRData.csv",
        "w_summary": r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Acuity Brands\widget_summary_acuity.csv"
    },
    "Pepsico": {
        "config":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Pepsi2\ConfigBackup.zip",
        "tenant":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Pepsi2\TenantLogs.Csv",
        "adoption":  r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Pepsi2\Adoption.csv",
        "psr":       r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Pepsi2\ELKPSRData.csv",
    },
    "Nike": {
            "config":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Nike\o9.ConfigbackupforTenant_Nike_639136680799395334.json.zip",
            "tenant":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Nike\tenant_logs.Csv",
            "adoption":  r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Nike\adoption.csv",
            "psr":       r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Nike\ELKPSRData.csv",
        },
    "MFPNA": {
            "config":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\MFPNA\o9.ConfigbackupforTenant_MFPNA_639136677777757059.json.zip",
            "tenant":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\MFPNA\tenant_logs.Csv",
            "adoption":  r"C:\Users\sahil.garg\Documents\o9\APEX\Data\MFPNA\adoption.csv",
            "psr":       r"C:\Users\sahil.garg\Documents\o9\APEX\Data\MFPNA\ELKPSRData.csv",
        },
    "MFPGlobal": {
            "config":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\MFPGlobal\o9.ConfigbackupforTenant_MFPGlobal_639136678700669391.json.zip",
            "tenant":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\MFPGlobal\tenant_logs.Csv",
            "adoption":  r"C:\Users\sahil.garg\Documents\o9\APEX\Data\MFPGlobal\adoption.csv",
            "psr":       r"C:\Users\sahil.garg\Documents\o9\APEX\Data\MFPGlobal\ELKPSRData.csv",
        },
    "WLN": {
            "config":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\AT&T\WLN\ConfigBackup.zip",
            "tenant":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\AT&T\WLN\TenantLogs.Csv",
            "adoption":  r"C:\Users\sahil.garg\Documents\o9\APEX\Data\AT&T\WLN\Adoption.csv",
            "psr":       r"C:\Users\sahil.garg\Documents\o9\APEX\Data\AT&T\WLN\ELKPSRData.csv",
        },
    "WLS": {
            "config":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\AT&T\WLS\ConfigBackup.zip",
            "tenant":    r"C:\Users\sahil.garg\Documents\o9\APEX\Data\AT&T\WLS\TenantLogs.Csv",
            "adoption":  r"C:\Users\sahil.garg\Documents\o9\APEX\Data\AT&T\WLS\Adoption.csv",
            "psr":       r"C:\Users\sahil.garg\Documents\o9\APEX\Data\AT&T\WLS\ELKPSRData.csv",
        },
    "WestRock": {
        "config": r"C:\Users\sahil.garg\Documents\o9\APEX\Data\WestRock\ConfigBackup.zip",
        "tenant": r"C:\Users\sahil.garg\Documents\o9\APEX\Data\WestRock\TenantLogs.Csv",
        "adoption": r"C:\Users\sahil.garg\Documents\o9\APEX\Data\WestRock\Adoption.csv",
        "psr": r"C:\Users\sahil.garg\Documents\o9\APEX\Data\WestRock\ELKPSR.csv",
    },
}

deu = data_extraction_utils()
er = entity_ranking()

paths = PATHS[CLIENT]
print("Running for : %s", CLIENT)

print("Loading config data...")
df_vwml = deu.get_widgetmeasureslist_from_config(paths["config"])
df_vwml[["Widget","Measure"]].drop_duplicates().to_csv("df_wml.csv", index=False) #
df_md = deu.get_measuredescriptions_from_config(paths["config"])
df_md.to_csv("df_md.csv", index=False, quoting=csv.QUOTE_ALL) #
# df_md already contains [Measure, Grain] — reuse it directly as the
# Measure <-> DimAttr structural input; no separate config read needed.
df_da = df_md

wml = df_vwml[["Widget", "Measure"]].drop_duplicates()
wmmdl = wml.merge(df_md, how="left", on="Measure")
wmmdl = wmmdl.groupby("Widget").agg(
    measure_list=("Measure", list),
    measure_descriptions=("Description", list)
).reset_index()

print("Computing measure interaction scores from tenant logs...")
df_tenant_raw = pd.read_csv(paths["tenant"], low_memory=False)
df_tenant_stats, df_dimattr_stats = deu.get_measure_and_dim_attrs_stats_from_tenantlogs(df_tenant_raw)
measure_scores = er.generate_measure_ranks_from_logs_data(df_tenant_stats)
# measure_scores.to_csv("measure_scores.csv", index=False) #
print("Computing dimension.attribute interaction scores from tenant logs...")
dimattr_scores = er.generate_dimattr_ranks_from_logs_data(df_dimattr_stats)
# dimattr_scores.to_csv("dimattr_scores.csv", index=False) #

print("Computing view interaction scores from adoption logs...")
try:
    df_adoption_raw = pd.read_csv(paths["adoption"])
    df_adoption_stats = deu.get_view_stats_from_adoptionlogs(df_adoption_raw)
    view_scores = er.generate_view_ranks_from_adoption_data(df_adoption_stats)
except Exception as e:
    print(f"WARNING: Could not load adoption data — view interaction scores will be zero. Reason: {e}")
    view_scores = pd.DataFrame(columns=["View", "interaction_score"])

print("Computing widget interaction scores from PSR logs...")
try:
    df_psr_raw = pd.read_csv(paths["psr"], sep="^")
    df_psr_stats = deu.get_widget_stats_from_psrlogs(df_psr_raw)
    widget_scores = er.generate_widget_ranks_from_psr_data(df_psr_stats)
except Exception as e:
    print(f"WARNING: Could not load PSR data — widget interaction scores will be zero. Reason: {e}")
    widget_scores = pd.DataFrame(columns=["Widget", "interaction_score"])

print("Running PageRank")
measure_final, widget_final, dimattr_final = er.generate_ranks(
    config_data=df_vwml,
    md_data=df_da,
    view_scores=view_scores,
    widget_scores=widget_scores,
    measure_scores=measure_scores,
    dimattr_scores=dimattr_scores,
)

print("Top 20 measures:\n%s", measure_final.head(20))
print("Top 10 widgets:\n%s", widget_final.head(10))
print("Top 20 dim.attrs:\n%s", dimattr_final.head(20))

# measure_final.to_csv(f"measure_ranks_{CLIENT}_0.csv", index=False, quoting=csv.QUOTE_ALL)
measure_final = measure_final.merge(df_md, how="left", on="Measure")
measure_final.to_csv(f"measure_ranks_{CLIENT}.csv", index=False, quoting=csv.QUOTE_ALL)

# widget_final = widget_final.merge(pd.read_csv(paths["w_summary"]), how="left", on="Widget")
widget_final = widget_final.merge(wmmdl, how="left", on="Widget")
widget_final.to_csv(f"widget_ranks_{CLIENT}.csv", index=False, quoting=csv.QUOTE_ALL)

dimattr_final.to_csv(f"dimattr_ranks_{CLIENT}.csv", index=False, quoting=csv.QUOTE_ALL)

print("Completed")