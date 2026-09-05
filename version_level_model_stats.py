import json
import pandas as pd
import csv, json

gts_json = json.load(open(r"C:\Users\sahil.garg\Documents\o9\APEX\Data\Pepsico\pepsico_version_level_model_stats.json"))
df = pd.DataFrame(columns=[
    "Sequence ID.[Sequence ID]", "Version", "Model Stats Member", "Model Stats Value", "Model Stats Type"
])

model_stats_json = gts_json.get("Result", {}).get("History", [])[0].get("ModelStats", {}).get("ModelStatsDetail", {})

seq_id = 0
j = 0
for mg in model_stats_json.get("MeasureGroups", []):
    for version, count in mg.get("RowCountByVersion", {}).items():
        if count > 0:
            df.loc[j] = [
                str(seq_id).zfill(4), version, mg.get("Name"), count, "MeasureGroup"
            ]
        j += 1
        seq_id += 1

seq_id = 2001
for gr in model_stats_json.get("Graphs", []):
    for version, count in gr.get("RowCountByVersion", {}).items():
        if count > 0:
            df.loc[j] = [
                str(seq_id).zfill(4), version, gr.get("Name"), count, "Graph"
            ]
        j += 1
        seq_id += 1

seq_id = 4001
for dm in model_stats_json.get("MeasureGroups", []):
    for version, count in dm.get("RowCountByVersion", {}).items():
        if version == "Count":
            version = "CurrentWorkingView"

        if count > 0:
            df.loc[j] = [
                str(seq_id).zfill(4), version, dm.get("Name"), count, "Dimension"
            ]
        j += 1
        seq_id += 1

df.to_csv("ModelStats_versionlevel.csv", index=False)


