import datetime
import aiohttp

from ahttp_client import BodyJson, RequestCore, request, Query, Header
from bs4 import BeautifulSoup
from typing import Annotated, Optional

from app.services.base_meal import BaseMeal
from app.models.enumeration.school_meal_type import SchoolMealType
from app.models.meal_response import MealResponse
from app.utils.weekday import Weekday


class SchoolMeal(BaseMeal):
    def __init__(self):
        super().__init__("https://www.kangwon.ac.kr")
        self.data: dict[
            SchoolMealType,
            dict[datetime.date, dict[str, MealResponse | None]]
        ] = {building: dict() for building in list(SchoolMealType)}

    async def meal(self, building: SchoolMealType, date: datetime.date = None) -> dict[str, MealResponse]:
        if date is None:
            date = datetime.date.today()
        if building not in self.data:
            self.data[building] = dict()
        if date not in self.data[building]:
            await self._fetch_meal(building=building, date=date)
        return self.data[building][date]

    @request("POST", "/ko/extn/37/wkmenu-mngr/list.do")
    async def _fetch_meal(
        self,
        response: aiohttp.ClientResponse,
        building: Annotated[SchoolMealType, Query],
        date: Annotated[Optional[datetime.date], Query] = None,
    ):
        if date is None:
            date = datetime.date.today()
        weekday = Weekday(date)
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')

        for br in soup.find_all("br"):
            br.replace_with("\n")

        body = soup.find("main", {"id": "sub-wrapper"}).find("div", {"class": "sub-contents-container"})

        restaurant_name_list = {
            SchoolMealType.CheonJi: ["멀티샵", "스낵", "양식", "천지 백두산", "하루 돈까스", "하루 정식"],
            SchoolMealType.BaekNok: ["Asian(누들,그릴,중식)", "Global(돈가스)", "백록소반", "백록화담(직화)", "천원의아침밥"],
            SchoolMealType.Duri: ["크누정식", "크누석식", "크누그라탕", "천원의아침밥", "뚝배기정식", "돈가스세트"]
        }

        for index in range(7):
            meal_date = weekday.monday + datetime.timedelta(days=index)
            self.data[building][meal_date] = {
                name: MealResponse() for name in restaurant_name_list[building]
            }

        # Return Empty data
        if body.find('div', {"class": "meal-container"}) is None:
            return self.data

        for index, value in enumerate(body.find_all("div", {"class": "meal-container"})):
            restaurant_name_tag = value.find('h5', {"class": "sub-content-title"})
            raw_restaurant_name = restaurant_name_tag.text
            restaurant_name = [
                name
                for name in restaurant_name_list[building] + [raw_restaurant_name]
                if raw_restaurant_name.startswith(name)
            ][0]

            table_container = value.find('div', {"class": "table-container"})
            # thead = table_container.find('thead')
            tbody = table_container.find('tbody')

            # date_translate = thead.find_all('th', {"class": None})

            for j, meal_type_tag in enumerate(tbody.find_all('tr')):
                meal_type = meal_type_tag.find('td', {"class": "time-th"}).text

                for k, meal_info in enumerate(value.find_all("td", {"class": "menu-cell"})):
                    meal_date = weekday.monday + datetime.timedelta(days=k)
                    if meal_date not in self.data[building]:
                        self.data[building][meal_date] = dict()
                    if restaurant_name not in self.data[building][meal_date]:
                        self.data[building][meal_date][restaurant_name] = MealResponse()

                    if meal_type == "아침":
                        self.data[building][meal_date][restaurant_name].breakfast = meal_info.text.split('\n')
                    elif meal_type == "점심":
                        self.data[building][meal_date][restaurant_name].lunch = meal_info.text.split('\n')
                    elif meal_type == "저녁":
                        self.data[building][meal_date][restaurant_name].dinner = meal_info.text.split('\n')

        for index in range(2):
            meal_date = weekday.sunday + datetime.timedelta(days=-(1 - index))
            self.data[building][meal_date] = {
                name: MealResponse() for name in restaurant_name_list[building]
            }
        return self.data

    async def before_request(self, request_obj: RequestCore, path: str):
        date: datetime.date = request_obj.params.pop("date") if "date" in request_obj.params.keys() else datetime.date.today()
        building: SchoolMealType = request_obj.params.pop("building")

        body_form = aiohttp.FormData()
        body_form.add_field("caftrCd", building.value)
        body_form.add_field("targetDate", (Weekday(date).monday + datetime.timedelta(days=-1)).strftime("%Y%m%d"))
        body_form.add_field("campusCd", "1")
        request_obj.body = body_form

        return request_obj, path
