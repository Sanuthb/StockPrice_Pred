# Flask Stock Prediction Project

<h3>Overview</h3>
<p>This project is a Flask-based web application for stock price prediction and recommendation. It uses a trained TensorFlow model to predict stock prices and provides Buy/Sell/Hold recommendations based on the predictions. It also fetches popular stock data using Yahoo Finance.</p>

<h2>Steps to Clone and Set Up the Project</h2>
<h4>1. Clone the Repository</h4>
To start, clone the repository from GitHub to your local machine:

```bash
git clone 
```

<h4>2. Create a Virtual Environment</h4>
Set up a Python virtual environment to manage dependencies:

```bash
python3 -m venv venv or python -m venv venv
source ./venv/bin/activate  # For Linux/Mac
.\venv\Scripts\activate     # For Windows
```

<h4>3. Install Dependencies</h4>
Install the required Python packages from the <b>requirements.txt</b> file:

```bash
pip install -r requirements.txt
```

If the above command fails or requirements.txt does not work, you can install the modules individually using:
```bash
pip install flask pandas numpy tensorflow scikit-learn yfinance
```

<h4>5. Start the Flask Application</h4>
Run the Flask app locally:

```bash
python app.py
```
