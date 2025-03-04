import requests
import os
from dotenv import load_dotenv
from google_docs import write_to_google_docs

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

GOOGLE_DOC_ID = "1UOnVik1VCxNK7Gtq6imIXHB_QtA8Nkk3qzK2eO-YqiA"

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"



def generate_post(prompt):
    """Calls Gemini API to generate a LinkedIn post."""
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"❌ API Error: {response.text}"


def generate_content_plan(past_content):
    """✅ Generates a structured 1-month LinkedIn content plan with full weekly posts."""
    
    # ✅ Calculate the average length of past posts
    past_words = past_content.split()
    avg_length = len(past_words) // max(1, past_content.count("\n"))  # Avoid division by zero
    
    # ✅ Ensure posts match past length but with a minimum of 100 words
    min_length = max(100, avg_length)

    prompt = f"""
Analyze the following past LinkedIn posts:\n{past_content}\n
🔹 Identify key themes and engagement patterns.  
🔹 Generate **4 fully written LinkedIn posts** (one per week).  
🔹 Each post must follow this structure:  
    - **Hook:** Start with an engaging first sentence.  
    - **Main Content:** Write at least {min_length} words to match the past post lengths.  
    - **Call to Action (CTA):** End with a strong CTA to drive engagement.  
    - **Hashtags:** Add 1-3 relevant hashtags.  

🔹 **Return only the LinkedIn posts. Do NOT include explanations, analysis, or extra comments.**  
"""
    return generate_post(prompt)  # ✅ Ensures AI generates full-length posts



def read_past_posts():
    """Reads past LinkedIn posts from a text file."""
    try:
        with open("past_posts.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""


def write_generated_posts(content):
    """✅ Writes AI-generated 1-month content plan to a TXT file."""
    with open("generated_posts.txt", "w", encoding="utf-8") as file:
        file.write("📅 **1-Month LinkedIn Content Plan**\n\n")
        file.write(content)
    print("✅ Content plan saved to generated_posts.txt")


def main():
    """✅ Main function to generate ONLY a 1-month LinkedIn content plan."""
    past_content = read_past_posts()

    if not past_content:
        print("⚠️ No past posts found. Please add some to past_posts.txt")
        return

    print("📝 Generating 1-month LinkedIn content plan...")
    content_plan = generate_content_plan(past_content)  # ✅ Only generating content plan

    print("\n📅 Generated 1-Month Content Plan:\n", content_plan)

    # ✅ Save the full content plan to TXT and Google Docs
    write_generated_posts(content_plan)
    write_to_google_docs(GOOGLE_DOC_ID, f"📅 **1-Month LinkedIn Content Plan:**\n{content_plan}")

    print("\n📁 Saved to generated_posts.txt and Google Docs!")


# ✅ ENSURE FUNCTIONS ARE DEFINED BEFORE CALLING main()
if __name__ == "__main__":
    main()
  

# prompt = f"Based on these past LinkedIn posts:\n{past_content}\n\nGenerate a new LinkedIn post idea:"

# def write_generated_posts(content):
#     """Writes generated posts to a local file."""
#     with open("generated_posts.txt", "w", encoding="utf-8") as file:
#         file.write(content)


#     """Main function to generate new posts based on past content."""
#     past_content = read_past_posts()

#     if not past_content:
#         print("⚠️ No past posts found. Please add some to past_posts.txt")
#         return


    