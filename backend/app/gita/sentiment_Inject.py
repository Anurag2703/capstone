import pandas as pd

# Load the cleaned dataset
file_path = "Bhagwad_Gita_Cleaned.xlsx"
df = pd.read_excel(file_path)

# Clean column names for uniformity
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Sanity check
if not {'chapter', 'verse'}.issubset(df.columns):
    raise ValueError("The Excel file must contain 'chapter' and 'verse' columns.")

# Mapping: (chapter, verse) -> sentiment
sentiment_map = {
    (2, 56): "anger", (2, 62): "anger", (2, 63): "anger", (5, 26): "anger",
    (16, 1): "anger", (16, 2): "anger", (16, 3): "anger", (16, 21): "anger",

    (2, 7): "confusion", (3, 2): "confusion", (18, 61): "confusion",

    (12, 13): "dealing with envy", (12, 14): "dealing with envy", (16, 19): "dealing with envy", (18, 71): "dealing with envy",

    (2, 13): "death of a loved one", (2, 20): "death of a loved one", (2, 22): "death of a loved one",
    (2, 25): "death of a loved one", (2, 27): "death of a loved one",

    (11, 33): "demotivated", (18, 48): "demotivated", (18, 78): "demotivated",

    (5, 18): "discriminated", (5, 19): "discriminated", (6, 32): "discriminated", (9, 29): "discriminated",

    (4, 10): "fear", (11, 50): "fear", (18, 30): "fear",

    (4, 36): "feeling sinful", (4, 37): "feeling sinful", (5, 10): "feeling sinful",
    (9, 30): "feeling sinful", (10, 3): "feeling sinful", (14, 6): "feeling sinful", (18, 66): "feeling sinful",

    (15, 15): "forgetfulness", (18, 61): "forgetfulness",

    (2, 3): "depression", (2, 14): "depression", (5, 21): "depression",

    (14, 17): "greed", (16, 21): "greed", (17, 25): "greed",

    (3, 8): "laziness", (3, 20): "laziness", (6, 16): "laziness", (18, 39): "laziness",

    (6, 30): "loneliness", (9, 29): "loneliness", (13, 16): "loneliness", (13, 18): "loneliness",

    (4, 11): "losing hope", (9, 22): "losing hope", (9, 34): "losing hope",
    (18, 66): "losing hope", (18, 78): "losing hope",

    (3, 37): "lust", (3, 41): "lust", (3, 43): "lust", (5, 22): "lust", (16, 21): "lust",

    (11, 44): "practicing forgiveness", (12, 13): "practicing forgiveness", (12, 14): "practicing forgiveness",
    (16, 1): "practicing forgiveness", (16, 2): "practicing forgiveness", (16, 3): "practicing forgiveness",

    (16, 4): "pride", (16, 13): "pride", (16, 14): "pride", (16, 15): "pride",
    (18, 26): "pride", (18, 58): "pride",

    (2, 66): "seeking peace", (2, 71): "seeking peace", (4, 39): "seeking peace",
    (5, 29): "seeking peace", (8, 28): "seeking peace",

    (2, 60): "temptation", (2, 61): "temptation", (2, 70): "temptation", (7, 14): "temptation",

    (6, 5): "uncontrolled mind", (6, 6): "uncontrolled mind", (6, 26): "uncontrolled mind", (6, 35): "uncontrolled mind",
}

# Inject sentiments
df["sentiment"] = df.apply(
    lambda row: sentiment_map.get((row["chapter"], row["verse"]), None),
    axis=1
)

# Save the updated file
output_file = "Bhagwad_Gita_with_Sentiments_Tagged.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Sentiment tagging complete. File saved as: {output_file}")




# # import pandas as pd

# # file_path = "Bhagwad_Gita_with_Sentiment.xlsx"
# # df = pd.read_excel(file_path)

# # Clean and print column names
# df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
# print("✅ Cleaned columns:", df.columns.tolist())





# import pandas as pd

# # Load the file
# file_path = "Bhagwad_Gita_with_Sentiment.xlsx"
# df = pd.read_excel(file_path)

# # Clean column names for safety
# df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# # Drop columns that contain the word 'sentiment' (e.g., 'sentiment', 'seniment', etc.)
# columns_to_drop = [col for col in df.columns if "sentiment" in col]
# df.drop(columns=columns_to_drop, inplace=True)

# # Save to new file
# output_path = "Bhagwad_Gita_Cleaned.xlsx"
# df.to_excel(output_path, index=False)

# print(f"✅ Removed columns: {columns_to_drop}")
# print(f"✅ Cleaned file saved to: {output_path}")
