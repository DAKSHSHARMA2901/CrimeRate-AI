🔐 CrimeRate AI
A smart machine learning–powered web application that predicts and compares crime rates across major Indian cities based on year, city, and crime type. Built using Flask, Pandas, Scikit-learn, HTML, TailwindCSS, and Chart.js.


🚀 Features
🔍 Predict Crime Rates based on historical data

📊 Compare Crime Trends between two cities

🧠 Uses a trained machine learning model for real-time predictions

📈 Adjusts population growth over years to enhance accuracy

🧾 Dataset preview with clean tabular format

💡 Fully responsive UI with modern design using TailwindCSS

🧠 Tech Stack
Backend	Frontend	ML & Data	Deployment
Flask (Python)	HTML, TailwindCSS	Pandas, Sklearn, Pickle	Render / Railway
📁 Folder Structure
csharp
Copy
Edit
CrimeRate-AI/
├── app.py                  # Main Flask app
├── requirements.txt        # Python dependencies
├── Model/
│   └── model.pkl           # Trained ML model
├── Dataset/
│   └── new_dataset.xlsx    # Crime data
├── templates/
│   ├── index.html          # Home page
│   ├── about.html          # About page
│   └── dataset.html        # Dataset preview
├── static/
│   └── styles, icons etc.
🔮 How It Works
User selects city, crime type, and year.

If data exists in the dataset, it displays real historical stats.

If not, the app:

Estimates population growth from historical data

Predicts crime rate using an ML model

Classifies the region into:

✅ Very Low Crime

🟡 Low Crime

🟠 High Crime

🔴 Very High Crime

Optionally compares predictions across two cities.

📦 Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/dakshsharma2901/CrimeRate-AI.git
cd CrimeRate-AI
Create a virtual environment:

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # On Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the app:

bash
Copy
Edit
python app.py
🌐 Hosting (Optional)
You can deploy CrimeRate AI on platforms like:

Render

Railway

Vercel (frontend only + API backend)

📚 Dataset Info
Source: Indian cities' crime statistics (2014–2021)

Features include: Year, City, Crime Type, Population, Crime Rate

The model uses regression to learn patterns and make predictions even for future years.

🙋‍♂️ About
This project was developed by Daksh Sharma as a part of a machine learning web application initiative.

