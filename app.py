import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.pipeline.train_pipeline import TrainPipeline

# Page configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .prediction-result {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-result {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_sample_data():
    """Load sample data for visualization"""
    try:
        data_path = os.path.join('notebook', 'data', 'stud.csv')
        if os.path.exists(data_path):
            return pd.read_csv(data_path)
        else:
            # Create sample data if file doesn't exist
            np.random.seed(42)
            sample_data = {
                'gender': np.random.choice(['male', 'female'], 100),
                'race_ethnicity': np.random.choice(['group A', 'group B', 'group C', 'group D', 'group E'], 100),
                'parental_level_of_education': np.random.choice([
                    'some high school', 'high school', 'some college', 
                    'associate\'s degree', 'bachelor\'s degree', 'master\'s degree'
                ], 100),
                'lunch': np.random.choice(['standard', 'free/reduced'], 100),
                'test_preparation_course': np.random.choice(['none', 'completed'], 100),
                'math_score': np.random.randint(0, 100, 100),
                'reading_score': np.random.randint(0, 100, 100),
                'writing_score': np.random.randint(0, 100, 100)
            }
            return pd.DataFrame(sample_data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def create_visualizations(df):
    """Create interactive visualizations"""
    if df is None:
        return
    
    # Score distribution
    fig1 = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Math Scores', 'Reading Scores', 'Writing Scores'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig1.add_trace(go.Histogram(x=df['math_score'], name='Math', opacity=0.7, marker_color='#1f77b4'), row=1, col=1)
    fig1.add_trace(go.Histogram(x=df['reading_score'], name='Reading', opacity=0.7, marker_color='#ff7f0e'), row=1, col=2)
    fig1.add_trace(go.Histogram(x=df['writing_score'], name='Writing', opacity=0.7, marker_color='#2ca02c'), row=1, col=3)
    
    fig1.update_layout(
        title_text="Score Distributions",
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Performance by demographics
    col1, col2 = st.columns(2)
    
    with col1:
        fig2 = px.box(df, x='gender', y='math_score', color='gender',
                     title='Math Scores by Gender')
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        fig3 = px.box(df, x='lunch', y='math_score', color='lunch',
                     title='Math Scores by Lunch Type')
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    # Correlation heatmap
    numeric_cols = ['math_score', 'reading_score', 'writing_score']
    corr_matrix = df[numeric_cols].corr()
    
    fig4 = px.imshow(corr_matrix, 
                     text_auto=True, 
                     aspect="auto",
                     title="Score Correlations",
                     color_continuous_scale='RdBu')
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎓 Student Performance Predictor</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["🏠 Home", "📊 Data Analysis", "🔮 Prediction", "🚀 Model Training"])
    
    if page == "🏠 Home":
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        ## Welcome to the Student Performance Predictor!
        
        This application uses machine learning to predict student math scores based on various demographic and academic factors.
        
        ### Features:
        - **📊 Data Analysis**: Explore the dataset with interactive visualizations
        - **🔮 Prediction**: Get instant predictions for student performance
        - **🚀 Model Training**: Train new models with the latest data
        
        ### How it works:
        1. The model analyzes factors like gender, ethnicity, parental education, lunch type, and test preparation
        2. It uses advanced machine learning algorithms to predict math scores
        3. The predictions help identify students who might need additional support
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Load and display sample statistics
        df = load_sample_data()
        if df is not None:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Students", len(df))
            with col2:
                st.metric("Average Math Score", f"{df['math_score'].mean():.1f}")
            with col3:
                st.metric("Average Reading Score", f"{df['reading_score'].mean():.1f}")
            with col4:
                st.metric("Average Writing Score", f"{df['writing_score'].mean():.1f}")
    
    elif page == "📊 Data Analysis":
        st.markdown('<h2 class="sub-header">📊 Data Analysis & Visualization</h2>', unsafe_allow_html=True)
        
        df = load_sample_data()
        if df is not None:
            # Dataset overview
            st.subheader("Dataset Overview")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Dataset Shape:**", df.shape)
                st.write("**Features:**", list(df.columns))
            
            with col2:
                st.write("**Data Types:**")
                st.write(df.dtypes)
            
            # Show sample data
            st.subheader("Sample Data")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Visualizations
            st.subheader("Interactive Visualizations")
            create_visualizations(df)
            
            # Statistical summary
            st.subheader("Statistical Summary")
            st.dataframe(df.describe(), use_container_width=True)
    
    elif page == "🔮 Prediction":
        st.markdown('<h2 class="sub-header">🔮 Student Performance Prediction</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        Enter student information below to predict their math score. The model considers various factors 
        that influence academic performance.
        """)
        
        # Create input form
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                gender = st.selectbox("Gender", ["male", "female"])
                race_ethnicity = st.selectbox("Race/Ethnicity", [
                    "group A", "group B", "group C", "group D", "group E"
                ])
                parental_education = st.selectbox("Parental Level of Education", [
                    "some high school",
                    "high school", 
                    "some college",
                    "associate's degree",
                    "bachelor's degree",
                    "master's degree"
                ])
            
            with col2:
                lunch = st.selectbox("Lunch Type", ["standard", "free/reduced"])
                test_prep = st.selectbox("Test Preparation Course", ["none", "completed"])
                reading_score = st.slider("Reading Score", 0, 100, 70)
                writing_score = st.slider("Writing Score", 0, 100, 70)
            
            submitted = st.form_submit_button("🔮 Predict Math Score", use_container_width=True)
            
            if submitted:
                try:
                    # Create custom data object
                    custom_data = CustomData(
                        gender=gender,
                        race_ethnicity=race_ethnicity,
                        parental_level_of_education=parental_education,
                        lunch=lunch,
                        test_preparation_course=test_prep,
                        reading_score=reading_score,
                        writing_score=writing_score
                    )
                    
                    # Get prediction
                    pred_df = custom_data.get_data_as_data_frame()
                    predict_pipeline = PredictPipeline()
                    
                    # Check if model exists
                    if os.path.exists("artifacts/model.pkl") and os.path.exists("artifacts/preprocessor.pkl"):
                        results = predict_pipeline.predict(pred_df)
                        predicted_score = round(results[0], 2)
                        
                        # Display result
                        st.markdown(f"""
                        <div class="prediction-result success-result">
                            🎯 Predicted Math Score: {predicted_score}/100
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Performance interpretation
                        if predicted_score >= 80:
                            st.success("🌟 Excellent performance expected!")
                        elif predicted_score >= 70:
                            st.info("👍 Good performance expected!")
                        elif predicted_score >= 60:
                            st.warning("⚠️ Average performance - consider additional support")
                        else:
                            st.error("🚨 Below average performance - immediate intervention recommended")
                        
                        # Show input summary
                        st.subheader("Input Summary")
                        input_data = {
                            "Feature": ["Gender", "Race/Ethnicity", "Parental Education", "Lunch", "Test Prep", "Reading Score", "Writing Score"],
                            "Value": [gender, race_ethnicity, parental_education, lunch, test_prep, reading_score, writing_score]
                        }
                        st.dataframe(pd.DataFrame(input_data), use_container_width=True, hide_index=True)
                        
                    else:
                        st.error("❌ Model not found! Please train the model first using the Model Training page.")
                        
                except Exception as e:
                    st.error(f"❌ Prediction failed: {str(e)}")
    
    elif page == "🚀 Model Training":
        st.markdown('<h2 class="sub-header">🚀 Model Training</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        Train a new machine learning model with the latest data. This process will:
        1. Load and preprocess the training data
        2. Train multiple ML algorithms
        3. Select the best performing model
        4. Save the model for predictions
        """)
        
        if st.button("🚀 Start Training", use_container_width=True):
            try:
                with st.spinner("Training in progress... This may take a few minutes."):
                    # Create progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Initialize training pipeline
                    status_text.text("Initializing training pipeline...")
                    progress_bar.progress(10)
                    
                    train_pipeline = TrainPipeline()
                    
                    status_text.text("Loading and preprocessing data...")
                    progress_bar.progress(30)
                    
                    status_text.text("Training multiple models...")
                    progress_bar.progress(60)
                    
                    # Start training
                    r2_score = train_pipeline.start_training()
                    
                    status_text.text("Saving best model...")
                    progress_bar.progress(90)
                    
                    progress_bar.progress(100)
                    status_text.text("Training completed!")
                    
                    # Display results
                    st.success(f"✅ Training completed successfully!")
                    st.metric("Model R² Score", f"{r2_score:.4f}")
                    
                    # Performance interpretation
                    if r2_score >= 0.8:
                        st.success("🌟 Excellent model performance!")
                    elif r2_score >= 0.7:
                        st.info("👍 Good model performance!")
                    elif r2_score >= 0.6:
                        st.warning("⚠️ Average model performance")
                    else:
                        st.error("🚨 Poor model performance - consider data quality or feature engineering")
                    
                    st.info("💡 You can now use the trained model for predictions!")
                    
            except Exception as e:
                st.error(f"❌ Training failed: {str(e)}")
                st.info("💡 Make sure the data file exists at 'notebook/data/stud.csv'")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🎓 Student Performance Predictor | Built with Streamlit & Machine Learning</p>
        <p>📊 Helping educators make data-driven decisions</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()