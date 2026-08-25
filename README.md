# exam-project
# 🏋️‍♂️ Personal Fitness Tracker Dashboard

A Python-based **Personal Fitness Tracker Dashboard** designed to log, analyze, and visualize daily fitness activities. The project incorporates Object-Oriented Programming (OOP) concepts, input validation, and data manipulation libraries like **NumPy** and **Pandas**, along with graphical visualization using **Matplotlib** and **Seaborn**.

---

## 📌 Features

* **User Input & Data Validation**: Interactive CLI interface to log activities with error handling (ensures positive non-zero numerical values for duration and calories).
* **Object-Oriented Architecture (`FitnessTracker`)**: Encapsulated modular design with methods for logging, filtering, analyzing metrics, and generating visual reports.
* **Data Handling & Computation**:
  * Automated CSV data loading and persistence (`fitness_activities.csv`).
  * Feature engineering (e.g., computed metric `Calories_per_Minute`).
  * Numerical analysis using NumPy arrays (totals, averages, frequency metrics).
  * Data filtering by activity type or custom date ranges.
* **Data Visualization**:
  * **Bar Chart**: Total time spent on each activity type.
  * **Line Graph**: Trend of calories burned over time.
  * **Pie Chart**: Percentage distribution of activities.
  * **Heatmap**: Correlation matrix between exercise duration and calories burned.

---

## 🛠️ Requirements & Tech Stack

Ensure you have Python **3.8+** installed along with the following packages:

* **Python**
* **Pandas**
* **NumPy**
* **Matplotlib**
* **Seaborn**

---

## 🚀 Installation & Setup

1. **Clone or Download the Repository**:
   ```bash
   git clone <your-repository-url>
   cd fitness-tracker
