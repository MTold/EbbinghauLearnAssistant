from sqlmodel import SQLModel, Field
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum


class ItemStatus(str, Enum):
    PENDING = "pending"
    DUE_TODAY = "due_today"
    COMPLETED = "completed"


# ==================== 用户相关 ====================

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.now)


class UserCreate(SQLModel):
    username: str
    email: str
    password: str


class UserLogin(SQLModel):
    username: str
    password: str


class UserResponse(SQLModel):
    id: int
    username: str
    email: str
    created_at: datetime


class TokenResponse(SQLModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ==================== 学习内容相关 ====================


class LearningItem(SQLModel, table=True):
    __tablename__ = "learning_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(index=True)
    content: str
    category: str = Field(default="默认", index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    review_count: int = Field(default=0)
    last_reviewed_at: Optional[datetime] = None
    next_review_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta(days=1))


class ReviewLog(SQLModel, table=True):
    __tablename__ = "review_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="learning_items.id", index=True)
    reviewed_at: datetime = Field(default_factory=datetime.now)
    was_on_time: bool = True


class LearningItemCreate(SQLModel):
    title: str
    content: str
    category: str = "默认"


class LearningItemUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None


class LearningItemResponse(SQLModel):
    id: int
    title: str
    content: str
    category: str
    created_at: datetime
    review_count: int
    last_reviewed_at: Optional[datetime]
    next_review_at: datetime
    status: ItemStatus
    total_reviews: int = 7


class ReviewLogResponse(SQLModel):
    id: int
    item_id: int
    reviewed_at: datetime
    was_on_time: bool


class StatsResponse(SQLModel):
    total_items: int
    pending_today: int
    completed_all: int
    categories_count: int


class OverviewStats(SQLModel):
    total_items: int
    total_reviews: int
    on_time_reviews: int
    late_reviews: int
    due_today: int
    completed: int
    pending: int
    category_distribution: dict


class TrendDataPoint(SQLModel):
    date: str
    count: int


class TrendsResponse(SQLModel):
    learning_trend: List[TrendDataPoint]
    review_trend: List[TrendDataPoint]
    on_time_rate: float
