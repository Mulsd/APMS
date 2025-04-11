from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库配置
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 数据库模型
class ProjectDB(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)  # 添加主键
    #项目细节
    proj = Column(String(255)) #项目名称
    company = Column(String(255)) #公司名称
    order = Column(String(255)) #委托类型
    assign = Column(String(255)) #负责人
    shot = Column(String(255)) #镜头名
    perpay = Column(Float) #单价
    count = Column(Integer) #数量
    #财务细节
    inpay = Column(Float) #甲方付款入账
    inpayya = Column(String(50)) #甲方付款状态
    outpayya = Column(String(50)) #外包工资付款状态
    outpay = Column(Float) #工资外包出账
    allpay = Column(Float) #计算后金额
    inpayfor = Column(String(255)) #入账币种
    outpayfor = Column(String(255)) #出账币种
    #管理细节
    note = Column(String(255)) #备注
    tag = Column(String(50)) #完成状态
    start = Column(DateTime) #项目下发时间
    end = Column(DateTime, nullable=True) #项目结束时间

# Pydantic 模型
class ProjectBase(BaseModel):
    proj: str
    company: str
    order: str
    assign: str
    shot: str
    perpay: float
    count: int
    inpay: float
    inpayya: str
    outpayya: str
    outpay: float
    allpay: float
    inpayfor: str
    outpayfor: str
    note: str
    tag: str
    start: datetime
    end: Optional[datetime] = None

class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True

# API 路由
# 添加安全配置
SECRET_KEY = "123456789"  # 请更改为一个安全的密钥
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 用户模型
class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# 模拟用户数据库（实际应用中应该使用真实数据库）
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("114514"),  # 请更改为安全的密码
        "disabled": False,
    }
}

# 身份验证相关函数
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(fake_users_db, username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

# 登录接口
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 修改现有的 API 路由，添加身份验证
@app.get("/api/projects/")
def read_projects(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        projects = db.query(ProjectDB).all()
        return projects
    finally:
        db.close()

# 其他路由也需要类似修改
@app.post("/api/projects/")
def create_project(project: ProjectBase, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        db_project = ProjectDB(**project.dict())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    finally:
        db.close()

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        db.delete(project)
        db.commit()
        return {"message": "Project deleted"}
    finally:
        db.close()

# 创建数据库表
Base.metadata.create_all(bind=engine)


# 添加更新接口
@app.put("/api/projects/{project_id}")
def update_project(project_id: int, project: ProjectBase, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        db_project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # 更新项目数据
        for key, value in project.dict().items():
            setattr(db_project, key, value)
        
        db.commit()
        db.refresh(db_project)
        return db_project
    finally:
        db.close()