import os
import pandas as pd

TEARSHEET_DIR = "reports/tearsheets"
SECTOR_DIR = "reports/sector"

print("=" * 50)
print("REPORT VERIFICATION")
print("=" * 50)

# -------------------------------
# Company Tearsheets
# -------------------------------

if os.path.exists(TEARSHEET_DIR):

    tearsheets = [
        f for f in os.listdir(TEARSHEET_DIR)
        if f.endswith(".pdf")
    ]

    print(f"\nCompany Tearsheets : {len(tearsheets)}")

    for pdf in sorted(tearsheets[:5]):
        size = os.path.getsize(
            os.path.join(TEARSHEET_DIR, pdf)
        ) / 1024

        print(f"{pdf:<35} {size:.2f} KB")

else:

    print("Tearsheet folder not found.")

# -------------------------------
# Sector Reports
# -------------------------------

if os.path.exists(SECTOR_DIR):

    sectors = [
        f for f in os.listdir(SECTOR_DIR)
        if f.endswith(".pdf")
    ]

    print(f"\nSector Reports : {len(sectors)}")

    for pdf in sorted(sectors):

        size = os.path.getsize(
            os.path.join(SECTOR_DIR, pdf)
        ) / 1024

        print(f"{pdf:<35} {size:.2f} KB")

else:

    print("Sector report folder not found.")

# -------------------------------
# Skipped Companies
# -------------------------------

skip_file = "output/skipped_tearsheets.csv"

if os.path.exists(skip_file):

    skipped = pd.read_csv(skip_file)

    print(f"\nSkipped Companies : {len(skipped)}")

else:

    print("\nNo skipped companies file found.")

print("\nVerification Completed Successfully.")