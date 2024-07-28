from flask import Flask, request, jsonify
from surprise import Dataset, Reader, KNNBasic, accuracy
from surprise.model_selection import train_test_split
import numpy as np
import ssl

# Bypass SSL verification (not recommended for production)
ssl._create_default_https_context = ssl._create_unverified_context

# Initialize Flask application
app = Flask(__name__)


# Function to check and download the dataset if it's not available
def load_ml_100k():
    try:
        data = Dataset.load_builtin('ml-100k', prompt=False)
    except Exception as e:
        print("Dataset ml-100k could not be found. Downloading now...")
        from surprise import Dataset
        data = Dataset.load_builtin('ml-100k', prompt=False)
    return data


# Load the Movielens-100k dataset
data = load_ml_100k()

# Split the data into training and testing sets
trainset, testset = train_test_split(data, test_size=0.2)

# Use the KNNBasic algorithm
algo = KNNBasic()

# Train the algorithm on the training set
algo.fit(trainset)

# Predict ratings for the test set
predictions = algo.test(testset)

# Compute and print the RMSE
accuracy.rmse(predictions)


# Function to get top N recommendations for each user
def get_top_n_recommendations(predictions, n=10):
    top_n = {}
    for uid, iid, true_r, est, _ in predictions:
        if uid not in top_n:
            top_n[uid] = []
        top_n[uid].append((iid, est))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


# Get top 10 recommendations for all users
top_n_recommendations = get_top_n_recommendations(predictions, n=10)


# Endpoint to get top n recommended items
@app.route('/get_top_n_recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    user_recommendations = top_n_recommendations.get(user_id, [])
    return jsonify(user_recommendations)


# Endpoint to do partial training of the model
@app.route('/partial_train', methods=['POST'])
def partial_train():
    # Parse the input data
    data = request.get_json()
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    rating = data.get('rating')

    # Create a new Dataset from the input data
    new_data = np.array([[user_id, book_id, rating]])
    reader = Reader(rating_scale=(1, 5))
    new_dataset = Dataset.load_from_df(new_data, reader)

    # Update the trainset with new data
    global trainset
    trainset.build_full_trainset().add_testset(new_dataset.build_full_trainset().build_testset())

    # Train the algorithm with the new data
    algo.fit(trainset)

    # Predict ratings for the updated trainset
    new_predictions = algo.test(trainset.build_testset())

    # Update the top_n_recommendations
    global top_n_recommendations
    top_n_recommendations = get_top_n_recommendations(new_predictions, n=10)

    return jsonify({"message": "Model updated successfully"}), 200


if __name__ == '__main__':
    # Run webserver using flask
    app.run(debug=True, port=8555)
