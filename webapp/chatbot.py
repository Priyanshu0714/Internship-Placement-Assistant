# from jedi.inference.utils import to_list
import pandas as pd
import requests
import speech_recognition as sr
import torch
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
from optparse import Values

# Load SBERT Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Headers for web scraping
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


# Function to scrape Internshala internships
def scrape_internshala():
    URL = [
        "https://internshala.com/internships/computer-science-internship/",
        "https://internshala.com/internships/computer-science-internship/page-2/",
        "https://internshala.com/internships/computer-science-internship/page-3/",
        "https://internshala.com/internships/computer-science-internship/page-4/",
        "https://internshala.com/internships/computer-science-internship/page-5/",
    ]

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    internships = []
    for page in URL:
        response = requests.get(page, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        for card in soup.find_all("div", class_="individual_internship"):
            title_tag = card.find("a", class_="job-title-href")
            company_tag = card.find("p", class_="company-name")
            locations_tag = card.find("div", class_="locations")
            if locations_tag:
                span_tag = locations_tag.find("span")
                if span_tag:
                    location_link = span_tag.find("a")
                    if location_link:
                        location_text = location_link.text.strip()
            stipend_tag = card.find("span", class_="stipend")
            if title_tag:
                job_title = title_tag.text
                job_link = title_tag.get("href")
            if company_tag:
                company_name = company_tag.text.strip()

            if stipend_tag:
                stipend_name = stipend_tag.text.strip()

            testing = {
                "Title": job_title,
                "Company": company_name,
                "Location": location_text,
                "Stipend": stipend_name,
                "Link": job_link,
            }
            internships.append(testing)

    df = pd.DataFrame(internships)
    df.to_csv("internshala_internships.csv", index=False)
    return df


# Function to load and process internship data
def process_data():
    df = pd.read_csv("internships.csv")
    df.fillna("", inplace=True)

    # Compute embeddings for internship titles
    df["Embedding"] = df["Title"].apply(
        lambda x: model.encode(x, convert_to_tensor=True)
    )

    return df


# Function to recommend internships using SBERT
def recommend_internships(query, df, num_recommendations=10):
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Compute cosine similarity
    similarities = [
        util.pytorch_cos_sim(query_embedding, emb)[0].item() for emb in df["Embedding"]
    ]

    # Add similarity scores to dataframe
    df["Similarity"] = similarities

    # Get top recommendations
    recommendations = df.sort_values(by="Similarity", ascending=False).head(
        num_recommendations
    )

    return recommendations[["Title", "Company", "Stipend", "Link"]].reset_index(
        drop=True
    )


# Function for speech input
def get_speech_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Speak your query...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust to surrounding noise
        try:
            audio = recognizer.listen(source, timeout=7)  # Listen for 5 seconds
            query = recognizer.recognize_google(audio)  # Convert speech to text
            print(f"🗣️ You said: {query}")
            return query
        except sr.UnknownValueError:
            print("❌ Sorry, I couldn't understand. Try again.")
            return None
        except sr.RequestError:
            print("❌ Error with speech recognition service.")
            return None


# Main Chatbot Loop
def chat_bot(user_input):
    # print("\n🔹 Welcome to the Internship Chatbot!")

    # Load and process data
    df = process_data()

    while True:
        # print("\n🔹 Choose input method:")
        # print("1. Type your query")
        # print("2. Speak your query")
        # print("3. Exit")
        #
        # choice = input("Enter choice (1/2/3): ").strip()
        #
        # if choice == "3":
        #     print("🔹 Thank you for using the chatbot!")
        #     break
        # elif choice == "1":
        #     user_input = input("\nEnter an internship title: ").strip()
        # elif choice == "2":
        #     user_input = get_speech_input()
        #     if not user_input:
        #         continue  # If speech input failed, restart loop
        # else:
        #     print("❌ Invalid choice! Try again.")
        #     continue

        recommendations = recommend_internships(user_input, df)

        if not recommendations.empty:
            # print("\n✅ Recommended Internships:")
            # print(recommendations.to_string(index=False))
            return recommendations.values.tolist()
        else:
            return "\n❌ No matching internships found. Try a different keyword."
            # print("\n❌ No matching internships found. Try a different keyword.")


# Run the chatbot
# if __name__ == "__main__":
#     scrape_internshala()
#     chat_bot()
#
