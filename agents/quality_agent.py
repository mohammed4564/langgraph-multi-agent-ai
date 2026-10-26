import json
from pathlib import Path
import pandas as pd
from agents.base import BaseAgent
from agents.registry import register
from core.llm import get_llm

DATA_FILE = Path(__file__).resolve().parents[1] / 'data' / 'customers.csv'

@register
class QualityAgent(BaseAgent):
    name = 'quality'
    description = 'Compute actual CSV missing-value and duplicate checks'
    keywords = ('quality', 'duplicate', 'missing', 'null', 'validate', 'csv')

    def run(self, request: str) -> str:
        df = pd.read_csv(DATA_FILE)
        checks = {
            'rows': len(df),
            'missing_by_column': {k: int(v) for k, v in df.isna().sum().items()},
            'duplicate_rows': int(df.duplicated().sum()),
            'duplicate_customer_ids': int(df.duplicated(subset=['CustomerID']).sum()),
        }
        summary = get_llm().invoke(
            'Explain these measured data quality results concisely. Do not invent metrics.\n'
            + json.dumps(checks)
        )
        return 'Measured results:\n' + json.dumps(checks, indent=2) + '\n\nAnalysis:\n' + str(summary.content)
