from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import json
from .helpers import get_soup

def notice(req):
    url = "https://www.uiu.ac.bd/notice/"
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

def journal(req):
    soup = get_soup("journal")
    paper_list = []
    paper_details = soup.select("#conference-paper > div")
    
    if len(paper_details) < 1:
        paper_list.append({"message": "No papers found"})
    else:
        for paper in paper_details:
            year = paper.select("span")[0].text.strip()
            paper_url = paper.select_one("a").get("href")
            publication = (
                paper.select_one(".paper-event").text.strip().split("Publication:")[1].strip()
            )
            authors = [i.text.strip() for i in paper.select(".paper-contributors span")]
            paper_tags = [i.text.strip() for i in paper.select(".paper-tags > span")]

            paper_info = {
                "year": year,
                "paper_url": paper_url,
                "publication": publication,
                "authors": authors,
                "paper_tags": paper_tags,
            }

            paper_list.append(paper_info)
    
    return JsonResponse(paper_list, safe=False)

def jobs(req):
    with open("api/static/jobs.json", "r") as file:
        jobs = json.load(file)
    return JsonResponse(jobs, safe=False)