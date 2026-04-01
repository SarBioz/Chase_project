import os
import pandas as pd

# ── Configure these paths ────────────────────────────────────────────────────
NORMAL_CSV    = "normal_ids_only.csv"   # CSV with Normal patient IDs
QMCI_CSV      = "qmci_ids_only.csv"     # CSV with QMCI patient IDs
NORMAL_FOLDER = "Normal"                # Folder containing Normal .txt files
QMCI_FOLDER   = "QMCI"                 # Folder containing QMCI .txt files
# ─────────────────────────────────────────────────────────────────────────────


def get_ids_from_csv(csv_path):
    """Return a set of patient IDs (as strings) from the first column of a CSV."""
    df = pd.read_csv(csv_path, header=None, dtype=str)
    ids = set(df.iloc[:, 0].str.strip())
    return ids


def get_ids_from_folder(folder_path):
    """Return a set of patient IDs extracted from txt filenames (prefix before first '_')."""
    ids = set()
    for fname in os.listdir(folder_path):
        if fname.endswith(".txt"):
            patient_id = fname.split("_")[0].strip()
            ids.add(patient_id)
    return ids


def check_match(label, csv_path, folder_path):
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"  CSV    : {csv_path}")
    print(f"  Folder : {folder_path}")
    print(f"{'='*55}")

    csv_ids    = get_ids_from_csv(csv_path)
    folder_ids = get_ids_from_folder(folder_path)

    in_csv_not_folder = csv_ids - folder_ids
    in_folder_not_csv = folder_ids - csv_ids
    matched           = csv_ids & folder_ids

    print(f"  IDs in CSV             : {len(csv_ids)}")
    print(f"  IDs in Folder          : {len(folder_ids)}")
    print(f"  Matched                : {len(matched)}")

    if in_csv_not_folder:
        print(f"\n  [MISSING from folder]  : {len(in_csv_not_folder)} ID(s)")
        for pid in sorted(in_csv_not_folder):
            print(f"    - {pid}")
    else:
        print(f"\n  All CSV IDs found in folder.")

    if in_folder_not_csv:
        print(f"\n  [EXTRA in folder / not in CSV] : {len(in_folder_not_csv)} ID(s)")
        for pid in sorted(in_folder_not_csv):
            print(f"    + {pid}")
    else:
        print(f"  No extra IDs in folder.")


if __name__ == "__main__":
    check_match("NORMAL", NORMAL_CSV, NORMAL_FOLDER)
    check_match("QMCI",   QMCI_CSV,   QMCI_FOLDER)
