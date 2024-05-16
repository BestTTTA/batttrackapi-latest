from fastapi import FastAPI
from services.Login_and_Register import register
from fastapi.middleware.cors import CORSMiddleware

from services.Employee import employee,add_emp_to_step
from services.Login_and_Register import login
from services.Project import add_serial,create_project,search,update_status_serial,update_timeend_serial,update_timestart_serial
from services.Step import add_step, step_update_endbreak, step_update_startbreak, step_update_status, step_update_timeend,step_update_timestart,step_create_break
from services.Update_image import update_image

app = FastAPI(
    title="Batttrack",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(login.router)
app.include_router(register.router)

# Employee
app.include_router(employee.router)
app.include_router(add_emp_to_step.router)

# Upload Image
app.include_router(update_image.router)

# Project
app.include_router(create_project.router)
app.include_router(add_serial.router)
app.include_router(search.router)
app.include_router(update_status_serial.router)
app.include_router(update_timestart_serial.router)
app.include_router(update_timeend_serial.router)

# Project Step
app.include_router(add_step.router)
app.include_router(step_create_break.router)
app.include_router(step_update_timeend.router)
app.include_router(step_update_endbreak.router)
app.include_router(step_update_startbreak.router)
app.include_router(step_update_status.router)
app.include_router(step_update_timestart.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)