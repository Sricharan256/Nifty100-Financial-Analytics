import os

deliverables = [

    "output/pros_cons_generated.csv",
    "output/analysis_parsed.csv",
    "output/cashflow_intelligence.xlsx",
    "output/distress_alerts.csv",
    "reports/portfolio/portfolio_summary.pdf",
    "reports/tearsheets",
    "reports/sector"

]

print("=" * 50)
print("SPRINT 5 REVIEW")
print("=" * 50)

for item in deliverables:

    if os.path.exists(item):

        print(f"✓ {item}")

    else:

        print(f"✗ {item}")

print()
print("Sprint 5 Review Completed.")