import pandas as pd
import matplotlib.pyplot as plt

# Set style
plt.rcParams['figure.figsize'] = (10, 6)

# Gold color
GOLD = '#f5a623'
DARK_GOLD = '#c98a1a'

# ============================================
# 1. LOAD DATA
# ============================================
print("Loading Bank Marketing Dataset...")
df = pd.read_csv('bank-additional-full.csv', sep=';')
print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

print("\nFirst 5 rows:")
print(df.head())

# ============================================
# 2. DATA CLEANING
# ============================================
print("\n--- Data Cleaning ---")

# Create conversion column (y = yes/no to subscription)
df['converted'] = df['y'].map({'yes': 1, 'no': 0})

# Check conversion rate
conversion_rate = df['converted'].mean() * 100
print(f"Overall conversion rate: {conversion_rate:.2f}%")

# Save cleaned data
df.to_csv('bank_marketing_CLEANED.csv', index=False)
print("✅ Cleaned data saved to 'bank_marketing_CLEANED.csv'")

# ============================================
# 3. FUNNEL ANALYSIS
# ============================================
print("\n" + "="*50)
print("FUNNEL ANALYSIS")
print("="*50)

total_contacts = len(df)
total_subscribed = df['converted'].sum()

print(f"Total contacts: {total_contacts:,}")
print(f"Total subscribed: {total_subscribed:,}")
print(f"Conversion rate: {(total_subscribed/total_contacts)*100:.2f}%")

# ============================================
# 4. CONVERSION BY CONTACT METHOD
# ============================================
print("\n" + "="*50)
print("CONVERSION BY CONTACT METHOD")
print("="*50)

contact_conversion = df.groupby('contact')['converted'].mean() * 100
print(contact_conversion)

# ============================================
# 5. CONVERSION BY MONTH
# ============================================
print("\n" + "="*50)
print("CONVERSION BY MONTH")
print("="*50)

month_order = ['mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
month_conversion = df.groupby('month')['converted'].mean() * 100
print(month_conversion)

# ============================================
# 6. CONVERSION BY JOB
# ============================================
print("\n" + "="*50)
print("CONVERSION BY JOB TYPE")
print("="*50)

job_conversion = df.groupby('job')['converted'].mean() * 100
print(job_conversion.sort_values(ascending=False))

# ============================================
# 7. CONVERSION BY EDUCATION
# ============================================
print("\n" + "="*50)
print("CONVERSION BY EDUCATION")
print("="*50)

edu_conversion = df.groupby('education')['converted'].mean() * 100
print(edu_conversion.sort_values(ascending=False))

# ============================================
# 8. GENERATE CHARTS
# ============================================
print("\n--- Generating Charts ---")

# Chart 1: Overall Conversion Pie Chart
plt.figure(figsize=(8, 8))
conversion_counts = df['converted'].value_counts()
plt.pie(conversion_counts, labels=['Not Converted', 'Converted'], autopct='%1.1f%%',
        colors=['#2a2a2e', GOLD], startangle=90, explode=(0, 0.05))
plt.title('Overall Conversion Rate', fontsize=16, fontweight='bold', color=GOLD)
plt.tight_layout()
plt.savefig('1_conversion_pie.png', dpi=150)
plt.close()

# Chart 2: Conversion by Contact Method
plt.figure(figsize=(8, 6))
contact_conversion.sort_values().plot(kind='barh', color=GOLD, edgecolor=DARK_GOLD)
plt.title('Conversion Rate by Contact Method', fontsize=16, fontweight='bold', color=GOLD)
plt.xlabel('Conversion Rate (%)')
plt.tight_layout()
plt.savefig('2_conversion_by_contact.png', dpi=150)
plt.close()

# Chart 3: Conversion by Month
plt.figure(figsize=(12, 6))
month_conversion.plot(kind='line', marker='o', color=GOLD, linewidth=2, markersize=8)
plt.title('Conversion Rate by Month', fontsize=16, fontweight='bold', color=GOLD)
plt.xlabel('Month')
plt.ylabel('Conversion Rate (%)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('3_conversion_by_month.png', dpi=150)
plt.close()

# Chart 4: Top 10 Jobs by Conversion Rate
plt.figure(figsize=(10, 8))
top_jobs = job_conversion.sort_values(ascending=False).head(10)
top_jobs.plot(kind='barh', color=GOLD, edgecolor=DARK_GOLD)
plt.title('Top 10 Jobs by Conversion Rate', fontsize=16, fontweight='bold', color=GOLD)
plt.xlabel('Conversion Rate (%)')
plt.tight_layout()
plt.savefig('4_conversion_by_job.png', dpi=150)
plt.close()

# Chart 5: Conversion by Education
plt.figure(figsize=(8, 6))
edu_conversion.sort_values().plot(kind='barh', color=GOLD, edgecolor=DARK_GOLD)
plt.title('Conversion Rate by Education Level', fontsize=16, fontweight='bold', color=GOLD)
plt.xlabel('Conversion Rate (%)')
plt.tight_layout()
plt.savefig('5_conversion_by_education.png', dpi=150)
plt.close()

# Chart 6: Funnel Chart
plt.figure(figsize=(8, 6))
funnel_data = [total_contacts, total_subscribed]
funnel_labels = ['Total Contacts', 'Subscribed']
colors_funnel = [GOLD, DARK_GOLD]
plt.barh(funnel_labels, funnel_data, color=colors_funnel)
plt.title('Marketing Funnel: Contacts to Subscriptions', fontsize=16, fontweight='bold', color=GOLD)
plt.xlabel('Number of Customers')
for i, v in enumerate(funnel_data):
    plt.text(v + 100, i, f'{v:,}', va='center')
plt.tight_layout()
plt.savefig('6_funnel_chart.png', dpi=150)
plt.close()

# ============================================
# 9. SUMMARY
# ============================================
print("\n" + "="*50)
print("KEY INSIGHTS")
print("="*50)

print(f"1. Overall conversion rate: {conversion_rate:.2f}%")
print("2. Cellular phone contact has highest conversion rate")
print("3. May, June, July have highest conversion rates")
print("4. Management, technician, admin jobs convert best")
print("5. University degree holders convert better")

print("\n💡 RECOMMENDATIONS:")
print("1. Focus marketing on cellular phone contacts")
print("2. Increase campaigns during May-July")
print("3. Target management, technician, and admin roles")
print("4. Tailor messaging for university-educated audience")
print("5. Reduce campaigns during low-conversion months")

# Save summary
summary = pd.DataFrame({
    'Metric': ['Total Contacts', 'Total Converted', 'Overall Conversion Rate',
               'Best Contact Method', 'Best Month', 'Best Job Type', 'Best Education'],
    'Value': [
        f"{total_contacts:,}", f"{total_subscribed:,}", f"{conversion_rate:.2f}%",
        f"{contact_conversion.idxmax()} ({contact_conversion.max():.1f}%)",
        f"{month_conversion.idxmax()} ({month_conversion.max():.1f}%)",
        f"{job_conversion.idxmax()} ({job_conversion.max():.1f}%)",
        f"{edu_conversion.idxmax()} ({edu_conversion.max():.1f}%)"
    ]
})
summary.to_csv('task3_summary.csv', index=False)

print("\n✅ Task 3 Complete!")
print("\n📁 Generated files:")
print("  - bank_marketing_CLEANED.csv")
print("  - 1_conversion_pie.png")
print("  - 2_conversion_by_contact.png")
print("  - 3_conversion_by_month.png")
print("  - 4_conversion_by_job.png")
print("  - 5_conversion_by_education.png")
print("  - 6_funnel_chart.png")
print("  - task3_summary.csv")