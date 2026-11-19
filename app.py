
from flask import Flask, jsonify, render_template, request

def add_number(numbers, number):
    numbers.append(number)
    return sum(numbers)

def get_total(numbers):
    return sum(numbers)

def create_app():
    app = Flask(__name__)
    numbers = []

    @app.get('/')
    def index():
        return render_template('index.html')

    @app.post('/api/numbers')
    def submit_number():
        data = request.get_json(silent=True)

        if (not isinstance(data, dict)
                or set(data) != {'number'}
                or type(data['number']) is not int):
            return jsonify({'error': 'Ervenytelen szam!'}), 400

        number = data['number']
        total = add_number(numbers, number)

        return jsonify({
            'number': number,
            'sum': total
        }), 201

    @app.get('/api/sum')
    def get_sum():
        return jsonify({'sum': get_total(numbers)}), 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
