from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import json
from .helpers import get_soup

def notice(req):
    with open("api/static/notice.json", "r") as file:
        data = json.load(file)

    return JsonResponse(data, safe=False)

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
            paper_title = paper.find("h2", class_ = "paper-title").text.strip()
            publication = (
                paper.select_one(".paper-event").text.strip().split("Publication:")[1].strip()
            )
            authors = [i.text.strip() for i in paper.select(".paper-contributors span")]
            paper_tags = [i.text.strip() for i in paper.select(".paper-tags > span")]

            paper_info = {
                "year": year,
                "paper_title": paper_title,
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