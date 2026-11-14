
import numpy as np
from pathlib import Path

# ==========================================
# FRESHFLOW JUICE COMPANY
# NUMPY DATASET GENERATION
# ==========================================

# STEP 1: CREATE DATASET

np.random.seed(42)

rows = 5000

data = np.zeros((rows, 12), dtype=float)

# STEP 2: GENERATE BASIC DATA

data[:, 0] = np.arange(100001, 100001 + rows)
data[:, 1] = np.random.randint(1, 31, rows)
data[:, 2] = np.random.randint(1, 4, rows)
data[:, 3] = np.random.randint(1, 9, rows)

# STEP 3: PRODUCT CATEGORY MAPPING

product_category = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 4
}

data[:, 4] = np.array([
    product_category[int(p)] for p in data[:, 3]
])

# STEP 4: GENERATE SALES INFORMATION

data[:, 5] = np.random.randint(1, 11, rows)

data[:, 6] = np.round(
    np.random.uniform(20, 200, rows), 2
)

data[:, 7] = np.round(
    np.random.uniform(10, 150, rows), 2
)

data[:, 8] = np.round(
    np.random.uniform(0, 0.30, rows), 2
)

data[:, 9] = np.random.randint(1, 101, rows)
data[:, 10] = np.random.randint(1, 5, rows)
data[:, 11] = np.random.randint(1, 6, rows)

# STEP 5: INSERT DATA QUALITY ISSUES

# Missing unit price - 4 records
data[0:4, 6] = np.nan

# Missing unit cost - 4 records
data[4:8, 7] = np.nan

# Missing customer ratings - 20 records
data[8:28, 11] = np.nan

# Duplicate transaction IDs - 5 records involved
data[28:32, 0] = data[27, 0]

# Zero or negative quantity - 4 records
data[32:36, 5] = [0, -1, 0, -2]

# Negative unit price - 2 records
data[36:38, 6] = [-10, -25]

# Negative unit cost - 2 records
data[38:40, 7] = [-5, -15]

# Invalid discount rates - 2 records
data[40:42, 8] = [1.2, 1.5]

# Invalid customer ratings - 3 records
data[42:45, 11] = [0, 6, 8]

# Incorrect product/category mapping - 4 records
data[45:49, 4] = [3, 3, 1, 3]

# Unknown outlet codes - 2 records
data[49:51, 2] = [99, 100]

# Unusually high but valid prices - 3 records
data[51:54, 6] = [500, 750, 1000]

# High but valid discounts - 5 records
data[54:59, 8] = [0.70, 0.80, 0.85, 0.90, 0.95]

# Zero stock before transaction - 5 records
data[59:64, 9] = [0, 0, 0, 0, 0]

# STEP 6: DEFINE COLUMN NAMES

column_names = (
    "transaction_id,day_index,outlet_id,product_code,"
    "category_code,quantity,unit_price,unit_cost,"
    "discount_rate,stock_before_units,payment_code,"
    "customer_rating"
)

# STEP 7: SAVE CSV FILE

file_path = (
    Path(__file__).resolve().parent
    / "freshflow_sales.csv"
)

np.savetxt(
    file_path,
    data,
    delimiter=",",
    header=column_names,
    comments="",
    fmt="%.2f"
)

# STEP 8: DISPLAY DATASET INFORMATION

print("\n================================")
print("FRESHFLOW DATASET GENERATED!")
print("================================")

print("Dataset shape:", data.shape)
print("Total rows:", data.shape[0])
print("Total columns:", data.shape[1])

print("\nFirst 5 records:")
print(data[:5])

print("\nMissing values by column:")
print(np.isnan(data).sum(axis=0))

print("\nCSV file saved successfully at:")
print(file_path)

print("\n================================")
print("PROCESS COMPLETED SUCCESSFULLY")
print("================================")

