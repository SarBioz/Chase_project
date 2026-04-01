import pandas as pd

# ── Configure these paths ────────────────────────────────────────────────────
NORMAL_FILE = "normal_demographic.xlsx"
QMCI_FILE   = "qmci_demographic.xlsx"
# ─────────────────────────────────────────────────────────────────────────────


def pick_representative_visit(group):
    """For a patient's visits, find the visit closest to the mean VisitNumber."""
    mean_visit = group["VisitNumber"].mean()
    closest_idx = (group["VisitNumber"] - mean_visit).abs().idxmin()
    return group.loc[closest_idx]


def compute_stats(filepath, label):
    df = pd.read_excel(filepath, dtype=str)

    # Remove rows 2 and 3 (index 1 and 2)
    df = df.drop(index=[1, 2]).reset_index(drop=True)

    # Convert numeric columns
    df["Age"]            = pd.to_numeric(df["Age"], errors="coerce")
    df["EducationYears"] = pd.to_numeric(df["EducationYears"], errors="coerce")
    df["VisitNumber"]    = pd.to_numeric(df["VisitNumber"], errors="coerce")

    # For each patient, pick the visit closest to their mean VisitNumber
    representative = (
        df.groupby("PatientID", group_keys=False)
        .apply(pick_representative_visit)
        .reset_index(drop=True)
    )

    # For Sex, take one value per patient (first non-null)
    sex_per_patient = (
        df.groupby("PatientID")["Sex"]
        .first()
        .reset_index()
    )

    print(f"\n{'='*45}")
    print(f"  {label}  (n={len(representative)} patients)")
    print(f"{'='*45}")

    print(f"  Mean Age            : {representative['Age'].mean():.2f}")
    print(f"  Mean EducationYears : {representative['EducationYears'].mean():.2f}")

    sex_counts = sex_per_patient["Sex"].value_counts()
    print(f"  Sex distribution:")
    for sex, count in sex_counts.items():
        print(f"    {sex}: {count}")


compute_stats(NORMAL_FILE, "NORMAL")
compute_stats(QMCI_FILE,   "QMCI")
