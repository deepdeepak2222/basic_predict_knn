from flask import Flask, request, jsonify
from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization")


app = Flask(__name__)


def generate_summary(book_content):
    summary = summarizer(book_content, max_length=50, min_length=4, do_sample=False)
    return summary[0]['summary_text']


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
