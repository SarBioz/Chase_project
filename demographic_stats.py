import pandas as pd

# ── Configure these paths ────────────────────────────────────────────────────
NORMAL_FILE = "normal_demographic.xlsx"
QMCI_FILE   = "qmci_demographic.xlsx"
# ─────────────────────────────────────────────────────────────────────────────


def compute_stats(filepath, label):
    df = pd.read_excel(filepath, dtype=str)

    # Remove rows 2 and 3 (index 1 and 2, i.e. the 2nd and 3rd rows after header)
    df = df.drop(index=[1, 2]).reset_index(drop=True)

    # Convert numeric columns
    df["Age"]            = pd.to_numeric(df["Age"], errors="coerce")
    df["EducationYears"] = pd.to_numeric(df["EducationYears"], errors="coerce")

    print(f"\n{'='*45}")
    print(f"  {label}  (n={len(df)})")
    print(f"{'='*45}")

    # Mean Age
    print(f"  Mean Age            : {df['Age'].mean():.2f}")

    # Mean Education Years
    print(f"  Mean EducationYears : {df['EducationYears'].mean():.2f}")

    # Sex distribution + percentage
    sex_counts = df["Sex"].value_counts()
    sex_pct    = df["Sex"].value_counts(normalize=True) * 100
    print(f"  Sex distribution:")
    for sex in sex_counts.index:
        print(f"    {sex}: {sex_counts[sex]} ({sex_pct[sex]:.1f}%)")


compute_stats(NORMAL_FILE, "NORMAL")
compute_stats(QMCI_FILE,   "QMCI")
