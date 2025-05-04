# Industry Valley Game

A strategic economic simulation game where players manage US industrial policy to compete with China's manufacturing capacity.

## Game Overview

Players implement various policies to boost US industrial capacity while managing:

- GDP growth
- Worker happiness
- International relations
- Innovation
- Budget constraints

## Local Development

### Frontend

The frontend is a single HTML file with embedded JavaScript. To run locally:

1. Clone this repository
2. Open `docs/index.html` in a web browser

### Backend

The backend is a Flask server that handles economic calculations. To run locally:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the server:

```bash
python app.py
```

The server will start on `http://localhost:8000`

## Deployment

### Frontend (GitHub Pages)

1. Create a new repository on GitHub
2. Push this code to the repository
3. Enable GitHub Pages in the repository settings:
   - Go to Settings > Pages
   - Under "Source", select the main branch
   - Under "Folder", select `/docs`
   - Click Save
4. Your game will be available at `https://<username>.github.io/<repository-name>`

### Backend (Render)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment Variables:
     - Add `PYTHON_VERSION`: `3.9.0`
4. After deployment, copy your Render URL
5. Update `API_BASE_URL` in `docs/index.html` with your Render URL

## Project Structure

```
.
├── README.md
├── requirements.txt
├── app.py
├── aa_dd_model.py
└── docs/
    └── index.html
```

## License

MIT License
