# First check in main function if user entered two URLs
import sys

# This function sends request to the given URL and tries to download the HTML content of the page
import requests

def fetch_page(url):
    # we add user-agent so server thinks request is from browser
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to fetch page. Status code:", response.status_code)
            return None
    
    except requests.exceptions.RequestException as e:
        print("Error while fetching:", e)
        return None


# This function extracts only the visible text inside <body> tag
from bs4 import BeautifulSoup

def extract_body_text(html):
    soup = BeautifulSoup(html, "html.parser")
    
    if soup.body:
        text = soup.body.get_text(separator=" ")
        return text
    else:
        return ""


# This function converts text into words
import re

def get_words(text):
    # convert to lowercase
    text = text.lower()
    
    # extract only alphanumeric words
    words = re.findall(r'[a-z0-9]+', text)
    
    return words


# This function counts how many times each word appears
def count_frequency(words):
    freq = {}
    
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    
    return freq


# This function calculates 64-bit polynomial rolling hash
def polynomial_hash(word):
    p = 53
    m = 1 << 64   # 2^64
    
    result = 0
    power = 1
    
    for ch in word:
        ascii_value = ord(ch)
        result = (result + ascii_value * power) % m
        power = (power * p) % m
    
    return result


# This function computes simhash for whole document
def compute_simhash(freq_dict):
    vector = [0] * 64
    
    for word, freq in freq_dict.items():
        h = polynomial_hash(word)
        
        for i in range(64):
            bitmask = 1 << i
            
            if h & bitmask:
                vector[i] += freq
            else:
                vector[i] -= freq
    
    # Now build final hash
    simhash = 0
    
    for i in range(64):
        if vector[i] > 0:
            simhash |= (1 << i)
    
    return simhash


# This function compares two simhash values
def compare_simhash(hash1, hash2):
    xor = hash1 ^ hash2
    
    # count number of 1s
    distance = 0
    while xor:
        distance += xor & 1
        xor >>= 1
    
    common_bits = 64 - distance
    
    return distance, common_bits


# This is main function
def main():
    if len(sys.argv) != 3:
        print("Please provide exactly two URLs.")
        print("Example: python Assignment2.py url1 url2")
        return
    
    url1 = sys.argv[1]
    url2 = sys.argv[2]

    print("First URL:", url1)
    print("Second URL:", url2)

    html1 = fetch_page(url1)
    html2 = fetch_page(url2)

    if html1 is None or html2 is None:
        print("Could not fetch one of the pages.")
        return

    print("Both pages fetched successfully.")

    text1 = extract_body_text(html1)
    text2 = extract_body_text(html2)

    print("Length of first page text:", len(text1))
    print("Length of second page text:", len(text2))

    words1 = get_words(text1)
    words2 = get_words(text2)

    print("Total words in first page:", len(words1))
    print("Total words in second page:", len(words2))

    freq1 = count_frequency(words1)
    freq2 = count_frequency(words2)

    print("Unique words in first page:", len(freq1))
    print("Unique words in second page:", len(freq2))

    print("Hash of word 'hello':", polynomial_hash("hello"))

    simhash1 = compute_simhash(freq1)
    simhash2 = compute_simhash(freq2)

    print("Simhash of first page:", simhash1)
    print("Simhash of second page:", simhash2)

    distance, common = compare_simhash(simhash1, simhash2)

    print("Hamming Distance:", distance)
    print("Common Bits:", common)

if __name__ == "__main__":
    main()
