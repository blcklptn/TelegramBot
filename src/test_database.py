from utils import dataspace
from models.models import Admins, Users
from utils.validator import check_email, check_name, check_revenue
import asyncio

admin = Admins(
    username = 'blcklptn',
    user_id = '123'
)

user = Users(
    FirstName = "Даниил",
    MiddleName = "Денисович",
    LastName = "Ермолаев",

    username = 'blcklptn',
    user_id = '123',
    phone_number = '+79991324369',
    email = 'blcklptn@gmail.com',

    company_name = "Салаватский Индустриальный колледж",
    revenue = 12341
)


dataspace.ManageUsers().add_user(user)
dataspace.ManageUsers().new_pay(123)