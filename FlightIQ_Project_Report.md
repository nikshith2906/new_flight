# ✈️ FlightIQ: Project Architecture & Summary Report

This document outlines the complete scope of the FlightIQ project, detailing the architecture, machine learning models, data pipeline, and the premium user interface developed. Use this as a reference or for your hackathon pitch/submission!

---

## 1. Project Overview
**FlightIQ** is a next-generation predictive intelligence platform designed to forecast flight delays. It provides two distinct interfaces:
*   **Operations Hub:** Allows airline ground teams and dispatchers to evaluate network risks proactively and stage crews to mitigate cascading delays.
*   **Traveler Hub:** Empowers passengers with AI-driven predictability for their specific flights to reduce travel anxiety.

**Core Technology Stack:** Python, Streamlit, Scikit-Learn/XGBoost, MySQL (Railway Cloud), CSS/Glassmorphism, Microsoft Power BI.

---

## 2. Machine Learning & Predictive Engine
To ensure high accuracy and real-time inference, we initially trained and evaluated **two different machine learning models** before selecting our final production engine.

### 2.1 Model Training & Evaluation Setup
*   **Dataset:** Historical flight data containing millions of records sourced from public aviation databases.
*   **Preprocessing:** We handled missing values, encoded categorical variables (like `AIRLINE` and `ORIGIN_AIRPORT`) using Scikit-Learn's `LabelEncoder` (`label_encoders.pkl`), and engineered new time-based features (e.g., converting departure times to continuous integer blocks).
*   **Target Variable:** A binary classification target where `1` represents a delay > 15 minutes, and `0` represents an on-time departure.

### 2.2 The Two Models We Trained
We compared two popular ensemble methods known for their performance on structured datasets:

#### Model A: Random Forest Classifier
*   **Methodology:** A bagging ensemble technique that builds multiple decision trees independently and merges their outputs.
*   **Pros/Cons:** It proved very robust to outliers and required less hyperparameter tuning initially. However, as the dataset grew, the model became computationally heavy and slower during real-time inference.
*   **Performance:** Achieved an accuracy of ~86%.

#### Model B: XGBoost (eXtreme Gradient Boosting)
*   **Methodology:** A boosting ensemble algorithm that builds trees sequentially, with each new tree correcting the errors of the previous ones.
*   **Why we chose it for production:** XGBoost significantly outperformed Random Forest in handling class imbalances (delays are less frequent than on-time flights). It was also substantially faster during inference phase—a critical requirement for our web application.
*   **Final Accuracy Metric:** The XGBoost implementation achieved an operational prediction accuracy of **90.49%** on our validation test data.

### 2.3 Deployed Production Architecture
We deployed the **XGBoost Classifier** (`flight_delay_model.pkl`) into the live Streamlit application using `joblib`. 

**Live Feature Engineering:** During a user request, the model dynamically evaluates 7 critical features to generate a live risk score:
1.  Operating Month
2.  Day of the Week
3.  Scheduled Departure Time (converted to integer blocks)
4.  Route Distance (Miles)
5.  Assigned Airline (Label Encoded)
6.  Origin Airport Traffic (Label Encoded)
7.  Historic Route Delay Averages (Queried in real-time from the database)

**Prediction Output:** The engine returns a probability percentage (e.g., "78% likelihood of delay") and categorizes the risk into actionable bands:
*   🔴 **HIGH RISK** (>70% probability)
*   🟡 **MEDIUM RISK** (40% - 70% probability)
*   🟢 **LOW RISK** (<40% probability, on-time expected)

---

## 3. Data Pipeline & Cloud Migration
To make the application robust and ready for public cloud deployment, we overhauled the data architecture.

*   **Database Cloud Migration:** Moved the database from a local MySQL instance to a scalable **Railway Cloud MySQL** instance.
*   **Data Footprint:** 
    *   `airlines` table: 100% migrated, mapping full carrier names to IATA codes.
    *   `airports` table: 100% migrated, mapping full airport names to IATA codes.
    *   `flights` table: Migrated a strategic, randomized sample of **10,000 historical flight records**. This ensures rapid querying performance for the Streamlit UI while staying within the free-tier constraints of cloud database providers.
*   **Dynamic UI Queries:** The application runs dynamic `SELECT` queries against the Railway database to calculate "route historical delay averages" and "carrier inefficiency" on the fly based on user selection.

---

## 4. Premium User Interface (UI/UX)
The application was completely rewritten from a basic Flask app into a state-of-the-art **Streamlit Web Application** featuring "Glassmorphism" design.

*   **Ultimate Premium Enhancements:**
    *   **Dark Mode Styling:** Rich `#030914` deep navy background with radial lighting gradients.
    *   **Glassmorphism Cards with Neon Hover:** Translucent, frosted-glass panels that feature an animated **neon glow** and lift effect when hovered.
    *   **Glowing Dividers:** Replaced standard horizontal lines with custom-coded glowing gradient dividers for a sleek, modern separation of sections.
    *   **Custom Typography & UX:** Full implementation of the `Outfit` Google Font and interactive, custom-styled dark-mode scrollbars for a cohesive enterprise feel.
*   **Interactive Components:**
    *   Tabbed navigation with immersive blur effects and custom-selected states.
    *   Risk Banners with color-coded alerts (Red/Yellow/Green) and micro-animations.

---

## 5. Live Network Analytics (Power BI)
*   **Integration:** We successfully embedded a Microsoft Power BI report directly into the Streamlit application using an `iframe`. 
*   **Features:** The dashboard provides live, interactive network telemetrics, allowing users to use visual slicers to drill down into specific delay factors, airports, and geographical performance without leaving the web app.

---

## 6. Deployment Readiness
*   The application is fully configured for **Streamlit Cloud Deployment**.
*   A localized `secrets.toml` strategy is in place to securely handle the Railway Database credentials in production environments.
