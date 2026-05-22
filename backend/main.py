from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select, func
from datetime import datetime, timedelta, date
from typing import List, Optional
from collections import defaultdict

from database import engine, get_session, init_db
from models import (
    User, UserCreate, UserLogin, UserResponse, TokenResponse,
    LearningItem, LearningItemCreate, LearningItemUpdate, LearningItemResponse,
    ReviewLog, ReviewLogResponse, StatsResponse, OverviewStats, TrendsResponse,
    TrendDataPoint, ItemStatus
)
from auth import verify_password, get_password_hash, create_access_token, decode_token

app = FastAPI(title="艾宾浩斯复习助手 API", version="2.0.0")

security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REVIEW_INTERVALS = [1, 3, 7, 14, 30, 60, 90]


def calculate_next_review(review_count: int) -> timedelta:
    if review_count >= len(REVIEW_INTERVALS):
        return timedelta(days=REVIEW_INTERVALS[-1])
    return timedelta(days=REVIEW_INTERVALS[review_count])


def get_item_status(item: LearningItem) -> ItemStatus:
    if item.review_count >= len(REVIEW_INTERVALS):
        return ItemStatus.COMPLETED

    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    next_review = item.next_review_at

    if next_review.date() <= today_start.date():
        return ItemStatus.DUE_TODAY
    return ItemStatus.PENDING


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
        )

    user = session.get(User, int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
        )

    return user


@app.on_event("startup")
def on_startup():
    init_db()


# ==================== 认证接口 ====================

@app.post("/api/auth/register", response_model=TokenResponse, status_code=201)
def register(data: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(
        select(User).where((User.username == data.username) | (User.email == data.email))
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已被注册"
        )

    user = User(
        username=data.username,
        email=data.email,
        password_hash=get_password_hash(data.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )
    )


@app.post("/api/auth/login", response_model=TokenResponse)
def login(data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == data.username)).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )
    )


@app.get("/api/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        created_at=current_user.created_at
    )


# ==================== 学习内容接口 ====================

@app.get("/api/items", response_model=List[LearningItemResponse])
def get_items(
    category: Optional[str] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(LearningItem).where(LearningItem.user_id == current_user.id)

    if category and category != "全部":
        query = query.where(LearningItem.category == category)

    items = session.exec(query.order_by(LearningItem.created_at.desc())).all()

    return [
        LearningItemResponse(
            id=item.id,
            title=item.title,
            content=item.content,
            category=item.category,
            created_at=item.created_at,
            review_count=item.review_count,
            last_reviewed_at=item.last_reviewed_at,
            next_review_at=item.next_review_at,
            status=get_item_status(item),
            total_reviews=len(REVIEW_INTERVALS)
        )
        for item in items
    ]


@app.post("/api/items", response_model=LearningItemResponse, status_code=201)
def create_item(
    data: LearningItemCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    item = LearningItem(
        user_id=current_user.id,
        title=data.title,
        content=data.content,
        category=data.category or "默认",
        created_at=datetime.now(),
        review_count=0,
        next_review_at=datetime.now() + timedelta(days=1)
    )
    session.add(item)
    session.commit()
    session.refresh(item)

    return LearningItemResponse(
        id=item.id,
        title=item.title,
        content=item.content,
        category=item.category,
        created_at=item.created_at,
        review_count=item.review_count,
        last_reviewed_at=item.last_reviewed_at,
        next_review_at=item.next_review_at,
        status=get_item_status(item),
        total_reviews=len(REVIEW_INTERVALS)
    )


@app.put("/api/items/{item_id}", response_model=LearningItemResponse)
def update_item(
    item_id: int,
    data: LearningItemUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    item = session.exec(
        select(LearningItem).where(
            LearningItem.id == item_id,
            LearningItem.user_id == current_user.id
        )
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="学习内容不存在")

    if data.title is not None:
        item.title = data.title
    if data.content is not None:
        item.content = data.content
    if data.category is not None:
        item.category = data.category

    session.commit()
    session.refresh(item)

    return LearningItemResponse(
        id=item.id,
        title=item.title,
        content=item.content,
        category=item.category,
        created_at=item.created_at,
        review_count=item.review_count,
        last_reviewed_at=item.last_reviewed_at,
        next_review_at=item.next_review_at,
        status=get_item_status(item),
        total_reviews=len(REVIEW_INTERVALS)
    )


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    item = session.exec(
        select(LearningItem).where(
            LearningItem.id == item_id,
            LearningItem.user_id == current_user.id
        )
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="学习内容不存在")

    logs = session.exec(select(ReviewLog).where(ReviewLog.item_id == item_id)).all()
    for log in logs:
        session.delete(log)

    session.delete(item)
    session.commit()
    return None


@app.post("/api/items/{item_id}/review", response_model=LearningItemResponse)
def review_item(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    item = session.exec(
        select(LearningItem).where(
            LearningItem.id == item_id,
            LearningItem.user_id == current_user.id
        )
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="学习内容不存在")

    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    was_on_time = item.next_review_at.date() >= today_start.date()

    review_log = ReviewLog(
        item_id=item.id,
        reviewed_at=now,
        was_on_time=was_on_time
    )
    session.add(review_log)

    item.review_count += 1
    item.last_reviewed_at = now
    item.next_review_at = now + calculate_next_review(item.review_count)

    session.commit()
    session.refresh(item)

    return LearningItemResponse(
        id=item.id,
        title=item.title,
        content=item.content,
        category=item.category,
        created_at=item.created_at,
        review_count=item.review_count,
        last_reviewed_at=item.last_reviewed_at,
        next_review_at=item.next_review_at,
        status=get_item_status(item),
        total_reviews=len(REVIEW_INTERVALS)
    )


@app.get("/api/items/{item_id}/logs", response_model=List[ReviewLogResponse])
def get_review_logs(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    item = session.exec(
        select(LearningItem).where(
            LearningItem.id == item_id,
            LearningItem.user_id == current_user.id
        )
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="学习内容不存在")

    logs = session.exec(
        select(ReviewLog)
        .where(ReviewLog.item_id == item_id)
        .order_by(ReviewLog.reviewed_at.desc())
    ).all()

    return [
        ReviewLogResponse(
            id=log.id,
            item_id=log.item_id,
            reviewed_at=log.reviewed_at,
            was_on_time=log.was_on_time
        )
        for log in logs
    ]


# ==================== 统计接口 ====================

@app.get("/api/stats", response_model=StatsResponse)
def get_stats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    items = session.exec(
        select(LearningItem).where(LearningItem.user_id == current_user.id)
    ).all()

    categories = session.exec(
        select(LearningItem.category).where(LearningItem.user_id == current_user.id).distinct()
    ).all()

    total = len(items)
    pending_today = sum(1 for item in items if get_item_status(item) == ItemStatus.DUE_TODAY)
    completed_all = sum(1 for item in items if item.review_count >= len(REVIEW_INTERVALS))

    return StatsResponse(
        total_items=total,
        pending_today=pending_today,
        completed_all=completed_all,
        categories_count=len(categories)
    )


@app.get("/api/stats/overview", response_model=OverviewStats)
def get_overview(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    items = session.exec(
        select(LearningItem).where(LearningItem.user_id == current_user.id)
    ).all()

    all_logs = []
    for item in items:
        logs = session.exec(select(ReviewLog).where(ReviewLog.item_id == item.id)).all()
        all_logs.extend(logs)

    category_count = defaultdict(int)
    for item in items:
        category_count[item.category] += 1

    return OverviewStats(
        total_items=len(items),
        total_reviews=len(all_logs),
        on_time_reviews=sum(1 for log in all_logs if log.was_on_time),
        late_reviews=sum(1 for log in all_logs if not log.was_on_time),
        due_today=sum(1 for item in items if get_item_status(item) == ItemStatus.DUE_TODAY),
        completed=sum(1 for item in items if get_item_status(item) == ItemStatus.COMPLETED),
        pending=sum(1 for item in items if get_item_status(item) == ItemStatus.PENDING),
        category_distribution=dict(category_count)
    )


@app.get("/api/stats/trends", response_model=TrendsResponse)
def get_trends(
    days: int = 30,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    now = datetime.now()
    start_date = (now - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)

    items = session.exec(
        select(LearningItem).where(LearningItem.user_id == current_user.id)
    ).all()

    learning_by_date = defaultdict(int)
    review_by_date = defaultdict(int)

    for item in items:
        if item.created_at >= start_date:
            date_key = item.created_at.strftime("%Y-%m-%d")
            learning_by_date[date_key] += 1

        logs = session.exec(
            select(ReviewLog).where(ReviewLog.item_id == item.id)
        ).all()

        for log in logs:
            if log.reviewed_at >= start_date:
                date_key = log.reviewed_at.strftime("%Y-%m-%d")
                review_by_date[date_key] += 1

    all_dates = []
    current = start_date
    while current <= now:
        all_dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    learning_trend = [
        TrendDataPoint(date=d, count=learning_by_date.get(d, 0))
        for d in all_dates
    ]

    review_trend = [
        TrendDataPoint(date=d, count=review_by_date.get(d, 0))
        for d in all_dates
    ]

    all_logs = []
    for item in items:
        logs = session.exec(select(ReviewLog).where(ReviewLog.item_id == item.id)).all()
        all_logs.extend(logs)

    total_reviews = len(all_logs)
    on_time_count = sum(1 for log in all_logs if log.was_on_time)
    on_time_rate = (on_time_count / total_reviews * 100) if total_reviews > 0 else 100.0

    return TrendsResponse(
        learning_trend=learning_trend,
        review_trend=review_trend,
        on_time_rate=on_time_rate
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
