import pandas as pd

# ── Configure these paths ────────────────────────────────────────────────────
NORMAL_CSV       = "normal_ids_only.csv"
QMCI_CSV         = "qmci_ids_only.csv"
DEMOGRAPHIC_FILE = "demographicfull.csv"   # has: PatientID, Sex, EducationYears
VISITS_FILE      = "patientvisits.csv"     # has: PatientID, Age

NORMAL_OUTPUT    = "normal_demographic.xlsx"
QMCI_OUTPUT      = "qmci_demographic.xlsx"
# ─────────────────────────────────────────────────────────────────────────────

# Load source files
demo   = pd.read_csv(DEMOGRAPHIC_FILE, dtype=str)
visits = pd.read_csv(VISITS_FILE, dtype=str)

# Normalise column names (strip whitespace)
demo.columns   = demo.columns.str.strip()
visits.columns = visits.columns.str.strip()

# Keep only needed columns
demo   = demo[["PatientID", "Sex", "EducationYears"]].copy()
visits = visits[["PatientID", "Age", "VisitNumber"]].copy()

# Strip whitespace from IDs
demo["PatientID"]   = demo["PatientID"].str.strip()
visits["PatientID"] = visits["PatientID"].str.strip()

# Merge sex + education + age into one lookup table
lookup = pd.merge(demo, visits, on="PatientID", how="outer")


def build_demographic(csv_path, output_path, label):
    ids = pd.read_csv(csv_path, header=None, dtype=str)
    ids.columns = ["PatientID"]
    ids["PatientID"] = ids["PatientID"].str.strip()

    result = pd.merge(ids, lookup, on="PatientID", how="left")

    # Report any IDs with missing data
    missing = result[result[["Sex", "EducationYears", "Age"]].isnull().any(axis=1)]
    if not missing.empty:
        print(f"\n[{label}] WARNING — {len(missing)} ID(s) with missing data:")
        for pid in missing["PatientID"].tolist():
            print(f"  {pid}")
    else:
        print(f"\n[{label}] All IDs matched successfully.")

    result.to_excel(output_path, index=False)
    print(f"[{label}] Saved -> {output_path}")


build_demographic(NORMAL_CSV, NORMAL_OUTPUT, "NORMAL")
build_demographic(QMCI_CSV,   QMCI_OUTPUT,   "QMCI")
