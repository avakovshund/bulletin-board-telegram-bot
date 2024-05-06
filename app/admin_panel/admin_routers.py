from aiogram import F, Router
from aiogram.filters import Command, or_f
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.admin_panel.admin_states import AdminMenu, AdminImage
import app.admin_panel.admin_keyboards as admin_kb
from app.database.orm_query import *
from app.admin_panel.admin_filter import IsAdmin

admin_router = Router()
admin_router.message.filter(IsAdmin())

# Admin command "/admin"
@admin_router.message(Command("admin"))
async def admin_start(message: Message, state: FSMContext):
    await message.answer('Admin health check: OK.',
                         reply_markup=admin_kb.admin_main_menu)
    await state.set_state(AdminMenu.admin_begin_work)

# Admin command "/image" that helps you to change welcome image
@admin_router.message(Command("image"))
async def admin_start(message: Message, state: FSMContext):
    await message.answer('Send your new welcome photo')
    await state.set_state(AdminImage.admin_send_image)

@admin_router.message(AdminImage.admin_send_image, F.photo)
async def admin_start(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)
    user_data = await state.get_data()
    if await orm_get_welcome_image(session) == None:
        await orm_set_welcome_image(session, user_data["image"])
    else:
        await orm_update_welcome_image(session, user_data["image"])
    await message.answer_photo(photo=user_data["image"],
                               caption='You have succesfully changed your welcome image to this.\nTo check use command /start')
    await state.clear()

# Searching ads
@admin_router.message(AdminMenu.admin_begin_work, F.text == 'Find 🔍')
async def admin_find_category(message: Message, state: FSMContext):
    await state.set_state(AdminMenu.admin_chosing_category)
    await message.answer('Choose the category', reply_markup=admin_kb.admin_find_all)

@admin_router.message(AdminMenu.admin_chosing_category, F.text)
async def admin_find_advertisements(message: Message, state: FSMContext, session: AsyncSession):
    if message.text in ['Category 1', 'Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5', 'Category 6']: 
        await message.answer(text=f'All available ads in the category "{message.text}" ⬇')
        for advertisements in await orm_category_advertisements(session, message):
            await message.answer_photo(
                photo=advertisements.added_photo,
                caption=f'Category: {advertisements.category}' + f'\nText: {advertisements.added_text}' +
                f'\nPrice: {advertisements.added_price}' + f'\nTime of publication: {advertisements.timestamp}',
                reply_markup=admin_kb.admin_inline_menu(advertisements.user_id, advertisements.id)
                )
        await message.answer(text=f'These are all available ads in the category "{message.text}" ⬆', reply_markup=admin_kb.admin_find_all)
    elif message.text == 'Back to main menu ⬅️':
        await state.set_state(AdminMenu.admin_begin_work)
        await message.answer('Main menu.', reply_markup=admin_kb.admin_main_menu)
    else:
        await message.answer('I don`t understand you.', reply_markup=admin_kb.admin_find_all)

# Deleting ad
@admin_router.callback_query(F.data.startswith('delete_'))
async def admin_delete_adv(callback: CallbackQuery, session: AsyncSession):
    advertisements_id = callback.data.split("_")[-1]
    await orm_delete_advertisement(session, advertisements_id)
    await callback.answer('The ad has been successfully deleted.')

# Editing ad
@admin_router.callback_query(F.data.startswith('update_'))
async def admin_update_adv(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    advertisements_id = callback.data.split("_")[-1]
    advertisement_to_change = await orm_get_advertisement(session, advertisements_id)
    AdminMenu.advertisement_to_change = advertisement_to_change
    await callback.answer()
    await callback.message.answer('Select a new ad category.\nTo skip the changes, enter: "."', reply_markup=admin_kb.admin_find_all)
    await state.set_state(AdminMenu.admin_update_category)

@admin_router.message(AdminMenu.admin_update_category, or_f(F.text, F.text == '.'))
async def update_name(message: Message, state: FSMContext):
    if message.text == 'Back to main menu ⬅️':
        await state.set_state(AdminMenu.admin_begin_work)
        await message.answer('Main menu.', reply_markup=admin_kb.admin_main_menu)
    else:
        if message.text == '.':
            await state.update_data(category=AdminMenu.advertisement_to_change.category)
        else:
            await state.update_data(category=message.text)
        await message.answer('Enter a new ad text.', reply_markup=ReplyKeyboardRemove())
        await state.set_state(AdminMenu.admin_update_text)

@admin_router.message(AdminMenu.admin_update_text, or_f(F.text, F.text == '.'))
async def update_name(message: Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(added_text=AdminMenu.advertisement_to_change.added_text)
    else:
        await state.update_data(added_text=message.text)
    await message.answer('Enter a new ad price.')
    await state.set_state(AdminMenu.admin_update_price)
    
@admin_router.message(AdminMenu.admin_update_price, or_f(F.text, F.text == '.'))
async def update_name(message: Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(added_price=AdminMenu.advertisement_to_change.added_price)
    else:
        await state.update_data(added_price=message.text)
    await message.answer('Send a new ad photo.')
    await state.set_state(AdminMenu.admin_update_photo)

@admin_router.message(AdminMenu.admin_update_photo, or_f(F.photo, F.text == '.'))
async def update_name(message: Message, state: FSMContext, session: AsyncSession):
    if message.text == '.':
        await state.update_data(added_photo=AdminMenu.advertisement_to_change.added_photo)
    else:
        await state.update_data(added_photo=message.photo[-1].file_id)
    user_data = await state.get_data()
    await orm_update_advertisement(session, AdminMenu.advertisement_to_change.id, user_data)
    await message.answer('Ad successfully changed!', reply_markup=admin_kb.admin_main_menu)
    advertisements = await orm_get_advertisement(session, AdminMenu.advertisement_to_change.id)
    await message.answer_photo(
                photo=advertisements.added_photo,
                caption='CHANGED AD🔽' + f'\nCategory: {advertisements.category}' + f'\nText: {advertisements.added_text}' +
                f'\nPrice: {advertisements.added_price}' + f'\nTime of publication: {advertisements.timestamp}',
                reply_markup=admin_kb.admin_inline_menu(advertisements.user_id, advertisements.id)
                )
    AdminMenu.advertisement_to_change = None
    await state.set_state(AdminMenu.admin_begin_work)

# Premium settings panel
@admin_router.message(AdminMenu.admin_begin_work, F.text == 'Premium Settings')
async def admin_premium(message: Message, state: FSMContext):
    await state.set_state(AdminMenu.admin_premium_settings)
    await message.answer("What do you want to do?\nTo get the ID, send the user`s message to this bot: @userinfobot", reply_markup=admin_kb.admin_premium)


@admin_router.message(AdminMenu.admin_premium_settings, F.text)
async def admin_premium_settings(message: Message, state: FSMContext, session: AsyncSession):
    if message.text == 'Add user':
        await state.set_state(AdminMenu.admin_premium_add)
        await message.answer('Enter the ID of the user you want to add.', reply_markup=admin_kb.admin_back)
    elif message.text == 'Continue subscription':
        await state.set_state(AdminMenu.admin_premium_update)
        await message.answer('Enter the user ID to which you want to prolong the subscription.', reply_markup=admin_kb.admin_back) 
    elif message.text == 'Delete user':
        await state.set_state(AdminMenu.admin_premium_delete)
        await message.answer('Enter the ID of the user you want to delete.', reply_markup=admin_kb.admin_back)
    elif message.text == 'User`s list':
        await message.answer('Here is a list of all premium users 🔽')
        count = 0
        for premium_list in await orm_list_premium(session):
            count += 1 
            user = premium_list.user_id
            await message.answer(text=f'№: {count}\n'+ f'ID: {premium_list.user_id}\n' + f'Time of receiving a premium subscription: {premium_list.timestamp}\n' + f'Expiration date of the premium subscription: {premium_list.timed_out}\n',
                                 reply_markup=admin_kb.admin_inline_write_to_user(user))
    elif message.text == 'Back to main menu ⬅️':
        await state.set_state(AdminMenu.admin_begin_work)
        await message.answer('Main menu.', reply_markup=admin_kb.admin_main_menu)
    else:
        await message.answer('Try again!')

# Adding a premium subscription to user
@admin_router.message(AdminMenu.admin_premium_add, F.text)
async def admin_premium_settings(message: Message, state: FSMContext):
    if message.text == 'Get back ⬅️':
        await state.set_state(AdminMenu.admin_premium_settings)
        await message.answer('What do you want to do?', reply_markup=admin_kb.admin_premium)
    elif message.text:
        await state.update_data(user_id=int(message.text))
        await state.set_state(AdminMenu.admin_premium_add_month)
        await message.answer('Enter the number of months of the premium subscription (1,2, etc.).', reply_markup=admin_kb.admin_back)
    else:
        message.answer('Try again!')


@admin_router.message(AdminMenu.admin_premium_add_month, F.text)
async def admin_premium_settings(message: Message, state: FSMContext, session: AsyncSession):
    if message.text == 'Get back ⬅️':
        await state.set_state(AdminMenu.admin_premium_add)
        await message.answer('Enter the ID of the user you want to add.', reply_markup=admin_kb.admin_back)
    elif message.text:
        await state.update_data(month=int(message.text))
        user_data = await state.get_data()
        await orm_add_premium(session, user_data)
        await message.answer(f'User with ID {user_data["user_id"]} succesfully get {user_data["month"] * 30} days.')
        await state.set_state(AdminMenu.admin_premium_settings)
        await message.answer('What do you want to do?\nTo get the ID, send the user`s message to this bot: @userinfobot', reply_markup=admin_kb.admin_premium)
    else:
        message.answer('Try again!')
    
# Prolong a user`s premium subscription
@admin_router.message(AdminMenu.admin_premium_update, F.text)
async def admin_premium_settings(message: Message, state: FSMContext, session: AsyncSession):
    if message.text == 'Get back ⬅️':
        await state.set_state(AdminMenu.admin_premium_settings)
        await message.answer('What do you want to do??', reply_markup=admin_kb.admin_premium)
    elif message.text:
        await state.update_data(user_id=int(message.text))
        await state.set_state(AdminMenu.admin_premium_update_month)
        await message.answer('Enter the number of months of the subscription (1,2, etc.).', reply_markup=admin_kb.admin_back)
    else:
        message.answer('Try again!')
    

@admin_router.message(AdminMenu.admin_premium_update_month, F.text)
async def admin_premium_settings(message: Message, state: FSMContext, session: AsyncSession):
    if message.text == 'Get back ⬅️':
        await state.set_state(AdminMenu.admin_premium_update)
        await message.answer('Enter the user ID to which you want to prolong the subscription.', reply_markup=admin_kb.admin_back)
    elif message.text:
        await state.update_data(month=int(message.text))
        user_data = await state.get_data()
        await orm_update_premium(session, user_data)
        await message.answer(f'User with ID {user_data["user_id"]} has successfully renewed his subscription for {user_data["month"] * 30} days.')
        await state.set_state(AdminMenu.admin_premium_settings)
        await message.answer('What do you want to do??\nTo get the ID, send the user`s message to this bot: @userinfobot', reply_markup=admin_kb.admin_premium)
    else:
        message.answer('Try again!')

# Delete a user`s premium subscription
@admin_router.message(AdminMenu.admin_premium_delete, F.text)
async def admin_premium_settings(message: Message, state: FSMContext, session: AsyncSession):
    if message.text == 'Get back ⬅️':
        await state.set_state(AdminMenu.admin_premium_settings)
        await message.answer('What do you want to do??', reply_markup=admin_kb.admin_premium)
    elif message.text:
        user = message.text
        for premium_list in await orm_list_premium(session):
            if int(user) == premium_list.user_id:
                await orm_delete_premium(session, user)
                await message.answer(f'The user with ID {user} has been successfully deleted.')
                await state.set_state(AdminMenu.admin_premium_settings)
                await message.answer('What do you want to do??\nTo get the ID, send the user`s message to this bot: @userinfobot',
                                     reply_markup=admin_kb.admin_premium)
    else:
        message.answer('Try again!')