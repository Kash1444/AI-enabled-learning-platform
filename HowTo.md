### inga ella commands um podunga so that new user can easily run the code

You need **two terminals**: one for the backend, one for the frontend.

---

### -> setup (once)

1 ---> git clone https://github.com/Kash1444/AI-enabled-learning-platform.git <br>
2 ---> open the folder "AI-enabled-learning-platform" in VS Code (or any IDE) <br>

---

### -> backend (terminal 1)

Needs Python 3.11+. No API key required — it runs fully offline in DEMO_MODE.

1 ---> cd ai-backend <br>
2 ---> python -m venv .venv <br>
3 ---> .venv\Scripts\activate (Windows) &nbsp;&nbsp; OR &nbsp;&nbsp; source .venv/bin/activate (Mac/Linux) <br>
4 ---> pip install -r requirements.txt <br>
5 ---> copy .env.example .env (Windows) &nbsp;&nbsp; OR &nbsp;&nbsp; cp .env.example .env <br>
6 ---> python seed.py &nbsp;&nbsp;(loads demo employees + competencies — run once) <br>
7 ---> python run.py <br>
8 ---> API is at http://localhost:8000 and docs at http://localhost:8000/docs <br>

In VS Code, pick the interpreter at `ai-backend/.venv` (Ctrl+Shift+P →
"Python: Select Interpreter") or it will report the packages as missing.

**If port 8000 is already used on your machine:** change `PORT=` in
`ai-backend/.env` and set the same port in `frontend/.env`
(`VITE_API_URL=http://localhost:<that port>`).

---

### -> frontend (terminal 2)

1 ---> cd frontend <br>
2 ---> npm install (Ensure node is installed in your device) <br>
3 ---> npm run dev <br>
4 ---> Open the localhost URL in any Browser <br>
Ex URL: <br>
http://localhost:5173 (PORT number may be different)

---

### -> demo logins

employee@demo.com / Employee@123 <br>
trainer@demo.com / Trainer@123 <br>
admin@demo.com / Admin@123

---

### -> checking that it works

With the backend running, in the ai-backend folder (venv activated):

1 ---> python smoke_test.py &nbsp;&nbsp;(hits every endpoint the frontend uses) <br>
2 ---> pytest -q &nbsp;&nbsp;(runs the test suite) <br>

---

### -> resetting the demo data

Delete `ai-backend/storage/app.db` and the contents of
`ai-backend/storage/chroma/` and `ai-backend/storage/uploads/`, then run
`python seed.py` again. Stop the server first, or Windows will report the
files as in use.
