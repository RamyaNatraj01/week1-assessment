# Week 1 Assessment — Python & Data Engineering

## Setup

1. Install Python 3 and Visual Studio Code with the Jupyter extension.
2. Open a terminal in the project root and create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the project dependencies and notebook kernel:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python -m pip install ipykernel
   ```

4. Open [notebooks/analysis.ipynb](notebooks/analysis.ipynb) in VS Code, select the `.venv` Python kernel, and run all cells. The notebook reads its input files from `data/` and saves charts under `reports/charts/`.
5. To export the notebook to Python:

   ```powershell
   jupyter nbconvert --to script .\notebooks\analysis.ipynb --output-dir .\notebooks
   ```

6. For Task 2 API work, keep `API_KEY` in your local `.env` file. Do not commit `.env` or share its contents.

## Findings

1. The source dataset contains 8 employees across Sales, HR, IT, and Finance.
2. IT has the largest headcount with 3 employees; Sales and HR have 2 each, and Finance has 1.
3. Finance has the highest average and maximum salary at 90,000.
4. After removing the duplicate row, the two missing salaries are filled with the median of 64,000.
5. Legal is listed in the department data but has no employees.
