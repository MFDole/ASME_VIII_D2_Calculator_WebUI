#programme for determinining whether and indication is acceptable or rejectable with height/length using fracture mechanics analysis data 
#using ASME VIII Div 2. In lieu of RT inspection. Code is work in progress.
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Data from ASME VIII, Div2. Table for PAUT fracture mechanics comparison using linear interpolation.
data = {
    0.0: (0.031, 0.034),
    0.05: (0.033, 0.038),
    0.1: (0.036, 0.043),
    0.15: (0.041, 0.054),
    0.2: (0.047, 0.066),
    0.25: (0.055, 0.078),
    0.3: (0.064, 0.09),
    0.35: (0.074, 0.103),
    0.4: (0.083, 0.116),
    0.45: (0.085, 0.129),
    0.5: (0.087, 0.143)
}
#linear interpolation - floats due to to nature of classification method
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        flaw_type = request.form['flaw_type']
        a = float(request.form['a'])
        l = float(request.form['l'])
        t = float(request.form['t'])
        a_l = a / l
        a_t = a / t
        closest_a_l = min(data.keys(), key=lambda x: abs(x - a_l))
        if flaw_type == "Surface":
            threshold = data[closest_a_l][0]
        else:  # Subsurface
            threshold = data[closest_a_l][1]
        if a_t > threshold:
            result = "Rejectable"
        else:
            result = "Acceptable"
        return jsonify(result=result)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
