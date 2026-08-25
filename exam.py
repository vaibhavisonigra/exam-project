import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class FitnessTracker:

  def __init__(self, csv_file="fitness_activities.csv"):
    self.csv_file = csv_file
    self.data = pd.DataFrame()
    self.load_data()

  def load_data(self):
    """Loads and cleans data from the CSV file."""
    if os.path.exists(self.csv_file):
      self.data = pd.read_csv(self.csv_file)
      self.data["Date"] = pd.to_datetime(self.data["Date"])
      # Computed Metric: Calories per Minute
      self.data["Calories_per_Minute"] = (
          self.data["Calories Burned"] / self.data["Duration (Minutes)"]
      )
    else:
      # Initialize empty DataFrame if file doesn't exist
      self.data = pd.DataFrame(
          columns=[
              "Date",
              "Activity Type",
              "Duration (Minutes)",
              "Calories Burned",
              "Calories_per_Minute",
          ]
      )

  def log_activity(self, activity_type, duration, calories, date=None):
    """Logs a new activity with user input validation."""
    if date is None:
      date = pd.Timestamp.now().strftime("%Y-%m-%d")

    new_row = pd.DataFrame([{
        "Date": pd.to_datetime(date),
        "Activity Type": str(activity_type).strip().capitalize(),
        "Duration (Minutes)": float(duration),
        "Calories Burned": float(calories),
        "Calories_per_Minute": float(calories) / float(duration),
    }])

    self.data = pd.concat([self.data, new_row], ignore_index=True)
    # Save back to CSV
    self.data.to_csv(self.csv_file, index=False)
    print(" Activity successfully logged and saved!")

  def calculate_metrics(self):
    """Calculates numerical metrics using NumPy and Pandas."""
    if self.data.empty:
      print(" No data available to calculate metrics.")
      return

    total_calories = np.sum(self.data["Calories Burned"].to_numpy())
    avg_duration = np.mean(self.data["Duration (Minutes)"].to_numpy())
    avg_calories = np.mean(self.data["Calories Burned"].to_numpy())
    activity_counts = self.data["Activity Type"].value_counts()

    print("\n" + "=" * 40)
    print("      FITNESS TRACKER METRICS      ")
    print("=" * 40)
    print(f"Total Calories Burned : {total_calories:.2f} kcal")
    print(f"Average Duration      : {avg_duration:.2f} mins")
    print(f"Average Calories/Session: {avg_calories:.2f} kcal")
    print("Activity Frequency:")
    print(activity_counts.to_string())
    print("=" * 40)

  def filter_activities(self, condition_type="activity", value=None):
    """Filters activities based on type or date range."""
    if self.data.empty:
      print(" Dataset is empty.")
      return self.data

    if condition_type == "activity" and value:
      filtered = self.data[
          self.data["Activity Type"].str.lower() == str(value).lower()
      ]
    elif condition_type == "date" and isinstance(value, tuple):
      start_date, end_date = value
      filtered = self.data[
          (self.data["Date"] >= pd.to_datetime(start_date))
          & (self.data["Date"] <= pd.to_datetime(end_date))
      ]
    else:
      filtered = self.data

    print(f"--- Filtered Results ({condition_type}: {value}) ---")
    print(filtered if not filtered.empty else "No matching records found.")
    return filtered

  def generate_report(self):
    """Summarizes fitness data for user review."""
    if self.data.empty:
      print(" No data to generate report.")
      return

    print("\n" + "=" * 40)
    print("         SUMMARY REPORT           ")
    print("=" * 40)
    print(f"Total Logged Sessions : {len(self.data)}")
    print(
        "Total Time Spent      :"
        f" {self.data['Duration (Minutes)'].sum()} mins"
    )
    print(
        "Most Frequent Activity:"
        f" {self.data['Activity Type'].mode()[0] if not self.data['Activity Type'].empty else 'N/A'}"
    )
    print("Detailed Logs:")
    print(self.data.to_string(index=False))

  def plot_visualizations(self):
    """Generates 4 required charts using Matplotlib & Seaborn."""
    if self.data.empty:
      print(" No data available for visualization.")
      return

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 1. Bar Chart: Time spent on each activity type
    time_per_activity = self.data.groupby("Activity Type")[
        "Duration (Minutes)"
    ].sum()
    axes[0, 0].bar(
        time_per_activity.index, time_per_activity.values, color="skyblue"
    )
    axes[0, 0].set_title("Total Time Spent per Activity")
    axes[0, 0].set_xlabel("Activity Type")
    axes[0, 0].set_ylabel("Duration (Minutes)")

    # 2. Line Graph: Calories burned over time
    sorted_df = self.data.sort_values("Date")
    axes[0, 1].plot(
        sorted_df["Date"],
        sorted_df["Calories Burned"],
        marker="o",
        color="orange",
        linewidth=2,
    )
    axes[0, 1].set_title("Calories Burned Over Time")
    axes[0, 1].set_xlabel("Date")
    axes[0, 1].set_ylabel("Calories Burned")
    axes[0, 1].tick_params(axis="x", rotation=45)

    # 3. Pie Chart: Percentage distribution of activities
    activity_counts = self.data["Activity Type"].value_counts()
    axes[1, 0].pie(
        activity_counts.values,
        labels=activity_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=sns.color_palette("pastel"),
    )
    axes[1, 0].set_title("Activity Distribution")

    # 4. Heatmap: Correlation between duration and calories burned
    numeric_df = self.data[["Duration (Minutes)", "Calories Burned"]]
    sns.heatmap(
        numeric_df.corr(), annot=True, cmap="coolwarm", ax=axes[1, 1], vmin=-1, vmax=1
    )
    axes[1, 1].set_title("Correlation: Duration vs Calories")

    plt.tight_layout()
    plt.show()


# Interactive CLI Menu
def main():
  tracker = FitnessTracker()

  while True:
    print("\n--- PERSONAL FITNESS TRACKER MENU ---")
    print("1. Log New Activity")
    print("2. View Metrics")
    print("3. Filter Activities")
    print("4. View Visual Progress (Plots)")
    print("5. Generate Summary Report")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ").strip()

    if choice == "1":
      act_type = input("Enter Activity Type (e.g., Running, Yoga): ").strip()
      while True:
        try:
          duration = float(input("Enter Duration in minutes (> 0): "))
          calories = float(input("Enter Calories burned (> 0): "))
          if duration > 0 and calories > 0:
            break
          print("⚠️ Duration and Calories must be positive numbers!")
        except ValueError:
          print("⚠️ Invalid input! Please enter valid numerical values.")

      date_in = (
          input("Enter Date (YYYY-MM-DD) or press Enter for Today: ").strip()
          or None
      )
      tracker.log_activity(act_type, duration, calories, date_in)

    elif choice == "2":
      tracker.calculate_metrics()

    elif choice == "3":
      print("Filter by: 1. Activity Type  2. Date Range")
      f_choice = input("Choice (1/2): ").strip()
      if f_choice == "1":
        val = input("Enter activity name: ").strip()
        tracker.filter_activities("activity", val)
      elif f_choice == "2":
        start = input("Enter Start Date (YYYY-MM-DD): ").strip()
        end = input("Enter End Date (YYYY-MM-DD): ").strip()
        tracker.filter_activities("date", (start, end))

    elif choice == "4":
      tracker.plot_visualizations()

    elif choice == "5":
      tracker.generate_report()

    elif choice == "6":
      print("\nExiting Fitness Tracker. Stay healthy!")
      break
    else:
      print("⚠️ Invalid option, please try again.")


if __name__ == "__main__":
  main()