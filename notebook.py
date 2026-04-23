# /// script
# dependencies = [
#     "marimo",
#     "llama-cpp-python",
#     "openai",
#     "pydantic-ai",
#     "nbformat",
# ]
# requires-python = ">=3.12"
# ///

import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def display_status():
    return


@app.cell
def _():
     # avec différentes couleurs et tailles de la lettre H (modifiez le nombre dans les parenthèses pour obtenir une autre taille)


    def hello_world(nombre):  
        for i in range(nombre):
            print("Hello World")
    def main():
        hello_world(2)
    if __name__=="__main__":main()

    # How to use python code inside a jupyter notebook?

    # To run Python code inside a Jupyter Notebook, you need to follow these steps:

    #    1. Install Jupyter Notebook: You can install it by running the command `pip install jupyter` in your terminal or command prompt.
    #    2. Launch Jupyter Notebook: Once installed, you can launch Jupyter Notebook by typing `jupyter notebook` in your terminal or command prompt. This will open a new window with the Jupyter Notebook interface.
    #    3. Create a new notebook: In the Jupyter Notebook interface, click on "New" in the top right corner and select "Python 3 (or the version you have installed)" to create a new notebook.

    # Now you can write and run Python code inside the notebook by creating cells and executing them. To do this, simply type your code in a cell and click the "Run" button or press Shift+Enter. The output will be displayed below the cell.
    return


if __name__ == "__main__":
    app.run()
