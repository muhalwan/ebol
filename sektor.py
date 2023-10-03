import pandas as pd


def get_hierarchy_final_refined_corrected_v2(kbli_code, kbli_coding_df):
    # jika Not Found None
    if kbli_code == "Not Found":
        return None, None, None, None

    # 4 digit kbli
    kbli_prefix = float(str(kbli_code)[:4])

    # nilai awal
    kelas_1, kelas_2, kelas_3, kelas_4 = None, None, None, None

    # Sektor Kelas 4
    kelas_4_row = kbli_coding_df[kbli_coding_df['Kelas 4'] == kbli_prefix]
    if not kelas_4_row.empty:
        kelas_4 = kelas_4_row['Sektor'].values[0]

    # Sektor Kelas 3
    kbli_prefix //= 10
    kelas_3_row = kbli_coding_df[kbli_coding_df['Kelas 3'] == kbli_prefix]
    if not kelas_3_row.empty:
        kelas_3 = kelas_3_row['Sektor'].values[0]
    else:
        current_index = kelas_4_row.index[0] if not kelas_4_row.empty else None
        while current_index and pd.isna(kbli_coding_df.iloc[current_index]['Kelas 3']):
            current_index -= 1
        if current_index:
            kelas_3 = kbli_coding_df.iloc[current_index]['Sektor']

    # Sektor Kelas 2
    kbli_prefix //= 10
    kelas_2_row = kbli_coding_df[kbli_coding_df['Kelas 2'] == kbli_prefix]
    if not kelas_2_row.empty:
        kelas_2 = kelas_2_row['Sektor'].values[0]
    else:
        current_index = kelas_3_row.index[0] if not kelas_3_row.empty else None
        while current_index and pd.isna(kbli_coding_df.iloc[current_index]['Kelas 2']):
            current_index -= 1
        if current_index:
            kelas_2 = kbli_coding_df.iloc[current_index]['Sektor']

    # Sektor Kelas 1
    current_index = kelas_2_row.index[0] if not kelas_2_row.empty else None
    while current_index and pd.isna(kbli_coding_df.iloc[current_index]['Kelas 1']):
        current_index -= 1
    if current_index:
        kelas_1 = kbli_coding_df.iloc[current_index]['Sektor']

    return kelas_1, kelas_2, kelas_3, kelas_4


company_kbli_df = pd.read_csv("Company_KBLI_Results.csv")
kbli_coding_df = pd.read_csv("KBLI_Coding.csv", encoding="cp1252")


company_kbli_df['Kelas 1'], company_kbli_df['Kelas 2'], company_kbli_df['Kelas 3'], company_kbli_df['Kelas 4'] = zip(
    *company_kbli_df['KBLI'].map(lambda x: get_hierarchy_final_refined_corrected_v2(x, kbli_coding_df)))


company_kbli_df.to_csv("Processed_Companies.csv", index=False)
