from datetime import date

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import Task
from database.enums.task_enums import TaskStatus


async def insert_task(
        session: AsyncSession,
        user_id: int,
        title: str,
        description: str | None,
        due_date: date | None,
        status: TaskStatus
) -> Task:
    async with session.begin():
        new_task = Task(
            user_id=user_id,
            title=title,
            description=description,
            due_date=due_date,
            status=status
        )
        session.add(new_task)
        await session.flush()
        return new_task


async def get_tasks(
        session: AsyncSession,
        user_id: int,
        status: TaskStatus = None,
        due_date: date = None
) -> list[Task]:
    async with session:
        query = select(Task).where(Task.user_id == user_id)
        if status is not None:
            query = query.where(Task.status == status)
        if due_date is not None:
            query = query.where(Task.due_date == due_date)

        result = await session.execute(query)
        return list(result.scalars().all())


async def update_task(
        session: AsyncSession,
        task_id: int,
        user_id: int,
        **kwargs
) -> Task | None:
    async with session.begin():
        query = (
            update(Task)
            .where(
                Task.id == task_id,
                Task.user_id == user_id
            )
            .values(**kwargs)
            .returning(Task)
        )

        result = await session.execute(query)
        updated_task = result.scalars().first()
        return updated_task

async def delete_task(
        session: AsyncSession,
        task_id: int,
        user_id: int
) -> bool:
    async with session.begin():
        query = (
            delete(Task)
            .where(
                Task.id == task_id,
                Task.user_id == user_id
            )
            .returning(Task.id)
        )
        result = await session.execute(query)
        deleted_task_id = result.scalar_one_or_none()
        return deleted_task_id is not None
