"""CipherForge Flask Web Application.

Provides a web interface for the 5-phase encryption algorithm.
"""

from flask import Flask, render_template, request
from engine import encrypt, decrypt

app = Flask(__name__)


@app.route("/")
def index():
    """Display the homepage."""
    return render_template("index.html")


@app.route("/workshop", methods=["GET", "POST"])
def workshop():
    """Handle encryption and decryption requests."""
    result = ""
    original = ""

    form_data = {
        "shift": "5",
        "block_size": "4",
        "password": "SECRET",
        "noise_interval": "3",
        "noise_chars": "~",
        "xor_password": "XORKEY",
    }

    if request.method == "POST":
        original = request.form.get("message", "")
        action = request.form.get("action", "encrypt")

        form_data["shift"] = request.form.get("shift", "5")
        form_data["block_size"] = request.form.get("block_size", "4")
        form_data["password"] = request.form.get("password", "SECRET")
        form_data["noise_interval"] = request.form.get("noise_interval", "3")
        form_data["noise_chars"] = request.form.get("noise_chars", "~")
        form_data["xor_password"] = request.form.get("xor_password", "XORKEY")

        key = {
            "shift": int(form_data["shift"]),
            "block_size": int(form_data["block_size"]),
            "password": form_data["password"],
            "noise_interval": int(form_data["noise_interval"]),
            "noise_chars": form_data["noise_chars"],
            "xor_password": form_data["xor_password"],
        }

        if action == "encrypt":
            result = encrypt(original, key)
        else:
            result = decrypt(original, key)

    return render_template(
        "workshop.html",
        result=result,
        original=original,
        form_data=form_data,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
