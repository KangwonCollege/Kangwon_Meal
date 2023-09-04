import aiohttp


def dict_to_form(data: dict[str, str]):
    form_data = aiohttp.FormData()
    for key, value in data.items():
        form_data.add_field(key, value)
    return form_data
