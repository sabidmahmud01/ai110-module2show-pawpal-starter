from pawpal_system import Pet, Task, Owner, Scheduler

def main():
    # Create an Owner
    owner = Owner(name="Alice", time_available=120)  # 120 minutes per day

    # Create Pets
    buddy = Pet(name="Buddy", species="dog", age=3, special_needs=["needs daily walks"])
    whiskers = Pet(name="Whiskers", species="cat", age=2)

    # Add pets to owner
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # Create Tasks
    walk_task = Task(description="Walk Buddy", time=30, frequency="daily")
    feed_buddy_task = Task(description="Feed Buddy", time=10, frequency="daily")
    feed_whiskers_task = Task(description="Feed Whiskers", time=5, frequency="daily")
    groom_whiskers_task = Task(description="Groom Whiskers", time=20, frequency="weekly")

    # Add tasks to pets
    buddy.add_task(walk_task)
    buddy.add_task(feed_buddy_task)
    whiskers.add_task(feed_whiskers_task)
    whiskers.add_task(groom_whiskers_task)

    # Create Scheduler
    scheduler = Scheduler(owner)

    # Generate the plan
    plan = scheduler.generate_plan()

    # Print Today's Schedule
    print("Today's Schedule:")
    print(scheduler.explain_plan())

if __name__ == "__main__":
    main()
