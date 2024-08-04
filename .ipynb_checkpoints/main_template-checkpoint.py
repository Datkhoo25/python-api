from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

class UppercaseText(Resource):

    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the data in uppercase, yes.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be converted to uppercase
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The text in uppercase
        """
        text = request.args.get('text')

        return jsonify({"text": text.upper()})

class TextManipulation(Resource):

    def get(self):
        """
        This method responds to the GET request for text manipulation.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be manipulated
            - name: duplication_factor
              in: query
              type: integer
              required: false
              description: Number of times to repeat the text
            - name: capitalization
              in: query
              type: string
              enum: [UPPER, LOWER, None]
              required: false
              description: Capitalization option (UPPER, LOWER, or None)
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            manipulated_text:
                                type: string
                                description: The manipulated text
        """
        text = request.args.get('text')
        duplication_factor = int(request.args.get('duplication_factor', 1))
        capitalization = request.args.get('capitalization', 'None')

        # Manipulate the text based on duplication factor and capitalization
        manipulated_text = text * duplication_factor
        if capitalization == 'UPPER':
            manipulated_text = manipulated_text.upper()
        elif capitalization == 'LOWER':
            manipulated_text = manipulated_text.lower()

        return jsonify({"manipulated_text": manipulated_text})

api.add_resource(TextManipulation, "/manipulate") # "/manipulate" is the extention
api.add_resource(UppercaseText, "/uppercase")  #"/uppercase" is the extention

if __name__ == "__main__":
    app.run(debug=True)