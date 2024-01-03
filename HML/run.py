from app import app

app.run(
    host='0.0.0.0',
    port=8051,
    debug=True,
    threaded=True
)
