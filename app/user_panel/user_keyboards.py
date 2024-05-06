from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from app.admin_panel.admin_filter import my_admin_list

# User panel inline and reply keyboards
start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Start")]
                                         ],
                               resize_keyboard=True, input_field_placeholder='Click below...')

main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Find 🔍')],
                                          [KeyboardButton(text='Add an ad ➕'), KeyboardButton(text='Donate 💳')],
                                          [KeyboardButton(text='My ads 📢')]
                                          ],
                                resize_keyboard=True, input_field_placeholder='Select a button.')

sell_or_give = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='For sale 📦'), KeyboardButton(text='Offer 🤝🏻')],
                                             [KeyboardButton(text='Back to the main menu ⬅️')]],
                                   resize_keyboard=True, input_field_placeholder='Are you selling or offering?')

add_sell = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Category 1'), KeyboardButton(text='Category 2'), KeyboardButton(text='Category 3')],
                                         [KeyboardButton(text='Go back 🔙')]
                                         ],
                               resize_keyboard=True, input_field_placeholder='Select a category.', one_time_keyboard=True)

add_give = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Category 4'), KeyboardButton(text='Category 5'), KeyboardButton(text='Category 6')],
                                         [KeyboardButton(text='Go back 🔙')]
                                         ],
                               resize_keyboard=True, input_field_placeholder='Select a category.', one_time_keyboard=True)

add_all = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Category 1'), KeyboardButton(text='Category 2'), KeyboardButton(text='Category 3')],
                                        [KeyboardButton(text='Category 4'), KeyboardButton(text='Category 5'), KeyboardButton(text='Category 6')],
                                        [KeyboardButton(text='Go back 🔙')]
                                        ],
                               resize_keyboard=True, input_field_placeholder='Select a category.', one_time_keyboard=True)

find_all = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Category 1'), KeyboardButton(text='Category 2'), KeyboardButton(text='Category 3')],
                                        [KeyboardButton(text='Category 4'), KeyboardButton(text='Category 5'), KeyboardButton(text='Category 6')],
                                        [KeyboardButton(text='Back to the main menu ⬅️')]
                                        ],
                               resize_keyboard=True, input_field_placeholder='Select a category.', one_time_keyboard=True)

get_back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Go back 🔙")]
                                         ],
                               resize_keyboard=True)

remove_keyboard = ReplyKeyboardRemove()

inline_donat = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Donate at the link 💵',
                                                                           url='YOUR DONATE LINK')]])


def inline_write_to_user(user_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Write to the author ✍🏻",
                                                                           url=f"tg://user?id={user_id}")]])
    return keyboard

# Write here your main admin ID
inline_dev = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Write to the administrator ✍🏻",
                                                                        url=f"tg://user?id={my_admin_list[0]}")]])

def inline_delete_adv(id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Delete the ad",
                                                                           callback_data=f"delete_{id}")]])
    return keyboard
