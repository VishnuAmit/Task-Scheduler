import pytest
from unittest.mock import patch
from task_scheduler import topological_sort, execute_tasks, run_task, concurrent_execute_tasks

# Test 1: Verifying the correct order of it if dependencies exist.
def test_topological_sort_basic():
    tasks = ["A", "B", "C", "D"]
    dependencies = [("B", "A"), ("B", "D"), ("C", "D")]
    expected = ["B", "C", "A", "D"]
    result = topological_sort(tasks, dependencies)
    assert result == expected

# Test 2:  If it has no dependencies, it should return the same or in any order as it doesnt matter
def test_topological_sort_no_dependencies():
    tasks = ["A", "B", "C"]
    dependencies = []
    result = topological_sort(tasks, dependencies)
    assert set(result) == set(tasks) 

# Test 3: Raise exception if cycle exists
def test_topological_sort_cycle_detection():
    tasks = ["A", "B", "C"]
    dependencies = [("A", "B"), ("B", "C"), ("C", "A")]
    with pytest.raises(Exception) as exc_info:
        topological_sort(tasks, dependencies)
    assert "Cycle detected" in str(exc_info.value)

# Test 4: all tasks execute within time period
@patch('task_scheduler.sleep') 
@patch('task_scheduler.randint')
def test_execute_tasks_successful(mock_randint, mock_sleep):
    mock_randint.return_value = 2
    mock_sleep.return_value = None
    
    tasks = ["A", "B", "C"]
    dependencies = [("A", "B"), ("B", "C")]
    
    with patch('builtins.print') as mock_print:
        execute_tasks(tasks, dependencies, timeout=10)
        
    mock_print_calls = [str(call) for call in mock_print.call_args_list]
    assert any("Successful Tasks: ['A', 'B', 'C']" in call for call in mock_print_calls)

# Test 5: tasks are cancelled if it exceeds the timeout
@patch('task_scheduler.sleep')
@patch('task_scheduler.randint')
def test_execute_tasks_timeout(mock_randint, mock_sleep):
    mock_randint.return_value = 6 
    mock_sleep.return_value = None
    
    tasks = ["A", "B", "C"]
    dependencies = [("A", "B"), ("B", "C")]
    
    with patch('builtins.print') as mock_print:
        execute_tasks(tasks, dependencies, timeout=5)
        
    mock_print_calls = [str(call) for call in mock_print.call_args_list]
    assert any("cannot finish within the timeout" in call for call in mock_print_calls)

# Test 6: returns end time of a task.
def test_run_task():
    task_name = "Test Task"
    start_time = 0.0
    execution_time = 1
    
    with patch('task_scheduler.sleep') as mock_sleep:
        mock_sleep.return_value = None
        with patch('builtins.print') as mock_print:
            end_time = run_task(task_name, start_time, execution_time)
            
    assert end_time == start_time + execution_time

# Test 7: No tasks
def test_topological_sort_no_tasks():
    tasks = []
    dependencies = []
    result = topological_sort(tasks, dependencies)
    assert result == []

# Test 8: single task with no dependencies
def test_topological_sort_single_task():
    tasks = ["A"]
    dependencies = []
    result = topological_sort(tasks, dependencies)
    assert result == ["A"]

# Test 9: with multiple dependencies
def test_topological_sort_multiple_dependencies():
    tasks = ["A", "B", "C", "D", "E"]
    dependencies = [("B", "A"), ("C", "B"), ("D", "A"), ("D", "C"), ("E", "D")]
    expected = ["E", "D", "C", "B", "A"]
    result = topological_sort(tasks, dependencies)
    assert result == expected

## FOR CONCURRENT METHOD
# Test 1: basic test 
@patch('task_scheduler.sleep')
@patch('task_scheduler.randint')
def test_concurrent_execute_tasks_basic(mock_randint, mock_sleep):
    mock_randint.return_value = 2
    mock_sleep.return_value = None

    tasks = ["A", "B", "C"]
    dependencies = [("B", "A"), ("C", "B")]

    with patch('builtins.print') as mock_print:
        concurrent_execute_tasks(tasks, dependencies, max_workers=2)

    # Check if the tasks were printed
    mock_print_calls = [str(call) for call in mock_print.call_args_list]
    assert any("Starting Task" in call for call in mock_print_calls)
    assert any("Completed Task" in call for call in mock_print_calls)

# Test 2: No tasks
def test_concurrent_execute_tasks_no_tasks():
    tasks = []
    dependencies = []
    with patch('builtins.print') as mock_print:
        concurrent_execute_tasks(tasks, dependencies, max_workers=2)
    assert any("Successful Tasks: []" in str(call) for call in mock_print.call_args_list)

# Test 3: circular dependency
def test_concurrent_execute_tasks_circular_dependency():
    tasks = ["A", "B", "C"]
    dependencies = [("A", "B"), ("B", "C"), ("C", "A")]
    with patch('builtins.print') as mock_print:
        concurrent_execute_tasks(tasks, dependencies, max_workers=2)
    assert any("Error: Cycle detected" in str(call) for call in mock_print.call_args_list)

if __name__ == '__main__':
    pytest.main(['-v'])