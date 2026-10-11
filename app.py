from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from humanize import humanize
from advanced_humanize import advanced_humanize
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sameer-humanizer-secret-2024")

ACCESS_KEY = "725030"


# ============================================================
# LOGIN PAGE
# ============================================================
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SAMEER — Login</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #05060a;
    background-image:
      radial-gradient(circle at 15% 20%, rgba(120, 80, 255, 0.25), transparent 45%),
      radial-gradient(circle at 85% 80%, rgba(0, 200, 255, 0.18), transparent 45%),
      radial-gradient(circle at 50% 50%, rgba(255, 80, 200, 0.10), transparent 60%);
    color: #fff;
    overflow: hidden;
    padding: 20px;
  }
  .orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.5;
    animation: float 12s ease-in-out infinite;
  }
  .orb1 { width: 400px; height: 400px; background: #7b5cff; top: -100px; left: -100px; }
  .orb2 { width: 350px; height: 350px; background: #00d4ff; bottom: -100px; right: -100px; animation-delay: -4s; }
  .orb3 { width: 300px; height: 300px; background: #ff4fa3; top: 40%; left: 60%; animation-delay: -8s; opacity: 0.25; }

  @keyframes float {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(30px, -30px) scale(1.1); }
  }

  .login-card {
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 420px;
    padding: 48px 40px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255,255,255,0.06);
    animation: slideUp 0.6s cubic-bezier(0.2, 0.9, 0.3, 1);
  }
  @keyframes slideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 42px;
    font-weight: 700;
    letter-spacing: 8px;
    text-align: center;
    background: linear-gradient(135deg, #a78bfa 0%, #22d3ee 50%, #f472b6 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
  }
  .tagline {
    text-align: center;
    color: rgba(255,255,255,0.5);
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 36px;
  }

  label {
    display: block;
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.55);
    margin-bottom: 10px;
  }
  input[type="password"] {
    width: 100%;
    padding: 14px 18px;
    font-size: 16px;
    font-family: 'Space Grotesk', monospace;
    letter-spacing: 3px;
    color: #fff;
    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    outline: none;
    transition: 0.25s;
  }
  input[type="password"]:focus {
    border-color: #7b5cff;
    box-shadow: 0 0 0 4px rgba(123, 92, 255, 0.15);
    background: rgba(0,0,0,0.5);
  }

  button {
    width: 100%;
    margin-top: 24px;
    padding: 14px;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #fff;
    background: linear-gradient(135deg, #7b5cff 0%, #22d3ee 100%);
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.25s;
    box-shadow: 0 10px 30px rgba(123, 92, 255, 0.35);
  }
  button:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(123, 92, 255, 0.5);
  }
  button:active { transform: translateY(0); }

  .error {
    margin-top: 16px;
    padding: 12px;
    border-radius: 10px;
    background: rgba(255, 80, 80, 0.12);
    border: 1px solid rgba(255, 80, 80, 0.3);
    color: #ff9b9b;
    font-size: 13px;
    text-align: center;
    animation: shake 0.4s;
  }
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-8px); }
    75% { transform: translateX(8px); }
  }

  .footer {
    margin-top: 32px;
    text-align: center;
    font-size: 11px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 1px;
  }
</style>
</head>
<body>
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>
  <div class="orb orb3"></div>

  <div class="login-card">
    <div class="logo">SAMEER</div>
    <div class="tagline">AI Text Humanizer</div>

    <form method="POST" action="/login">
      <label>Access Key</label>
      <input type="password" name="key" placeholder="••••••" autofocus required>
      <button type="submit">Unlock</button>
    </form>

    {% if error %}
    <div class="error">{{ error }}</div>
    {% endif %}

    <div class="footer">Protected access • SAMEER © 2024</div>
  </div>
</body>
</html>
"""


# ============================================================
# MAIN APP PAGE
# ============================================================
APP_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SAMEER — AI to Human Text</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    background: #05060a;
    background-image:
      radial-gradient(circle at 10% 10%, rgba(120, 80, 255, 0.18), transparent 40%),
      radial-gradient(circle at 90% 90%, rgba(0, 200, 255, 0.14), transparent 40%),
      radial-gradient(circle at 50% 50%, rgba(255, 80, 200, 0.06), transparent 60%);
    color: #fff;
    padding: 40px 20px 60px;
  }

  .orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(100px);
    opacity: 0.35;
    z-index: 0;
    pointer-events: none;
  }
  .orb1 { width: 500px; height: 500px; background: #7b5cff; top: -150px; left: -150px; }
  .orb2 { width: 450px; height: 450px; background: #00d4ff; bottom: -150px; right: -150px; }

  .container {
    position: relative;
    z-index: 2;
    max-width: 1000px;
    margin: 0 auto;
  }

  /* HEADER */
  .header {
    text-align: center;
    margin-bottom: 40px;
    animation: fadeDown 0.7s ease;
  }
  @keyframes fadeDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 52px;
    font-weight: 700;
    letter-spacing: 12px;
    background: linear-gradient(135deg, #a78bfa 0%, #22d3ee 50%, #f472b6 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
  }
  .tagline {
    color: rgba(255,255,255,0.45);
    font-size: 13px;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 4px;
  }
  .badge {
    display: inline-block;
    margin-top: 14px;
    padding: 6px 16px;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #22d3ee;
    background: rgba(34, 211, 238, 0.08);
    border: 1px solid rgba(34, 211, 238, 0.25);
    border-radius: 999px;
  }

  /* CARDS */
  .card {
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 22px;
    padding: 28px;
    margin-bottom: 22px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    animation: slideUp 0.6s cubic-bezier(0.2, 0.9, 0.3, 1) backwards;
  }
  .card:nth-of-type(1) { animation-delay: 0.1s; }
  .card:nth-of-type(2) { animation-delay: 0.2s; }
  @keyframes slideUp {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .card-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
  }
  .card-label {
    font-size: 12px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    font-weight: 600;
  }
  .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #7b5cff;
    box-shadow: 0 0 12px #7b5cff;
    display: inline-block;
    margin-right: 10px;
    vertical-align: middle;
  }
  .dot.green { background: #22d3ee; box-shadow: 0 0 12px #22d3ee; }

  textarea {
    width: 100%;
    height: 220px;
    padding: 18px;
    font-size: 15px;
    line-height: 1.7;
    color: #eaeaea;
    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    outline: none;
    resize: vertical;
    font-family: 'Inter', sans-serif;
    transition: 0.25s;
  }
  textarea:focus {
    border-color: #7b5cff;
    box-shadow: 0 0 0 4px rgba(123, 92, 255, 0.12);
    background: rgba(0,0,0,0.5);
  }
  textarea::placeholder { color: rgba(255,255,255,0.25); }

  #output {
    min-height: 220px;
    padding: 18px;
    font-size: 15px;
    line-height: 1.7;
    color: #eaeaea;
    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: 'Inter', sans-serif;
  }
  #output.empty { color: rgba(255,255,255,0.25); font-style: italic; }

  .btn-row {
    display: flex;
    gap: 12px;
    margin-top: 18px;
    flex-wrap: wrap;
  }

  button {
    padding: 14px 32px;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #fff;
    background: linear-gradient(135deg, #7b5cff 0%, #22d3ee 100%);
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.25s;
    box-shadow: 0 10px 30px rgba(123, 92, 255, 0.35);
    font-family: 'Inter', sans-serif;
  }
  button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(123, 92, 255, 0.5);
  }
  button:active:not(:disabled) { transform: translateY(0); }
  button:disabled {
    background: rgba(255,255,255,0.08);
    color: rgba(255,255,255,0.4);
    box-shadow: none;
    cursor: not-allowed;
  }

  .btn-ghost {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: none;
  }
  .btn-ghost:hover:not(:disabled) {
    background: rgba(255,255,255,0.10);
    border-color: rgba(255,255,255,0.25);
    box-shadow: none;
  }

  .btn-full { flex: 1; min-width: 180px; }

  .stats {
    margin-top: 14px;
    display: flex;
    gap: 24px;
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    letter-spacing: 1px;
  }
  .stats span b { color: #22d3ee; font-weight: 600; }

  .toast {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%) translateY(80px);
    padding: 14px 28px;
    background: rgba(34, 211, 238, 0.15);
    border: 1px solid rgba(34, 211, 238, 0.4);
    color: #22d3ee;
    border-radius: 12px;
    font-size: 14px;
    letter-spacing: 1px;
    transition: 0.4s cubic-bezier(0.2, 0.9, 0.3, 1);
    z-index: 100;
    backdrop-filter: blur(20px);
  }
  .toast.show { transform: translateX(-50%) translateY(0); }

  .footer {
    text-align: center;
    margin-top: 30px;
    font-size: 11px;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.25);
  }

  /* LOGOUT */
  .logout {
    position: absolute;
    top: 20px;
    right: 20px;
    padding: 8px 18px;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.6);
    text-decoration: none;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
    transition: 0.25s;
    background: rgba(0,0,0,0.3);
  }
  .logout:hover {
    color: #ff9b9b;
    border-color: rgba(255, 80, 80, 0.4);
    background: rgba(255, 80, 80, 0.08);
  }

  @media (max-width: 600px) {
    .logo { font-size: 36px; letter-spacing: 8px; }
    .card { padding: 20px; }
    .btn-full { min-width: 100%; }
  }
</style>
</head>
<body>
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>

  <a href="/logout" class="logout">Logout</a>

  <div class="container">
    <div class="header">
      <div class="logo">SAMEER</div>
      <div class="tagline">AI Text Humanizer</div>
      <div class="badge">● Offline Engine • No API</div>
    </div>

    <div class="card">
      <div class="card-head">
        <div class="card-label"><span class="dot"></span>Input Text</div>
        <div class="stats"><span>Chars: <b id="inLen">0</b></span></div>
      </div>
      <textarea id="input" placeholder="Paste your AI-generated text here..."></textarea>
      <div class="btn-row">
        <button id="go" onclick="convert()" class="btn-full">Make It Human</button>
        <button onclick="clearAll()" class="btn-ghost">Clear</button>
      </div>
    </div>

    <div class="card">
      <div class="card-head">
        <div class="card-label"><span class="dot green"></span>Humanized Output</div>
        <div class="stats"><span>Chars: <b id="outLen">0</b></span></div>
      </div>
      <div id="output" class="empty">Your humanized text will appear here...</div>
      <div class="btn-row">
        <button onclick="copyOut()" class="btn-ghost btn-full">Copy Output</button>
        <button onclick="downloadOut()" class="btn-ghost">Download .txt</button>
      </div>
    </div>

    <div class="footer">SAMEER © 2024 • Built with Flask + Python</div>
  </div>

  <div id="toast" class="toast">Copied!</div>

<script>
const input = document.getElementById('input');
const output = document.getElementById('output');
const goBtn = document.getElementById('go');
const inLen = document.getElementById('inLen');
const outLen = document.getElementById('outLen');

input.addEventListener('input', () => { inLen.textContent = input.value.length; });

async function convert() {
  const text = input.value.trim();
  if (!text) { showToast('Please paste some text first.'); return; }
  goBtn.disabled = true;
  goBtn.textContent = 'Working...';
  output.classList.remove('empty');
  output.textContent = 'Processing your text...';

  try {
    const res = await fetch('/humanize', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text: text})
    });
    if (res.status === 401) { window.location.href = '/'; return; }
    const data = await res.json();
    output.textContent = data.result || 'No output.';
    outLen.textContent = output.textContent.length;
  } catch (e) {
    output.textContent = 'Error: ' + e.message;
  }

  goBtn.disabled = false;
  goBtn.textContent = 'Make It Human';
}

function clearAll() {
  input.value = '';
  output.textContent = 'Your humanized text will appear here...';
  output.classList.add('empty');
  inLen.textContent = '0';
  outLen.textContent = '0';
}

function copyOut() {
  const t = output.textContent;
  if (!t || output.classList.contains('empty')) return;
  navigator.clipboard.writeText(t);
  showToast('Copied to clipboard!');
}

function downloadOut() {
  const t = output.textContent;
  if (!t || output.classList.contains('empty')) return;
  const blob = new Blob([t], {type: 'text/plain'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'humanized_output.txt';
  a.click();
  URL.revokeObjectURL(url);
  showToast('Downloaded!');
}

let toastTimer;
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2200);
}

// Keyboard shortcut: Ctrl+Enter to convert
input.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); convert(); }
});
</script>
</body>
</html>
"""


# ============================================================
# ROUTES
# ============================================================
@app.route("/")
def home():
    if not session.get("logged_in"):
        return render_template_string(LOGIN_HTML, error=None)
    return render_template_string(APP_HTML)


@app.route("/login", methods=["POST"])
def login():
    key = request.form.get("key", "").strip()
    if key == ACCESS_KEY:
        session["logged_in"] = True
        return redirect(url_for("home"))
    return render_template_string(LOGIN_HTML, error="Wrong access key. Try again.")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/humanize", methods=["POST"])
def do_humanize():
    if not session.get("logged_in"):
        return jsonify({"error": "unauthorized"}), 401
    data = request.get_json()
    text = data.get("text", "")

    # PASS 1: base humanizer (word swaps, contractions, splitting)
    stage1 = humanize(text)

    # PASS 2: advanced humanizer (clichés, rhythm, redundancy)
    stage2 = advanced_humanize(stage1)

    return jsonify({"result": stage2})


if __name__ == "__main__":
    print("=" * 50)
    print("  Website running at: http://127.0.0.1:5000")
    print("  Access key: 725030")
    print("  Press Ctrl+C here to stop.")
    print("=" * 50)
    app.run(debug=False, host="127.0.0.1", port=5000)
