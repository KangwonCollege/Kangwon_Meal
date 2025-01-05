import datetime

import asyncio
from bs4 import BeautifulSoup

from .school_meal_type import SchoolMealType
from ..base_meal import BaseMeal
from ..meal_response import MealResponse

from utils.weekday import weekday


class SchoolMeal(BaseMeal):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super(SchoolMeal, self).__init__("https://wwwk.kangwon.ac.kr", loop=loop)

        self.data: dict[
            SchoolMealType,
            dict[
                datetime.date, dict[
                    str, MealResponse | None
                ]
            ]
        ] = {
            building: dict() for building in list(SchoolMealType)
        }

    async def meal(self, building: SchoolMealType, date: datetime.date = None) -> dict[str, MealResponse]:
        if building not in self.data:
            self.data[building] = dict()

        if date not in self.data[building]:
            await self.update(building, date)
        return self.data[building][date]

    async def update(self, building: SchoolMealType, date: datetime.date = None):
        if date is None:
            date = datetime.date.today()

        weekday_response = weekday(date)
        params = {
            "sc1": building.value,
            "sc5": (weekday_response.Monday + datetime.timedelta(days=-1)).strftime("%Y%m%d")
        }
        response = await self.requests.post(
            "https://wwwk.kangwon.ac.kr/www/selecttnCafMenuListWU.do",
            raise_on=True,
            params=params
        )
        soup = BeautifulSoup(response.data, 'html.parser')

        for br in soup.find_all("br"):
            br.replace_with("\n")

        body = soup.find("main", {"class": "colgroup"}).find("div", {"id": "contents"})

        # Warning: This restaurant list was compiled as of the 2023 school year.
        # These name may be changed.
        restaurant_name_list = {
            SchoolMealType.CheonJi: ["한식", "양식", "스넥", "멀티샵(2~3종)랜덤/간식", "특식(랜덤)"],
            SchoolMealType.BaekNok: ["백록한라산", "THE진국", "양식", "스넥", "한그릇/한그릇 플러스", "백록정식"],
            SchoolMealType.Duri: ["크누정식", "뚝배기정식", "돈가스&파스타", "우동", "크누석식"]
        }

        # School Meal Information does not exist.
        if body.find('div', {"class": "over_scroll_table"}) is None:

            for index in range(7):
                meal_date = weekday_response.Monday + datetime.timedelta(days=index)
                self.data[building][meal_date] = {
                    restaurant_name: MealResponse()
                    for restaurant_name in restaurant_name_list[building]
                }
            return self.data

        table = body.find('div', {"class": "over_scroll_table"}).find('table')
        tbody = table.find('tbody')

        restaurant_name = None
        restaurant_name_max_key = 0
        for index, value in enumerate(tbody.find_all("tr")):
            if index >= restaurant_name_max_key:
                restaurant_name = None

            if restaurant_name is None:
                restaurant_name_tag = value.find('th', {"scope": "rowgroup"})
                restaurant_name = restaurant_name_tag.text
                restaurant_name_max_key = index + int(restaurant_name_tag.get("rowspan", 1))
            meal_type = value.find('th', {"rowspan": None}).text
            for j, meal_info in enumerate(value.find_all("td")):
                meal_date = weekday_response.Monday + datetime.timedelta(days=j)
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
            meal_date = weekday_response.Sunday + datetime.timedelta(days=-(1 - index))
            self.data[building][meal_date] = {
                restaurant_name: MealResponse()
                for restaurant_name in restaurant_name_list[building]
            }
