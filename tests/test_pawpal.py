import pytest
from datetime import date, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler


def test_generate_plan_normal_case():
    # Create an owner with limited time
    owner = Owner(name="Alice", time_available=60)  # 60 minutes available

    # Create a pet
    buddy = Pet(name="Buddy", species="dog", age=3)
    owner.add_pet(buddy)

    # Add tasks
    walk_task = Task(description="Walk Buddy", time=30, frequency="daily")
    feed_task = Task(description="Feed Buddy", time=10, frequency="daily")
    groom_task = Task(description="Groom Buddy", time=25, frequency="weekly")  # This should be excluded due to time

    buddy.add_task(walk_task)
    buddy.add_task(feed_task)
    buddy.add_task(groom_task)

    # Create scheduler
    scheduler = Scheduler(owner)

    # Generate plan
    plan = scheduler.generate_plan()

    # Assert that only tasks fitting in time are included
    assert len(plan) == 2  # walk and feed should fit, groom should not
    assert walk_task in plan
    assert feed_task in plan
    assert groom_task not in plan


def test_generate_plan_edge_case_no_tasks():
    # Create an owner
    owner = Owner(name="Alice", time_available=60)

    # Create a pet with no tasks
    buddy = Pet(name="Buddy", species="dog", age=3)
    owner.add_pet(buddy)

    # Create scheduler
    scheduler = Scheduler(owner)

    # Generate plan
    plan = scheduler.generate_plan()

    # Assert that plan is empty
    assert len(plan) == 0


def test_task_completion():
    # Create a task
    task = Task(description="Walk the dog", time=30, frequency="daily")
    
    # Initially, task should not be completed
    assert task.completed == False
    
    # Mark the task as complete
    task.mark_complete()
    
    # Verify that the task is now completed
    assert task.completed == True


def test_task_addition_to_pet():
    # Create a pet
    pet = Pet(name="Buddy", species="dog", age=3)

    # Initially, pet should have no tasks
    assert len(pet.get_tasks()) == 0

    # Create and add a task
    task = Task(description="Walk Buddy", time=30, frequency="daily")
    pet.add_task(task)

    # Verify that the pet now has one task
    assert len(pet.get_tasks()) == 1
    assert task in pet.get_tasks()


# --- Sorting ---

def test_sort_by_time_chronological_order():
    owner = Owner(name="Sam", time_available=200)
    pet = Pet(name="Luna", species="cat", age=1)
    owner.add_pet(pet)
    pet.add_task(Task("Evening feed",  15, "daily",  scheduled_time="18:00"))
    pet.add_task(Task("Morning walk",  30, "daily",  scheduled_time="07:00"))
    pet.add_task(Task("Midday meds",   10, "daily",  scheduled_time="12:00"))

    scheduler = Scheduler(owner)
    result = scheduler.sort_by_time()
    times = [t.scheduled_time for t in result]
    assert times == ["07:00", "12:00", "18:00"]


def test_sort_by_time_untimed_tasks_come_last():
    owner = Owner(name="Sam", time_available=200)
    pet = Pet(name="Luna", species="cat", age=1)
    owner.add_pet(pet)
    pet.add_task(Task("Monthly checkup", 60, "monthly", scheduled_time=None))
    pet.add_task(Task("Morning walk",    30, "daily",   scheduled_time="07:00"))

    scheduler = Scheduler(owner)
    result = scheduler.sort_by_time()
    assert result[0].scheduled_time == "07:00"
    assert result[-1].scheduled_time is None


# --- Recurrence ---

def test_mark_complete_daily_returns_next_day():
    today = date.today()
    task = Task(description="Walk", time=20, frequency="daily", due_date=today)
    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.description == "Walk"
    assert next_task.completed is False


def test_mark_complete_weekly_returns_next_week():
    today = date.today()
    task = Task(description="Grooming", time=45, frequency="weekly", due_date=today)
    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(weeks=1)


def test_mark_complete_monthly_returns_none():
    task = Task(description="Vet visit", time=60, frequency="monthly")
    next_task = task.mark_complete()
    assert next_task is None


def test_mark_task_complete_requeues_recurring(  ):
    owner = Owner(name="Jo", time_available=200)
    pet = Pet(name="Pip", species="dog", age=4)
    owner.add_pet(pet)
    pet.add_task(Task("Morning walk", time=30, frequency="daily"))

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Morning walk", pet)

    tasks = pet.get_tasks()
    assert len(tasks) == 2                     # original + new occurrence
    assert tasks[0].completed is True
    assert tasks[1].completed is False


# --- Conflict Detection ---

def test_detect_conflicts_flags_duplicate_time():
    owner = Owner(name="Alex", time_available=200)
    pet = Pet(name="Rex", species="dog", age=2)
    owner.add_pet(pet)
    pet.add_task(Task("Walk",  30, "daily", scheduled_time="08:00"))
    pet.add_task(Task("Feed",  10, "daily", scheduled_time="08:00"))  # same time

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_detect_conflicts_no_conflict():
    owner = Owner(name="Alex", time_available=200)
    pet = Pet(name="Rex", species="dog", age=2)
    owner.add_pet(pet)
    pet.add_task(Task("Walk",  30, "daily", scheduled_time="07:00"))
    pet.add_task(Task("Feed",  10, "daily", scheduled_time="08:00"))

    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []


def test_detect_conflicts_ignores_untimed_tasks():
    owner = Owner(name="Alex", time_available=200)
    pet = Pet(name="Rex", species="dog", age=2)
    owner.add_pet(pet)
    pet.add_task(Task("Walk", 30, "daily", scheduled_time=None))
    pet.add_task(Task("Feed", 10, "daily", scheduled_time=None))  # both untimed, no conflict

    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []


# --- Filtering ---

def test_filter_tasks_by_completion_status():
    owner = Owner(name="Kim", time_available=200)
    pet = Pet(name="Coco", species="cat", age=3)
    owner.add_pet(pet)
    done   = Task("Brush teeth", 5,  "daily")
    todo   = Task("Evening feed", 10, "daily")
    done.mark_complete()
    pet.add_task(done)
    pet.add_task(todo)

    scheduler = Scheduler(owner)
    incomplete = scheduler.filter_tasks(completed=False)
    assert len(incomplete) == 1
    assert incomplete[0].description == "Evening feed"


def test_filter_tasks_by_pet_name():
    owner = Owner(name="Kim", time_available=200)
    cat = Pet(name="Coco", species="cat", age=3)
    dog = Pet(name="Rex",  species="dog", age=2)
    owner.add_pet(cat)
    owner.add_pet(dog)
    cat.add_task(Task("Cat nap check", 5,  "daily"))
    dog.add_task(Task("Dog walk",      30, "daily"))

    scheduler = Scheduler(owner)
    coco_tasks = scheduler.filter_tasks(pet_name="Coco")
    assert len(coco_tasks) == 1
    assert coco_tasks[0].description == "Cat nap check"