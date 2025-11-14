import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class DiseasePredictionApp:
    def __init__(self):
        self.data = None
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
    def load_sample_data(self):
        """Load sample disease prediction dataset"""
        # Create sample data for demonstration
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'age': np.random.randint(1, 90, n_samples),
            'blood_pressure': np.random.randint(80, 200, n_samples),
            'cholesterol': np.random.randint(100, 300, n_samples),
            'blood_sugar': np.random.randint(70, 200, n_samples),
            'bmi': np.random.uniform(18, 40, n_samples),
            'heart_rate': np.random.randint(60, 120, n_samples),
            'smoking': np.random.choice([0, 1], n_samples),
            'alcohol': np.random.choice([0, 1], n_samples),
            'exercise': np.random.choice([0, 1], n_samples),
            'family_history': np.random.choice([0, 1], n_samples)
        }
        
        # Create target variable based on features
        risk_score = (
            data['age'] * 0.1 +
            data['blood_pressure'] * 0.08 +
            data['cholesterol'] * 0.07 +
            data['blood_sugar'] * 0.09 +
            data['bmi'] * 0.12 +
            (1 - data['exercise']) * 20 +
            data['smoking'] * 15 +
            data['alcohol'] * 10 +
            data['family_history'] * 12
        )
        
        # Create disease categories
        conditions = [
            'No Disease' if score < 50 else
            'Low Risk' if score < 80 else
            'Medium Risk' if score < 120 else
            'High Risk'
            for score in risk_score
        ]
        
        data['disease_risk'] = conditions
        self.data = pd.DataFrame(data)
        return self.data
    
    def preprocess_data(self):
        """Preprocess the data for training"""
        if self.data is None:
            self.load_sample_data()
        
        # Encode target variable
        X = self.data.drop('disease_risk', axis=1)
        y = self.label_encoder.fit_transform(self.data['disease_risk'])
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, X.columns
    
    def train_model(self, model_type='random_forest'):
        """Train the selected model"""
        X_train, X_test, y_train, y_test, feature_names = self.preprocess_data()
        
        if model_type == 'random_forest':
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == 'svm':
            model = SVC(kernel='rbf', probability=True, random_state=42)
        elif model_type == 'logistic_regression':
            model = LogisticRegression(random_state=42, max_iter=1000)
        else:
            model = RandomForestClassifier(random_state=42)
        
        # Train model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        
        self.model = model
        return model, accuracy, y_test, y_pred, y_pred_proba, feature_names
    
    def run(self):
        """Main method to run the Streamlit app"""
        st.set_page_config(
            page_title="Disease Prediction App",
            page_icon="🏥",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            color: #2E86AB;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            border-left: 5px solid #2E86AB;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Header
        st.markdown('<h1 class="main-header">🏥 Disease Risk Prediction System</h1>', 
                   unsafe_allow_html=True)
        
        # Sidebar
        st.sidebar.title("Navigation")
        app_mode = st.sidebar.selectbox(
            "Choose App Mode",
            ["Data Overview", "Model Training", "Risk Prediction", "Feature Analysis"]
        )
        
        # Load data
        if self.data is None:
            self.load_sample_data()
        
        if app_mode == "Data Overview":
            self.show_data_overview()
        elif app_mode == "Model Training":
            self.show_model_training()
        elif app_mode == "Risk Prediction":
            self.show_risk_prediction()
        elif app_mode == "Feature Analysis":
            self.show_feature_analysis()
    
    def show_data_overview(self):
        """Display data overview section"""
        st.header("📊 Data Overview")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Dataset Sample")
            st.dataframe(self.data.head(10), use_container_width=True)
        
        with col2:
            st.subheader("Dataset Info")
            st.write(f"**Total Samples:** {len(self.data)}")
            st.write(f"**Features:** {len(self.data.columns) - 1}")
            st.write(f"**Disease Risk Distribution:**")
            risk_counts = self.data['disease_risk'].value_counts()
            st.dataframe(risk_counts)
        
        # Visualizations
        st.subheader("Data Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Disease risk distribution
            fig = px.pie(
                self.data, 
                names='disease_risk',
                title='Disease Risk Distribution',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Age distribution by disease risk
            fig = px.box(
                self.data,
                x='disease_risk',
                y='age',
                title='Age Distribution by Disease Risk',
                color='disease_risk'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation heatmap
        st.subheader("Feature Correlation Heatmap")
        numeric_data = self.data.select_dtypes(include=[np.number])
        fig = px.imshow(
            numeric_data.corr(),
            title="Feature Correlation Matrix",
            aspect="auto",
            color_continuous_scale="RdBu_r"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def show_model_training(self):
        """Display model training section"""
        st.header("🤖 Model Training")
        
        # Model selection
        col1, col2, col3 = st.columns(3)
        
        with col1:
            model_type = st.selectbox(
                "Select Model",
                ["random_forest", "svm", "logistic_regression"],
                format_func=lambda x: x.replace('_', ' ').title()
            )
        
        with col2:
            train_button = st.button("🚀 Train Model", type="primary")
        
        with col3:
            if st.button("🔄 Reset Models"):
                st.session_state.pop('trained_model', None)
                st.rerun()
        
        if train_button:
            with st.spinner('Training model... This may take a few seconds.'):
                model, accuracy, y_test, y_pred, y_pred_proba, feature_names = self.train_model(model_type)
                
                # Store in session state
                st.session_state.trained_model = {
                    'model': model,
                    'accuracy': accuracy,
                    'y_test': y_test,
                    'y_pred': y_pred,
                    'y_pred_proba': y_pred_proba,
                    'feature_names': feature_names,
                    'model_type': model_type
                }
        
        # Display results if model is trained
        if 'trained_model' in st.session_state:
            model_info = st.session_state.trained_model
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Model Type", model_info['model_type'].replace('_', ' ').title())
            with col2:
                st.metric("Accuracy", f"{model_info['accuracy']:.2%}")
            with col3:
                st.metric("Test Samples", len(model_info['y_test']))
            with col4:
                st.metric("Classes", len(np.unique(model_info['y_test'])))
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Confusion Matrix
                cm = confusion_matrix(model_info['y_test'], model_info['y_pred'])
                fig = px.imshow(
                    cm,
                    title="Confusion Matrix",
                    labels=dict(x="Predicted", y="Actual", color="Count"),
                    x=self.label_encoder.classes_,
                    y=self.label_encoder.classes_,
                    color_continuous_scale="Blues"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Feature Importance (for tree-based models)
                if hasattr(model_info['model'], 'feature_importances_'):
                    importances = model_info['model'].feature_importances_
                    feature_imp_df = pd.DataFrame({
                        'feature': model_info['feature_names'],
                        'importance': importances
                    }).sort_values('importance', ascending=True)
                    
                    fig = px.bar(
                        feature_imp_df,
                        x='importance',
                        y='feature',
                        title="Feature Importance",
                        orientation='h'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Feature importance not available for this model type")
            
            # Classification Report
            st.subheader("Classification Report")
            report = classification_report(
                model_info['y_test'], 
                model_info['y_pred'],
                target_names=self.label_encoder.classes_,
                output_dict=True
            )
            report_df = pd.DataFrame(report).transpose()
            st.dataframe(report_df.style.background_gradient(cmap='Blues'), use_container_width=True)
    
    def show_risk_prediction(self):
        """Display risk prediction interface"""
        st.header("🔍 Disease Risk Prediction")
        
        if 'trained_model' not in st.session_state:
            st.warning("⚠️ Please train a model first in the 'Model Training' section.")
            return
        
        st.subheader("Enter Patient Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.slider("Age", 1, 100, 30)
            blood_pressure = st.slider("Blood Pressure", 80, 200, 120)
            cholesterol = st.slider("Cholesterol", 100, 300, 200)
        
        with col2:
            blood_sugar = st.slider("Blood Sugar", 70, 200, 100)
            bmi = st.slider("BMI", 18.0, 40.0, 24.0)
            heart_rate = st.slider("Heart Rate", 60, 120, 72)
        
        with col3:
            smoking = st.selectbox("Smoking", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            alcohol = st.selectbox("Alcohol Consumption", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            exercise = st.selectbox("Regular Exercise", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            family_history = st.selectbox("Family History", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        
        # Create input array
        input_data = np.array([[
            age, blood_pressure, cholesterol, blood_sugar,
            bmi, heart_rate, smoking, alcohol, exercise, family_history
        ]])
        
        # Scale input data
        input_scaled = self.scaler.transform(input_data)
        
        # Make prediction
        model_info = st.session_state.trained_model
        prediction = model_info['model'].predict(input_scaled)
        prediction_proba = model_info['model'].predict_proba(input_scaled)
        
        predicted_class = self.label_encoder.inverse_transform(prediction)[0]
        confidence = np.max(prediction_proba)
        
        # Display results
        st.subheader("Prediction Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk level card
            risk_colors = {
                'No Disease': '🟢',
                'Low Risk': '🟡', 
                'Medium Risk': '🟠',
                'High Risk': '🔴'
            }
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>{risk_colors.get(predicted_class, '⚪')} Predicted Risk Level</h3>
                <h2 style="color: {'green' if predicted_class == 'No Disease' else 'orange' if predicted_class == 'Low Risk' else 'red'};">
                    {predicted_class}
                </h2>
                <p>Confidence: {confidence:.2%}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Probability distribution
            prob_df = pd.DataFrame({
                'Risk Level': self.label_encoder.classes_,
                'Probability': prediction_proba[0]
            }).sort_values('Probability', ascending=True)
            
            fig = px.bar(
                prob_df,
                x='Probability',
                y='Risk Level',
                title="Risk Level Probabilities",
                orientation='h',
                color='Probability',
                color_continuous_scale='RdYlGn_r'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Risk factors analysis
        st.subheader("Risk Factors Analysis")
        
        # Calculate feature contributions (simplified)
        feature_contributions = {}
        if hasattr(model_info['model'], 'feature_importances_'):
            importances = model_info['model'].feature_importances_
            for i, feature in enumerate(model_info['feature_names']):
                feature_contributions[feature] = importances[i] * input_data[0][i]
        
        if feature_contributions:
            contrib_df = pd.DataFrame({
                'Feature': list(feature_contributions.keys()),
                'Contribution': list(feature_contributions.values())
            }).sort_values('Contribution', ascending=True)
            
            fig = px.bar(
                contrib_df,
                x='Contribution',
                y='Feature',
                title="Feature Contributions to Risk",
                orientation='h',
                color='Contribution',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def show_feature_analysis(self):
        """Display feature analysis section"""
        st.header("📈 Feature Analysis")
        
        # Feature distribution by risk level
        selected_feature = st.selectbox(
            "Select Feature to Analyze",
            self.data.columns[:-1]  # Exclude target
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Box plot
            fig = px.box(
                self.data,
                x='disease_risk',
                y=selected_feature,
                title=f'{selected_feature} Distribution by Risk Level',
                color='disease_risk'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Violin plot
            fig = px.violin(
                self.data,
                x='disease_risk',
                y=selected_feature,
                title=f'{selected_feature} Density by Risk Level',
                color='disease_risk',
                box=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Scatter plot matrix
        st.subheader("Feature Relationships")
        
        selected_features = st.multiselect(
            "Select Features for Scatter Matrix",
            self.data.columns[:-1],
            default=self.data.columns[:4].tolist()  # First 4 features
        )
        
        if len(selected_features) >= 2:
            fig = px.scatter_matrix(
                self.data,
                dimensions=selected_features,
                color='disease_risk',
                title="Feature Scatter Matrix",
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)

def main():
    app = DiseasePredictionApp()
    app.run()

if __name__ == "__main__":
    main()