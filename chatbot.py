import random

import pandas as pd
import requests
import speech_recognition as sr
import torch
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util

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


# Function to process internship data
def process_data():
    df = pd.read_csv("internshala_internships.csv")
    df.fillna("", inplace=True)
    df["Embedding"] = df["Title"].apply(
        lambda x: model.encode(x, convert_to_tensor=True)
    )
    return df


# Function to recommend internships using SBERT
def recommend_internships(query, df, num_recommendations=5):
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = [
        util.pytorch_cos_sim(query_embedding, emb)[0].item() for emb in df["Embedding"]
    ]
    df["Similarity"] = similarities
    recommendations = df.sort_values(by="Similarity", ascending=False).head(
        num_recommendations
    )
    return recommendations[
        ["Title", "Company", "Stipend", "Location", "Link"]
    ].reset_index(drop=True)


# Function for speech input
def get_speech_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak your query...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio, language="hi")
            print(f"🗣️ You said: {query}")
            return query
        except sr.UnknownValueError:
            print("❌ Couldn't understand. Try again.")
            return None
        except sr.RequestError:
            print("❌ Speech service error.")
            return None


# Function to handle chatbot conversation
def chat_bot(user_input=None):
    df = process_data()

    if not user_input:
        user_input = input("💬 Type your query or say it aloud: ")
        if not user_input.strip():
            user_input = get_speech_input()
            if not user_input:
                return "❌ No input detected. Try again."

    recommendations = recommend_internships(user_input, df)

    if not recommendations.empty:
        response_templates = [
            "🔹 {Title} at {Company} (Stipend: {Stipend}, Location: {Location}). Apply here: {Link}",
            "🛠️ Check this: {Title} by {Company}. Location: {Location}, Stipend: {Stipend}. Link: {Link}",
            "🚀 Great opportunity: {Title} at {Company}. {Location} | ₹{Stipend}. Apply now: {Link}",
        ]
        return [
            random.choice(response_templates).format(**row)
            for _, row in recommendations.iterrows()
        ]
    else:
        return "❌ No matching internships found. Try a different keyword."


# Run the chatbot
if __name__ == "__main__":
    scrape_internshala()
    while True:
        response = chat_bot()
        if isinstance(response, list):
            for item in response:
                print(item)
        else:
            print(response)
        print("\nType 'exit' to quit.")
        if input().lower() == "exit":
            break
