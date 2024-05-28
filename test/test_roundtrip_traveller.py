import asyncio
import re

import pytest
from playwright.async_api import async_playwright, expect
from src.travellers import Traveller
from unittest import TestCase


@pytest.fixture
def travel_list():
    return Traveller(input="../test/input.yml")


class TestExample:

    @pytest.mark.asyncio
    @pytest.mark.order(1)
    async def test_launch_search(self, travel_list):
        travelPlan = travel_list.travelPlan
        roundTrip = travelPlan["TravelPlan"]["roundTrip"]
        print("Round Trip = ", roundTrip)

        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)
            page = await self.browser.new_page()
            await page.goto("https://flightbookings.airnewzealand.co.nz/vbook/actions/search")

            if roundTrip:
                await page.get_by_label("Return trip").check()
                print("Round Trip flag is selected")
            else:
                await page.get_by_text("One‐way trip").click()
                print("One-way Trip flag is selected")

            await page.get_by_label("From airport or city").click()
            await page.get_by_label("From airport or city").fill("auc")
            await page.get_by_role("option", name=re.compile("Auckland")).first.click()

            await page.get_by_label("To airport or city").click()
            await page.get_by_label("To airport or city").press_sequentially("qu")
            await page.get_by_role("option", name="Queenstown").click()

            # await page.get_by_label("Leave on date, in day day").click()
            await page.get_by_label("Leave on date, in day day").fill("29/05")
            # await page.locator("#calendarpanel-0").get_by_text("28").nth(1).click()
            if roundTrip:
                await page.get_by_label("Return on date, in day day").click()
                await page.locator("#calendarpanel-0").get_by_text("30").nth(1).click()
            await page.context.storage_state(path="temp/val.json")
            await page.screenshot(path="temp/tc-1.png")
            await page.get_by_role("button", name="Search").click()
            await page.context.storage_state(path="temp/val2.json")

            # await page.pause()

    @pytest.mark.asyncio
    @pytest.mark.order(2)
    async def test_itenary(self, travel_list):
        travelPlan = travel_list.travelPlan
        roundTrip = travelPlan["TravelPlan"]["roundTrip"]

        URL = "https://flightbookings.airnewzealand.co.nz/vbook/actions/selectitinerary"

        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)

            page = await self.browser.new_page(storage_state="temp/val2.json")
            await page.goto(URL)
            print("Url: >> ", page.url)
            expect(page.get_by_text("Select your flight to"))

            if roundTrip:
                # select start flight
                await page.locator('//*[@id="flightSortOptions-viewpoint-DOMESTIC-1"]/div[2]').click()
                await page.locator(
                    '//*[@id="viewpoint-DOMESTIC-1"]/div[3]/fieldset/div[1]/div/div/div/div/div[1]').click()

                # select return flight
                expect(page.get_by_text("Select your return flight to"))
                await page.locator('//*[@id="flightSortOptions-viewpoint-DOMESTIC-2"]/div[2]').click()
                await page.locator(
                    '//*[@id="viewpoint-DOMESTIC-2"]/div[3]/fieldset/div[1]/div/div/div[1]/div[1]/div[1]').click()
            else:
                await page.get_by_label("Flight sort options").get_by_text("Departs").click()
                await page.locator(
                    '//*[@id="viewpoint-DOMESTIC-1"]/div[3]/fieldset/div[1]/div/div/div/div/div[1]').click()

            expect(page.get_by_role("button", name="Continue")).to_be_enabled()
            await page.get_by_role("button", name="Continue").click()
            await page.context.storage_state(path="temp/val3.json")
            # await page.pause()

    @pytest.mark.asyncio
    @pytest.mark.order(3)
    async def test_single_traveller(self, travel_list):
        travelPlan = travel_list.travelPlan
        roundTrip = travelPlan["TravelPlan"]["roundTrip"]
        print(travelPlan["Travellers"])
        URL = "https://flightbookings.airnewzealand.co.nz/vbook/actions/travellerdetails"

        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)

            page = await self.browser.new_page(storage_state="temp/val3.json")
            print(page.url)
            print(travelPlan["Travellers"])
            await page.goto(URL)
            await page.get_by_role("heading", name="Adult").click()
            await page.get_by_text("Title").click()
            await page.get_by_label("Title").select_option("MR")
            await page.get_by_label("First name").click()
            await page.get_by_label("First name").fill(travelPlan["Travellers"][0]["firstName"])
            await page.get_by_label("Family name").click()
            await page.get_by_label("Family name").fill(travelPlan["Travellers"][0]["lastName"])
            await page.get_by_label("Membership number").click()
            await page.get_by_label("Membership number").click()
            await page.get_by_label("Mobile or Landline").click()
            await page.get_by_label("Mobile or Landline").fill(travelPlan["Travellers"][0]["phone"])
            await page.get_by_label("Email address").click()
            await page.get_by_label("Email address").fill(travelPlan["Travellers"][0]["email"])
            await page.get_by_text("Email me a reminder of this").click()
            await page.get_by_role("button", name="Continue").click()
            await page.context.storage_state(path="temp/val4.json")
            # await page.pause()

    @pytest.mark.asyncio
    @pytest.mark.order(4)
    async def test_single_traveller_extras(self, travel_list):
        travelPlan = travel_list.travelPlan
        roundTrip = travelPlan["TravelPlan"]["roundTrip"]

        URL = "https://flightbookings.airnewzealand.co.nz/vbook/actions/extras"

        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)

            page = await self.browser.new_page(storage_state="temp/val4.json")
            await page.goto(URL)
            print(page.url)

            await page.get_by_role("heading", name="Extras").click()
            await page.get_by_text("Add travel insurance").click()
            await page.locator("label").filter(has_text="No thanks, I am happy to make").click()
            await page.get_by_text("$0 $").click()
            await page.get_by_role("button", name="Continue").click()
            await page.context.storage_state(path="temp/val5.json")

    @pytest.mark.asyncio
    @pytest.mark.order(5)
    async def test_select_seat(self, travel_list):
        travelPlan = travel_list.travelPlan
        roundTrip = travelPlan["TravelPlan"]["roundTrip"]

        URL = "https://flightbookings.airnewzealand.co.nz/vbook/actions/select-your-seats"

        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)
            page = await self.browser.new_page(storage_state="temp/val5.json")
            await page.goto(URL)
            print(page.url)
            expect(page.get_by_role("heading", name="Select your seats"))

            many = page.get_by_text(re.compile(r"Available"))  # .first.click()
            print("many=", many, dir(many))
            await many.nth(1).click()
            await many.nth(2).click()

            # remainder
            # await page.get_by_role("button", name="Continue").click()
            await page.get_by_label("Seat information").get_by_role("button", name="Continue").click()
            await page.context.storage_state(path="temp/val6.json")
            # await page.pause()

    @pytest.mark.asyncio
    @pytest.mark.order(6)
    async def test_review_pay(self, travel_list):
        travelPlan = travel_list.travelPlan
        roundTrip = travelPlan["TravelPlan"]["roundTrip"]

        URL = "https://flightbookings.airnewzealand.co.nz/vbook/actions/purchasetickets"

        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)
            page = await self.browser.new_page(storage_state="temp/val6.json")
            await page.goto(URL)
            print(page.url)
            expect(page.get_by_role("heading", name="Review and pay"))
            expect(page.get_by_role("heading", name="Pay with credit"))
            await page.get_by_role("tab", name="Pay with online banking").click()
            await page.get_by_role("tab", name="Pay with credit card/travel").click()
            # Card Details - AMEX
            await page.get_by_label("Card number").click()
            await page.get_by_label("Card number").fill("345678901234564")
            await page.get_by_label("Name on card").click()
            await page.get_by_label("Name on card").fill("Tom Alter")
            await page.get_by_label("Month").select_option("1")
            await page.get_by_label("Year").select_option("2028")
            await page.get_by_label("Security code").click()
            await page.get_by_label("Security code").fill("1000")
            expect(page.get_by_role("heading", name="Final step:"))
            expect(page.get_by_text("Total to pay"))
            await page.get_by_text("Total to pay").click()
            await page.get_by_role("button", name="Pay now").click()
            await page.context.storage_state(path="temp/val7.json")
            # await page.pause()


if __name__ == "__main__":
    pytest.main()
