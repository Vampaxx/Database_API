    
## ------------------------------------Rough work (not for this case)---------------------------------------------------------##

@app.route("/unprotected")
def unprotected():
    return jsonify({"message":"anyone can view this"})

@app.route("/protected")
@token_required
def protected():
    return jsonify({"message":"This is available for prople with valid tokens"})

