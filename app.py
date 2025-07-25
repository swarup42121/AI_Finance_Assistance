from flask import Flask, request, jsonify, render_template_string,render_template
import google.generativeai as genai

# Configure Generative AI API
genai.configure(api_key="AIzaSyCE0ZADlWlQ5iiw-CrejlTo4EH72rcI_Mc")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize Flask app
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("user_input.html")

def clean_res(resp):
    clean_response = resp[7:]
    clean_response = clean_response[:-4]
    return clean_response
@app.route("/process", methods=["POST"])
def process():
    print("\n\nin PRocess function :\n\n ")
    try:
        # Get data from the frontend
        amount = request.form.get("amount")
        risk = request.form.get("risk")
        duration = request.form.get("duration")

        # Construct a message for the AI model
        message = f"Investment query: Amount - {amount}, Risk - {risk}, Duration - {duration}. Return the response in HTML Tags only and add the bootstrap classes to make it look nice. Strictly return table tags only as i have head and body tags already."

        # Log the received data for debugging
        app.logger.info(f"Received data: Amount={amount}, Risk={risk}, Duration={duration}")

        # Generate response using Generative AI
        response = model.generate_content(message)

        # Log the response for debugging
        app.logger.info(f"AI Response: {response.text}")
        cleaned_resp = clean_res(response.text)
        print("Going to render ai_roadmap :")
        return render_template("ai_roadmap.html",response = cleaned_resp)
        # Return the response to the frontend
        return jsonify({"response": response.text})
    except Exception as e:
        # Log error for debugging
        print("In exception block : ")
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
