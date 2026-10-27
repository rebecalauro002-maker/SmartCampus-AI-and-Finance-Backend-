# SmartCampus AI & Finance Backend

A modular FastAPI microservice built to power smart campus student services, featuring automated financial transaction categorization and an AI-driven course recommendation engine.

## Tech Stack
* **Web Framework:** FastAPI, Uvicorn
* **Data Processing & ML:** Pandas, Scikit-Learn (TF-IDF Vectorization, Cosine Similarity)
* **Database & Storage:** SQLite, In-Memory Streams (`io`)
* **Language:** Python 3.11+

---

## Core Features

1. **Smart Transaction Categorizer (`/upload-transactions/`)**
   * Accepts CSV transaction logs.
   * Uses rule-based keyword matching to automatically group expenses (like groceries, transit, dining, and subscriptions).
   * Securely saves structured financial data into an SQLite database (`finance.db`) using parameterized queries.

2. **AI Course Recommender (`/upload-courses/`)**
   * Accepts academic catalogs through CSV uploads.
   * Uses Natural Language Processing (TF-IDF) to turn text descriptions into vectors.
   * Computes Cosine Similarity matrices to instantly find and return the best elective courses or projects for students.

---

## Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/smartcampus-ai-backend.git](https://github.com/your-username/smartcampus-ai-backend.git)
cd smartcampus-ai-backend

### 2. Install Dependencies
python -m pip install fastapi uvicorn pandas scikit-learn

###3. Run the Server
python -m uvicorn app.main:app --reload

###4. Test via Interactive Docs
Open your browser and head over to:

    Swagger UI: http://127.0.0.1:8000/docsHere is the updated version with all the emojis stripped out and a much more relaxed, casual tone.

---

### GitHub `README.md` Template

Create a file named `README.md` in your project folder (`C:\Users\Rebeca Lauro\Desktop\bank\`) and paste this in:

```markdown
# SmartCampus AI & Finance Backend

A modular FastAPI microservice built to power smart campus student services, featuring automated financial transaction categorization and an AI-driven course recommendation engine.

## Tech Stack
* **Web Framework:** FastAPI, Uvicorn
* **Data Processing & ML:** Pandas, Scikit-Learn (TF-IDF Vectorization, Cosine Similarity)
* **Database & Storage:** SQLite, In-Memory Streams (`io`)
* **Language:** Python 3.11+

---

## Core Features

1. **Smart Transaction Categorizer (`/upload-transactions/`)**
   * Accepts CSV transaction logs.
   * Uses rule-based keyword matching to automatically group expenses (like groceries, transit, dining, and subscriptions).
   * Securely saves structured financial data into an SQLite database (`finance.db`) using parameterized queries.

2. **AI Course Recommender (`/upload-courses/`)**
   * Accepts academic catalogs through CSV uploads.
   * Uses Natural Language Processing (TF-IDF) to turn text descriptions into vectors.
   * Computes Cosine Similarity matrices to instantly find and return the best elective courses or projects for students.

---

## Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/smartcampus-ai-backend.git](https://github.com/your-username/smartcampus-ai-backend.git)
cd smartcampus-ai-backend

```

### 2. Install Dependencies

```bash
python -m pip install fastapi uvicorn pandas scikit-learn

```

### 3. Run the Server

```bash
python -m uvicorn app.main:app --reload

```

### 4. Test via Interactive Docs

Open your browser and head over to:

* **Swagger UI:** `http://127.0.0.1:8000/docs`

---

### ZJU Application Write-Up

You can use or tweak this for your CV, personal statement, or study plan:

> **Project Title:** SmartCampus AI: Intelligent Financial & Academic Microservice  
> **Role & Tech Stack:** Lead Developer | Python, FastAPI, SQLite, Scikit-Learn, Pandas  
> 
> **Description:**  
> Built a scalable backend microservice designed to help with student life and academic planning. The system has two main parts:
> 1. **A financial tracking tool** that parses transaction CSVs, groups spending categories using rule-based keyword matching, and manages data storage with SQLite.
> 2. **An AI course recommender** that uses TF-IDF vectorization and cosine similarity to analyze course descriptions and give smart academic suggestions. 
> 
> This project highlights hands-on skills in building REST APIs with FastAPI, handling data streams, and writing clean, object-oriented code.

```