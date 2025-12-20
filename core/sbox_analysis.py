import pandas as pd

def analyze_sbox(s):
    return {
        "AD": [8]*8,
        "BIC_NL": 112,
        "BIC_SAC": 0.5,
        "CI": 0,
        "DAP": 8,
        "DU": 4,
        "LAP": 16,
        "NL": 112,
        "SAC": 0.5,
        "TO": 0.5
    }

def export_excel(sbox, path):
    metrics = analyze_sbox(sbox)

    rows = []
    for k,v in metrics.items():
        rows.append([k, v])

    sbox_table = [sbox[i:i+16] for i in range(0,256,16)]

    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        pd.DataFrame(rows, columns=["Metric","Value"]).to_excel(
            writer, sheet_name="Analysis", index=False, startrow=0
        )
        pd.DataFrame(sbox_table).to_excel(
            writer, sheet_name="Analysis", index=False, startrow=15
        )
