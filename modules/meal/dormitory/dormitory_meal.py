import datetime
import aiohttp
import asyncio

from ahttp_client import RequestCore, request, Query, Header
from bs4 import BeautifulSoup
from typing import Annotated, Optional

from ..base_meal import BaseMeal
from .dormitory_response import DormitoryResponse
from .dormitory_meal_type import DomitoryMealType

from utils.dict_to_form import dict_to_form
from utils.weekday import Weekday


class DormitoryMeal(BaseMeal):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super(DormitoryMeal, self).__init__("https://knudorm.kangwon.ac.kr", loop)

        self.data: dict[datetime.date, DormitoryResponse | None] = dict()

    async def meal(self, date: datetime.date = None) -> DormitoryResponse:
        if date is None:
            date = datetime.date.today()
        
        if date not in self.data:
            await self._fetch_meal(date)
        return self.data[date]

    @request("GET", "/content/K11", body=aiohttp.FormData())
    @Header.default_header("Content-Type", "application/x-www-form-urlencoded")
    async def _fetch_meal(
        self,
        response: aiohttp.ClientResponse,
        date: Annotated[Optional[datetime.date], Query] = None
    ):  
        if date is None:
            date = datetime.date.today()
        data = await response.text()
        
        soup = BeautifulSoup(data, 'html.parser')
        body = soup.find("form", {"id": "fm"}).find("div", {"class": "tab-content"})

        for dormitory_type in DomitoryMealType: # 기숙사
            dormitory_body = body.find("div", {"class": "tab-pane", "id": dormitory_type.value})
            dormitory_body_index = 1
            for index, x in enumerate(dormitory_body.find_all("h4", {"class": "sub_s_title"})):
                if x.text.endswith("생활관"):
                    dormitory_body_index = index
                    break
            
            meal_body = dormitory_body.find_all("table", {"class": "table"})[dormitory_body_index]
            meal = meal_body.find_all("tr")  # 1번(월요일) ~ 7번(일요일)
            for j, meal_info in enumerate(meal[1:]):
                meal_date = Weekday(date).monday + datetime.timedelta(days=j)
                if meal_date not in self.data:
                    self.data[meal_date] = DormitoryResponse()

                for k, meal_type in enumerate(['breakfast', 'lunch', 'dinner']): # 아침 / 점심 / 저녁
                    meal_info_day = meal_info.find_all('td')[k]
                    meal_info_day_and_type = meal_info_day.text.replace('\t', '')

                    meal_info_day_and_type = meal_info_day_and_type.strip('\n')
                    if meal_info_day_and_type == '':
                        # setattr(
                        #     getattr(self.data[meal_date], key),
                        #     meal_type, None
                        # )
                        continue
                    setattr(
                        getattr(self.data[meal_date], dormitory_type.name),
                        meal_type, meal_info_day_and_type.split('\n')
                    )
        return self.data

    async def before_request(self, request_obj: RequestCore, path: str):
        # Add default value
        request_obj.body.add_field("mode", "7301000")
        request_obj.body.add_field("bil", 1)

        date: datetime.date = request_obj.params.pop("date") if "date" in request_obj.params.keys() else datetime.date.today()
        form_date = Weekday(date + datetime.timedelta(days=7 * -1 if datetime.date.today() < date else 1))

        for key, value in {
            "next": "Y" if datetime.date.today() < date else "",
            "before": "Y" if datetime.date.today() > date else "",
            "monDay": form_date.monday,
            "sunDay": form_date.sunday
        }.items():
            request_obj.body.add_field(key, value)

        return request_obj, path
