from rest_api.app import create_app

api_app = create_app()
api_app.run(host='0.0.0.0', port=5000)


