import json

try:
    with open('data.json', 'r') as file:
        task_dict = json.load(file)
    print("File data =", type(task_dict))
    
except FileNotFoundError:
    task_dict = []
    print("Error: The file 'data.json' was not found.")

# helper functions
def random_id_generator(Xn):
    c = 19
    list_of_num = []
    for a in range(5):  
        result = (a*Xn+c) % 7
        list_of_num.append(result)

    number = int(''.join(str(x) for x in list_of_num))
    return number

def finding_task(id):
    for i in range(len(task_dict)):
        if id == task_dict[i]["id"]:
            index = i
            break
        else:
            index = -1
    return index
            

class Task:
    def display_tasks(self):
        print(
            f'''
            {'='*60}
            Id{" "*10} Task{" "*10}Status
            {'='*60}
            '''
        )
        for i in range(len(task_dict)):
            if task_dict[i]["status"] == 0:
                show = "Not Done"
            else:
                show = "Done"
            print(
                f'''
            {task_dict[i]["id"]}{" "*9} {task_dict[i]["task"]}{" "*9}{show}
                '''
            )

    def add_task(self,task_name,id):
        generate_id = random_id_generator(id)
        task = {
            "id":generate_id,
            "task":task_name,
            "status":0
        }
        task_dict.append(task)
        print("Task added successfully!")

    def edit_task(self):
        print('''
        What do you want to edit?
              1. Task
              2. Status
            choose between 1 or 2.
        ''')
        userChoice = int(input("Choice: "))
        if userChoice != 1 and userChoice != 2:
            print("Invalid choice. Try again!")
            return
        id = int(input("Enter the id of the task you want to edit: "))
        id_index = finding_task(id)

        if id_index == -1:
            print("Couldn't find the id.")
            return
        
        if userChoice == 1:
            task_name = input("Enter the new task name: ")
            temp = task_dict[id_index]["task"]
            task_dict[id_index]["task"] = task_name
            print(f"{temp} has been changed to {task_name}")
        elif userChoice == 2:
            print(
                '''
                Change the status.
                0. Haven't done yet
                1. Done
            '''
            )
            status = int(input("Enter your choice: "))
            if status != 0 and status != 1:
                print("Invalid status update.")
            temp = task_dict[id_index]["status"]
            task_dict[id_index]["status"] = status
            print(f"Status {temp} has been changed to {status}")

    def delete_task(self):
        id = int(input("Enter the id of the task you want to delete: "))
        id_index = finding_task(id)
        task_dict[id_index].clear()
        task_dict.remove({})
    
task = Task()

# task_dict.append(task.add_task("test2",2))
choice = 1
seed = 1
while choice !=0:
    print(
        '''
        Welcome to your CLI Task Manager. What do you want to do today?
        1. Display all your tasks.
        2. Add a new task.
        3. Edit an existing task.
        4. Delete a task
        0. Quit the program
        '''
    )
    answer = int(input("Enter your choice: "))
    if answer == 0:
        choice = 0
        print("Quiting program")
        break
    if answer == 1:
        task.display_tasks()
    elif answer == 2:
        new_task = input("Task: ")
        task.add_task(new_task,seed)
        seed+=1
    elif answer == 3:
        task.edit_task()
    elif answer == 4:
        task.delete_task()
    else:
        print("Invalid choice")


with open("data.json", "w") as final:
    json.dump(task_dict, final, indent=2, default=lambda x: list(x) if isinstance(x, tuple) else str(x))

print("Data written to data.json")