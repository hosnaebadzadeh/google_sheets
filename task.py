import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("apikey.json", scope)
client = gspread.authorize(creds)
sheet = client.open("taskmanager").sheet1


def add_new_task(task_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Incomplete"
    sheet.append_row([task_name, status, timestamp])


def update_task_status(row_number):
    sheet.update_cell(row_number, 2, "Completed")
    sheet.update_cell(row_number, 3, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def load_tasks():
    tasks = sheet.get_all_records()
    return tasks


st.title("Simple Task Tracker")

# create
st.subheader("Create a Task")
task_name = st.text_input("Task Name")
if st.button("Add Task"):
    if task_name.strip():
        add_new_task(task_name)
        st.success("Task added!")
    else:
        st.warning("Please enter a valid task name.")


st.subheader("Current Tasks")
tasks = load_tasks()
if tasks:
    task_df = pd.DataFrame(tasks)
    st.dataframe(task_df)

    
    st.subheader("Complete a Task")
    task_choices = [f"{i+1}: {task['Task Name']}" for i, task in enumerate(tasks) if task["Status"] == "Incomplete"]
    if task_choices:
        selected_task = st.selectbox("Select a task to complete:", task_choices)
        if st.button("Mark Completed"):
            task_index = int(selected_task.split(":")[0])
            update_task_status(task_index + 1)  # Adjust for header row
            st.success(f"Task '{tasks[task_index - 1]['Task Name']}' marked as completed!")
    else:
        st.info("No incomplete tasks to mark as completed.")
else:
    st.info("No tasks available. Add a task to get started!")

# https://github.com/hosnaebadzadeh
