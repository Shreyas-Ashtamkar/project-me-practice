import streamlit as st
from datetime import datetime
# DO NOT USE DB LIKE THIS, USE HELPER FUNCTIONS
from projectmepractice import db
# DO NOT USE DB LIKE THIS, USE HELPER FUNCTIONS
import pandas as pd
from projectmepractice.types import UserType, ProjectType, AllocationType

class _data:
    users = []
    projects = []
    allocations = []
    
    _users:list[UserType] = db.User.select()
    _projects:list[ProjectType] = db.Project.select()
    _allocations:list[AllocationType] = db.Allocation.select()
    
    def __init__(self):
        self.refresh()
    
    def _get_users(self):
        users = []
        for user in _data._users:
            # user = user.to_dict()
            user = {
                "id":user.id,
                "name":user.name,
                "current_project":user.current_project.title if user.current_project else "",
            }
            # current_project = user["current_project"]
            # user["current_project"] = current_project["title"] if current_project else ""
            users.append(user)
            # "allocations":[str(alloc) for alloc in user.allocations]
        return users
    
    def _get_projects(self):
        projects = []
        for project in _data._projects:
            # project = project.to_dict()
            project = {
                "id":project.get_id(),
                "title":project.title,
                # "has_parts":project.has_parts,
                "tags":project.tags,
                # "allocations":[alloc.user.name for alloc in project.allocations]
            }
            projects.append(project)
        return projects

    def _get_allocations(self):
        allocations = []
        for alloc in _data._allocations:
            alloc = {
                "id":alloc.id,
                "user_name":alloc.user.name,
                "project_name":alloc.project.title,
                "allocated_on":alloc.date
            }
            # alloc["user_id"] = alloc["user"]["name"]
            # alloc["user"] = alloc["user"]["name"]
            allocations.append(alloc)
        return allocations

    def _get_user_objects(self):
        return list(_data._users)
    
    def refresh(self):
        self.users = pd.DataFrame(self._get_users())
        self.projects = pd.DataFrame(self._get_projects())
        self.allocations = pd.DataFrame(self._get_allocations())
        return True

data = _data()

st.set_page_config(page_title="Live Dashboard", layout="wide")

# --- Streamlit Config ---
st.title("📊 Real-Time Projects Dashboard")
st.write("⏱️ Auto-refreshes every 60 seconds. Click the button below to manually refresh.")

# --- Handle Manual Refresh ---
if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = datetime.now()

if st.button("🔄 Manual Refresh Now"):
    st.session_state['last_refresh'] = datetime.now()

st.caption(f"Last refreshed: {st.session_state['last_refresh'].strftime('%Y-%m-%d %H:%M:%S')}")

# --- Load Data ---
@st.cache_data(ttl=60)
def load_data():
    data.refresh()

load_data()

screen = st.query_params.get("screen")
user = st.query_params.get("user")
project = st.query_params.get("project")
allocation = st.query_params.get("allocation")

st.query_params.clear()
dashboard_screen, users_screen, projects_screen, allocations_screen = st.tabs(["Dashboard","Users","Projects", "Allocations"], default=screen if screen else "Dashboard")

# selected_tab.
with dashboard_screen:
    st.subheader("Users")
    st.dataframe(data.users, width="content")

    st.subheader("Project")
    st.dataframe(data.projects, width="content")

    st.subheader("Allocations")
    st.dataframe(data.allocations, width="content")

with users_screen:
    if not user:
        st.subheader("Users")
        st.table(_data._users,border=True)
    else:
        st.text(f"User Name : {user}")
        st.text("Future Usecase : This place will show all details of user - joining, when first project sent, each project details")
        if st.button("clear"):
            screen = user = project = allocation = None

with projects_screen:
    st.subheader("Project")
    st.table(_data._projects)

with allocations_screen:
    st.subheader("Allocations")
    st.table(_data._allocations)