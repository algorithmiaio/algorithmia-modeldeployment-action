import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError


class NotebookExecutor:
    def __init__(self, workspace_path, notebook_path, timeout=600):
        self.workspace_path = workspace_path
        self.notebook_full_path = f"{workspace_path}/{notebook_path}"
        self.timeout = timeout

    def run(self):
        if os.path.exists(self.notebook_full_path):
            print(f"Running notebook: {self.notebook_full_path}")
            nb = nbformat.read(open(self.notebook_full_path), as_version=4)
            ep = ExecutePreprocessor(
                timeout=self.timeout, kernel_name="python3", allow_errors=True
            )
            try:
                ep.preprocess(nb, {"metadata": {"path": self.workspace_path}})
                print("Finished executing notebook.")
            except CellExecutionError as e:
                raise Exception(f"An error occurred while executing the notebook: {e}")
        else:
            print(
                f"Notebook file not found at path: {self.notebook_full_path}. Omitting notebook execution step."
            )
