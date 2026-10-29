from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    post = None
    error = None

    if request.method == "POST":
        post_id = request.form.get("post_id", "").strip()

        if not post_id.isdigit():
            error = "Please enter a valid number."
        elif not 1 <= int(post_id) <= 100:
            error = "Please enter a number between 1 and 100."
        else:
            try:
                response = requests.get(
                    f"https://jsonplaceholder.typicode.com/posts/{post_id}",
                    timeout=5
                )
                response.raise_for_status()
                post = response.json()

            except requests.exceptions.Timeout:
                error = "The API request timed out. Please try again."

            except requests.exceptions.RequestException:
                error = "Unable to fetch data. Please try again later."

    return render_template("index.html", post=post, error=error)


if __name__ == "__main__":
    app.run(debug=True)