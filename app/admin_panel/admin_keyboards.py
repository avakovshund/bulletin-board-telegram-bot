from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Admin panel inline and reply keyboards
admin_start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Start')]
                                         ],
                               resize_keyboard=True, input_field_placeholder='Click below...')

admin_main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Find 🔍')],
                                                [KeyboardButton(text='Premium Settings')]
                                          ],
                                resize_keyboard=True, input_field_placeholder='Choose the botton.')

admin_premium = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Add user'), KeyboardButton(text='Delete user')],
                                              [KeyboardButton(text='User`s list'), KeyboardButton(text='Continue subscription')],
                                              [KeyboardButton(text='Back to main menu ⬅️')]
                                              ],
                                    resize_keyboard=True)

admin_find_all = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Category 1'), KeyboardButton(text='Category 2'), KeyboardButton(text='Category 3')],
                                        [KeyboardButton(text='Category 4'), KeyboardButton(text='Category 5'), KeyboardButton(text='Category 6')],
                                        [KeyboardButton(text='Back to main menu ⬅️')]
                                        ],
                               resize_keyboard=True, input_field_placeholder='Choose the category.', one_time_keyboard=True)

admin_back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Get back ⬅️')]], resize_keyboard=True)

def admin_inline_menu(user_id, id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Write to author ✍🏻",
                                                                           url=f"tg://user?id={user_id}")],
                                                     [InlineKeyboardButton(text="Delete",
                                                                           callback_data=f"delete_{id}"),
                                                      InlineKeyboardButton(text="Edit",
                                                                           callback_data=f"update_{id}")]])
    return keyboard

def admin_inline_write_to_user(user_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Write to user ✍🏻",
                                                                           url=f"tg://user?id={user_id}")]])
    return keyboard