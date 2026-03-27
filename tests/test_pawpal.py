import pytest
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