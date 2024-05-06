from aiogram.fsm.state import StatesGroup, State

# Admin FSM
class AdminMenu(StatesGroup):
    admin_begin_work = State()
    admin_chosing_category = State()
    admin_find_category = State()
    
    advertisement_to_change = None
    
    admin_update_category = State()
    admin_update_text = State()
    admin_update_price = State()
    admin_update_photo = State()

    admin_premium_settings = State()
    admin_premium_add = State()
    admin_premium_add_month = State()
    admin_premium_update = State()
    admin_premium_update_month = State()
    admin_premium_delete = State()
    admin_premium_list = State()

class AdminImage(StatesGroup):
    admin_send_image = State()