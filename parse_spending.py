import pandas as pd
import numpy as np
import glob


def clean_pct(val):
    try:
        return float(val)
    except:
        return np.nan


pd.options.display.max_rows = 999
pd.options.display.max_columns = 999

headers = [
    "CAND_ID",
    "CAND_NAME",
    "CAND_ICI",
    "PTY_CD",
    "CAND_PTY_AFFILIATION",
    "TTL_RECEIPTS",
    "TRANS_FROM_AUTH",
    "TTL_DISB",
    "TRANS_TO_AUTH",
    "COH_BOP",
    "COH_COP",
    "CAND_CONTRIB",
    "CAND_LOANS",
    "OTHER_LOANS",
    "CAND_LOAN_REPAY",
    "OTHER_LOAN_REPAY",
    "DEBTS_OWED_BY",
    "TTL_INDIV_CONTRIB",
    "CAND_OFFICE_ST",
    "CAND_OFFICE_DISTRICT",
    "SPEC_ELECTION",
    "PRIM_ELECTION",
    "RUN_ELECTION",
    "GEN_ELECTION",
    "GEN_ELECTION_PRECENT",
    "OTHER_POL_CMTE_CONTRIB",
    "POL_PTY_CONTRIB",
    "CVG_END_DT",
    "INDIV_REFUNDS",
    "CMTE_REFUNDS"
]

files_locs = glob.glob("./raw_data/*.txt")

dataframes = []

for F in files_locs:
    with open(F) as f:
        lines = [l.split("|") for l in f.read().split("\n")]

    df = pd.DataFrame(lines, columns=headers)
    dataframes.append(df)

elections_df = pd.concat(dataframes, axis=0)
elections_df["CVG_END_DT"] = pd.to_datetime(
    elections_df["CVG_END_DT"], format="%m/%d/%Y")

for col in elections_df:
    try:
        elections_df[col] = elections_df[col].astype(float)
    except Exception as e:
        print(col)
        print(e)


elections_df["GEN_ELECTION_PRECENT"] = [
    clean_pct(v) for v in elections_df["GEN_ELECTION_PRECENT"].values]

# dataset to analyze
train_set = elections_df.dropna(subset=["GEN_ELECTION_PRECENT"])

train_set.to_csv("train_set.csv")
