
from backend.data_loader import load_market_data
from backend.data_validator import validate_market_data


# Load sample CSV data
df = load_market_data(
    "data/processed/sample_market.csv"
)

print("\nORIGINAL DATA")
print(df.head())


# Validate market data
cleaned_df, issues = validate_market_data(df)


print("\nVALIDATION REPORT")
print("=" * 45)

for issue in issues:
    print(issue)


print("\nCLEANED MARKET DATA")
print(cleaned_df.head())


print("\nDATA VALIDATION COMPLETED!")
