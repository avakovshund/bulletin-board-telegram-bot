from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from datetime import datetime, timedelta

from app.database.models import Advertisements, Premium, Misc


# Add premium user
async def orm_add_premium(session: AsyncSession, user_data: dict):
    prem = Premium(
        user_id=user_data['user_id'],
        timed_out=datetime.now() + timedelta(days=30 * user_data['month']),
    )
    session.add(prem)
    await session.commit()
    await session.close()

# Prolong of the subscription period
async def orm_update_premium(session: AsyncSession, user_data: dict):
    query = select(Premium).where(Premium.user_id == user_data["user_id"])
    result = await session.execute(query)
    premium_instance = result.scalar_one_or_none()
    new_timed_out = premium_instance.timed_out + timedelta(days=30 * user_data["month"])
    update_query = update(Premium).where(Premium.user_id == user_data["user_id"]).values(
        timed_out=new_timed_out
    )
    await session.execute(update_query)
    await session.commit()
    await session.close()

# Delete premium user
async def orm_delete_premium(session: AsyncSession, user: int): 
    query = delete(Premium).where(Premium.user_id == user)
    await session.execute(query)
    await session.commit()
    await session.close()
    
# Premium user`s list
async def orm_list_premium(session: AsyncSession):
    query = select(Premium)
    result = await session.execute(query)
    await session.close()
    return result.scalars().all()
    
# Add adv
async def orm_add_adv(session: AsyncSession, user_data: dict, message: Message):
    adv = Advertisements(
        category=user_data["category"],
        user_id=message.from_user.id,
        added_photo=user_data["added_photo"],
        added_text=user_data["added_text"],
        added_price=user_data["added_price"]
        )
    session.add(adv)
    await session.commit()
    await session.close()

# Get all ads
async def orm_all_advertisements(session: AsyncSession):
    query = select(Advertisements)
    result = await session.execute(query)
    adv = result.scalars().all()
    await session.close()
    return adv

# Get my ads
async def orm_my_advertisements(session: AsyncSession, message: Message):
    query = select(Advertisements).where(Advertisements.user_id == message.from_user.id)
    result = await session.execute(query)
    await session.close()
    return result.scalars().all()

# Ads by category
async def orm_category_advertisements(session: AsyncSession, message: Message):
    query = select(Advertisements).where(Advertisements.category == message.text)
    result = await session.execute(query)
    await session.close()
    return result.scalars().all()

# Delete ad
async def orm_delete_advertisement(session: AsyncSession, orm_advertisements_id: int):
    query = delete(Advertisements).where(Advertisements.id == orm_advertisements_id)
    await session.execute(query)
    await session.commit()
    await session.close()
    
# Removal of the ad after 30 days
async def orm_delete_30_advertisement(session: AsyncSession, orm_advertisements_id: int):
    query = delete(Advertisements).where(Advertisements.id == orm_advertisements_id)
    await session.execute(query)
    await session.commit()
    await session.close()

# Edit an ad
async def orm_update_advertisement(session: AsyncSession, orm_advertisements_id: int, user_data: dict):
    query = update(Advertisements).where(Advertisements.id == orm_advertisements_id).values(
        category=user_data["category"],
        added_photo=user_data["added_photo"],
        added_text=user_data["added_text"],
        added_price=user_data["added_price"]
    )
    await session.execute(query)
    await session.commit()
    await session.close()

# Ad by ID
async def orm_get_advertisement(session: AsyncSession, orm_advertisements_id: int):
    query = select(Advertisements).where(Advertisements.id == orm_advertisements_id)
    result = await session.execute(query)
    await session.close()
    return result.scalar()
    
# Edit an welcome image
async def orm_update_welcome_image(session: AsyncSession, image: str):
    query = update(Misc).where(Misc.id == 1).values(
        welcome_image_id=image,
        timestamp=datetime.now()
    )
    await session.execute(query)
    await session.commit()
    await session.close()

# Set welcome image
async def orm_set_welcome_image(session: AsyncSession, name: str):
    image = Misc(
        welcome_image_id=name
    )
    session.add(image)
    await session.commit()
    await session.close()

# Get Misc
async def orm_get_welcome_image(session: AsyncSession):
    query = select(Misc.welcome_image_id).where(Misc.id == 1)
    result = await session.execute(query)
    await session.close()
    return result.scalar()