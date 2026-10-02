from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base,engine
from routers.accountreg import router as Accountrouter 
from routers.users import router as Userrouter
from routers.login import router as Loginrouter
from routers.wire_transfer import router as Wirerouter
from routers.user_chat import router as userchatrouter
from routers.admin_chat import router as adminchatrouter
from routers.dashboard import router as dashboardrouter
from routers.image import router as imagerouter
from routers.notifications import router as notificationrouter
from routers.account import router as accountrouter
from routers.transaction import router as transactionrouter
from routers.pin import router as pinrouter
from routers.tickets import router as ticketrouter
from routers.admin import router as adminrouter
Base.metadata.create_all(engine)
app = FastAPI(title="Banking system")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(Accountrouter)
app.include_router(Userrouter)
app.include_router(Loginrouter)
app.include_router(Wirerouter)
app.include_router(userchatrouter)
app.include_router(adminchatrouter)
app.include_router(dashboardrouter)
app.include_router(imagerouter)
app.include_router(notificationrouter)
app.include_router(accountrouter)
app.include_router(transactionrouter)
app.include_router(pinrouter)
app.include_router(ticketrouter)
app.include_router(adminrouter)
app.mount("/static", StaticFiles(directory="static"))
