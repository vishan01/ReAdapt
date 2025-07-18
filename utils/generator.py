import subprocess
import tempfile
import os

def compile_latex_to_pdf(latex_code:str)->tuple:
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "resume.tex")
        pdf_path = os.path.join(tmpdir, "resume.pdf")

        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)

        # Compile LaTeX to PDF
        try:            
            os.system(f"pdflatex -interaction=nonstopmode --output-directory={tmpdir} {tex_path} ")
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            return pdf_bytes, None

        except subprocess.CalledProcessError as e:
            return e, "LaTeX compilation failed. Please check your LaTeX code."
