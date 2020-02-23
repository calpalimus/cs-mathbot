from matplotlib import pyplot as plt
import io

def Plot2D(points, x_label, y_label, title):
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = [
        r'\usepackage{amsmath}',
        r'\usepackage{amsfonts}'
    ]
    x_array = [point[0] for point in points]
    y_array = [point[1] for point in points]
    fig,axis = plt.subplots(1,1)
    axis.plot(x_array, y_array, '-')
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.set_title(title)
    result = io.BytesIO()
    fig.savefig(result, format='png')
    result.seek(0,0)
    return result

__all__ = [
    'Plot2D',
]