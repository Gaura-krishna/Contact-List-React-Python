from flask import Flask
 
app = Flask(__name__)

 #default Api Route

@app.route("/api")
def members():
    return { "message":"Python Server testing"}


if __name__=="__main__":
    app.run(debug=True)