from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
import csv
import base64

app = FastAPI(
    title="Question Retrieval API",
    description="An API to retrieve questions from a CSV file.",
    version="1.0"
)

# Define a Pydantic model to represent questions
class Question(BaseModel):
    id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    answer: str
    use: str
    subject: str

# Check authorization header
def verify_token(authorization: Optional[str] = Header(None)):
    """Verify the provided token in the Authorization header."""
    if not authorization or "Basic" not in authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    encoded_credentials = authorization.split(" ")[1]  # Split "Basic encoded_credentials"
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")  # Decode the Base64 encoded string
    username, _, password = decoded_credentials.partition(':')

    TOKENS = {"alice": "wonderland"}
    if username not in TOKENS or TOKENS[username] != password:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username

@app.get("/status/", tags=["Health Check"])
def read_status():
    """Check the health status of the API."""
    return {"status": "API is functional"}

@app.get("/questions/", response_model=List[Question], tags=["Questions"])
def read_questions(
    use: str, 
    subject: str, 
    count: int, 
    user: str = Depends(verify_token)
):
    """
    Retrieve questions from the CSV based on the specified use and subject.
    
    Parameters:
    - `use`: The intended use of the question.
    - `subject`: The subject/topic of the question.
    - `count`: The number of questions to retrieve.
    """
    questions = []
    with open("questions.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["use"] == use and row["subject"] == subject:
                question_data = {
                    "id": len(questions) + 1,
                    "question": row["question"],
                    "subject": row["subject"],
                    "use": row["use"],
                    "answer": row["correct"],
                    "option_a": row["responseA"],
                    "option_b": row["responseB"],
                    "option_c": row["responseC"],
                    "option_d": row["responseD"]
                }
                questions.append(Question(**question_data))
            if len(questions) == count:
                break
    return questions

class NewQuestion(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: str
    remark: Optional[str] = ""

# Check admin credentials
def verify_admin_credentials(authorization: Optional[str] = Header(None)):
    """Verify the provided admin credentials in the Authorization header."""
    if not authorization or "Basic" not in authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    encoded_credentials = authorization.split(" ")[1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
    username, _, password = decoded_credentials.partition(':')

    # Check for admin password
    if password != "4dm1N":
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username

@app.post("/questions/", response_model=Question, tags=["Questions"])
def create_question(
    new_question: NewQuestion, 
    admin: str = Depends(verify_admin_credentials)
):
    """
    Add a new question to the CSV.

    Parameters:
    - `new_question`: A Pydantic model that holds the new question data.
    """
    # Calculate the new ID based on the number of rows in the CSV
    with open("questions.csv", "r", newline='', encoding="utf-8") as f:
        id_count = sum(1 for row in f)

    with open("questions.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "question", "subject", "use", "correct",
            "responseA", "responseB", "responseC", "responseD", "remark"
        ])
        writer.writerow(new_question.dict())
    
    return {
        "id": id_count,
        "question": new_question.question,
        "option_a": new_question.responseA,
        "option_b": new_question.responseB,
        "option_c": new_question.responseC,
        "option_d": new_question.responseD,
        "answer": new_question.correct,
        "use": new_question.use,
        "subject": new_question.subject
    }
