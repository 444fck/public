from django.shortcuts import render, redirect
import mysql.connector
from .scheduler import scheduler
import feedparser
from datetime import datetime
from django.views import View
from django.http import HttpResponse
import threading
from .models import Configuration, FeedBack

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

import hashlib

# Create your views here.
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hoangphuc34",
        database="nckh"
    )
cursor = mydb.cursor()

#global var
default = 10000
#import config from db
query1= "SET SQL_SAFE_UPDATES = 0;"
cursor.execute(query1)
query = """SELECT `time` FROM `setting`;"""
cursor.execute(query)
x = cursor.fetchall()
for row in x:
   default = int(row[0])

def auto_del_dup():
    auto = """delete t1 FROM web t1 INNER  JOIN web t2
              WHERE t1.id > t2.id  AND t1.title = t2.title
              AND t1.link = t2.link AND t1.published = t2.published;"""
    cursor.execute(auto)
    mydb.commit()
    print("================Task del running=================")
scheduler.add_job(auto_del_dup, 'interval', seconds=600)


class JobScheduler:
    jobs = {}
    links = {}
    paused = False

    @classmethod
    def add_job(cls, url, interval):
        job = scheduler.add_job(cls.job_function, 'interval', seconds=interval, args=[url])
        cls.jobs[url] = job

    @classmethod
    def add_job_misp(cls, url, interval):
        job = scheduler.add_job(cls.job_function_misp, 'interval', seconds=interval, args=[url])
        cls.jobs[url] = job

    @classmethod
    def remove_job(cls, url):
        if url in cls.jobs:
            job = cls.jobs.pop(url)
            job.remove()

    @classmethod
    def pause(cls):
        cls.paused = True

    @classmethod
    def resume(cls):
        cls.paused = False

    @staticmethod
    def job_function(url):
        if url == 'http://www.zone-h.org/rss/specialdefacements':
            if not JobScheduler.paused:
                feed = feedparser.parse(url)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time =", current_time)
                sql = """INSERT IGNORE INTO web(title, link, published)
                        VALUES (%(title)s, %(link)s, %(published)s)"""

                for entry in feed.entries:
                    link_hash = hashlib.md5(entry.link.encode('utf-8')).hexdigest()
                    if link_hash not in JobScheduler.links:
                        data = {
                            'title': entry.title,
                            'link' : entry.link,
                            'published' : entry.published,
                        }
                        cursor.execute(sql, data)
                        mydb.commit()
                        JobScheduler.links[link_hash] = entry.link
                        print('Added new link:', entry.link)
                    else:
                        print('Duplicated link:', entry.link)
                print('zone-h task is running')
            else:
                print('zone-h task is paused')
        else:
            print('Unkown task')

    @staticmethod
    def job_function_misp(url):
        if url == 'https://www.example.com/misp':
            if not JobScheduler.paused:
                print('misp task is running')
            else:
                print('misp task is paused')
        else:
            print('Unkown task')

def scheduler_start_zoneh():
    def run_scheduler():
        JobScheduler.add_job('http://www.zone-h.org/rss/specialdefacements', interval=default)
        scheduler.start()
    thread = threading.Thread(target=run_scheduler)
    thread.start()

def scheduler_start_misp():
    def run_scheduler():
        JobScheduler.add_job_misp('https://www.example.com/misp', interval=default)
        scheduler.start()
    thread = threading.Thread(target=run_scheduler)
    thread.start()

def pause_job(request):
    JobScheduler.pause()
    return HttpResponse('Job paused')

def remuse_job(request):
    JobScheduler.resume()
    return HttpResponse('Job remused')

def config(request):
    global default
    config = default
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    selected_source = request.POST.get('source', 'zoneh')
    config = request.POST.get("config")
    if config and config.isdigit():
        default = int(config)
        test = int(config)
        timesql = "UPDATE `setting` SET time=" + str(config) + " WHERE name='admin';"
        cursor.execute(timesql)
        mydb.commit()
        if selected_source == 'misp':
            print('this is misp')
            JobScheduler.remove_job('http://www.zone-h.org/rss/specialdefacements')
            scheduler_start_misp()
        elif selected_source == 'zoneh':
            print('this is zoneh')
            JobScheduler.remove_job('https://www.example.com/misp')
            JobScheduler.add_job('http://www.zone-h.org/rss/specialdefacements', test)
        new_config = Configuration(firstname=firstname, lastname=lastname, email=email, config=default, source=selected_source)
        new_config.save()
        print(new_config.firstname, new_config.lastname, new_config.email, new_config.config, new_config.source)
        for job_name , job in JobScheduler.jobs.items():
            print(job_name, job.trigger)
    return render(request, 'function/config.html', {'context':selected_source, 'default':default})



def feed_search(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        if searched:
            sql = "SELECT id, link FROM web WHERE title LIKE %s"
            cursor.execute(sql, ('%' + searched + '%',))
            result = cursor.fetchall()
            if result:
                return render(request, 'function/search.html', {'result' : result})
            else:
                return render(request, 'function/search.html', {'result': result})
        else:
            return render(request, 'function/search.html', {})
    else:
        return render(request, 'function/search.html',{})

def list(request):
    auto = """delete t1 FROM web t1 INNER  JOIN web t2
              WHERE t1.id > t2.id  AND t1.title = t2.title
              AND t1.link = t2.link AND t1.published = t2.published;"""
    cursor.execute(auto)

    page = request.GET.get('page', 1)
    start = (int(page) - 1) * 10

    list = f" SELECT * FROM WEB LIMIT {start}, 10;"
    cursor.execute(list)
    result = cursor.fetchall()

    total = "SELECT COUNT(*) FROM WEB;"
    cursor.execute(total)
    count = cursor.fetchone()[0]
    pages = range(1, int(count / 10) + 2)

    mydb.commit()
    return render(request, 'function/list.html',{'result': result, 'pages':pages})

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback = request.POST.get('feedback')
        if name and email and feedback:
            new_feedback = FeedBack(name=name, email=email, feedback=feedback)
            new_feedback.save()
            return render(request, 'function/feedback.html')
    return render(request, 'function/feedback.html')