from app import app

app.run(
    host='0.0.0.0',
    port=8031,
    debug=True,
    threaded=True
)
