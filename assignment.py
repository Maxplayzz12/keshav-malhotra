#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
import pandas as pd
import json

# API Endpoints
CURRENT_QUIZ_URL = "https://api.jsonserve.com/rJvd7g"
HISTORICAL_QUIZ_URL = "https://api.jsonserve.com/XgAgFJ"

# Fetch data function
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {url}")
        return None

# Fetch Quiz Data
current_quiz = fetch_data(CURRENT_QUIZ_URL)
historical_quiz = fetch_data(HISTORICAL_QUIZ_URL)

# Print to debug structure
print("Historical Quiz Data Sample:")
print(json.dumps(historical_quiz[:2], indent=4))  # Print first 2 elements

# Ensure historical_quiz is a list before converting to DataFrame
if isinstance(historical_quiz, list):
    historical_df = pd.DataFrame(historical_quiz)
else:
    print("Unexpected data format:", type(historical_quiz))


# In[7]:


print(json.dumps(historical_quiz[:2], indent=4))  # Show first 2 elements


# In[8]:


historical_df = pd.DataFrame(historical_quiz)


# In[10]:


print("Historical DataFrame Columns:", historical_df.columns)


# In[11]:


print(historical_df.head())


# In[2]:


import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

# API Endpoints
HISTORICAL_QUIZ_URL = "https://api.jsonserve.com/XgAgFJ"

# Fetch Data Function
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {url}")
        return None

# Fetch Quiz Data
historical_quiz = fetch_data(HISTORICAL_QUIZ_URL)

# Convert to DataFrame
if isinstance(historical_quiz, list):
    historical_df = pd.DataFrame(historical_quiz)
else:
    print("Unexpected format:", type(historical_quiz))
    exit()

# **Extract Topics from "quiz" column**
historical_df["topic"] = historical_df["quiz"].apply(lambda x: x.get("title") if isinstance(x, dict) else "Unknown")

# **Convert "accuracy" to numeric**
historical_df["accuracy"] = historical_df["accuracy"].str.replace("%", "").astype(float) / 100  # Convert to fraction

# **Convert "submitted_at" to datetime for trend analysis**
historical_df["submitted_at"] = pd.to_datetime(historical_df["submitted_at"])

# **Analyze Performance**
def analyze_performance(df):
    topic_accuracy = df.groupby("topic")["accuracy"].mean()
    return topic_accuracy

topic_accuracy = analyze_performance(historical_df)

# **Plot 1: Bar Chart - Topic-Wise Accuracy**
plt.figure(figsize=(10, 5))
sns.barplot(x=topic_accuracy.index, y=topic_accuracy.values, palette="viridis")
plt.title("Topic-Wise Accuracy")
plt.ylabel("Accuracy")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# **Plot 2: Pie Chart - Topic Distribution**
plt.figure(figsize=(8, 8))
historical_df["topic"].value_counts().plot.pie(autopct="%1.1f%%", cmap="Pastel1", startangle=90, shadow=True)
plt.title("Quiz Topic Distribution")
plt.ylabel("")  # Hide y-label for cleaner view
plt.show()

# **Plot 3: Line Chart - Accuracy Trends Over Time**
plt.figure(figsize=(10, 5))
sns.lineplot(x=historical_df["submitted_at"], y=historical_df["accuracy"], hue=historical_df["topic"], marker="o", palette="tab10")
plt.title("Accuracy Trends Over Time")
plt.ylabel("Accuracy")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.grid(axis="both", linestyle="--", alpha=0.7)
plt.show()

# **Plot 4: Box Plot - Spread of Accuracy Across Topics**
plt.figure(figsize=(10, 5))
sns.boxplot(x="topic", y="accuracy", data=historical_df, palette="Set2")
plt.title("Spread of Accuracy Across Topics")
plt.ylabel("Accuracy")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()




# In[3]:


import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

# API Endpoints
HISTORICAL_QUIZ_URL = "https://api.jsonserve.com/XgAgFJ"

# Fetch Data Function
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {url}")
        return None

# Fetch Quiz Data
historical_quiz = fetch_data(HISTORICAL_QUIZ_URL)

# Convert to DataFrame
if isinstance(historical_quiz, list):
    historical_df = pd.DataFrame(historical_quiz)
else:
    print("Unexpected format:", type(historical_quiz))
    exit()

# **Extract Topics from "quiz" column**
historical_df["topic"] = historical_df["quiz"].apply(lambda x: x.get("title") if isinstance(x, dict) else "Unknown")

# **Convert "accuracy" to numeric**
historical_df["accuracy"] = historical_df["accuracy"].str.replace("%", "").astype(float) / 100  # Convert to fraction

# **Convert "submitted_at" to datetime for trend analysis**
historical_df["submitted_at"] = pd.to_datetime(historical_df["submitted_at"])

# **Identify Weak Areas (Topics with Accuracy < 50%)**
weak_topics = historical_df.groupby("topic")["accuracy"].mean()
weak_topics = weak_topics[weak_topics < 0.5]
print("\n🔴 Weak Areas (Accuracy < 50%):")
print(weak_topics)

# **Analyze Improvement Trends Over Time**
historical_df["date"] = historical_df["submitted_at"].dt.date  # Extract only date
trend_df = historical_df.groupby(["date", "topic"])["accuracy"].mean().reset_index()

plt.figure(figsize=(10, 5))
sns.lineplot(x="date", y="accuracy", hue="topic", data=trend_df, marker="o", palette="tab10")
plt.title("📈 Accuracy Trends Over Time")
plt.ylabel("Accuracy")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.grid(axis="both", linestyle="--", alpha=0.7)
plt.show()

# **Detect Performance Gaps (High Variation in Accuracy)**
topic_variance = historical_df.groupby("topic")["accuracy"].std()
high_variance_topics = topic_variance[topic_variance > 0.15]  # Threshold: 0.15 standard deviation
print("\n⚠️ Performance Gaps (High Variation in Accuracy):")
print(high_variance_topics)

# **Plot Box Plot for Performance Gaps**
plt.figure(figsize=(10, 5))
sns.boxplot(x="topic", y="accuracy", data=historical_df, palette="Set2")
plt.title("📉 Accuracy Spread Across Topics (Performance Gaps)")
plt.ylabel("Accuracy")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# In[4]:


import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

# API Endpoints
HISTORICAL_QUIZ_URL = "https://api.jsonserve.com/XgAgFJ"

# Fetch Data Function
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {url}")
        return None

# Fetch Quiz Data
historical_quiz = fetch_data(HISTORICAL_QUIZ_URL)

# Convert to DataFrame
if isinstance(historical_quiz, list):
    historical_df = pd.DataFrame(historical_quiz)
else:
    print("Unexpected format:", type(historical_quiz))
    exit()

# **Extract Topics from "quiz" column**
historical_df["topic"] = historical_df["quiz"].apply(lambda x: x.get("title") if isinstance(x, dict) else "Unknown")

# **Convert "accuracy" to numeric**
historical_df["accuracy"] = historical_df["accuracy"].str.replace("%", "").astype(float) / 100  # Convert to fraction

# **Convert "submitted_at" to datetime for trend analysis**
historical_df["submitted_at"] = pd.to_datetime(historical_df["submitted_at"])

# **Identify Weak Areas (Topics with Accuracy < 50%)**
weak_topics = historical_df.groupby("topic")["accuracy"].mean()
weak_topics = weak_topics[weak_topics < 0.5]

# **Identify Performance by Difficulty Levels**
difficulty_levels = ["easy", "medium", "hard"]
historical_df["difficulty"] = historical_df["quiz"].apply(lambda x: x.get("difficulty", "unknown") if isinstance(x, dict) else "unknown")

difficulty_performance = historical_df.groupby("difficulty")["accuracy"].mean()

# **Generate Recommendations**
recommendations = {}

if not weak_topics.empty:
    recommendations["Weak Topics"] = list(weak_topics.index)
    recommendations["Actionable Steps"] = [
        "Revise theory for these topics.",
        "Practice more questions from these topics.",
        "Attempt quizzes with different question types."
    ]

if difficulty_performance.get("easy", 1) < 0.6:
    recommendations["Difficulty Level Advice"] = "Focus on understanding basic concepts first."

if difficulty_performance.get("hard", 0) < 0.5:
    recommendations["Advanced Practice"] = "Attempt more difficult-level questions to improve problem-solving skills."

# **Print Recommendations**
print("\n📌 Personalized Recommendations:")
for key, value in recommendations.items():
    print(f"\n🔹 {key}:")
    if isinstance(value, list):
        for v in value:
            print(f"  - {v}")
    else:
        print(f"  {value}")

# **Plot Weak Areas**
if not weak_topics.empty:
    plt.figure(figsize=(10, 5))
    sns.barplot(x=weak_topics.index, y=weak_topics.values, palette="Reds_r")
    plt.title("🔴 Weak Topics (Accuracy < 50%)")
    plt.ylabel("Accuracy")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


# In[ ]:




