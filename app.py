from flask import Flask, render_template, request, jsonify
from sympy.parsing.latex import parse_latex
from sympy import symbols, Eq, solve, lambdify, latex
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve_problem():
    plane_latex = request.form.get('plane')
    line_x_latex = request.form.get('line_x')
    line_y_latex = request.form.get('line_y')
    line_z_latex = request.form.get('line_z')

    x, y, z, t = symbols('x y z t')

    try:
        plane_expr = parse_latex(plane_latex.replace('=', '-(') + ')')
        line_x = parse_latex(line_x_latex.split('=')[1])
        line_y = parse_latex(line_y_latex.split('=')[1])
        line_z = parse_latex(line_z_latex.split('=')[1])
    except Exception as e:
        return jsonify({'error': f'Failed to parse input: {e}'})

    plane_sub = plane_expr.subs({x: line_x, y: line_y, z: line_z})
    t_value = solve(Eq(plane_sub, 0), t)
    if not t_value:
        return jsonify({'error': 'No intersection found.'})
    t_value = t_value[0]

    point = (line_x.subs(t, t_value), line_y.subs(t, t_value), line_z.subs(t, t_value))

    steps = [
        '1. Substitute the line parametric equations into the plane equation.',
        f'2. Solve for $t$: {latex(Eq(plane_sub, 0))}',
        f'3. Intersection point is {point}'
    ]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xx, yy = np.meshgrid(range(-5, 6), range(-5, 6))
    plane_lambda = lambdify((x, y), solve(plane_expr, z)[0], 'numpy')
    zz = plane_lambda(xx, yy)
    ax.plot_surface(xx, yy, zz, alpha=0.5)

    t_vals = np.linspace(t_value-5, t_value+5, 50)
    line_x_lambda = lambdify(t, line_x, 'numpy')
    line_y_lambda = lambdify(t, line_y, 'numpy')
    line_z_lambda = lambdify(t, line_z, 'numpy')
    ax.plot(line_x_lambda(t_vals), line_y_lambda(t_vals), line_z_lambda(t_vals), 'r')

    ax.scatter(*point, color='k', s=50)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return jsonify({'steps': steps, 'point': str(point), 'image': img_b64})

if __name__ == '__main__':
    app.run(debug=True)
