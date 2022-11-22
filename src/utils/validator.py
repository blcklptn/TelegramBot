from email_validator import validate_email, EmailNotValidError

async def check_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError as ex:
        return False


async def check_name(name: str) -> bool:
    if len(name.split(' ')) == 3:
        return True
    else:
        return False


async def check_revenue(revenue) -> bool:
    if isinstance(revenue, int):
        return True
    else:
        return False

async def file_extension(file_name: str) -> str:
    extension = file_name.split('.')[-1]
    if extension == '.xlsx':
        return 'excel'
    elif extension == '.xls':
        return 'excel'
    elif extension == '.json':
        return 'json'
    return 'unknown'

