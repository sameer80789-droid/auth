from flask import Flask, request, jsonify, render_template_string
from humanize import humanize  # imports from your humanize.py

app = Flask(__name__)

# ---------------- HTML PAGE ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AI to Human Text</title>
<style>
  body {
    font-family: Arial, sans-serif;
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
    background: #f0f2f5;
  }
  h1 { text-align: center; color: #222; }
  .box {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    margin-bottom: 20px;
  }
  textarea {
    width: 100%;
    height: 200px;
    padding: 14px;
    font-size: 16px;
    border: 2px solid #ccc;
    border-radius: 8px;
    box-sizing: border-box;
    font-family: Georgia, serif;
    resize: vertical;
  }
  button {
    display: block;
    margin: 16px auto 0;
    padding: 12px 40px;
    font-size: 18px;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: 0.2s;
  }
  button:hover { background: #45a049; }
  button:disabled { background: #999; cursor: not-allowed; }
  #output {
    min-height: 150px;
    padding: 14px;
    font-size: 16px;
    border: 2px solid #ccc;
    border-radius: 8px;
    background: #fafafa;
    font-family: Georgia, serif;
    white-space: pre-wrap;
    line-height: 1.6;
  }
  .copy-btn {
    background: #333;
    font-size: 14px;
    padding: 8px 20px;
  }
  .copy-btn:hover { background: #111; }
  label { font-weight: bold; display: block; margin-bottom: 8px; }
</style>
</head>
<body>

<h1>AI Text to Human Text</h1>

<div class="box">
  <label>Paste your AI text:</label>
  <textarea id="input" placeholder="Paste AI text here..."></textarea>
  <button id="go" onclick="convert()">Make It Human</button>
</div>

<div class="box">
  <label>Humanized output:</label>
  <div id="output">Your output will show here...</div>
  <button class="copy-btn" onclick="copyOut()">Copy Output</button>
</div>

<script>
async function convert() {
  const text = document.getElementById('input').value.trim();
  if (!text) {
    alert('Please paste some text first.');
    return;
  }
  const btn = document.getElementById('go');
  btn.disabled = true;
  btn.textContent = 'Working...';
  document.getElementById('output').textContent = 'Processing...';

  try {
    const res = await fetch('/humanize', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text: text})
    });
    const data = await res.json();
    document.getElementById('output').textContent = data.result || 'No output.';
  } catch (e) {
    document.getElementById('output').textContent = 'Error: ' + e.message;
  }

  btn.disabled = false;
  btn.textContent = 'Make It Human';
}

function copyOut() {
  const out = document.getElementById('output').textContent;
  navigator.clipboard.writeText(out);
  alert('Copied!');
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/humanize", methods=["POST"])
def do_humanize():
    data = request.get_json()
    text = data.get("text", "")
    result = humanize(text)
    return jsonify({"result": result})

if __name__ == "__main__":
    print("=" * 50)
    print("  Website running at: http://127.0.0.1:5000")
    print("  Open that link in your browser.")
    print("  Press Ctrl+C here to stop.")
    print("=" * 50)
    app.run(debug=False, host="127.0.0.1", port=5000)