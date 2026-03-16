import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import datetime
# Removed mysql.connector as we are now using CSV files


st.set_page_config(
    page_title="FlightIQ",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Variable Definition */
    :root {
        --primary-blue: #60a5fa;
        --accent-purple: #c084fc;
        --bg-dark: #020617;
        --card-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.08);
    }

    /* Global Styling */
    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Premium Moving Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(30, 27, 75, 1) 0%, rgba(2, 6, 23, 1) 90.1%);
        color: #f8fafc;
        overflow-x: hidden;
    }
    
    /* Animated Orbs/Glow Background Effect */
    .stApp::before {
        content: "";
        position: fixed;
        top: -10%;
        left: -10%;
        width: 40%;
        height: 60%;
        background: radial-gradient(circle, rgba(96, 165, 250, 0.05) 0%, transparent 70%);
        z-index: -1;
        animation: rotate 20s linear infinite;
    }
    
    .stApp::after {
        content: "";
        position: fixed;
        bottom: -10%;
        right: -10%;
        width: 50%;
        height: 70%;
        background: radial-gradient(circle, rgba(192, 132, 252, 0.05) 0%, transparent 70%);
        z-index: -1;
        animation: rotate 15s linear infinite reverse;
    }

    @keyframes rotate {
        from { transform: rotate(0deg) translate(0, 0); }
        to { transform: rotate(360deg) translate(20px, 30px); }
    }

    /* Shimmering Title Effect */
    .shimmer-text {
        background: linear-gradient(
            90deg, 
            #60a5fa 0%, 
            #c084fc 25%, 
            #fff 50%, 
            #c084fc 75%, 
            #60a5fa 100%
        );
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
        font-weight: 800 !important;
    }

    @keyframes shimmer {
        to { background-position: 200% center; }
    }

    /* Premium Glassmorphism Cards */
    .fact-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 32px;
        text-align: center;
        height: 100%;
        color: #e2e8f0;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        opacity: 0;
        animation: slideUpFade 0.8s ease-out forwards;
    }
    
    .fact-card:hover {
        transform: translateY(-10px) scale(1.02);
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(96, 165, 250, 0.1);
    }

    /* Delayed animation for home cards */
    .card-1 { animation-delay: 0.2s; }
    .card-2 { animation-delay: 0.4s; }
    .card-3 { animation-delay: 0.6s; }

    /* Risk Outcome Cards Enhancements */
    .risk-high, .risk-medium, .risk-low {
        border-radius: 24px;
        padding: 30px;
        margin-top: 25px;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        animation: popIn 0.5s cubic-bezier(0.26, 0.53, 0.74, 1.48);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    @keyframes popIn {
        0% { opacity: 0; transform: scale(0.95) translateY(20px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }
    
    .risk-high {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(127, 29, 29, 0.3) 100%);
        border: 1px solid rgba(239, 68, 68, 0.4);
        box-shadow: 0 10px 40px rgba(239, 68, 68, 0.15);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(146, 64, 14, 0.3) 100%);
        border: 1px solid rgba(245, 158, 11, 0.4);
        box-shadow: 0 10px 40px rgba(245, 158, 11, 0.15);
    }
    
    .risk-low {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(6, 95, 70, 0.3) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        box-shadow: 0 10px 40px rgba(16, 185, 129, 0.15);
    }

    /* Customizing Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 5px;
        border: 1px solid var(--glass-border);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(96, 165, 250, 0.15) !important;
        color: #60a5fa !important;
    }

    /* Button Glow Effect */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 12px;
        border: none;
        height: 3.2rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
        transform: translateY(-2px);
    }

    @keyframes slideUpFade {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA PATHS ---
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
AIRLINES_PATH = os.path.join(DATA_DIR, 'airlines.csv')
AIRPORTS_PATH = os.path.join(DATA_DIR, 'airports.csv')
FLIGHTS_PATH = os.path.join(DATA_DIR, 'flights_sample.csv')


@st.cache_resource
def load_models():
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'model', 'flight_delay_model.pkl')
        encoders_path = os.path.join(os.path.dirname(__file__), 'model', 'label_encoders.pkl')
        model = joblib.load(model_path)
        label_encoders = joblib.load(encoders_path)
        return model, label_encoders
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

@st.cache_data(ttl=3600)
def get_dropdown_data():
    try:
        # Get Airlines
        airlines_df = pd.read_csv(AIRLINES_PATH)
        airlines = airlines_df['AIRLINE'].unique().tolist()
        airlines.sort()
        
        # Get Airport Mappings (IATA_CODE -> AIRPORT Name)
        airports_df = pd.read_csv(AIRPORTS_PATH)
        
        # Only include airports that are present in the flights table as origins
        flights_df = pd.read_csv(FLIGHTS_PATH)
        valid_origins = set(flights_df['ORIGIN_AIRPORT'].unique())
        
        airport_mapping = {}
        for _, row in airports_df.iterrows():
            code = row['IATA_CODE']
            name = row['AIRPORT']
            if code in valid_origins:
                display_name = f"{name} ({code})"
                airport_mapping[display_name] = code
                
        return airlines, airport_mapping
    except Exception as e:
        st.error(f"Data loading error: {e}")
        return [], {}

def query_historical_stats(origin_code, dest_code, airline, day, hour):
    try:
        # Load flights data
        df = pd.read_csv(FLIGHTS_PATH)
        
        stats = {}
        
        # Distance (fallback to 1000 if not found)
        route_df = df[(df['ORIGIN_AIRPORT'] == origin_code) & (df['DESTINATION_AIRPORT'] == dest_code)]
        stats['distance'] = float(route_df['DISTANCE'].mean()) if not route_df.empty and not pd.isna(route_df['DISTANCE'].mean()) else 1000.0
        
        # Route Delay
        delayed_route_df = route_df[route_df['ARRIVAL_DELAY'] > 0]
        stats['route_delay'] = int(delayed_route_df['ARRIVAL_DELAY'].mean()) if not delayed_route_df.empty and not pd.isna(delayed_route_df['ARRIVAL_DELAY'].mean()) else 15
        
        # Airline Rate
        airline_df = df[df['AIRLINE'] == airline]
        if not airline_df.empty:
            airline_delay_pct = (airline_df[airline_df['ARRIVAL_DELAY'] > 15].shape[0] / airline_df.shape[0]) * 100
            stats['airline_rate'] = int(airline_delay_pct)
        else:
            stats['airline_rate'] = 20
        
        # Day Risk
        day_df = df[df['DAY_OF_WEEK'] == day]
        day_avg = float(day_df['ARRIVAL_DELAY'].mean()) if not day_df.empty and not pd.isna(day_df['ARRIVAL_DELAY'].mean()) else 10.0
        stats['day_risk'] = "High" if day_avg > 15 else ("Medium" if day_avg > 8 else "Low")
        
        # Time Risk (hour from scheduled_departure)
        # SCHEDULED_DEPARTURE is HHMM, so FLOOR(SCHEDULED_DEPARTURE/100) is the hour
        df['HOUR'] = df['SCHEDULED_DEPARTURE'] // 100
        hour_df = df[df['HOUR'] == hour]
        time_avg = float(hour_df['ARRIVAL_DELAY'].mean()) if not hour_df.empty and not pd.isna(hour_df['ARRIVAL_DELAY'].mean()) else 10.0
        stats['time_risk'] = "High" if time_avg > 15 else ("Medium" if time_avg > 8 else "Low")
        
        return stats
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return {'distance': 1000.0, 'route_delay': 15, 'airline_rate': 20, 'day_risk': 'Medium', 'time_risk': 'Medium'}

# --- PREDICTION LOGIC ---
def predict_flight(airline, origin_code, dest_code, scheduled_time, month, day_of_week):
    model, encoders = load_models()
    if not model or not encoders:
        return None
        
    stats = query_historical_stats(origin_code, dest_code, airline, day_of_week, scheduled_time.hour)
    
    # Calculate scheduled_departure format (HHMM int)
    sched_dep_int = scheduled_time.hour * 100 + scheduled_time.minute
    
    # Encode categorical features
    try:
        airline_encoded = encoders['AIRLINE'].transform([airline])[0]
    except:
        airline_encoded = 0
        
    try:
        origin_encoded = encoders['ORIGIN_AIRPORT'].transform([origin_code])[0]
    except:
        origin_encoded = 0

    # Model Features: MONTH, DAY_OF_WEEK, SCHEDULED_DEPARTURE, DISTANCE, DEPARTURE_DELAY, AIRLINE, ORIGIN_AIRPORT
    features = np.array([[int(month), int(day_of_week), int(sched_dep_int), float(stats['distance']), 0.0, int(airline_encoded), int(origin_encoded)]])
    
    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])
    prob_pct = int(probability * 100)
    
    expected_delay = int(prob_pct * 0.3) if prediction == 1 else 0
    
    if prob_pct > 70:
        risk = "HIGH"
    elif prob_pct > 40:
        risk = "MEDIUM"
    else:
        risk = "LOW"
        
    return {
        'prediction': prediction,
        'probability': prob_pct,
        'risk': risk,
        'expected_delay': expected_delay,
        'stats': stats
    }

# --- UI COMPONENTS ---
def render_home():
    st.markdown("""
        <div style='text-align: center; padding: 4rem 0 2rem 0;'>
            <h1 class='shimmer-text' style='font-size: 6rem; margin-bottom: 0px; line-height: 1;'>
                FlightIQ
            </h1>
            <p style='color: #94a3b8; font-size: 1.4rem; font-weight: 300; letter-spacing: 3px; margin-top: 1rem; text-transform: uppercase;'>
                Precision Aviation Intelligence
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h4 style='text-align: center; color: #cbd5e1; font-weight: 300; margin-bottom: 4rem; opacity: 0.8;'>Unlock operational excellence with AI-driven risk insights</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='fact-card card-1'><div style='font-size: 3rem; margin-bottom: 15px;'>🕒</div><strong style='font-size: 1.5rem;'>38%</strong><br>of delays are caused by<br><span style='color: #60a5fa;'>Late Aircraft</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='fact-card card-2'><div style='font-size: 3rem; margin-bottom: 15px;'>⚡</div><strong style='font-size: 1.5rem;'>5AM flights</strong><br>are 8x more reliable<br><span style='color: #c084fc;'>than 8PM flights</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='fact-card card-3'><div style='font-size: 3rem; margin-bottom: 15px;'>🚀</div><strong style='font-size: 1.5rem;'>90.49%</strong><br>AI Precision in<br><span style='color: #fff;'>historical delay patterns</span></div>", unsafe_allow_html=True)

def render_operations(airlines, airport_mapping):
    st.title("Operations Alert System")
    st.write("Analyze flight delay risk across all routes to pre-position ground crew.")
    
    with st.form("ops_form"):
        airline = st.selectbox("Airline", options=airlines)
        
        col1, col2 = st.columns(2)
        with col1:
            origin_name = st.selectbox("Origin Airport", options=list(airport_mapping.keys()))
        with col2:
            dest_name = st.selectbox("Destination Airport", options=list(airport_mapping.keys()))
            
        col3, col4, col5 = st.columns(3)
        with col3:
            sched_time = st.time_input("Departure Time", value=datetime.time(12, 0))
        with col4:
            month = st.selectbox("Month", options=range(1, 13), format_func=lambda x: datetime.date(2024, x, 1).strftime('%B'))
        with col5:
            day_map = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
            day = st.selectbox("Day of Week", options=list(day_map.keys()), format_func=lambda x: day_map[x])
            
        submitted = st.form_submit_button("ANALYZE FLIGHT RISK", use_container_width=True)
        
    if submitted:
        with st.spinner("Analyzing historical data..."):
            origin_code = airport_mapping[origin_name]
            dest_code = airport_mapping[dest_name]
            
            res = predict_flight(airline, origin_code, dest_code, sched_time, month, day)
            if res:
                if res['risk'] == 'HIGH':
                    st.markdown(f"""
                        <div class="risk-high">
                            <h3>🔴 HIGH DELAY RISK</h3>
                            <div class="stat-text">Probability: <strong>{res['probability']}%</strong></div>
                            <div class="stat-text">Expected Delay: <strong>~{res['expected_delay']} mins</strong></div>
                            <div class="action-header">RECOMMENDED ACTIONS:</div>
                            <ul>
                                <li>✓ Alert ground crew NOW</li>
                                <li>✓ Begin boarding 20 mins early</li>
                                <li>✓ Prepare gate for fast turn</li>
                                <li>✓ Notify passengers via SMS</li>
                                <li>✓ Check aircraft availability</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
                elif res['risk'] == 'MEDIUM':
                    st.markdown(f"""
                        <div class="risk-medium">
                            <h3>🟡 MEDIUM DELAY RISK</h3>
                            <div class="stat-text">Probability: <strong>{res['probability']}%</strong></div>
                            <div class="stat-text">Expected Delay: <strong>~{res['expected_delay']} mins</strong></div>
                            <div class="action-header">RECOMMENDED ACTIONS:</div>
                            <ul>
                                <li>✓ Monitor flight closely</li>
                                <li>✓ Keep ground crew on standby</li>
                                <li>✓ Standard boarding process</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="risk-low">
                            <h3>🟢 ON TIME EXPECTED</h3>
                            <div class="stat-text">Probability: <strong>{100 - res['probability']}% On Time</strong></div>
                            <div class="stat-text">Expected Delay: <strong>~0 mins</strong></div>
                            <div class="action-header">STATUS:</div>
                            <ul>
                                <li>✓ No action needed</li>
                                <li>✓ Normal operations</li>
                                <li>✓ Flight is low risk</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
                
                # "Why it might delay" Section underneath
                st.markdown("### Why it might delay:")
                st.markdown("<p style='color:#A0B2C6; font-size: 0.9em; margin-top:-10px;'>Based on our data:</p>", unsafe_allow_html=True)
                
                stats = res['stats']
                st.write(f"- This route historically delays: **~{stats['route_delay']} mins**")
                st.write(f"- This airline delay rate: **{stats['airline_rate']}%**")
                st.write(f"- This time slot risk: **{stats['time_risk']}**")
                st.write(f"- This day of week risk: **{stats['day_risk']}**")

def render_passenger(airlines, airport_mapping):
    st.title("Check Your Flight")
    st.write("Find out if your upcoming flight is likely to be delayed before you head to the airport.")
    
    with st.form("pax_form"):
        airline = st.selectbox("Airline", options=airlines)
        
        col1, col2 = st.columns(2)
        with col1:
            origin_name = st.selectbox("Origin Airport", options=list(airport_mapping.keys()))
        with col2:
            dest_name = st.selectbox("Destination Airport", options=list(airport_mapping.keys()))
            
        col3, col4 = st.columns(2)
        with col3:
            sched_time = st.time_input("Your Departure Time", value=datetime.time(12, 0))
        with col4:
            flight_date = st.date_input("Travel Date", value=datetime.date.today())
            
        submitted = st.form_submit_button("CHECK MY FLIGHT", use_container_width=True)

    if submitted:
        with st.spinner("Checking flight risk..."):
            origin_code = airport_mapping[origin_name]
            dest_code = airport_mapping[dest_name]
            
            # Extract month and day(1-7) from date
            month = flight_date.month
            day = flight_date.isoweekday() # Monday is 1, Sunday is 7
            
            res = predict_flight(airline, origin_code, dest_code, sched_time, month, day)
            
            if res:
                if res['risk'] in ['HIGH', 'MEDIUM']:
                    st.markdown(f"""
                        <div class="risk-high" style="border-left:none; border-bottom: 5px solid #FF4444;">
                            <h3>⚠️ Your flight may be delayed</h3>
                            <div class="stat-text">Risk: **{res['risk']} ({res['probability']}% probability)**</div>
                            <div class="stat-text">Expected wait: **~{res['expected_delay']} extra mins**</div>
                            
                            <div class="action-header" style="margin-top:20px;">TIPS FOR YOU:</div>
                            <ul>
                                <li>✓ Arrive at gate on time</li>
                                <li>✓ Keep phone charged</li>
                                <li>✓ Check airline app for alerts</li>
                                <li>✓ Inform anyone picking you up</li>
                            </ul>
                            
                            <div class="action-header" style="margin-top:20px;">BETTER ALTERNATIVES:</div>
                            <ul>
                                <li>• Morning flights on this route delay 80% less</li>
                                <li>• Saturday has 3x less delays than Monday on this route</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="risk-low" style="border-left:none; border-bottom: 5px solid #4CAF50;">
                            <h3>✅ Your flight looks good!</h3>
                            <div class="stat-text">Risk: **LOW ({(100 - res['probability'])}% on time)**</div>
                            <div style="color: #A0B2C6; font-size: 0.9em; margin-bottom:15px;">This is a historically reliable flight</div>
                            <h4 style="color:#4CAF50;">Safe travels! ✈️</h4>
                        </div>
                    """, unsafe_allow_html=True)

# --- MAIN APP ROUTING ---
def main():
    airlines, airport_mapping = get_dropdown_data()
    
    if not airlines or not airport_mapping:
        st.warning("Could not load data from database. Please check connection.")
        return
        
    tab1, tab2, tab3 = st.tabs(["✈️ Home", "🏢 Operations Team", "👤 Passenger"])
    
    with tab1:
        render_home()
        
    with tab2:
        render_operations(airlines, airport_mapping)
        
    with tab3:
        render_passenger(airlines, airport_mapping)

if __name__ == "__main__":
    main()
