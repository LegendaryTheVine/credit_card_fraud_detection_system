# Reference solution for Day 3. Cell markers (# %%) open as notebook cells in VS Code.
# NOTE: written without access to the dataset; run it once against the real file
# and confirm the numbers quoted in the lesson plan and answer key.

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../../../../student/data/creditcard.csv")

# %% 1. First look
print(df.shape)
print(df.dtypes.value_counts())
print("missing:", df.isna().sum().sum())
print("duplicates:", df.duplicated().sum())

# %% 2. Class balance
counts = df["Class"].value_counts()
print(counts)
print(df["Class"].value_counts(normalize=True) * 100)
print("always-not-fraud accuracy:", counts[0] / len(df))
ax = counts.plot.bar(logy=True)
ax.set_title("Class counts (log scale)")
plt.show()

# %% 3. Amount
print(df["Amount"].describe())
print(df.groupby("Class")["Amount"].describe())
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
df["Amount"].hist(bins=100, ax=axes[0]); axes[0].set_title("Amount")
np.log1p(df["Amount"]).hist(bins=100, ax=axes[1]); axes[1].set_title("log1p(Amount)")
plt.show()

# %% 4. Time: seconds since the first transaction, not clock time
print(df["Time"].max() / 3600, "hours of data")
df["hour"] = (df["Time"] // 3600) % 24
by_hour = df.groupby(["hour", "Class"]).size().unstack(fill_value=0)
by_hour.plot(subplots=True, figsize=(10, 6), title="Transactions per hour by class")
plt.show()
print((by_hour[1] / by_hour.sum(axis=1)).round(5))  # fraud share by hour

# %% 5. V1-V28
v = [f"V{i}" for i in range(1, 29)]
plt.figure(figsize=(10, 8))
sns.heatmap(df[v].corr(), cmap="coolwarm", center=0)
plt.title("Correlation of V1-V28")
plt.show()

corr_class = df[v].corrwith(df["Class"]).sort_values()
print(corr_class)
corr_class.plot.barh(figsize=(6, 8))
plt.show()

top = corr_class.abs().sort_values(ascending=False).index[:2]
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, col in zip(axes, top):
    sns.boxplot(data=df, x="Class", y=col, ax=ax)
plt.show()
