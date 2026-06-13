import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Читаем переменные окружения
PORT = int(os.environ.get('APP_PORT', 5000))
PONG_MESSAGE = os.environ.get('PONG_MESSAGE', 'pong')

@app.route('/')
def home():
    return jsonify({
        'service': 'Ping-Pong API',
        'endpoints': {
            '/ping': 'GET - возвращает pong-ответ',
            '/health': 'GET - проверка здоровья',
            '/info': 'GET - информация о сервисе'
        }
    })

@app.route('/ping')
def ping():
    """Главный endpoint: возвращает PONG_MESSAGE"""
    return jsonify({
        'message': PONG_MESSAGE,
        'port': PORT,
        'status': 'ok'
    })

@app.route('/health')
def health():
    """Endpoint для проверки работоспособности"""
    return jsonify({'status': 'healthy'})

@app.route('/info')
def info():
    """Возвращает информацию о сервисе"""
    return jsonify({
        'name': 'ping-pong-service',
        'port': PORT,
        'response': PONG_MESSAGE
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)