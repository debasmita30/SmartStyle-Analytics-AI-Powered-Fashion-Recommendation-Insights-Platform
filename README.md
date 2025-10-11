# 🌟 SmartStyle Analytics: AI-Powered Fashion Recommendation & Insights Platform

SmartStyle Analytics is an intelligent fashion data visualization and recommendation platform that analyzes product trends, customer ratings, and brand insights to enhance online shopping experiences.  

This interactive web app combines data science, visualization, and AI-driven logic to help users explore, compare, and make smarter purchase decisions.

---

## 🚀 Key Features

- 🧠 **AI-Powered Confidence Scoring** – Highlights products with high buyer retention and low return risk.  
- 👗 **Smart Recommendations** – Suggests alternative or safer options for users based on product attributes.  
- 📈 **Interactive Visualizations** – Dynamic charts to explore pricing, brand performance, and rating trends.  
- 💬 **Full Product Insights** – View detailed descriptions, ratings, and confidence levels for each item.  
- 🌈 **Modern UI** – Gradient background, animated visuals, and responsive design for a rich user experience.  
- 🔍 **Advanced Filtering** – Filter by brand, price range, and average rating.  

---

## 🧩 Dataset Information

**Dataset Used:** Fashion Dataset.csv  
**Source:** Custom-curated dataset inspired by e-commerce fashion platforms  

**Columns:**
| Column Name   | Description |
|----------------|-------------|
| p_id | Product ID |
| name | Product name |
| price | Price of the product |
| colour | Dominant color |
| brand | Brand name |
| img | Product image URL |
| ratingCount | Number of user ratings |
| avg_rating | Average customer rating |
| description | Product details |
| p_attributes | Attributes (style, material, fit, etc.) |

---

## ⚙️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python, Pandas  
- **Visualization:** Matplotlib, Plotly, Tableau  
- **Deployment:** Streamlit Cloud  
- **Dataset Hosting:** GitHub Raw File URL  

---

## 🧠 AI Logic (Confidence Score)

Confidence Score (%) = Weighted value derived from  
- High average ratings  
- High number of reviews  
- Low price-risk ratio  

The higher the score, the higher the likelihood that customers will keep the product (low return risk).

---

## 🪄 Installation & Run Locally

### 1️⃣ Clone the Repository

Install Dependencies
pip install streamlit pandas numpy matplotlib plotly

3️⃣ Run the App
streamlit run app.py


The app will open in your browser automatically.

☁️ Deployment on Streamlit Cloud

Push your repository to GitHub

Go to Streamlit Cloud

Click “New app” → Select your repo → Choose app.py

Set your subdomain, for example:

smartstyle-analytics.streamlit.app


Your app will deploy in seconds 🚀

📊 Tableau Dashboard

Experience the live, interactive analytics here:
👉 View Tableau Dashboard

<iframe src="https://public.tableau.com/views/SmartStyleAnalytics/FashionDashboard?:showVizHome=no&:embed=true" width="100%" height="700"></iframe>
Dashboards Included:

Category Performance Overview: Visualize ratings and prices across fashion types

Brand Comparison: Identify top brands by customer satisfaction

Price Distribution: Understand how price varies across different categories

Customer Insights: Analyze trends in ratings and descriptions

🔮 Future Enhancements

Integrate NLP to analyze product descriptions and customer sentiment

Build personalized recommendation engine using collaborative filtering

Enable visual similarity search (upload image → get similar styles)

Add real-time sales and trend prediction models

👩‍💻 Developer

Developed by: Debasmita Chatterjee

Project: SmartStyle Analytics
Type: AI + Data Visualization + Fashion Recommendation

🏷️ License

This project is released under the MIT License.

