from fastapi import FastAPI
from services import employee, login, project, register, projectStep
from fastapi.middleware.cors import CORSMiddleware
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
app.include_router(employee.router)
app.include_router(project.router)
app.include_router(projectStep.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)