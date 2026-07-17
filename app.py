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

# Schedule Generation Section
st.subheader("📅 Daily Schedule")

if st.button("Generate daily schedule", key="gen_schedule_btn"):
    if owner.pets and owner.get_all_tasks():
        st.markdown("**Generated Schedule:**")
        daily_tasks = scheduler.get_daily_plan()
        for task in daily_tasks:
            status_icon = "✓" if task.is_completed else "○"
            st.write(f"{status_icon} {task.description} ({task.task_type}) @ {task.scheduled_time.strftime('%H:%M')} — {task.pet.name}")
    elif not owner.pets:
        st.warning("Add pets to generate a schedule.")
    else:
        st.warning("Add tasks to generate a schedule.")

st.divider()

# Pending tasks summary
if owner.get_all_pending_tasks():
    st.markdown("**Pending tasks summary:**")
    pending = scheduler.get_pending_tasks()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total pending", len(pending))
    with col2:
        food_tasks = len([t for t in pending if t.task_type == "food"])
        st.metric("Feeding tasks", food_tasks)
    with col3:
        med_tasks = len([t for t in pending if t.task_type == "medicine"])
        st.metric("Medicine tasks", med_tasks)
