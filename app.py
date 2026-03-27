import streamlit as st
from pawpal_system import Pet, Task, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A smart pet care planning assistant that builds a daily schedule for your pet.")

st.divider()

# --- Owner & Pet Setup ---
st.subheader("Owner & Pet")
col_a, col_b = st.columns(2)
with col_a:
    owner_name = st.text_input("Owner name", value="Jordan")
    time_available = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=120)
with col_b:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])

if "pet" not in st.session_state:
    st.session_state.pet = Pet(name=pet_name, species=species, age=2)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, time_available=int(time_available))
    st.session_state.owner.add_pet(st.session_state.pet)

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")
col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task description", value="Morning walk")
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
    st.success(f"Task '{task_title}' added for {st.session_state.pet.name}.")

st.divider()

# --- Current Tasks ---
st.subheader(f"Tasks for {st.session_state.pet.name}")
current_tasks = st.session_state.pet.get_tasks()
if current_tasks:
    tab_all, tab_todo = st.tabs(["All tasks", "Incomplete only"])
    with tab_all:
        st.table([t.to_dict() for t in current_tasks])
    with tab_todo:
        scheduler_view = Scheduler(owner=st.session_state.owner)
        incomplete = scheduler_view.filter_tasks(completed=False)
        if incomplete:
            st.table([t.to_dict() for t in incomplete])
        else:
            st.success("All tasks are complete!")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Today's Schedule")
st.caption(f"Builds the best plan that fits within {st.session_state.owner.get_available_time()} minutes. Daily tasks are prioritized first.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=st.session_state.owner)
    plan = scheduler.generate_plan()

    if plan:
        st.success(scheduler.explain_plan())

        st.markdown("**Sorted by start time:**")
        sorted_tasks = scheduler.sort_by_time()
        st.table([t.to_dict() for t in sorted_tasks])
    else:
        st.warning("No tasks could be scheduled. Try adding tasks or increasing your available time.")

    # Conflict warnings — shown regardless of whether a plan was generated
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.markdown("---")
        st.markdown("**⚠️ Scheduling conflicts detected**")
        st.caption("Two or more tasks are scheduled at the same start time. Adjust a start time to avoid overlap.")
        for warning in conflicts:
            st.error(warning)
