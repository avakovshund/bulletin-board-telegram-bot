from app.database.orm_query import orm_all_advertisements, orm_delete_30_advertisement

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta

# Function that check ads for timing out(30 days) and if there is timed out advertisements it will be deleted
async def check_for_date(session: AsyncSession):
    today = datetime.now()
    count_check = 0
    count_delete = 0
    print('Check started.')
    for advertisement in await orm_all_advertisements(session):
        added_time = advertisement.timestamp.date()
        count_check += 1
        if added_time + timedelta(days=30) == today.date():
            count_delete += 1
            await orm_delete_30_advertisement(session, advertisement.id)
    print(f'Check finished. Checked {count_check}. Deleted {count_delete}.')