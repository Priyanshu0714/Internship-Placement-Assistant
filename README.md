![Screenshot 2025-03-28 232056](https://github.com/user-attachments/assets/c79e41e6-95ee-47bf-82b2-25bb1205266f)


## 📌 Project Overview
This project is a **web scraper and chatbot** designed to help users find internships from **Internshala** based on their preferences. It utilizes web scraping, NLP-based semantic search, and chatbot functionalities to provide relevant internship opportunities.

## 🚀 Features
- **Web Scraping:** Extracts internship listings from Internshala across multiple pages.
- **Data Processing:** Stores scraped data into a CSV file for further analysis.
- **NLP-Based Search:** Uses **SentenceTransformer** to find the best matching internships based on user queries.
- **Interactive Chatbot:** Provides internship recommendations and resume tips in a conversational style.
- **Custom Greetings & Farewells:** Supports multiple ways to greet and exit the chatbot interaction.
- **Domain-Specific Resume Tips:** Helps users optimize their resumes for different fields like Data Science, Machine Learning, etc.

## 📂 Project Structure
├── scrape_internshala.py   # Web scraping script
├── chatbot.py              # Main chatbot logic
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
└── internships.csv         # Scraped internship data

## 🔧 Installation & Setup
### 1️⃣ Clone the Repository
bash
git clone https://github.com/yourusername/internshala-chatbot.git
cd internshala-chatbot

### 2️⃣ Install Dependencies
Make sure you have Python installed. Then, install the required dependencies:
bash
pip install -r requirements.txt

### 3️⃣ Run the Web Scraper
This script will scrape internship details and store them in a CSV file.
bash
python scrape_internshala.py

### 4️⃣ Run the Chatbot
bash
python chatbot.py


## 🛠 Dependencies
- **BeautifulSoup4** (for web scraping)
- **Requests** (to fetch web pages)
- **Pandas** (for handling CSV data)
- **SentenceTransformers** (for semantic search)
- **NLTK** (for synonyms and text processing)

To install all dependencies, run:
bash
pip install -r requirements.txt


## 💡 How It Works
1. **Scraping Data:**
   - The scraper collects internship details (title, company, location, stipend, and link) from **Internshala**.
   - Stores data in internships.csv.
2. **Chatbot Interaction:**
   - Users enter internship-related queries.
   - The bot finds the **top 5 matching internships** using **semantic similarity**.
   - Displays internship details and provides **application links**.
   - Offers **resume tips** based on the domain of interest.

## 🎯 Example Chatbot Interaction

<img width="1470" alt="ss_internscout" src="https://github.com/user-attachments/assets/68eb560b-1c73-41b5-a601-57c132225441" />


User: Hello!
Bot: Namaste ji! 🙏 Aapka din shubh ho! Kaunsi internship ki talash kar rahe hain aaj?

User: Machine learning internships in Bangalore
Bot: 🔍 Searching for best matches...
1. ML Intern at XYZ Company in Bangalore 💰 ₹15,000/month
2. AI Intern at ABC Tech in Bangalore 💰 ₹12,000/month
...

Bot: Want resume tips for Machine Learning? (Yes/No)
User: Yes
Bot: Here are some tips for ML resumes:
- Mention TensorFlow/PyTorch experience
- Highlight Kaggle participation...

![Screenshot 2025-03-27 044217](https://github.com/user-attachments/assets/27d8c371-d9c5-40aa-b7e4-a42bb57b0864)


## 🏆 Future Improvements
- Adding **real-time internship updates**.
- Supporting **voice-based interaction**.
- Enhancing **resume optimization suggestions**.
- Deploying as a **Telegram bot** for easier access.

## 📜 License
This project is licensed under the **MIT License**.


Developed with ❤️ to help students find the best internships! 😊


