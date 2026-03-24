from collections import Counter
from typing import List, Dict, Any

def summarize_tasks(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarize task data with stats.
    
    Valid statuses: 'todo', 'in_progress', 'done'
    Invalid tasks (bad status) are ignored from counts.
    """
    valid_statuses = {'todo', 'in_progress', 'done'}