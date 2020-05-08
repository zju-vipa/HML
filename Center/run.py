from app import app

app.run(
    host='0.0.0.0',
    port=8022,
    debug=True,
    # threaded=True,  # 开启 flask 多线程，不然无法顾及辅助函数
)

print("app has run")  # this line can't be reach
