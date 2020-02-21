import os
import io
import tempfile
import subprocess

def GeneratePNGFromLaTeX(latex_expression):
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = os.path.join(tmpdir, 'expression.tex')
        with open(tex_file, 'w') as output:
            output.write('''\
\\documentclass[varwidth,12pt]{standalone}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\begin{document}
\\[
''')
            output.write(latex_expression)
            output.write('''\
\\]
\\end{document}
''')
        result = subprocess.run([
                "latex", "-halt-on-error", "-interaction=nonstopmode", "expression.tex"
            ], cwd=tmpdir)
        if result.returncode != 0:
            return None
        result = subprocess.run([
                "dvipng", 
                "-D", "250", 
                "-T", "tight", 
                "-z", "9",
                #"-bg", "Transparent", 
                "-o", "expression.png", 
                "expression.dvi"
            ], cwd=tmpdir)
        if result.returncode != 0:
            return None
        return io.BytesIO(open(os.path.join(tmpdir, "expression.png"), "rb").read())

__all__ = [
    'GeneratePNGFromLaTeX'
]