# 🎓 Student Performance Predictor

A comprehensive machine learning application that predicts student math scores based on demographic and academic factors. Built with Python, featuring both Streamlit and Flask web interfaces with modern responsive design.

## 🌟 Features

- **🤖 AI-Powered Predictions**: Advanced ML algorithms analyze multiple factors for accurate performance predictions
- **📊 Interactive Dashboard**: Modern Streamlit interface with real-time visualizations
- **🎨 Responsive Web UI**: Beautiful Flask application with Bootstrap styling
- **📈 Data Analysis**: Comprehensive exploratory data analysis with interactive charts
- **🚀 Model Training**: Complete ML pipeline with automated model selection
- **📱 Mobile-Friendly**: Fully responsive design that works on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sahil9309/mlproject.git
   cd mlproject
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package**
   ```bash
   pip install -e .
   ```

### 🎯 Usage

#### Option 1: Streamlit Application (Recommended)

Launch the modern Streamlit interface:

```bash
streamlit run app.py
```

Features:
- 🏠 **Home**: Overview and statistics
- 📊 **Data Analysis**: Interactive visualizations
- 🔮 **Prediction**: Real-time score prediction
- 🚀 **Model Training**: Train new models

#### Option 2: Flask Web Application

Launch the Flask web interface:

```bash
python flask_app.py
```

Then open http://localhost:5000 in your browser.

#### Option 3: Command Line Training

Train the model directly:

```bash
python src/pipeline/train_pipeline.py
```

## 📊 Model Performance

The system evaluates multiple ML algorithms and automatically selects the best performing model based on R² score.

## 🎯 Prediction Factors

The model considers these key factors:

| Factor | Description | Impact |
|--------|-------------|---------|
| **Gender** | Student's gender | Moderate |
| **Race/Ethnicity** | Ethnic background (Groups A-E) | Low-Moderate |
| **Parental Education** | Highest education level of parents | High |
| **Lunch Type** | Free/reduced or standard lunch | High |
| **Test Preparation** | Completion of prep course | Moderate |
| **Reading Score** | Student's reading performance | Very High |
| **Writing Score** | Student's writing performance | Very High |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

For support and questions:
- 📧 Email: sahiltalwekar123@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/Sahil9309/mlproject/issues)

---

<div align="center">
  <p>🎓 Built with ❤️ for educational excellence</p>
  <p>⭐ Star this repo if you found it helpful!</p>
</div>