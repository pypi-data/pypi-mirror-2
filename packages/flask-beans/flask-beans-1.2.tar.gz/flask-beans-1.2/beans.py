from flask import Flask, jsonify
from redis import Redis

app = Flask(__name__)
db = Redis(db='beans')

@app.route('/incr/<key>/<member>/')
def incr(key, member):
    return jsonify(count = db.zincrby(key, member))

@app.route('/count/<key>/<member>/')
def count(key, member):
    return jsonify(count = db.zscore(key, member))

@app.route('/reset/<key>/<member>/')
def reset(key, member):
    return jsonify(count = db.zrem(key, member))

@app.route('/list/<key>/')
def list(key):
    return jsonify(counts = db.zrange(key, 0, -1, withscores=True))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
