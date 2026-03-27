import streamlit as st
from pawpal_system import Pet, Task, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "pet" not in st.session_state:
    st.session_state.pet = Pet(name=pet_name, species=species, age=2)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, time_available=120)
    st.session_state.owner.add_pet(st.session_state.pet)

st.markdown("### Tasks")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"])
with col4:
    scheduled_time = st.text_input("Start time (HH:MM)", value="08:00")

if st.button("Add task"):
    new_task = Task(
        description=task_title,
        time=int(duration),
        frequency=frequency,
        scheduled_time=scheduled_time if scheduled_time else None,
    )
    st.session_state.pet.add_task(new_task)

current_tasks = st.session_state.pet.get_tasks()
if current_tasks:
    st.write("Current tasks:")
    st.table([t.to_dict() for t in current_tasks])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=st.session_state.owner)
    plan = scheduler.generate_plan()
    if plan:
        st.success(scheduler.explain_plan())
        sorted_tasks = scheduler.sort_by_time()
        st.write("Tasks sorted by start time:")
        st.table([t.to_dict() for t in sorted_tasks])
    else:
        st.warning("No tasks could be scheduled. Add tasks or increase available time.")

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.error(warning)
