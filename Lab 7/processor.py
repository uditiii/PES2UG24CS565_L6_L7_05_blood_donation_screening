import math

VALID_ABO = {"A", "B", "AB", "O"}
RH_MAP = {"+": "Positive", "-": "Negative"}


def validate_blood_type(blood_code):
    """
    Standardizes blood group and Rh factor (e.g. 'O+', 'AB-').
    Returns 'Invalid blood type' for anything that is not a valid ABO group
    followed by a +/- Rh sign (None, empty, non-string, unknown group, etc.).
    """
    if not isinstance(blood_code, str):
        return "Invalid blood type"
    cleaned = blood_code.strip().upper()
    if len(cleaned) < 2:
        return "Invalid blood type"
    antigen, rh_char = cleaned[:-1], cleaned[-1]
    if antigen not in VALID_ABO or rh_char not in RH_MAP:
        return "Invalid blood type"
    return f"{antigen} {RH_MAP[rh_char]}"


def calculate_pulse_pressure(bp_string):
    """
    Calculates pulse pressure (systolic - diastolic) and arterial ratio.
    Expects 'systolic/diastolic' (e.g. '120/80') with positive integers and
    systolic >= diastolic. Returns 'Invalid BP reading' otherwise.
    """
    if not isinstance(bp_string, str):
        return "Invalid BP reading"
    parts = bp_string.split('/')
    if len(parts) != 2:
        return "Invalid BP reading"
    try:
        systolic = int(parts[0])
        diastolic = int(parts[1])
    except ValueError:
        return "Invalid BP reading"
    if diastolic <= 0 or systolic < diastolic:
        return "Invalid BP reading"
    pulse_diff = systolic - diastolic
    try:
        ratio = round(systolic / diastolic, 2)
    except (OverflowError, ZeroDivisionError):
        return "Invalid BP reading"
    return f"Diff: {pulse_diff}, Ratio: {ratio}"


def parse_donor_registry(donor_entry):
    """
    Parses pipe-delimited record: 'DonorID|WeightKg|Hemoglobin'.
    Returns 'Invalid donor record' for non-strings, wrong token count, empty
    ID, non-numeric / non-finite / non-positive weight or hemoglobin.
    """
    if not isinstance(donor_entry, str):
        return "Invalid donor record"
    fields = donor_entry.split('|')
    if len(fields) != 3:
        return "Invalid donor record"
    donor_id = fields[0].strip()
    if not donor_id:
        return "Invalid donor record"
    try:
        weight = float(fields[1])
        hemoglobin = float(fields[2])
    except ValueError:
        return "Invalid donor record"
    if not (math.isfinite(weight) and math.isfinite(hemoglobin)):
        return "Invalid donor record"
    if weight <= 0 or hemoglobin <= 0:
        return "Invalid donor record"
    eligible = weight >= 50.0 and hemoglobin >= 12.5
    return f"Donor {donor_id}: {'Eligible' if eligible else 'Deferred'}"


def main():
    print("==== Running validate_blood_type ====")
    b_input = input("Enter blood type (e.g. A+, O-, AB+): ")
    print("Validated:", validate_blood_type(b_input))

    print("\n==== Running calculate_pulse_pressure ====")
    bp_input = input("Enter BP (e.g. 120/80): ")
    print("BP Metrics:", calculate_pulse_pressure(bp_input))

    print("\n==== Running parse_donor_registry ====")
    d_input = input("Enter record (ID|Weight|Hemoglobin): ")
    print("Status:", parse_donor_registry(d_input))

if __name__ == "__main__":
    main()