from aiogram.fsm.state import StatesGroup, State

# User FSM
class BuyAdvSell(StatesGroup):
    begin_work = State()
    selling_or_giving = State()
    find_category = State()
    chosing_category = State()
    
class ForSaleCategory(StatesGroup):
    adding_category_sell = State()
    adding_text_sell = State()
    adding_price_sell = State()
    adding_photo_sell = State()
    
class OfferCategory(StatesGroup):
    adding_category_give = State()
    adding_text_give = State()
    adding_price_give = State()
    adding_photo_give = State()