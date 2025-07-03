# Document Analyzer

Document Analyzer is a Flask-based web application that allows users to upload legal or contractual documents (in `.txt`, `.pdf`, or `.docx` formats) and automatically analyzes them for risky clauses or content. The application highlights potentially problematic sections and provides a risk score to help users quickly assess their documents.

## Features

- **User Authentication**: Secure registration and login with hashed passwords.
- **Document Upload & Analysis**: Authenticated users can upload documents and receive an automated risk analysis.
- **Risk Scoring**: The app uses natural language processing (NLP) and machine learning to detect risky phrases and compute a normalized risk score.
- **Highlighting**: Risky or important sentences are highlighted and shown to the user.
- **History Dashboard**: Users can view logs of all their past analyses, including filenames, risk scores, and extracted highlights.
- **Admin Panel**: Admin users can see all users and all analyses in the system.
- **Responsive UI**: Built with Bootstrap 5 for a modern, mobile-friendly design.

## How It Works

1. **User Registration & Login**

   - Users register with a username, email, and password or they can login directly using their Google Account.
   - Passwords are securely hashed before storage.
   - Users must be logged in to upload and analyze documents.

2. **Document Upload & Analysis**

   - Supported formats: `.txt`, `.pdf`, `.docx`.
   - Uploaded files are parsed and their text extracted.
   - The text is analyzed using NLP (spaCy) to detect risky phrases.
   - Each risky sentence found increases the document's risk score.
   - The risk score is normalized (0-100%).
   - Results are shown instantly and saved to the user's dashboard.

3. **Dashboard**

   - Users can see a table of their previous analyses, including file name, upload time, risk score, and highlights.
   - Users can delete their history entries.


## Example

- Upload a contract as a `.pdf` file.
- Get a result showing:
  - **Risk Score:** e.g., 42%
  - **Highlights:** List of sentences or clauses considered risky.

## Tech Stack

- **Backend:** Python, Flask, Flask-Login, Flask-WTF, Flask-SQLAlchemy, Flask-MySQLdb
- **Frontend:** HTML (Jinja2 templates), Bootstrap 5, JavaScript
- **Machine Learning/NLP:** spaCy 
- **Database:** MySQL (via SQLAlchemy ORM)
- **PDF/Docx Parsing:** PyPDF2, python-docx
- **Dotenv** for environment management

## File Structure

- `app.py` — Main Flask app and routes
- `models/models.py` — SQLAlchemy models (`User`, `AnalysisLog`)
- `ml/analyzer.py` — Risky clause detection logic (NLP)
- `templates/` — HTML templates for pages (index, dashboard, admin, etc.)
- `static/` — CSS and JavaScript assets
- `requirements.txt` — Python dependencies
- `config.py` — App configuration (reads from `.env`)

## Key Code Highlights

- **Document Analysis Logic**:
  ```python
  def analyze_document(text):
      doc = nlp(text)
      highlights = []
      risk_score = 0
      for sent in doc.sents:
          for phrase in RISKY_PHRASES:
              if phrase in sent.text.lower():
                  highlights.append(sent.text)
                  risk_score += 1
      risk_score = min(1.0, risk_score / 12.0) # Normalize risk
      return {
          'risk_score': round(risk_score * 100, 1),
          'highlights': highlights
      }
  ```

- **User Dashboard Table**:
  | Time         | Filename    | Risk Score | Highlights     | Action  |
  |--------------|-------------|------------|---------------|---------|
  | 2025-07-01   | contract.pdf| 42%        | [View Details] | Delete  |

## Setup & Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/MichaelWaruiru/document-analyzer.git
   cd document-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env` and fill in the necessary secrets (e.g., `SECRET_KEY`, `DATABASE_URL`).

4. **Initialize the database**

*Note: This creates the tables automatically in MySQL*
   ```bash
   flask init-db
   ```

5. **Run the app**
   ```bash
   flask run
   ```
   - The app will be available at `http://localhost:5000`

## Usage

- You can quickly upload a document for analysis without registering an account. If not you can do the following:

   - Register a new account.
   - Log in.
   - Upload your document for analysis.
   - View your results and analysis history on your dashboard.

## Security & Privacy

- User passwords are securely hashed.
- Uploaded documents are processed in-memory and not permanently stored.
- Only authenticated users can access document analysis features.

## Contributing

Pull requests and issues are welcome! Please open an issue first to discuss changes or suggestions.

## License

MIT License

---

**Made with ❤️ For You**