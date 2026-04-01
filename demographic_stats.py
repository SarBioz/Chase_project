import pandas as pd

# ── Configure these paths ────────────────────────────────────────────────────
NORMAL_FILE = "normal_demographic.xlsx"
QMCI_FILE   = "qmci_demographic.xlsx"
# ─────────────────────────────────────────────────────────────────────────────


def pick_representative_visit(group):
    """For a patient's visits, find the visit closest to the mean VisitNumber."""
    valid = group.dropna(subset=["VisitNumber"])
    if valid.empty:
        return group.iloc[0]
    mean_visit = valid["VisitNumber"].mean()
    closest_idx = (valid["VisitNumber"] - mean_visit).abs().idxmin()
    return valid.loc[closest_idx]


def compute_stats(filepath, label):
    df = pd.read_excel(filepath, dtype=str)

    # Remove rows 2 and 3 (index 1 and 2)
    df = df.drop(index=[1, 2]).reset_index(drop=True)

    # Convert numeric columns
    df["Age"]            = pd.to_numeric(df["Age"], errors="coerce")
    df["EducationYears"] = pd.to_numeric(df["EducationYears"], errors="coerce")
    df["VisitNumber"]    = pd.to_numeric(df["VisitNumber"], errors="coerce")

    # Report patients with NaN VisitNumber
    nan_visit_ids = df[df["VisitNumber"].isna()]["PatientID"].unique()
    if len(nan_visit_ids) > 0:
        print(f"\n[{label}] Patients with NaN VisitNumber ({len(nan_visit_ids)}):")
        for pid in sorted(nan_visit_ids):
            print(f"  {pid}")

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




 The behavior of Series.idxmin with all-NA values, or any-NA and skipna=False, is deprecated. In a future version this will raise ValueError
  closest_idx = (group["VisitNumber"] - mean_visit).abs().idxmin()
Traceback (most recent call last):
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3812, in get_loc
    return self._engine.get_loc(casted_key)
  File "pandas/_libs/index.pyx", line 167, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index.pyx", line 175, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index_class_helper.pxi", line 70, in pandas._libs.index.Int64Engine._check_type
KeyError: nan

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Volumes/ESD-USB/ADRC Data/demographic_stats.py", line 54, in <module>
    compute_stats(NORMAL_FILE, "NORMAL")
  File "/Volumes/ESD-USB/ADRC Data/demographic_stats.py", line 30, in compute_stats
    .apply(pick_representative_visit)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/groupby/groupby.py", line 1826, in apply
    result = self._python_apply_general(f, self._selected_obj)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/groupby/groupby.py", line 1887, in _python_apply_general
    values, mutated = self._grouper.apply_groupwise(f, data, self.axis)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/groupby/ops.py", line 928, in apply_groupwise
    res = f(group)
  File "/Volumes/ESD-USB/ADRC Data/demographic_stats.py", line 13, in pick_representative_visit
    return group.loc[closest_idx]
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/indexing.py", line 1192, in __getitem__
    return self._getitem_axis(maybe_callable, axis=axis)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/indexing.py", line 1432, in _getitem_axis
    return self._get_label(key, axis=axis)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/indexing.py", line 1382, in _get_label
    return self.obj.xs(label, axis=axis)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/generic.py", line 4323, in xs
    loc = index.get_loc(key)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3819, in get_loc
    raise KeyError(key) from err
KeyError: nan
(myenv) sajjadilab@sajjadiabsmini2 ADRC Data % python demographic_stats.py
/Volumes/ESD-USB/ADRC Data/demographic_stats.py:12: FutureWarning: The behavior of Series.idxmin with all-NA values, or any-NA and skipna=False, is deprecated. In a future version this will raise ValueError
  closest_idx = (group["VisitNumber"] - mean_visit).abs().idxmin()
Traceback (most recent call last):
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3812, in get_loc
    return self._engine.get_loc(casted_key)
  File "pandas/_libs/index.pyx", line 167, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index.pyx", line 175, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index_class_helper.pxi", line 70, in pandas._libs.index.Int64Engine._check_type
KeyError: nan

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Volumes/ESD-USB/ADRC Data/demographic_stats.py", line 54, in <module>
    compute_stats(NORMAL_FILE, "NORMAL")
  File "/Volumes/ESD-USB/ADRC Data/demographic_stats.py", line 30, in compute_stats
    .apply(pick_representative_visit)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/groupby/groupby.py", line 1826, in apply
    result = self._python_apply_general(f, self._selected_obj)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/groupby/groupby.py", line 1887, in _python_apply_general
    values, mutated = self._grouper.apply_groupwise(f, data, self.axis)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/groupby/ops.py", line 928, in apply_groupwise
    res = f(group)
  File "/Volumes/ESD-USB/ADRC Data/demographic_stats.py", line 13, in pick_representative_visit
    return group.loc[closest_idx]
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/indexing.py", line 1192, in __getitem__
    return self._getitem_axis(maybe_callable, axis=axis)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/indexing.py", line 1432, in _getitem_axis
    return self._get_label(key, axis=axis)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/indexing.py", line 1382, in _get_label
    return self.obj.xs(label, axis=axis)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/generic.py", line 4323, in xs
    loc = index.get_loc(key)
  File "/opt/anaconda3/envs/myenv/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3819, in get_loc
    raise KeyError(key) from err
KeyError: nan
