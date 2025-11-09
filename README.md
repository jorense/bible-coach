# Bible Coach

An interactive AI companion that guides users through the Bible study
framework of **Observation, Interpretation, and Application (OIA)**.
The app provides a simple chat interface powered by a lightweight coaching
engine that suggests questions, insights, and next steps based on the user's
responses.

## Features

- Conversational interface that keeps track of the OIA progression.
- Keyword extraction to highlight repeated themes in the passage shared by the
  user.
- Tailored prompts and application steps that encourage reflection and action.
- Modern single-page interface with a dark-themed chat layout.

## Getting started

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Open your browser and navigate to <http://localhost:8000>. Start chatting by
   sharing the passage you're studying.

## Running tests

The project includes unit tests that cover the FastAPI routes and the coaching
flow logic. Execute them with:

```bash
pytest
```

## Using the app from GitHub

Because the Bible Coach has both a FastAPI backend and a browser-based front
end, it cannot be hosted on GitHub Pages alone. However, you can spin it up in a
GitHub Codespace (or any GitHub-hosted VS Code environment) without extra
configuration:

1. Open the repository in a Codespace.
2. In the integrated terminal, install the dependencies and run the server:

   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Use the “Ports” tab to mark port `8000` as public and open it in the browser
   tab that Codespaces provides. You can now chat with the coach directly from
   GitHub.

If you only need automated verification on GitHub (e.g., for pull requests),
add a workflow that runs `pytest` on `ubuntu-latest`—no additional services are
required because the suite talks to the FastAPI app in-process.

## Project structure

```
app/
  bible_coach.py     # Conversation logic for OIA coaching
  main.py            # FastAPI application and API routes
frontend/
  index.html         # Chat UI markup
  styles.css         # Styling for the interface
  app.js             # Client-side chat interactions
```

## Notes

- The coaching responses are generated through deterministic heuristics—no
  external API keys are required.
- Conversations are handled entirely in the browser and sent to the backend for
  generating the next response.
