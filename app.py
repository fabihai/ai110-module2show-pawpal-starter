import streamlit as st
from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, your pet care planning assistant.

This app helps you schedule and manage care tasks for your pet(s).
"""
)

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Pet Owner")
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.divider()

# Pet Management Section
st.subheader("🐕 Your Pets")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("New pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])
with col3:
    st.empty()

if st.button("Add pet", key="add_pet_btn"):
    if pet_name.strip():
        new_pet = Pet(pet_name, owner)
        owner.add_pet(new_pet)
        st.success(f"✓ {pet_name} ({species}) added!")
        st.rerun()
    else:
        st.error("Please enter a pet name.")

# Display current pets
if owner.pets:
    st.markdown("**Current pets:**")
    for pet in owner.pets:
        st.write(f"  • {pet.name}")
else:
    st.info("No pets yet. Add one above to get started!")

st.divider()

# Task Management Section
st.subheader("📋 Tasks")

if owner.pets:
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_pet = st.selectbox("Pet", [p.name for p in owner.pets])
        pet_obj = next(p for p in owner.pets if p.name == selected_pet)
    with col2:
        task_description = st.text_input("Task description", value="Feed pet")
    with col3:
        task_type = st.selectbox("Type", ["food", "medicine", "play", "grooming"])

    col4, col5 = st.columns(2)
    with col4:
        task_hour = st.number_input("Time (hour)", min_value=0, max_value=23, value=10)
    with col5:
        task_frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

    if st.button("Add task", key="add_task_btn"):
        if task_description.strip():
            task = Task(
                description=task_description,
                pet=pet_obj,
                task_type=task_type,
                scheduled_time=time(task_hour, 0),
                frequency=task_frequency
            )
            scheduler.add_task(task)
            st.success(f"✓ Task '{task_description}' added for {selected_pet}!")
            st.rerun()
        else:
            st.error("Please enter a task description.")

    # Display tasks for each pet
    st.markdown("**Current tasks:**")
    for pet in owner.pets:
        if pet.get_tasks():
            st.markdown(f"*{pet.name}:*")
            for task in pet.get_tasks():
                st.write(f"  {task}")
        else:
            st.caption(f"{pet.name}: No tasks yet")

else:
    st.warning("Add a pet first before creating tasks.")

st.divider()

# Schedule Generation & Analysis Section (Phase 3)
st.subheader("📅 Schedule & Analytics")

if owner.pets and owner.get_all_tasks():
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["Daily Schedule", "Filter & Sort", "Conflicts", "Summary"])

    with tab1:
        st.markdown("**Daily Schedule (sorted by time):**")
        daily_tasks = scheduler.get_daily_plan()

        if daily_tasks:
            schedule_data = []
            for task in daily_tasks:
                schedule_data.append({
                    "Pet": task.pet.name,
                    "Time": task.scheduled_time.strftime('%H:%M'),
                    "Description": task.description,
                    "Type": task.task_type,
                    "Frequency": task.frequency,
                    "Status": "✓ Complete" if task.is_completed else "○ Pending"
                })
            st.table(schedule_data)
        else:
            st.info("No tasks scheduled yet.")

    with tab2:
        st.markdown("**Filter & Sort Tasks**")

        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            filter_type = st.selectbox("Filter by task type:",
                                      ["All"] + list(set(t.task_type for t in owner.get_all_tasks())))
        with filter_col2:
            filter_status = st.selectbox("Filter by status:",
                                        ["All", "Pending", "Completed"])

        # Apply filters using Scheduler methods
        filtered_tasks = owner.get_all_tasks()

        if filter_type != "All":
            filtered_tasks = scheduler.get_tasks_by_type(filter_type)

        if filter_status == "Pending":
            filtered_tasks = [t for t in filtered_tasks if not t.is_completed]
        elif filter_status == "Completed":
            filtered_tasks = [t for t in filtered_tasks if t.is_completed]

        # Sort by time
        filtered_tasks = sorted(filtered_tasks, key=lambda t: t.scheduled_time)

        if filtered_tasks:
            filter_data = []
            for task in filtered_tasks:
                filter_data.append({
                    "Pet": task.pet.name,
                    "Time": task.scheduled_time.strftime('%H:%M'),
                    "Description": task.description,
                    "Type": task.task_type,
                    "Status": "✓ Complete" if task.is_completed else "○ Pending"
                })
            st.table(filter_data)
            st.caption(f"Showing {len(filtered_tasks)} task(s)")
        else:
            st.info("No tasks match the selected filters.")

    with tab3:
        st.markdown("**Conflict Detection**")
        conflicts = scheduler.get_all_scheduling_conflicts()

        if conflicts:
            st.warning("⚠️ Scheduling conflicts detected!")
            for conflict in conflicts:
                st.warning(conflict, icon="⚠️")
        else:
            st.success("✓ No scheduling conflicts! Your schedule is optimized.", icon="✅")

    with tab4:
        st.markdown("**Schedule Summary**")
        pending = scheduler.get_pending_tasks()
        completed = scheduler.get_tasks_by_completion_status(True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", len(owner.get_all_tasks()))
        with col2:
            st.metric("Pending", len(pending))
        with col3:
            st.metric("Completed", len(completed))

        st.divider()

        # Breakdown by task type
        st.markdown("**Tasks by Type:**")
        task_types = set(t.task_type for t in owner.get_all_tasks())
        type_cols = st.columns(len(task_types))

        for i, task_type in enumerate(sorted(task_types)):
            type_count = len(scheduler.get_tasks_by_type(task_type))
            with type_cols[i]:
                st.metric(task_type.capitalize(), type_count)

        st.divider()

        # Breakdown by pet
        st.markdown("**Tasks by Pet:**")
        pet_cols = st.columns(len(owner.pets))

        for i, pet in enumerate(owner.pets):
            pet_task_count = len(pet.get_tasks())
            with pet_cols[i]:
                st.metric(pet.name, pet_task_count)

elif not owner.pets:
    st.warning("📍 Add a pet first before creating tasks.")
else:
    st.info("📍 Add tasks to see your schedule and analytics.")
