import pandas as pd

df = pd.read_csv("dataset/amazon.csv")

print(df.head())

print(df.columns)

print(df.info())

print(df.shape)
# Null values check
print(df.isnull().sum())
# Duplicate rows check
print(df.duplicated().sum())
print(df['rating'].unique())
# Convert invalid ratings to NaN
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
print(df['rating'].isnull().sum())
df = df.dropna(subset=['rating'])
print(df.info())
# discounted_price cleaning
df['discounted_price'] = df['discounted_price'].str.replace('₹', '', regex=False)
df['discounted_price'] = df['discounted_price'].str.replace(',', '', regex=False)
df['discounted_price'] = df['discounted_price'].astype(float)
# actual_price cleaning
df['actual_price'] = df['actual_price'].str.replace('₹', '', regex=False)
df['actual_price'] = df['actual_price'].str.replace(',', '', regex=False)
df['actual_price'] = df['actual_price'].astype(float)
# discount_percentage cleaning
df['discount_percentage'] = df['discount_percentage'].str.replace('%', '', regex=False)
df['discount_percentage'] = df['discount_percentage'].astype(float)
# rating_count cleaning
df['rating_count'] = df['rating_count'].str.replace(',', '', regex=False)

df['rating_count'] = pd.to_numeric(
    df['rating_count'],
    errors='coerce'
)
print(df.info())
# Price Difference
df['price_difference'] = (
    df['actual_price'] - df['discounted_price']
)

# Rating Category
df['rating_category'] = df['rating'].apply(
    lambda x: 'High' if x >= 4
    else 'Medium' if x >= 3
    else 'Low'
)

# Review Length
df['review_length'] = df['review_content'].apply(len)

# Check data
print(df.head())
# Top 10 highest rated products

top_products = df.sort_values(
    by='rating',
    ascending=False
)[['product_name', 'category', 'rating']].head(10)

print(top_products)
# Top 10 most reviewed products

most_reviewed = df.sort_values(
    by='rating_count',
    ascending=False
)[['product_name', 'rating_count', 'rating']].head(10)

print(most_reviewed)
# Category-wise average rating

category_rating = df.groupby('category')['rating'].mean()

category_rating = category_rating.sort_values(
    ascending=False
).head(10)

print(category_rating)
# Extract main category

df['main_category'] = df['category'].apply(
    lambda x: x.split('|')[0]
)

print(df[['category', 'main_category']].head())
# Average rating by main category

main_category_rating = df.groupby(
    'main_category'
)['rating'].mean().sort_values(
    ascending=False
)

print(main_category_rating)
# Export cleaned dataset

df.to_csv(
    "cleaned_amazon_dataset.csv",
    index=False
)

print("Cleaned dataset exported successfully")