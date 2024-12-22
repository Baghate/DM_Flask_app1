from flask import Flask, request, render_template, jsonify
import requests
from config import Config

app = Flask(__name__)

# Route for the root path
@app.route("/")
def index():
    return "The correct route is '/retrieve_wikidata/(id)'"

# Route to interact with the application
@app.route('/retrieve_wikidata/<wikidata_id>')
def retrieve_wikidata(wikidata_id):
    """
    Flask route to fetch information from Wikidata.
    :param wikidata_id: Wikidata identifier of the entity to query.
    :return: HTML page with results or an error message.
    """
    # URL for the Wikidata API
    wikidata_api_url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
    
    try:
        # Sending the request to the Wikidata API
        api_response = requests.get(wikidata_api_url)
        
        # Extracting metadata from the response
        http_status_code = api_response.status_code
        response_content_type = api_response.headers.get("Content-Type", "unknown")
        
        if http_status_code == 200 and "application/json" in response_content_type:
            # Decoding the JSON data
            json_response_data = api_response.json()

            # Checking if the requested entity exists in the response
            if wikidata_id in json_response_data.get("entities", {}):
                entity_details = json_response_data["entities"][wikidata_id]
            else:
                entity_details = None
        else:
            # Handling unexpected responses
            json_response_data = None
            entity_details = None

        # Preparing data for rendering the HTML template
        return render_template(
            "template.html",
            status_code=http_status_code,
            content_type=response_content_type,
            entity_data=entity_details,
            error_message=None if entity_details else "No data found for the given identifier.",
        )
    
    except requests.RequestException as error:
        # Handling connection errors
        return render_template(
            "template.html",
            status_code=None,
            content_type=None,
            entity_data=None,
            error_message=f"Error during the request: {str(error)}"
        )

if __name__ == "__main__":
    app.run(debug=True)