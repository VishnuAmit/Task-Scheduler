from time import sleep
from time import time
from collections import deque
from random import randint
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_task(task_name: str, start_time: float, execution_time: int):
    task_start_time = start_time
    task_end_time = task_start_time + execution_time

       # Log of each task... Whenever it runs.
    print(f"\n{'-'*60}")
    print(f"Task: {task_name}")
    print(f"{'='*60}")
    print(f"Start Time: {task_start_time:.2f} seconds")
    print(f"End Time  : {task_end_time:.2f} seconds")
    print(f"Duration  : {execution_time:.2f} seconds")
    print(f"{'-'*60}\n")

    
    # As the task is being executed.
    sleep(execution_time)

    return task_end_time  

# to determine the execution order
def topological_sort(tasks, dependencies):
        # if in-degree is 0
    graph = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}

    for dependency, task in dependencies:
        graph[dependency].append(task)
        in_degree[task] += 1

    # Find tasks with no incoming edges (in-degree = 0)
    queue = deque([task for task in tasks if in_degree[task] == 0])
    order = []

    while queue:
        current = queue.popleft()
        order.append(current)

            # decreasing indegree for neigboring tasks
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    
    # If the order contains all tasks return it
    if len(order) == len(tasks):
        return order
    else:
         raise Exception("Cycle detected in task dependencies and its not a good sign :(")

# # WITHOUT CONCURRENCY... COVERED ALL THE POSSIBILITIES - PASSED EVERYTHING

def execute_tasks(tasks, dependencies, timeout, start_threshold_timeout=0.8):
    try:
           # get the topological order
        execution_order = topological_sort(tasks, dependencies)
        print("Execution Order:", execution_order)
        print("\n" + "-"*40)

        task_execution_times = {task: randint(0, 10) for task in tasks}  # including 0 to get 0 duration as well..

         # Display the task execution times before starting the tasks -- I found this useful as it helped me to think faster about all edge cases and possibilites.
        print("Task Execution Times (before running):")
        for task, exec_time in task_execution_times.items():
            print(f"Task {task}: {exec_time} seconds")
        
        total_execution_time = sum(task_execution_times.values())
        threshold_time = total_execution_time * start_threshold_timeout

        print(f"\nTotal Execution Time: {total_execution_time} seconds")
        print(f"Start Threshold Timeout: {threshold_time:.2f} seconds\n")
        
        current_time = 0 

        # Lists 
        cancelled_tasks = []
        successful_tasks = []
        failed_tasks = []  
        unfinished_tasks = []  

        # Execute tasks in order
        for i, task in enumerate(execution_order):
            execution_time = task_execution_times[task] 
            
            # retry logic for tasks with execution time of 0
            retry_count = 0
            while execution_time == 0 and retry_count < 2:
                print(f"[Retrying] Task '{task}' has execution time 0. Retrying {retry_count + 1}st time.")
                execution_time = 0 
                '''you can also use randint(0,10) here but i hardcorded 0 because its unlikely that we 
                get three 0s in a row. To have something in failed tasks list, i assumed it as 0. If not it will retry and if got a different number, 
                it will get executed''' 
                retry_count += 1
            
            if execution_time == 0:  
                print(f"[Failed] Task '{task}' reached the max limit of 2 and is moved to failed tasks.")
                failed_tasks.append(task)
                continue  

            task_end_time = current_time + execution_time

            # If the task starts at or after the threshold -- cancelled..
            if current_time >= threshold_time:
                print(f"\n[Warning] Task '{task}' exceeds the start threshold and is cancelled.")
                cancelled_tasks.append(task)
                continue 
        
            # if current time is less than timeout, there is a chance you can run a task still..it may finish or may not
            if current_time < timeout:
                if task_end_time > timeout:
                    print(f"\n[Warning] Task '{task}' cannot finish within the timeout and moved on to unfinished list.")
                    unfinished_tasks.append(task)
                    cancelled_tasks.extend(execution_order[i+1:])  
                    break  
            else:
                # else cancel everything.
                print(f"\n[Warning] Task '{task}' starts after the timeout and is cancelled.")
                cancelled_tasks.append(task)
                cancelled_tasks.extend(execution_order[i+1:]) 
                break  

            current_time = run_task(task, current_time, execution_time)
            successful_tasks.append(task)

        print("-"*60)
        print(f"Successful Tasks: {successful_tasks}")
        print(f"Cancelled Tasks: {cancelled_tasks}")
        print(f"Failed Tasks: {failed_tasks}")
        print(f"Unfinished Tasks: {unfinished_tasks}")
        print("-"*60)

    except Exception as e:
        print(f"Error: {e}")

# WITH CONCURRENCY - RUNS GOOD. 
def concurrent_execute_tasks(tasks, dependencies, max_workers):
    try:
        # topological order of tasks
        execution_order = topological_sort(tasks, dependencies)
        print("Execution Order: ", execution_order)
        print("\n" + "-" * 40)

        task_execution_times = {task: randint(1, 10) for task in tasks}  # didnt consider 0 here to keep it simple


        print("Task Execution Times (before running):")
        for task, exec_time in task_execution_times.items():
            print(f"Task {task}: {exec_time} seconds")

        print("\n" + "-" * 40)

        successful_tasks = []
        failed_tasks = []

        # run tasks with simulated execution time
        def task_runner(task):
            exec_time = task_execution_times[task]
            print(f"Starting Task: {task} (Execution Time: {exec_time} seconds)")
            sleep(exec_time)
            print(f"Completed Task: {task}")
            return task

        start_time = time()

     
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # submit tasks to executor
            future_to_task = {executor.submit(task_runner, task): task for task in execution_order}

            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result() 
                    successful_tasks.append(result)
                except Exception as e:
                    print(f"Task {task} failed with error: {e}")
                    failed_tasks.append(task)

        end_time = time()

        print("\n" + "=" * 60)
        print(f"All Tasks Completed in {end_time - start_time:.2f} seconds")
        print(f"Successful Tasks: {successful_tasks}")
        print(f"Failed Tasks: {failed_tasks}")
        print("=" * 60)

    except Exception as e:
        print(f"Error: {e}")

# Example usage 1
tasks = ["A", "B", "C", "D"]
dependencies = [("B", "A"), ("B", "D"), ("C", "D")]

''' More test cases if required to check. '''
# # Example usage 2
# tasks = ["A", "B", "C", "D", "E"]
# dependencies = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]

# # Example usage 3 -- this will raise an exception as there is circular dependency
# tasks = ["A", "B", "C"]
# dependencies = [("A", "B"), ("B", "C"), ("C", "A")] 

# # Example usage 4
# tasks = ["A", "B", "C", "D"]
# dependencies = [("A", "D"), ("B", "D"), ("C", "D")]  # D depends on all other tasks

# # Example usage 5
# tasks = ["A", "B", "C", "D", "E"]
# dependencies = [("B", "A"), ("C", "A"), ("C", "B"), ("D", "C"), ("E", "D")]



# assuming 15 as timeout

# # If you want to have 4 diff lists with timeout and threshold without concurency, uncomment this method.
# execute_tasks(tasks, dependencies, timeout=15, start_threshold_timeout=0.8)

# if you want to run with concurrency ...
tasks_result = concurrent_execute_tasks(tasks, dependencies, 2)
