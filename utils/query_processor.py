import pandas as pd
import numpy as np
from groq import Groq
import re
import sys
from io import StringIO

class QueryProcessor:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
    def generate_pandas_code(self, user_query, df_info):
        
          
        
        prompt = f"""
You are a Python pandas expert. Convert the user's natural language query into executable pandas code.

Dataset Information:
- Dataset variable name: 'df'
- Columns: {df_info['columns']}
- Data types: {df_info['dtypes']}
- Sample data: 
{df_info['sample']}

CRITICAL Instructions:
1. DO NOT include any import statements (pandas, numpy, matplotlib, plotly are already available as pd, np, plt, px, go)
2. The 'datetime' column is already parsed as datetime
3. Use ONLY these pre-imported libraries: pd (pandas), np (numpy), plt (matplotlib.pyplot), px (plotly.express), go (plotly.graph_objects)
4. Return ONLY the executable Python code, no explanations or comments
5. Always assign final results to a variable called 'result'
6. For matplotlib plots: create the plot but DON'T call plt.show() - just assign the figure or the data
7. For plotly plots: create the figure and assign it to 'result'
8. For data analysis: assign the final dataframe/series/value to 'result'
9. When user query not relevant to energy dataset then output print statement "Can't Assist! Out of Context"

User Query: "{user_query}"

Generate the pandas code (NO IMPORTS):
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="deepseek-r1-distill-llama-70b",
                temperature=0.1,
                max_tokens=10000
            )
            
            # Extract code from response
            code = response.choices[0].message.content.strip()
            
            #  this removes markdown if present in code )
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].strip()
            
            # Remove any import statements
            code_lines = code.split('\n')
            cleaned_lines = []
            for line in code_lines:
                line = line.strip()
                if not (line.startswith('import ') or line.startswith('from ') or 
                       'import' in line.lower() and ('pandas' in line.lower() or 
                       'matplotlib' in line.lower() or 'plotly' in line.lower() or 
                       'numpy' in line.lower())):
                    cleaned_lines.append(line)
            
            cleaned_code = '\n'.join(cleaned_lines)
            return cleaned_code
            
        except Exception as e:
            return f"Error generating code: {str(e)}"
    
    def execute_code_safely(self, code, df):
        """
        Safely execute the generated pandas code
        """
        # Create a restricted environment
        safe_globals = {
            'df': df,
            'pd': pd,
            'np': np,
            '__builtins__': {
                'len': len, 'str': str, 'int': int, 'float': float,
                'list': list, 'dict': dict, 'tuple': tuple,
                'range': range, 'enumerate': enumerate,
                'zip': zip, 'sum': sum, 'min': min, 'max': max,
                'abs': abs, 'round': round, 'sorted': sorted,
                'type': type, 'isinstance': isinstance,
                'print': print
            }
        }
        
        # Add plotting capabilities
        import matplotlib.pyplot as plt
        import plotly.express as px
        import plotly.graph_objects as go
        import streamlit as st
        safe_globals['plt'] = plt
        safe_globals['px'] = px
        safe_globals['go'] = go
        safe_globals['st'] = st
        
        safe_locals = {}
        
        try:
            # Capture stdout to get any print statements
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            # Execute the code
            exec(code, safe_globals, safe_locals)
            
            # Restore stdout
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            # Get the result
            result = safe_locals.get('result', None)
            
            return {
                'success': True,
                'result': result,
                'output': output,
                'locals': safe_locals
            }
            
        except Exception as e:
            sys.stdout = old_stdout
            return {
                'success': False,
                'error': str(e),
                'result': None,
                'output': None
            }
    
    def get_dataset_info(self, df):
        """
        Extract dataset information for the prompt
        """
        return {
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'shape': df.shape,
            'sample': df.head(3).to_string()
        }