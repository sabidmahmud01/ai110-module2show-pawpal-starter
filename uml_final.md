# PawPal+ — Final UML Class Diagram

```mermaid
classDiagram
    class Pet {
        +str name
        +str species
        +int age
        +list~str~ special_needs
        +list~Task~ tasks
        +get_info() str
        +add_task(task: Task) None
        +get_tasks() list~Task~
    }

    class Task {
        +str description
        +int time
        +str frequency
        +str scheduled_time
        +date due_date
        +bool completed
        +mark_complete() Task
        +to_dict() dict
    }

    class Owner {
        +str name
        +int time_available
        +dict preferences
        +list~Pet~ pets
        +add_pet(pet: Pet) None
        +get_all_tasks() list~Task~
        +get_available_time() int
        +update_preferences(key, value) None
    }

    class Scheduler {
        +Owner owner
        +list~Task~ tasks
        +list~Task~ scheduled_plan
        +add_task(task: Task, pet: Pet) None
        +remove_task(description: str, pet: Pet) None
        +mark_task_complete(description: str, pet: Pet) None
        +sort_by_time() list~Task~
        +filter_tasks(completed, pet_name) list~Task~
        +detect_conflicts() list~str~
        +generate_plan() list~Task~
        +explain_plan() str
        -_filter_by_time(tasks) list~Task~
        -_sort_by_priority(tasks) list~Task~
    }

    Owner "1" --> "1..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler "1" --> "1" Owner : manages
    Scheduler "1" ..> "0..*" Task : schedules
```

## Relationship notes

- `Owner` owns one or more `Pet` objects. Each `Pet` maintains its own task list.
- `Scheduler` holds a reference to `Owner` and reads all tasks through `owner.get_all_tasks()`.
- `Task.mark_complete()` returns a new `Task` instance (the next recurrence) rather than mutating global state, keeping the method self-contained.
- `Scheduler.mark_task_complete()` is the coordinator that calls `Task.mark_complete()` and re-queues the result onto the correct `Pet`.
