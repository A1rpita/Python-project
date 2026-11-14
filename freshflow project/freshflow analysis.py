
# ============================================================
# FRESHFLOW JUICE COMPANY
# NUMPY DATA ANALYST ASSIGNMENT
# TASK A TO TASK L
# ============================================================

import numpy as np
from pathlib import Path


# ============================================================
# SECTION 1 - IMPORT AND LOAD DATA
# ============================================================

print("\n========== FRESHFLOW JUICE COMPANY ==========")

file_path = (
    Path(__file__).resolve().parent.parent
    / "datasets"
    / "freshflow_sales.csv"
)

# Load CSV using NumPy
data = np.genfromtxt(
    file_path,
    delimiter=",",
    skip_header=1,
    dtype=float,
    ndmin=2
)

# Keep the original data unchanged
raw_data = data.copy()

# Column positions
transaction_id = data[:, 0]
day = data[:, 1]
outlet = data[:, 2]
product = data[:, 3]
category = data[:, 4]
quantity = data[:, 5]
price = data[:, 6]
cost = data[:, 7]
discount_rate = data[:, 8]
stock = data[:, 9]
payment = data[:, 10]
rating = data[:, 11]

column_names = [
    "Transaction ID",
    "Day Index",
    "Outlet ID",
    "Product Code",
    "Category Code",
    "Quantity",
    "Unit Price",
    "Unit Cost",
    "Discount Rate",
    "Stock Before Units",
    "Payment Code",
    "Customer Rating"
]


# ============================================================
# TASK A - DATA PROFILE
# ============================================================

print("\n========== TASK A: DATA PROFILE ==========")

print("Dataset shape:", data.shape)
print("Total rows:", data.shape[0])
print("Total columns:", data.shape[1])
print("Data type:", data.dtype)
print("Number of dimensions:", data.ndim)
print("Total number of elements:", data.size)
print("Memory used in bytes:", data.nbytes)

print("\nMissing values by column:")

for i in range(data.shape[1]):
    missing_count = np.isnan(data[:, i]).sum()
    print(column_names[i], ":", missing_count)

print("\nMinimum and maximum values:")

for i in range(data.shape[1]):
    if np.isfinite(data[:, i]).any():
        print(
            column_names[i],
            "Minimum:", np.nanmin(data[:, i]),
            "Maximum:", np.nanmax(data[:, i])
        )

print("\nExpected rows: 5000")
print("Actual rows:", data.shape[0])
print("Expected columns: 12")
print("Actual columns:", data.shape[1])

if data.shape == (5000, 12):
    print("Dataset dimensions are correct.")
else:
    print("Warning: Dataset dimensions do not match the requirement.")


# ============================================================
# TASK B - INTEGRITY AUDIT
# ============================================================

print("\n========== TASK B: INTEGRITY AUDIT ==========")

# Check duplicate transaction IDs
valid_id = np.isfinite(transaction_id)

unique_ids, id_counts = np.unique(
    transaction_id[valid_id],
    return_counts=True
)

duplicate_ids = unique_ids[id_counts > 1]

duplicate_mask = (
    valid_id &
    np.isin(transaction_id, duplicate_ids)
)

print("Duplicate transaction IDs:", len(duplicate_ids))
print("Records involved in duplicate IDs:", duplicate_mask.sum())

# Check invalid transaction IDs
invalid_id = (
    ~np.isfinite(transaction_id) |
    (transaction_id <= 0) |
    (transaction_id != np.floor(transaction_id))
)

print("Invalid transaction IDs:", invalid_id.sum())

# Check day values
invalid_day = (
    ~np.isfinite(day) |
    (day < 1) |
    (day > 30) |
    (day != np.floor(day))
)

print("Invalid day values:", invalid_day.sum())

# Check outlet codes
invalid_outlet = (
    ~np.isfinite(outlet) |
    (~np.isin(outlet, [1, 2, 3]))
)

print("Unknown outlet codes:", invalid_outlet.sum())

# Check product codes
invalid_product = (
    ~np.isfinite(product) |
    (~np.isin(product, [1, 2, 3, 4, 5, 6, 7, 8]))
)

print("Unknown product codes:", invalid_product.sum())

# Check category codes
invalid_category = (
    ~np.isfinite(category) |
    (~np.isin(category, [1, 2, 3, 4]))
)

print("Unknown category codes:", invalid_category.sum())

# Check payment codes
invalid_payment = (
    ~np.isfinite(payment) |
    (~np.isin(payment, [1, 2, 3, 4]))
)

print("Unknown payment codes:", invalid_payment.sum())

# Check product and category mapping
correct_category = np.zeros(len(data), dtype=bool)

for i in range(len(data)):
    if product[i] in [1, 2, 3, 4] and category[i] == 1:
        correct_category[i] = True
    elif product[i] in [5, 6] and category[i] == 2:
        correct_category[i] = True
    elif product[i] == 7 and category[i] == 3:
        correct_category[i] = True
    elif product[i] == 8 and category[i] == 4:
        correct_category[i] = True

category_mismatch = (
    ~invalid_product &
    ~invalid_category &
    ~correct_category
)

print("Product/category mismatches:", category_mismatch.sum())

# Check quantity
invalid_quantity = (
    ~np.isfinite(quantity) |
    (quantity <= 0) |
    (quantity != np.floor(quantity))
)

print("Invalid quantities:", invalid_quantity.sum())

# Check prices
invalid_price = (
    ~np.isfinite(price) |
    (price <= 0)
)

print("Missing or invalid prices:", invalid_price.sum())

# Check costs
invalid_cost = (
    ~np.isfinite(cost) |
    (cost < 0)
)

print("Missing or invalid costs:", invalid_cost.sum())

# Check discount rate
invalid_discount = (
    ~np.isfinite(discount_rate) |
    (discount_rate < 0) |
    (discount_rate > 1)
)

print("Invalid discount rates:", invalid_discount.sum())

# Check customer ratings
invalid_rating = (
    np.isfinite(rating) &
    ((rating < 1) | (rating > 5))
)

print("Invalid customer ratings:", invalid_rating.sum())
print("Missing customer ratings:", np.isnan(rating).sum())

# Check stock
invalid_stock = (
    np.isfinite(stock) &
    (stock < 0)
)

print("Negative stock values:", invalid_stock.sum())
print("Zero stock values:", (stock == 0).sum())


# ============================================================
# TASK C - CLEANING STRATEGY
# ============================================================

print("\n========== TASK C: CLEANING STRATEGY ==========")

# A transaction can be used for revenue analysis
# even if its unit cost is missing.

revenue_valid = (
    ~invalid_id &
    ~duplicate_mask &
    ~invalid_day &
    ~invalid_outlet &
    ~invalid_product &
    ~invalid_category &
    ~category_mismatch &
    ~invalid_payment &
    ~invalid_quantity &
    ~invalid_price &
    ~invalid_discount
)

# Create a separate cleaned revenue dataset
revenue_data = data[revenue_valid].copy()

# Profit analysis also requires valid unit cost
profit_valid = (
    revenue_valid &
    np.isfinite(cost) &
    (cost >= 0)
)

profit_data = data[profit_valid].copy()

print("Original records:", len(data))
print("Valid revenue records:", len(revenue_data))
print("Valid profit records:", len(profit_data))
print("Records excluded from revenue analysis:", len(data) - len(revenue_data))
print("Records excluded from profit analysis:", len(data) - len(profit_data))

print("\nCleaning rules:")
print("1. Duplicate transaction IDs are held out for investigation.")
print("2. Missing or invalid prices are excluded from revenue analysis.")
print("3. Missing or invalid costs are excluded from profit analysis only.")
print("4. Missing customer ratings are allowed.")
print("5. Invalid customer ratings are not used in rating calculations.")
print("6. High prices and high valid discounts are flagged, not automatically deleted.")
print("7. Stock problems are reported separately.")
print("8. Original raw data remains unchanged.")

# Extract cleaned revenue columns
rev_id = revenue_data[:, 0]
rev_day = revenue_data[:, 1]
rev_outlet = revenue_data[:, 2]
rev_product = revenue_data[:, 3]
rev_quantity = revenue_data[:, 5]
rev_price = revenue_data[:, 6]
rev_discount_rate = revenue_data[:, 8]

# Extract cleaned profit columns
profit_id = profit_data[:, 0]
profit_outlet = profit_data[:, 2]
profit_product = profit_data[:, 3]
profit_quantity = profit_data[:, 5]
profit_price = profit_data[:, 6]
profit_cost = profit_data[:, 7]
profit_discount_rate = profit_data[:, 8]


# ============================================================
# TASK D - METRIC ENGINE
# ============================================================

print("\n========== TASK D: METRIC ENGINE ==========")

# Calculate revenue metrics
gross_sales = rev_quantity * rev_price

discount_amount = gross_sales * rev_discount_rate

net_revenue = gross_sales - discount_amount

# Calculate profit metrics using records with valid costs
profit_gross_sales = profit_quantity * profit_price

profit_discount = profit_gross_sales * profit_discount_rate

profit_net_revenue = profit_gross_sales - profit_discount

cost_of_goods_sold = profit_quantity * profit_cost

gross_profit = profit_net_revenue - cost_of_goods_sold

total_gross_sales = gross_sales.sum()
total_discount = discount_amount.sum()
total_net_revenue = net_revenue.sum()

total_cogs = cost_of_goods_sold.sum()
total_gross_profit = gross_profit.sum()

# Calculate gross margin safely
if total_net_revenue != 0:
    gross_margin = total_gross_profit / total_net_revenue * 100
else:
    gross_margin = np.nan

# Calculate average selling price safely
total_quantity = rev_quantity.sum()

if total_quantity > 0:
    average_selling_price = total_net_revenue / total_quantity
else:
    average_selling_price = np.nan

# Calculate average transaction value
if len(revenue_data) > 0:
    average_transaction_value = total_net_revenue / len(revenue_data)
else:
    average_transaction_value = np.nan

# Calculate weighted discount percentage
if total_gross_sales != 0:
    weighted_discount = total_discount / total_gross_sales * 100
else:
    weighted_discount = np.nan

print("Total gross sales: ₹", round(total_gross_sales, 2))
print("Total discount amount: ₹", round(total_discount, 2))
print("Total net revenue: ₹", round(total_net_revenue, 2))
print("Total cost of goods sold: ₹", round(total_cogs, 2))
print("Total gross profit: ₹", round(total_gross_profit, 2))
print("Gross margin percentage:", round(gross_margin, 2))
print("Average selling price: ₹", round(average_selling_price, 2))
print("Average transaction value: ₹", round(average_transaction_value, 2))
print("Weighted discount percentage:", round(weighted_discount, 2))


# ============================================================
# TASK E - PRODUCT AND OUTLET COMPARISON
# ============================================================

print("\n========== TASK E: PRODUCT AND OUTLET COMPARISON ==========")

outlet_names = {
    1: "Outlet A",
    2: "Outlet B",
    3: "Outlet C"
}

product_names = {
    1: "Orange Juice",
    2: "Mango Juice",
    3: "Apple Juice",
    4: "Watermelon Juice",
    5: "Banana Smoothie",
    6: "Mixed Fruit Smoothie",
    7: "Lemonade",
    8: "Iced Tea"
}

print("\nOUTLET-WISE PERFORMANCE")

outlet_revenue_values = []
outlet_profit_values = []
outlet_unit_values = []

for outlet_code in [1, 2, 3]:

    revenue_mask = rev_outlet == outlet_code
    profit_mask = profit_outlet == outlet_code

    outlet_revenue = net_revenue[revenue_mask].sum()
    outlet_profit = gross_profit[profit_mask].sum()
    outlet_units = rev_quantity[revenue_mask].sum()

    outlet_revenue_values.append(outlet_revenue)
    outlet_profit_values.append(outlet_profit)
    outlet_unit_values.append(outlet_units)

    print("\n", outlet_names[outlet_code])
    print("Revenue: ₹", round(outlet_revenue, 2))
    print("Gross profit: ₹", round(outlet_profit, 2))
    print("Units sold:", outlet_units)

outlet_revenue_values = np.array(outlet_revenue_values)
outlet_profit_values = np.array(outlet_profit_values)
outlet_unit_values = np.array(outlet_unit_values)

print("\nOUTLET RANKING BY REVENUE")

revenue_ranking = np.argsort(outlet_revenue_values)[::-1]

for position in revenue_ranking:
    print(
        outlet_names[position + 1],
        "₹", round(outlet_revenue_values[position], 2)
    )

print("\nOUTLET RANKING BY GROSS PROFIT")

profit_ranking = np.argsort(outlet_profit_values)[::-1]

for position in profit_ranking:
    print(
        outlet_names[position + 1],
        "₹", round(outlet_profit_values[position], 2)
    )

print("\nOUTLET RANKING BY UNITS SOLD")

unit_ranking = np.argsort(outlet_unit_values)[::-1]

for position in unit_ranking:
    print(
        outlet_names[position + 1],
        outlet_unit_values[position], "units"
    )


print("\nPRODUCT-WISE PERFORMANCE")

product_revenue_values = []
product_profit_values = []
product_unit_values = []

for product_code in range(1, 9):

    revenue_mask = rev_product == product_code
    profit_mask = profit_product == product_code

    product_revenue = net_revenue[revenue_mask].sum()
    product_profit = gross_profit[profit_mask].sum()
    product_units = rev_quantity[revenue_mask].sum()

    product_revenue_values.append(product_revenue)
    product_profit_values.append(product_profit)
    product_unit_values.append(product_units)

    print("\n", product_names[product_code])
    print("Revenue: ₹", round(product_revenue, 2))
    print("Gross profit: ₹", round(product_profit, 2))
    print("Units sold:", product_units)

product_revenue_values = np.array(product_revenue_values)
product_profit_values = np.array(product_profit_values)
product_unit_values = np.array(product_unit_values)

print("\nPRODUCT RANKING BY REVENUE")

product_revenue_ranking = np.argsort(product_revenue_values)[::-1]

for position in product_revenue_ranking:
    print(
        product_names[position + 1],
        "₹", round(product_revenue_values[position], 2)
    )

print("\nPRODUCT RANKING BY GROSS PROFIT")

product_profit_ranking = np.argsort(product_profit_values)[::-1]

for position in product_profit_ranking:
    print(
        product_names[position + 1],
        "₹", round(product_profit_values[position], 2)
    )

print("\nPRODUCT RANKING BY UNITS SOLD")

product_unit_ranking = np.argsort(product_unit_values)[::-1]

for position in product_unit_ranking:
    print(
        product_names[position + 1],
        product_unit_values[position], "units"
    )

print("\nNote: Highest sales volume does not always mean highest profit.")
print("Profit also depends on selling price, unit cost and discount.")


# ============================================================
# TASK F - DESCRIPTIVE STATISTICS
# ============================================================

print("\n========== TASK F: DESCRIPTIVE STATISTICS ==========")

# Statistics for transaction-level net revenue
if len(net_revenue) > 0:

    print("\nNET REVENUE STATISTICS")

    print("Mean:", round(np.mean(net_revenue), 2))
    print("Median:", round(np.median(net_revenue), 2))
    print("Standard deviation:", round(np.std(net_revenue), 2))
    print("Variance:", round(np.var(net_revenue), 2))
    print("Minimum:", round(np.min(net_revenue), 2))
    print("Maximum:", round(np.max(net_revenue), 2))
    print("Range:", round(np.ptp(net_revenue), 2))

    print("25th percentile:", round(np.percentile(net_revenue, 25), 2))
    print("50th percentile:", round(np.percentile(net_revenue, 50), 2))
    print("75th percentile:", round(np.percentile(net_revenue, 75), 2))

    # Check extreme values using IQR
    q1 = np.percentile(net_revenue, 25)
    q3 = np.percentile(net_revenue, 75)

    iqr = q3 - q1

    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr

    extreme_revenue = (
        (net_revenue < lower_limit) |
        (net_revenue > upper_limit)
    )

    print("Extreme revenue records:", extreme_revenue.sum())

    if np.mean(net_revenue) > np.median(net_revenue):
        print("Interpretation: Revenue may be positively skewed.")
    elif np.mean(net_revenue) < np.median(net_revenue):
        print("Interpretation: Revenue may be negatively skewed.")
    else:
        print("Interpretation: Mean and median are equal.")

    print("Extreme values should be investigated, not automatically deleted.")

# Statistics for gross profit
if len(gross_profit) > 0:
    print("\nGROSS PROFIT STATISTICS")
    print("Mean:", round(np.mean(gross_profit), 2))
    print("Median:", round(np.median(gross_profit), 2))
    print("Standard deviation:", round(np.std(gross_profit), 2))
    print("25th percentile:", round(np.percentile(gross_profit, 25), 2))
    print("75th percentile:", round(np.percentile(gross_profit, 75), 2))


# ============================================================
# TASK G - DAILY TREND ANALYSIS
# ============================================================

print("\n========== TASK G: DAILY TREND ANALYSIS ==========")

# Create revenue totals for all 30 days
daily_revenue = np.zeros(30)

for day_number in range(1, 31):

    day_mask = rev_day == day_number

    daily_revenue[day_number - 1] = net_revenue[day_mask].sum()

print("\nDAILY REVENUE")

for i in range(30):
    print(
        "Day", i + 1,
        "Revenue: ₹", round(daily_revenue[i], 2)
    )

# Calculate absolute daily changes
daily_change = np.diff(daily_revenue)

print("\nDAILY ABSOLUTE CHANGES")

for i in range(len(daily_change)):
    print(
        "Day", i + 2,
        "Change: ₹", round(daily_change[i], 2)
    )

# Calculate percentage changes safely
daily_percentage_change = np.full(29, np.nan)

for i in range(1, 30):

    previous_revenue = daily_revenue[i - 1]

    if previous_revenue != 0:
        daily_percentage_change[i - 1] = (
            (daily_revenue[i] - previous_revenue)
            / previous_revenue
        ) * 100

print("\nDAILY PERCENTAGE CHANGES")

for i in range(len(daily_percentage_change)):
    print(
        "Day", i + 2,
        "Percentage change:",
        round(daily_percentage_change[i], 2)
        if np.isfinite(daily_percentage_change[i])
        else "Undefined"
    )

# Calculate 3-day moving average
moving_average = np.convolve(
    daily_revenue,
    np.ones(3) / 3,
    mode="valid"
)

print("\n3-DAY MOVING AVERAGE")

for i in range(len(moving_average)):
    print(
        "Days", i + 1, "to", i + 3,
        "Average revenue: ₹", round(moving_average[i], 2)
    )

# Identify highest and lowest revenue days
highest_day = np.argmax(daily_revenue) + 1
lowest_day = np.argmin(daily_revenue) + 1

print("\nHighest revenue day:", highest_day)
print("Highest daily revenue: ₹", round(daily_revenue.max(), 2))

print("Lowest revenue day:", lowest_day)
print("Lowest daily revenue: ₹", round(daily_revenue.min(), 2))

# Flag unusual days using IQR
daily_q1 = np.percentile(daily_revenue, 25)
daily_q3 = np.percentile(daily_revenue, 75)
daily_iqr = daily_q3 - daily_q1

daily_lower_limit = daily_q1 - 1.5 * daily_iqr
daily_upper_limit = daily_q3 + 1.5 * daily_iqr

unusual_days = (
    (daily_revenue < daily_lower_limit) |
    (daily_revenue > daily_upper_limit)
)

print("Unusual days for review:")

for i in range(30):
    if unusual_days[i]:
        print(
            "Day", i + 1,
            "Revenue: ₹", round(daily_revenue[i], 2)
        )


# ============================================================
# TASK H - DISCOUNT INVESTIGATION
# ============================================================

print("\n========== TASK H: DISCOUNT INVESTIGATION ==========")

# Use profit-valid records so that all bands have
# comparable revenue and profit calculations.
band_gross_sales = profit_quantity * profit_price
band_discount_amount = band_gross_sales * profit_discount_rate
band_net_revenue = band_gross_sales - band_discount_amount
band_cogs = profit_quantity * profit_cost
band_gross_profit = band_net_revenue - band_cogs

# Discount bands:
# 0% to less than 5%
# 5% to less than 15%
# 15% and above

discount_band = np.select(
    [
        profit_discount_rate < 0.05,
        (profit_discount_rate >= 0.05) &
        (profit_discount_rate < 0.15),
        profit_discount_rate >= 0.15
    ],
    [1, 2, 3],
    default=0
)

band_names = {
    1: "Low discount (0% to below 5%)",
    2: "Medium discount (5% to below 15%)",
    3: "High discount (15% and above)"
}

for band_number in [1, 2, 3]:

    band_mask = discount_band == band_number

    band_count = band_mask.sum()
    band_units = profit_quantity[band_mask].sum()
    band_revenue = band_net_revenue[band_mask].sum()
    band_profit = band_gross_profit[band_mask].sum()

    if band_revenue != 0:
        band_margin = band_profit / band_revenue * 100
    else:
        band_margin = np.nan

    print("\n", band_names[band_number])
    print("Transactions:", band_count)
    print("Quantity sold:", band_units)
    print("Net revenue: ₹", round(band_revenue, 2))
    print("Gross profit: ₹", round(band_profit, 2))
    print("Gross margin:", round(band_margin, 2))

# Correlation between discount and quantity
correlation_mask = (
    np.isfinite(profit_discount_rate) &
    np.isfinite(profit_quantity)
)

correlation_discount = profit_discount_rate[correlation_mask]
correlation_quantity = profit_quantity[correlation_mask]

if (
    len(correlation_discount) >= 2 and
    np.std(correlation_discount) > 0 and
    np.std(correlation_quantity) > 0
):
    correlation = np.corrcoef(
        correlation_discount,
        correlation_quantity
    )[0, 1]

    print("\nDiscount and quantity correlation:", round(correlation, 3))
else:
    print("\nCorrelation cannot be calculated.")

print("\nInterpretation:")
print("A relationship between discount and quantity does not prove")
print("that discounts caused higher sales.")
print("Product type, outlet, day and customer behaviour may also affect sales.")
print("This comparison may contain selection bias and confounding.")


# ============================================================
# TASK I - ANOMALY REGISTER
# ============================================================

print("\n========== TASK I: ANOMALY REGISTER ==========")

# Identify unusually high valid prices using IQR
valid_prices = price[np.isfinite(price) & (price > 0)]

if len(valid_prices) > 0:

    price_q1 = np.percentile(valid_prices, 25)
    price_q3 = np.percentile(valid_prices, 75)
    price_iqr = price_q3 - price_q1

    high_price_limit = price_q3 + 1.5 * price_iqr

    high_price = (
        np.isfinite(price) &
        (price > high_price_limit)
    )
else:
    high_price_limit = np.nan
    high_price = np.zeros(len(data), dtype=bool)

# High valid discount flag
high_discount = (
    np.isfinite(discount_rate) &
    (discount_rate > 0.50) &
    (discount_rate <= 1)
)

# Zero stock flag
zero_stock = (
    np.isfinite(stock) &
    (stock == 0)
)

# Combine anomaly flags
anomaly_mask = (
    high_price |
    high_discount |
    zero_stock
)

anomaly_rows = np.where(anomaly_mask)[0]

print("High price threshold:", high_price_limit)
print("High price records:", high_price.sum())
print("High discount records:", high_discount.sum())
print("Zero stock records:", zero_stock.sum())
print("Total records with at least one anomaly:", anomaly_mask.sum())

print("\nANOMALY REGISTER")

for row in anomaly_rows:

    reasons = []

    if high_price[row]:
        reasons.append("HIGH_PRICE")

    if high_discount[row]:
        reasons.append("HIGH_DISCOUNT")

    if zero_stock[row]:
        reasons.append("ZERO_STOCK")

    print(
        "Transaction ID:", transaction_id[row],
        "| Reason:", ", ".join(reasons)
    )

print("\nAnomalies are flagged for review, not automatically deleted.")
print("Financial impact is estimated only where the required data is valid.")


# ============================================================
# TASK J - SCENARIO ANALYSIS
# ============================================================

print("\n========== TASK J: SCENARIO ANALYSIS ==========")

# Use the same profit-valid records for every scenario
# Quantity and unit cost remain unchanged.

baseline_revenue = band_net_revenue.sum()
baseline_profit = band_gross_profit.sum()

scenario_rates = [0.05, 0.10]

print("Baseline revenue: ₹", round(baseline_revenue, 2))
print("Baseline gross profit: ₹", round(baseline_profit, 2))

for scenario_rate in scenario_rates:

    scenario_discount = (
        band_gross_sales * scenario_rate
    )

    scenario_revenue = (
        band_gross_sales - scenario_discount
    )

    scenario_profit = (
        scenario_revenue - band_cogs
    )

    total_scenario_revenue = scenario_revenue.sum()
    total_scenario_profit = scenario_profit.sum()

    revenue_change = (
        total_scenario_revenue - baseline_revenue
    )

    profit_change = (
        total_scenario_profit - baseline_profit
    )

    if baseline_revenue != 0:
        revenue_change_percent = (
            revenue_change / baseline_revenue
        ) * 100
    else:
        revenue_change_percent = np.nan

    if baseline_profit != 0:
        profit_change_percent = (
            profit_change / baseline_profit
        ) * 100
    else:
        profit_change_percent = np.nan

    print("\nScenario discount:", scenario_rate * 100, "%")
    print("Scenario revenue: ₹", round(total_scenario_revenue, 2))
    print("Scenario gross profit: ₹", round(total_scenario_profit, 2))

    print("Revenue change: ₹", round(revenue_change, 2))
    print("Revenue change percentage:", round(revenue_change_percent, 2))

    print("Profit change: ₹", round(profit_change, 2))
    print("Profit change percentage:", round(profit_change_percent, 2))

print("\nScenario assumptions:")
print("1. Quantity sold remains constant.")
print("2. Unit cost remains constant.")
print("3. Only the discount rate changes.")
print("4. The scenarios are not sales forecasts.")
print("5. Actual customer demand may change after a discount change.")


# ============================================================
# TASK K - VALIDATION TESTS
# ============================================================

print("\n========== TASK K: VALIDATION TESTS ==========")

# Test 1: Check dataset shape
assert data.ndim == 2, "Dataset must be two-dimensional."
assert data.shape[1] == 12, "Dataset must contain 12 columns."

print("Test 1 passed: Dataset shape is valid.")

# Test 2: Check expected record count
assert data.shape[0] == 5000, "Dataset must contain 5000 rows."

print("Test 2 passed: Dataset contains 5000 rows.")

# Test 3: Check missing-value behaviour
test_missing = np.array([10.0, np.nan, 20.0])

assert np.isnan(test_missing[1]), "Missing value test failed."

print("Test 3 passed: Missing values are represented by NaN.")

# Test 4: Check safe zero denominator
test_numerator = 100
test_denominator = 0

if test_denominator != 0:
    test_result = test_numerator / test_denominator
else:
    test_result = np.nan

assert np.isnan(test_result), "Zero denominator test failed."

print("Test 4 passed: Zero denominator is handled safely.")

# Test 5: Independently calculate the first five profit rows
sample_count = min(5, len(profit_data))

manual_revenue = []
manual_profit = []

for i in range(sample_count):

    sample_gross_sales = (
        profit_data[i, 5] * profit_data[i, 6]
    )

    sample_discount = (
        sample_gross_sales * profit_data[i, 8]
    )

    sample_net_revenue = (
        sample_gross_sales - sample_discount
    )

    sample_cogs = (
        profit_data[i, 5] * profit_data[i, 7]
    )

    sample_gross_profit = (
        sample_net_revenue - sample_cogs
    )

    manual_revenue.append(sample_net_revenue)
    manual_profit.append(sample_gross_profit)

manual_revenue = np.array(manual_revenue)
manual_profit = np.array(manual_profit)

np.testing.assert_allclose(
    manual_revenue,
    profit_net_revenue[:sample_count]
)

np.testing.assert_allclose(
    manual_profit,
    gross_profit[:sample_count]
)

print("Test 5 passed: Five sample rows match manual calculations.")

# Test 6: Check that raw data has not changed
np.testing.assert_equal(data, raw_data)

print("Test 6 passed: Original raw data remains unchanged.")

print("\nAll validation tests completed successfully.")


# ============================================================
# TASK L - EXECUTIVE RECOMMENDATIONS
# ============================================================

print("\n========== TASK L: EXECUTIVE RECOMMENDATIONS ==========")

# Finding 1: Highest revenue outlet
best_outlet_index = np.argmax(outlet_revenue_values)

print("\nFINDING 1")
print(
    "The highest revenue outlet is:",
    outlet_names[best_outlet_index + 1]
)
print(
    "Revenue: ₹",
    round(outlet_revenue_values[best_outlet_index], 2)
)
print("Recommendation: Review this outlet's sales practices and")
print("identify practices that may be useful at other outlets.")
print("Metric to monitor: Daily net revenue by outlet.")

# Finding 2: Highest gross profit product
best_product_index = np.argmax(product_profit_values)

print("\nFINDING 2")
print(
    "The highest gross profit product is:",
    product_names[best_product_index + 1]
)
print(
    "Gross profit: ₹",
    round(product_profit_values[best_product_index], 2)
)
print("Recommendation: Review product-level pricing, cost and")
print("discount decisions before changing the product mix.")
print("Metric to monitor: Gross profit by product.")

# Finding 3: Highest revenue day
print("\nFINDING 3")
print("The highest revenue day is:", highest_day)
print(
    "Daily revenue: ₹",
    round(daily_revenue.max(), 2)
)
print("Recommendation: Investigate the transactions and conditions")
print("on this day before repeating any sales strategy.")
print("Metric to monitor: Daily net revenue and transaction count.")

print("\nLIMITATIONS")
print("1. The dataset covers only 30 observation days.")
print("2. Missing and invalid records affect the analysis.")
print("3. Gross profit does not include rent, salaries or other operating expenses.")
print("4. Correlation does not prove causation.")
print("5. Discount scenarios assume quantity remains unchanged.")
print("6. Transaction data alone cannot establish inventory waste.")

print("\nNEXT STEPS")
print("1. Review flagged transactions and data-quality issues.")
print("2. Monitor outlet and product performance regularly.")
print("3. Test discount changes before making business-wide decisions.")
print("4. Collect more data for stronger business conclusions.")

print("\n========== FRESHFLOW ASSIGNMENT COMPLETED ==========")

