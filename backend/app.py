from flask import Flask, jsonify

app = Flask(__name__)

# 示例电影数据
movie_data = [
    {"title": "毒液", "year": 2021, "rating": 7.5},
    {"title": "毒液2", "year": 2023, "rating": 8.0},
    # 其他电影...
]

@app.route('/')
def hello_world():
    return jsonify(message="Hello, world!")

@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movie_data)

if __name__ == '__main__':
    app.run(debug=True)
