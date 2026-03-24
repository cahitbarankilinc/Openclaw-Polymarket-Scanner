from .todo_stats import summarize_tasks


def render_summary(tasks):
    stats = summarize_tasks(tasks)
    
    # Format top tags
    if stats["top_tags"]:
        top_tags_str = ", ".join(stats["top_tags"])
    else:
        top_tags_str = "-"
    
    # Create the formatted output
    lines = [
        f"Total: {stats['total']}",
        f"Todo: {stats['by_status']['todo']}",
        f"In Progress: {stats['by_status']['in_progress']}",
        f"Done: {stats['by_status']['done']}",
        f"Avg Priority: {stats['average_priority']:.1f}",
        f"Completion Rate: {stats['completion_rate']:.1f}%",
        f"Top Tags: {top_tags_str}",
    ]
    
    return "\n".join(lines)