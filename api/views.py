from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

def notice(req):
    url = url = "https://www.uiu.ac.bd/notice/"
    response = requests.get(url)
    data_list = []

    soup = BeautifulSoup(response.text, "html.parser")
    notice_card = soup.find_all("div", class_="notice")
    
    for notice in notice_card:
        date = notice.find("span", class_="date").text.strip().split(",")[0]
        title = notice.find("div", class_="title").text.strip().capitalize()
        notice_url = notice.select(".title > a")[0]["href"].strip()

        data = {"date": date, "title": title, "url": notice_url}
        data_list.append(data)

    for data in data_list:
        res_details = requests.get(data['url'])
        soup = BeautifulSoup(res_details.text, "html.parser")
        response_details = soup.find("div", class_="notice-details").find_all("p")
        notice_details = []
        for detail in response_details:
            notice_details.append(detail.text.strip())
        notice_details = [i for i in notice_details if i != ""]
        data['details'] = notice_details

    return JsonResponse(data_list, safe=False)
