from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.fsm.context import FSMContext

from app.database.scheduled_func import check_for_date
from app.user_panel.user_states import BuyAdvSell, ForSaleCategory, OfferCategory
import app.user_panel.user_keyboards as kb
from app.database.orm_query import *
from app.admin_panel.admin_filter import my_admin_list, IsAdmin

 
user_router = Router()

# Command Start with Welcome image and Main menu
@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    image_id = await orm_get_welcome_image(session)
    await message.answer_photo(photo=image_id,
                               caption="\n🚩 Before you start using the bot, we recommend that you familiarize yourself with the rules of use using the command: /help\n" +
                               '\nLet`s get started with Main menu 🔽',
                               reply_markup=kb.main_menu)
    await state.set_state(BuyAdvSell.begin_work)

# Command Help
@user_router.message(Command('help'))
async def cmd_help(message: Message):
    file_help = open('app/user_panel/write_your_help_v1.txt', 'r', encoding='UTF-8')
    
    text_help = file_help.read()
    await message.answer(f'{text_help}', reply_markup=kb.inline_dev)

# Donate button 💳
@user_router.message(F.text == 'Donate 💳')
async def donat(message: Message, session: AsyncSession):
    await check_for_date(session)
    await message.answer(text='To support our project:\nYour bank 1: 1234 5678 9000 0009\nYour bank 2: 9876 5432 1000 0001\nOr the link below ⬇',
                         reply_markup=kb.inline_donat)

# My ads 📢
@user_router.message(F.text == 'My ads 📢')
async def my_advertisements(message: Message, session: AsyncSession, state: FSMContext):
    await message.answer('Your ads ⬇:')
    count = 0
    for advertisements in await orm_my_advertisements(session, message):
        count += 1
        await message.answer_photo(
            photo=advertisements.added_photo,
            caption=f'№: {count}' + f'\nCategory: {advertisements.category}' + f'\n{advertisements.added_text}' + f'\nPrice: {advertisements.added_price}',
            reply_markup=kb.inline_delete_adv(advertisements.id)
        )
    await message.answer('These are all your ads ⬆')

# Deleting your ad
@user_router.callback_query(F.data.startswith('delete_'))
async def delete_my_adv(callback: CallbackQuery, session: AsyncSession):
    advertisements_id = callback.data.split("_")[-1]
    await orm_delete_advertisement(session, advertisements_id)
    await callback.answer('The ad has been successfully deleted.')


# Find ads 🔍
@user_router.message(BuyAdvSell.begin_work, F.text == 'Find 🔍')
async def chose_category(message: Message, state: FSMContext):
    await state.set_state(BuyAdvSell.chosing_category)
    await message.answer('Select an ad category.', reply_markup=kb.find_all)

# Find by category
@user_router.message(BuyAdvSell.chosing_category, F.text)
async def find_advertisements(message: Message, state: FSMContext, session: AsyncSession):
    if message.text in ['Category 1', 'Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5', 'Category 6']:
        await message.answer(text=f'All available ads in the category "{message.text}" ⬇')
        for advertisements in await orm_category_advertisements(session, message):
            if str(advertisements.user_id) in my_admin_list:
                await message.answer_photo(
                    photo=advertisements.added_photo,
                    caption=f'💰Category: {advertisements.category}' + f'\n{advertisements.added_text}' + f'\nPrice: {advertisements.added_price}',
                    reply_markup=kb.inline_write_to_user(advertisements.user_id)
                    )
            else:
                await message.answer_photo(
                    photo=advertisements.added_photo,
                    caption=f'Category: {advertisements.category}' + f'\n{advertisements.added_text}' + f'\nPrice: {advertisements.added_price}',
                    reply_markup=kb.inline_write_to_user(advertisements.user_id)
                    )
        await message.answer(text=f'These are all available ads in the category "{message.text}" ⬆', reply_markup=kb.find_all)
    elif message.text == 'Back to the main menu ⬅️':
        await state.set_state(BuyAdvSell.begin_work)
        await message.answer('Main menu.', reply_markup=kb.main_menu)
    else:
        await message.answer('There is no such option.', reply_markup=kb.find_all)

# Add ad. You can add more than 3 ads if you have premium subscription
@user_router.message(BuyAdvSell.begin_work, F.text == 'Add an ad ➕')
async def add_new(message: Message, state: FSMContext, session: AsyncSession):
    all_my_advertisements = await orm_my_advertisements(session, message)
    all_my_advertisements_list = [adv.id for adv in all_my_advertisements]
    count = len(all_my_advertisements_list)
    
    premium_users = await orm_list_premium(session)
    premium_list = [user.user_id for user in premium_users]
    if count < 3:
        await state.set_state(BuyAdvSell.selling_or_giving)
        await message.answer('Do you have something to sell or offer?', reply_markup=kb.sell_or_give)
    elif message.from_user.id in premium_list or message.from_user.id in my_admin_list:
        await state.set_state(BuyAdvSell.selling_or_giving)
        await message.answer('Do you have something to sell or offer?', reply_markup=kb.sell_or_give)
    else:
        await message.answer('You have already submitted 3 ads.\nTo submit more than 3 ads, you need to purchase a premium subscription.', reply_markup=kb.main_menu)

# Sell/Offer
@user_router.message(BuyAdvSell.selling_or_giving)
async def select_sell_or_give(message: Message, state: FSMContext):
    if message.text == 'For sale 📦': 
        await state.set_state(ForSaleCategory.adding_category_sell)
        await message.answer('Select an ad category.', reply_markup=kb.add_sell)
    elif message.text == 'Offer 🤝🏻':
        await state.set_state(OfferCategory.adding_category_give)
        await message.answer('Select an ad category.', reply_markup=kb.add_give)
    elif message.text == 'Back to the main menu ⬅️':
        await state.set_state(BuyAdvSell.begin_work)
        await message.answer('Main menu.', reply_markup=kb.main_menu)
    else:
        await message.answer('There is no such option. Try again!')

# Category For sale
@user_router.message(ForSaleCategory.adding_category_sell, F.text)
async def new_advertisement(message: Message, state: FSMContext):
    if message.text in ['Category 1', 'Category 2', 'Category 3']:
        await state.update_data(category=message.text)
        await state.set_state(ForSaleCategory.adding_text_sell)
        await message.answer(text='Enter the text of the ad starting with "For sale..."', reply_markup=kb.get_back)
    elif message.text == 'Go back 🔙':
        await state.set_state(BuyAdvSell.selling_or_giving)
        await message.answer('Do you have something to sell or offer?', reply_markup=kb.sell_or_give)
    else:
        await message.answer('There is no such option. Try again!')

# Category Offer
@user_router.message(OfferCategory.adding_category_give, F.text)
async def new_advertisement(message: Message, state: FSMContext):
    if message.text in ['Category 4', 'Category 5', 'Category 6']:
        await state.update_data(category=message.text)
        await state.set_state(OfferCategory.adding_text_give)
        await message.answer(text='Enter the text of the ad starting with "I offer..."', reply_markup=kb.get_back)
    elif message.text == 'Go back 🔙':
        await state.set_state(BuyAdvSell.selling_or_giving)
        await message.answer('Do you have something to sell or offer?', reply_markup=kb.sell_or_give)
    else:
        await message.answer('There is no such option. Try again!')

# Text of ad for sale
@user_router.message(ForSaleCategory.adding_text_sell, F.text)
async def text_added(message: Message, state: FSMContext):
    if len(message.text) >= 8 and message.text.lower().startswith('for sale'):
        await state.update_data(added_text=message.text)
        await state.set_state(ForSaleCategory.adding_price_sell)
        await message.answer('Add price', reply_markup=kb.get_back)     
    elif message.text == "Go back 🔙":
        await state.set_state(ForSaleCategory.adding_category_sell)
        await message.answer('Select an ad category.', reply_markup=kb.add_sell)
    else:
        await message.reply('The ad text must start with "For Sale" and have more than 8 characters.')

# Text of offer ad
@user_router.message(OfferCategory.adding_text_give, F.text)
async def text_added(message: Message, state: FSMContext):
    if len(message.text) >= 8 and message.text.lower().startswith('i offer'):
        await state.update_data(added_text=message.text)
        await state.set_state(OfferCategory.adding_price_give)
        await message.answer('Add price', reply_markup=kb.get_back)
    elif message.text == "Go back 🔙":
        await state.set_state(OfferCategory.adding_category_give)
        await message.answer('Select an ad category.', reply_markup=kb.add_give)
    else:
        await message.reply('The text of the ad must start with "I Offer" and have more than 8 characters')   

# Adding price for sale
@user_router.message(ForSaleCategory.adding_price_sell, F.text)
async def price_added(message: Message, state: FSMContext):
    if message.text == 'Go back 🔙':
        await state.set_state(ForSaleCategory.adding_text_sell)
        await message.answer('Enter the text of the ad starting with "For sale..."', reply_markup=kb.get_back)
    elif message.text:
        await state.update_data(added_price=message.text)
        await state.set_state(ForSaleCategory.adding_photo_sell)
        await message.answer('Add one photo of the offer', reply_markup=kb.get_back)
    else:
        await message.answer('Try again!')
        
# Adding price of offer ad
@user_router.message(OfferCategory.adding_price_give, F.text)
async def price_added(message: Message, state: FSMContext):
    if message.text == 'Go back 🔙':
        await state.set_state(OfferCategory.adding_text_give)
        await message.answer('Enter the text of the ad starting with "I offer..."', reply_markup=kb.get_back)
    elif message.text:
        await state.update_data(added_price=message.text)
        await state.set_state(OfferCategory.adding_photo_give)
        await message.answer('Add one photo of the offer', reply_markup=kb.get_back)
    else:
        await message.answer('Try again!')

# Adding photo for sale
@user_router.message(ForSaleCategory.adding_photo_sell)
async def photo_added(message: Message, state: FSMContext, session: AsyncSession):
    user_data1 = await state.get_data()
    if message.text == 'Go back 🔙':
        await state.set_state(ForSaleCategory.adding_price_sell)
        await message.answer('Add price', reply_markup=kb.get_back)
    elif message.text:
        await message.reply('It must be a photo. Try again!')
    else:
        await state.update_data(added_photo=message.photo[-1].file_id)
        user_data = await state.get_data()
        await orm_add_adv(session, user_data, message)
        await message.answer('Your ad has been successfully published!🔽')
        await message.answer_photo(
                    photo=user_data["added_photo"],
                    caption=f'\nCategory: {user_data["category"]}' + f'\nText: {user_data["added_text"]}' +
                    f'\nPrice: {user_data["added_price"]}',
                    reply_markup=kb.main_menu
                    )
        await state.set_state(BuyAdvSell.begin_work)

# Adding photo of offer ad
@user_router.message(OfferCategory.adding_photo_give)
async def photo_added(message: Message, state: FSMContext, session: AsyncSession):
    user_data1 = await state.get_data()
    if message.text == 'Go back 🔙':
        await state.set_state(OfferCategory.adding_price_give)
        await message.answer('Add price', reply_markup=kb.get_back)
    elif message.text:
        await message.reply('It must be a photo. Try again!')
    else:
        await state.update_data(added_photo=message.photo[-1].file_id)
        user_data = await state.get_data()
        await orm_add_adv(session, user_data, message)
        await message.answer('Your ad has been successfully published!🔽')
        await message.answer_photo(
                    photo=user_data["added_photo"],
                    caption=f'\nCategory: {user_data["category"]}' + f'\nText: {user_data["added_text"]}' +
                    f'\nPrice: {user_data["added_price"]}',
                    reply_markup=kb.main_menu
                    )
        await state.set_state(BuyAdvSell.begin_work)