from flask import Flask, render_template, jsonify, request


# App config.
DEBUG = True
app = Flask(__name__)

# Create a list to hold our data
my_data = []


@app.route("/api/data")
def data():
    print(my_data)
    return jsonify(my_data)

@app.route('/')
def home():
    return render_template('index2.html')

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        the_box = request.form["the_box"]

        form_data = {
            "input": the_box,
        }

        my_data.append(form_data)

        return "Thanks for the form data!"

    return render_template("form.html")

 
if __name__ == "__main__":
    app.run()