from flask import Flask 

app = Flask(__name__)

@app.route("/")
def home():
    return '<h1>Hello!</h1>'

@app.route("/<input_string>")
def user(input_string):
    result = modify(input_string)
    return "Hello <br> <h1>" + result + "</h1> <br> this is question 1."

# 
def modify(input_string):
    # Has numbers so return original string without numbers
    if not input_string.isalpha():
        return ''.join([i for i in input_string if not i.isdigit()])

    # Mix of uppercase and lowercase, so capitalize first character
    elif not input_string.isupper() and not input_string.islower():
        return input_string.capitalize()

    # All uppercase so return string in lowercase
    elif input_string.isupper():
        return input_string.lower()
    
    # All lowercase so return string in uppercase
    return input_string.upper()

if __name__ == "__main__":
    app.run(debug=True) 
