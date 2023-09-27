**FASTAPI PROJECT**

**Overview**

This project simulates a company that creates quizzes for a smartphone application or a web browser. To simplify the system architecture across these platforms, an API is established to fetch a series of questions from a database.

**Database**

The database is represented by a file named questions.csv with the following fields:
- question: The content of the question
- subject: The category of the question
- correct: List of correct answers
- use: Type of quiz this question is intended for
- responseA to responseD: Possible answers with responseD being optional.

**Application Features**

On the application or web browser:

- Users can select a quiz type (use) and one or multiple categories (subject).
- Quizzes can contain 5, 10, or 20 questions.
- To ensure a diverse experience, the API returns questions in a random order. Thus, identical queries can produce different sets of questions.

**Authentication**

- Users are required to create an account.
- The API currently uses basic authentication, requiring a username and password.
- The authorization header should contain the string "Basic username:password".

**Endpoints**

- The API features an endpoint to verify its functionality.
- An admin user with the password 4dm1N can add a new question.
