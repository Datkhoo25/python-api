from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
import book_review

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

br= book_review.Book_review()


class UppercaseText(Resource):
    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the data in uppercase.
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
    
class AllReviews(Resource):
    def get(self):
        """
        This method responds to the GET request for the list of book reviews.
        ---
        tags:
        - Book Reviews Here
        parameters:
            - name: sort
              in: query
              type: string
              enum: [ASC, DESC]
              required: false
              description: Sort order for reviews (ASC or DESC)
            - name: max_records
              in: query
              type: integer
              required: false
              description: Maximum number of records to return
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: array
                        items:
                            type: object
                            properties:
                                book_title:
                                    type: string
                                    description: The title of the book
                                rating:
                                    type: integer
                                    description: The rating of the book
                                book_notes:
                                    type: string
                                    description: The review of the book
        """
        sort = request.args.get('sort', default=None)
        max_records = int(request.args.get('max_records', default=10))

        # Check for valid sort parameter
        if sort and sort.lower() not in ["asc", "desc"]:
            return {"error": "Invalid sort value"}, 400

        # Sort the book reviews if sort parameter is provided
        if sort =="ASC":
            print(sort)
            print(max_records)
            book_review = br.get_book_rating(sort=sort, max_records=max_records)
        elif sort =="DESC":
            print(sort)
            print(max_records)
            book_review = br.get_book_rating(sort=sort, max_records=max_records)
        else: 
            book_review = br.get_book_rating(max_records=max_records)


        return book_review, 200




    
class AddRecord(Resource):
    def post(self):
        """
        This method responds to the POST request for adding a new record to the DB table.
        ---
        tags:
        - Book Reviews
        parameters:
            - in: body
              name: body
              required: true
              schema:
                id: BookReview
                required:
                  - book
                  - rating
                properties:
                  book:
                    type: string
                    description: the name of the book
                  rating:
                    type: integer
                    description: the rating of the book (1-10)
                  notes:
                    type: string
                    description: optional notes about the book
        responses:
            200:
                description: A successful POST request
            400: 
                description: Bad request, missing 'Book' or 'Book_rating' in the request body
        """

        data = request.json
        print(data)

        # Check if 'Book' and 'Book_rating' are present in the request body
        if not data:
            return {"error": "Reuest body must be in json format"}, 400
        
        # Extract fields from request data
        book = data.get('book')  # Corrected to use parentheses. # Must be a ( ) instead of a []
        review = data.get('rating')  # Corrected to use parentheses
        notes = data.get('notes', '')  # Optional field with default value ''

        if not book or not review:
            return {"error": "Both 'book' and 'rating' are required fields"}, 400
        
        # Call the add_book_rating function to add the record to the DB table
        br.add_book_rating(book, review, notes)

        return {"message": "Record added successfully"}, 200



api.add_resource(AllReviews, "/all_reviews")
api.add_resource(AddRecord, "/add-record")
api.add_resource(UppercaseText, "/uppercase")

if __name__ == "__main__":
    app.run(debug=True)