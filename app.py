from flask import Flask, request, jsonify

from summarizer import generate_summary
app = Flask(__name__)


@app.route('/book/summary', methods=['POST'])
def get_summary():
    # Fetch the book content from the database or in-memory storage
    # This is a placeholder. Actual implementation will depend on your database or storage choice.
    data = request.get_json()
    book_content = data.get('content')
    summary = generate_summary(book_content)
    return jsonify({"summary": summary})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8555)
