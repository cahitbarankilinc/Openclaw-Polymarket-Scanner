import unittest
from src.todo_stats import summarize_tasks
from src.formatter import render_summary


class MediumBenchmarkTests(unittest.TestCase):
    def test_empty(self):
        expected = {
            "total": 0,
            "by_status": {"todo": 0, "in_progress": 0, "done": 0},
            "average_priority": 0.0,
            "top_tags": [],
            "completion_rate": 0.0,
        }
        self.assertEqual(summarize_tasks([]), expected)

    def test_summary_stats(self):
        tasks = [
            {"title": "A", "status": "todo", "priority": 3, "tags": ["API", "backend"]},
            {"title": "B", "status": "done", "priority": 5, "tags": ["api", "urgent", "api"]},
            {"title": "C", "status": "in_progress", "priority": 2, "tags": ["frontend"]},
            {"title": "D", "status": "done", "priority": 4, "tags": ["backend", "Bug"]},
        ]
        self.assertEqual(summarize_tasks(tasks), {
            "total": 4,
            "by_status": {"todo": 1, "in_progress": 1, "done": 2},
            "average_priority": 3.5,
            "top_tags": ["api", "backend", "bug"],
            "completion_rate": 50.0,
        })

    def test_invalid_tasks_are_ignored(self):
        tasks = [
            {"title": "A", "status": "todo", "priority": 3, "tags": ["x"]},
            {"title": "B", "status": "bad", "priority": 5, "tags": ["y"]},
            {"title": "C", "status": "done", "priority": 9, "tags": ["z"]},
            {"title": "D", "status": "done", "priority": 4, "tags": ["x", "x", "Y"]},
        ]
        self.assertEqual(summarize_tasks(tasks), {
            "total": 2,
            "by_status": {"todo": 1, "in_progress": 0, "done": 1},
            "average_priority": 3.5,
            "top_tags": ["x", "y"],
            "completion_rate": 50.0,
        })

    def test_render_summary(self):
        tasks = [
            {"title": "A", "status": "todo", "priority": 3, "tags": ["API", "backend"]},
            {"title": "B", "status": "done", "priority": 5, "tags": ["api", "urgent", "api"]},
            {"title": "C", "status": "in_progress", "priority": 2, "tags": ["frontend"]},
            {"title": "D", "status": "done", "priority": 4, "tags": ["backend", "Bug"]},
        ]
        expected = "\n".join([
            "Total: 4",
            "Todo: 1",
            "In Progress: 1",
            "Done: 2",
            "Avg Priority: 3.5",
            "Completion Rate: 50.0%",
            "Top Tags: api, backend, bug",
        ])
        self.assertEqual(render_summary(tasks), expected)

    def test_render_summary_no_tags(self):
        tasks = [
            {"title": "A", "status": "todo", "priority": 1, "tags": []},
        ]
        expected = "\n".join([
            "Total: 1",
            "Todo: 1",
            "In Progress: 0",
            "Done: 0",
            "Avg Priority: 1.0",
            "Completion Rate: 0.0%",
            "Top Tags: -",
        ])
        self.assertEqual(render_summary(tasks), expected)


if __name__ == "__main__":
    unittest.main()
