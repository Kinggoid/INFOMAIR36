import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
import seaborn as sns
from scipy import stats
from scipy.stats import zscore
import ptitprince as pt

# Import data
# Corrected line with matching quotes
df = pd.read_csv(r"C:\Users\jenne\Documents\CODE\GitHub\INFOMAIR36\part_two\experiment_code\fake_data.csv",
                 delimiter=";")

# Display the first few rows of the dataframe
print(df)

# Check for normality
columns_to_check = ["INF_nTURNS", "INF_TIME", "F_nTURNS", "F_TIME"]

for col in columns_to_check:
    # Shapiro-Wilk test
    stat, p_value = stats.shapiro(df[col])
    print(f"{col}:")
    print(f"Shapiro-Wilk Test Statistic = {stat}, p-value = {p_value}")
    
    if p_value > 0.05:
        print(f"{col} looks normally distributed (p > 0.05)")
    else:
        print(f"{col} does not look normally distributed (p <= 0.05)")
    
    print()
    
    # Plot histogram
    # plt.figure(figsize=(6, 4))
    # sns.histplot(df[col], kde=True)
    # plt.title(f"Histogram of {col}")
    # plt.show()
   
# -----------------------------------------------------------------------------
# If assumption for normality is met, z-score into 1:

# Apply the zscore function to each of the selected columns
df['INF_zscore'] = zscore(df['INF_nTURNS']) + zscore(df['INF_TIME'])
df['F_zscore'] = zscore(df['F_nTURNS']) + zscore(df['F_TIME'])
print(df)

# Check effects of communication style (informal/formal) on functionality score

# Perform a dependent t-test (paired t-test) between INF_nTURNS and F_nTURNS
t_stat, p_value = stats.ttest_rel(df['INF_zscore'], df['F_zscore'])

# Display results
print(f"\nZscore formal vs. informal:")
print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")

# Interpretation of p-value
alpha = 0.05  # Common significance level
if p_value < alpha:
    print(f"Reject the null hypothesis: There is a significant difference between the two groups.\n")
else:
    print(f"Fail to reject the null hypothesis: There is no significant difference between the two groups.\n")

# -----------------------------------------------------------------------------

# If assumption for normality is not met...

# (1) Compare first nTURNS informal vs. formal

# Dependent t-test (paired t-test) between INF_nTURNS and F_nTURNS
t_stat, p_value = stats.ttest_rel(df['INF_nTURNS'], df['F_nTURNS'])

# Display results
print(f"nTURNS formal vs. informal:")
print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")

# Interpretation of p-value
alpha = 0.05  # Common significance level
if p_value < alpha:
    print(f"Reject the null hypothesis: There is a significant difference between the two groups.\n")
else:
    print(f"Fail to reject the null hypothesis: There is no significant difference between the two groups.\n")

# Compare second TIME informal vs. formal

# Dependent t-test (paired t-test) between INF_nTURNS and F_nTURNS
t_stat, p_value = stats.ttest_rel(df['INF_TIME'], df['F_TIME'])

# Display results
print("TIME formal vs. informal:")
print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")

# Interpretation of p-value
alpha = 0.05  # Common significance level
if p_value < alpha:
    print(f"Reject the null hypothesis: There is a significant difference between the two groups.\n")
else:
    print(f"Fail to reject the null hypothesis: There is no significant difference between the two groups.\n")

# Experiment 2: QUESTIONNAIRE -----------------------------------------------------------

# Dependent t-test (paired t-test) between INF_nTURNS and F_nTURNS
t_stat, p_value = stats.ttest_rel(df['INF_CUQ'], df['F_CUQ'])

# Display results
print("QUESTIONNAIRE formal vs. informal:")
print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")

# Interpretation of p-value
alpha = 0.05  # Common significance level
if p_value < alpha:
    print(f"Reject the null hypothesis: There is a significant difference between the two groups.\n")
else:
    print(f"Fail to reject the null hypothesis: There is no significant difference between the two groups.\n")

# VISUALIZATIONS ---------------------------------------------------------------------------------------------

# Reshape into long format (df) 

# Melt the data to long format for "zscore", "nTURNS", and "TIME" with an added CATEGORY column
data_long = pd.melt(
    df,
    id_vars=["ID", "FORMAL_FIRST", "AGE", "GENDER"],
    value_vars=["INF_CUQ", "F_CUQ", "INF_nTURNS", "F_nTURNS", "INF_TIME", "F_TIME", "INF_zscore", "F_zscore"],
    var_name="VARIABLE",
    value_name="VALUE"
)

# Map variable names to category and measurement type
data_long['CATEGORY'] = data_long['VARIABLE'].apply(lambda x: 'Informal' if 'INF' in x else 'Formal')
data_long['MEASUREMENT'] = data_long['VARIABLE'].str.extract(r'(CUQ|nTURNS|TIME|zscore)')[0]

# Drop the original VARIABLE column as it has been split
data_long = data_long.drop(columns=['VARIABLE'])

# Pivot to get one row per ID, CATEGORY, and MEASUREMENT
data_long = data_long.pivot_table(
    index=["ID", "FORMAL_FIRST", "AGE", "GENDER", "CATEGORY"],
    columns="MEASUREMENT",
    values="VALUE"
).reset_index()

# Display the transformed DataFrame
print(data_long)

# RAINCLOUD PLOTS -------------------------------------------------------------------------

# Raincloud plot nTURNS formal vs. informal
plt.figure(figsize=(10, 6))

ax = pt.RainCloud(x="CATEGORY", y="nTURNS", data=data_long,
                  palette="Set2", bw=.2, width_viol=.7, 
                  ax=None, orient="h", move=.2)

# Display the plot
plt.title("No effects of communication style on amount of system turns")
plt.ylabel("Communication style")
plt.xlabel("Amount of turns")
plt.show()

# Raincloud plot time (sec) formal vs. informal
plt.figure(figsize=(10, 6))

ax = pt.RainCloud(x="CATEGORY", y="TIME", data=data_long,
                  palette="Set2", bw=.2, width_viol=.7, 
                  ax=None, orient="h", move=.2)

# Display the plot
plt.title("No effects of communication style on amount of time spend chatting")
plt.ylabel("Communication style")
plt.xlabel("Time spend chatting (sec)")
plt.show()

# Raincloud plot QUESTIONNAIRE formal vs. informal
plt.figure(figsize=(10, 6))

ax = pt.RainCloud(x="CATEGORY", y="CUQ", data=data_long,
                  palette="Set2", bw=.2, width_viol=.7, 
                  ax=None, orient="h", move=.2)

# Display the plot
plt.title("Effects of communication style on user satisfaction (CUQ)")
plt.ylabel("Communication style")
plt.xlabel("Score (CUQ)")
plt.show()