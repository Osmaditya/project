import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer
import nltk
nltk.download('punkt')
nltk.download('stopwords')

def scrape_and_summarize(query):
    # Step 1: Perform web scraping using requests and BeautifulSoup
    url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    print("Response status code:", response.status_code)  # Debug statement
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Step 2: Extract relevant text from the HTML content
    paragraphs = soup.find_all('p')
    print("Paragraphs found:", len(paragraphs))  # Debug statement
    text = ' '.join([para.text for para in paragraphs])
    print("Extracted text:", text)  # Debug statement
    
    # Step 3: Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Step 4: Calculate word frequency to identify important sentences
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    freq_dist = FreqDist(filtered_words)
    
    # Step 5: Choose important sentences based on word frequency
    most_common_words = freq_dist.most_common(10)  # Adjust number of most common words to consider
    important_sentences = []
    
    for sentence in sentences:
        if any(word in sentence.lower() for word, _ in most_common_words):
            important_sentences.append(sentence)
    
    # Step 6: Generate summary by joining selected sentences
    summary = TreebankWordDetokenizer().detokenize(important_sentences)
    
    return summary

if __name__ == '__main__':
    # Your code here

    try:
        user_query = input("Enter your query: ")
        
        summary = scrape_and_summarize(user_query)
        print(f"\nSummary for '{user_query}':")
        print(summary)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
