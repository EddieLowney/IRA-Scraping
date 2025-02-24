import pandas as pd

# File paths
conversion_file = "fips.txt"
fips_filename = "FIPS_CODES.csv"

fips_df = pd.read_csv(fips_filename, dtype=str, header=None, names=["FIPS"])
df = pd.read_csv(conversion_file, sep='\t')

df = df[67:]

df[["FIPS", "County"]] = df["Federal Information Processing System (FIPS) Codes for States and Counties"].str.split("        ", n=1, expand=True)

df['County'] = df['County'].str.strip()
df['FIPS'] = df['FIPS'].str.replace(r'\s+', '', regex=True)

fips_df.rename(columns=lambda x: x.strip(), inplace=True)
df.rename(columns=lambda x: x.strip(), inplace=True)

merged_df = fips_df.merge(df[['FIPS', 'County']], on="FIPS", how="left")

merged_df.to_csv("FIPS_with_County.csv", index=False)


