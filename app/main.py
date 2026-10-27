from fastapi import FastAPI, File, UploadFile, HTTPException #web server
import pandas as pd #spreadsheet manipulation
from sklearn.feature_extraction.text import TfidfVectorizer #text feature extraction
from sklearn.metrics.pairwise import cosine_similarity #similarity computation
import csv #csv file handling
import sqlite3 #database management
import io #in-memory file handling
import re #regular expressions
from datetime import date #date handling
from decimal import Decimal, InvalidOperation #decimal number handling
from pathlib import Path #file path handling
from pydantic import BaseModel, Field #data validation and settings management

# Initialize the FastAPI app
app = FastAPI(title="SmartCampus AI API", version="0.1.0")

categories = { #string with the categories and the keywords to match
    "groceries": ["lidl", "aldi", "spar", "tesco", "mercadona", "carrefour"],
    "entertainment": ["netflix", "hbo", "disney", "amazon prime"],
    "transportation": ["uber", "lyft", "taxi", "train", "bus"],
    "utilities": ["electricity", "water", "gas", "internet", "phone"],
    "dining": ["mcdonald's", "kfc", "burger king", "pizza hut", "subway"],
    "cafe": ["starbucks", "costa coffee", "cafe nero", "peet's coffee"],
    "shopping": ["amazon", "ebay", "zara", "h&m", "nike", "adidas"],
    "healthcare": ["cvs", "walgreens", "boots", "rite aid", "john lewis"],
    "travel": ["airbnb", "expedia", "booking.com", "tripadvisor", "skyscraper"],
    "education": ["coursera", "edx", "udemy", "khan academy", "lynda"],
    "personal care": ["sephora", "ulta", "lush", "the body shop", "aveda"],
    "finance": ["bank of america", "chase", "wells fargo", "citibank", "paypal"],
    "gifts": ["etsy", "hallmark", "redbubble", "zazzle", "shutterfly"],
    "subscriptions": ["spotify", "apple music", "youtube premium", "tidal", "audible"],
    "charity": ["red cross", "unicef", "world wildlife fund", "oxfam", "save the children"],
    "miscellaneous": ["miscellaneous", "other", "unknown"]
}

# CSV file parser to python 
def parse_transactions_file(file_path: str): #defines a function that takes a file path as input and returns a list of dictionaries containing merchant names and amounts from the transactions file
    path = Path(file_path) #creates a Path object from the provided file path
    if not path.exists(): #if path doesnt exist, return an empty list
        return []

    results = [] #results list to store the parsed transactions
    with open(path, mode="r", encoding="utf-8") as file: #opens the file in read mode with UTF-8 encoding
        reader = csv.DictReader(file) #creates a CSV reader object that reads the file as a dictionary, where each row is represented as a dictionary with column headers as keys
        for row in reader: #iterates over each row in the CSV file
            merchant = row["merchant_name"] #extracts the merchant name from the current row
            amount = row["amount"] #extracts the amount from the current row
            results.append({"merchant": merchant, "amount": amount}) #appends a dictionary containing the merchant name and amount to the results list
            
    return results

# Initialize the database and create the transactions table if it doesn't exist
def init_db(): #defines a function for sqlite database initialization and table creation
    conn = sqlite3.connect("finance.db") #establishes a connection to the SQLite database file named "finance.db"
    cursor = conn.cursor() #creates a cursor object to execute SQL commands
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            merchant_name TEXT,
            amount REAL,
            currency TEXT,
            category TEXT
        )
    """) #executes an SQL command to create a table named "transactions" with columns for id, date, merchant_name, amount, currency, and category if it doesn't already exist
    conn.commit() #commits the changes to the database, ensuring that the table creation is saved
    conn.close() #closes the database connection to free up resources and ensure data integrity

# Execute the database initialization function
init_db()

# Rule-Based Categorization Engine
def categorize(merchant: str) -> str: #defines a function that takes a merchant name as input and returns the corresponding category based on predefined keywords
    merchant_lower = merchant.lower() #converts the merchant name to lowercase for case-insensitive matching
    for category, keywords in categories.items(): #iterates over each category and its associated keywords in the categories dictionary
        for keyword in keywords: #iterates over each keyword in the current category's list of keywords
            if keyword in merchant_lower: #checks if the current keyword is present in the lowercase merchant name
                return category #returns the category if a match is found
    return "miscellaneous" #returns "miscellaneous" if no matching category is found for the merchant name

# FastAPI Endpoint to Upload and Process Transactions CSV
# FastAPI Endpoint to Upload and Process Transactions CSV
@app.post("/upload-transactions/") #defines a POST endpoint in the FastAPI application that allows users to upload a CSV file containing transaction data.
async def upload_transactions(file: UploadFile = File(...)): #defines an asynchronous function to handle the CSV upload and processing
    if not file.filename.endswith('.csv'): #checks if the uploaded file has a '.csv' extension
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")
        
    contents = await file.read() #reads the contents of the uploaded file asynchronously
    buffer = io.StringIO(contents.decode("utf-8")) #creates an in-memory text stream from the decoded contents of the uploaded file
    reader = csv.DictReader(buffer) #creates a CSV reader object
    
    # Verify schema requirements to prevent a KeyError crash
    if not reader.fieldnames or "merchant_name" not in reader.fieldnames or "amount" not in reader.fieldnames:
        raise HTTPException(
            status_code=400, 
            detail="Invalid CSV format. Transactions CSV must contain 'merchant_name', 'amount', and 'date' columns."
        )
    
    conn = sqlite3.connect("finance.db") #establishes a connection to the SQLite database file named "finance.db"
    cursor = conn.cursor() #creates a cursor object to execute SQL commands
    
    processed_count = 0 #initializes a counter to keep track of the number of processed transactions
    for row in reader: #iterates over each row in the CSV file
        merchant = row["merchant_name"] #extracts the merchant name from the current row
        amount = float(row["amount"]) #extracts the amount from the current row and converts it to a float
        trans_date = row.get("date", "2026-01-01") #extracts the transaction date from the current row, defaulting if not provided
        currency = row.get("currency", "EUR") #extracts the currency from the current row, defaulting to "EUR" if not provided
        
        category = categorize(merchant) #calls the categorize function to determine the category of the transaction based on the merchant name
        
        cursor.execute("""
            INSERT INTO transactions (date, merchant_name, amount, currency, category)
            VALUES (?, ?, ?, ?, ?)
        """, (trans_date, merchant, amount, currency, category)) #executes an SQL command to insert the transaction data into the database, using parameterized queries to prevent SQL injection
        
        processed_count += 1 #increments the processed transaction counter by 1 for each successfully processed transaction
        
    conn.commit() #commits the changes to the database, ensuring that all inserted transactions are saved
    conn.close() #closes the database connection to free up resources and ensure data integrity
    
    return {
        "status": "success", 
        "message": "Transactions imported and categorized successfully",
        "rows_processed": processed_count
    } #returns a JSON response indicating the success of the operation, along with the number of rows processed from the uploaded CSV file
    
class SmartCampusRecommender: #defines a class that implements a recommendation system for courses based on their descriptions using TF-IDF and cosine similarity.
    def __init__(self, courses_df: pd.DataFrame): #initializes the SmartCampusRecommender class with a DataFrame containing course titles and descriptions.
        self.courses_df = courses_df #stores the provided DataFrame containing course titles and descriptions as an instance variable
        self.similarity_matrix = None #initializes an instance variable to hold the similarity matrix
        self._prepare_model() #calls the private method _prepare_model to compute the similarity matrix

    def _prepare_model(self): #defines a private method that computes the similarity matrix for the course descriptions using TF-IDF vectorization and cosine similarity.
        """Precomputes text-based similarity using TF-IDF and Cosine Similarity."""
        vectorizer = TfidfVectorizer(stop_words='english') #creates an instance of TfidfVectorizer with English stop words
        tfidf_matrix = vectorizer.fit_transform(self.courses_df['description']) #fits the TF-IDF vectorizer and transforms the descriptions into a matrix
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix) #computes the cosine similarity between all pairs of course descriptions

    def recommend_courses(self, course_title: str, top_n: int = 2): #defines a method that recommends the top-N similar courses based on the description of a given course title.
        """Returns top-N similar courses based on curriculum descriptions."""
        if course_title not in self.courses_df['title'].values: #checks if the provided course title exists in the DataFrame
            raise ValueError(f"Course '{course_title}' not found in the catalog.") #raises a ValueError if not found
        
        idx = self.courses_df[self.courses_df['title'] == course_title].index[0] #retrieves the index of the course in the DataFrame
        similarity_scores = list(enumerate(self.similarity_matrix[idx])) #enumerates the similarity scores for the specified course
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True) #sorts the list of similarity scores in descending order
        
        top_indices = [i[0] for i in similarity_scores[1:top_n+1]] #extracts the indices of the top-N similar courses, excluding the course itself
        return self.courses_df['title'].iloc[top_indices].tolist() #returns a list of course titles corresponding to the top-N similar courses

# FastAPI Endpoint to Upload and Process Courses CSV
@app.post("/upload-courses/") #defines a POST endpoint in the FastAPI application that allows users to upload a CSV file containing course catalogs.
async def upload_courses(file: UploadFile = File(...)): #defines an asynchronous function to handle the course catalog CSV upload and processing.
    """
    Endpoint to upload a CSV file containing course catalogs 
    with 'title' and 'description' columns.
    """
    if not file.filename.endswith('.csv'): #checks if the uploaded file has a '.csv' extension
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    try:
        contents = await file.read() #reads the contents of the uploaded CSV file asynchronously
        df = pd.read_csv(io.BytesIO(contents)) #reads the contents of the uploaded CSV file into a pandas DataFrame
        
        # Verify schema requirements
        if 'title' not in df.columns or 'description' not in df.columns: #checks if required columns are present
            raise HTTPException( 
                status_code=400, 
                detail="CSV file must contain 'title' and 'description' columns."
            )
        
        # Initialize the recommender with the uploaded data
        recommender = SmartCampusRecommender(df) #initializes an instance of the SmartCampusRecommender class
        
        return {
            "message": "CSV uploaded and recommendation model initialized successfully!",
            "filename": file.filename,
            "total_courses_loaded": len(df),
            "sample_courses": df['title'].head(3).tolist()
        }
        
    except Exception as e: #catches any exceptions that occur during processing
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")