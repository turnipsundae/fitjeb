from crawl.models import Workout, Benchmark, Crawled
from crawl import settings as crawler_settings
from crawl.regexutils import TITLE_RE, UOM_RE, GENDER_RE, RX_RE
from crawl.regexutils import get_score_re, TIME_SCORE_RE, REPS_SCORE_RE#, WT_SCORE_RE
from crawl.regexutils import STD_UOM_TIME, STD_UOM_REPS

from datetime import datetime, timedelta

import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def get_workout_info(browser):
    # get title and description from meta tags by
    # examining property and content attributes.
    tags = browser.find_elements_by_tag_name('meta')
    # build a dictionary of the property value and content value
    info = {t.get_attribute('property') : t.get_attribute('content') for
        t in tags if t.get_attribute('property')}
    # the title is usually generic, like Monday MMDDYYYY
    # so look for a better name in the og:description, usually between
    # double astricks like **WORKOUT**. Otherwise, use the og:title.
    info['better_title'] = TITLE_RE.search(info['og:description'])
    if info['better_title']:
        info['better_title'] = info['better_title'].group(1)
    # Get unit of measure for workout results. Default to empty string.
    info['uom'] = UOM_RE.search(info['og:description']) or ""
    if info['uom']:
        info['uom'] = info['uom'].group(1)

    return info['better_title'] or info['og:title'], info['og:description'], info['uom']

def get_comments(browser):
    # comments are displayed under class name and class text,
    # under the ids comments/commentsContainer/.../comment-partial,
    # so just grab all of the class names and class text.
    # names = browser.find_elements_by_class_name('name')
    comments = browser.find_elements_by_class_name('text')

    # and zip them into a dictionary. Later use a generator.
    return comments

def get_benchmarks(comments, uom):
    # Comments show individual results.
    # Scrape each comment for gender, age, height, weight, results
    # Then produce benchmarks.
    male = {"gender": "M", "total_rxd":0, 
        "min_age":0, "avg_age":0, "max_age":0,
        "min_score":None, "avg_score":0, "max_score":0, 
        "total_score":0, "total_attempts":0,
    }
    female = {"gender": "F", "total_rxd":0, 
        "min_age":0, "avg_age":0, "max_age":0,
        "min_score":None, "avg_score":0, "max_score":0, 
        "total_score":0, "total_attempts":0,
    }

    benchmarks = {"M": male, "F": female}
    SCORE_RE, std_uom = get_score_re(uom)
    if not SCORE_RE:
        return None

    for c in comments:
        text = c.text
        # find gender by looking at first character from regex
        gender = GENDER_RE.search(text)
        if gender:
            gender = gender.group(1).upper()[0]
        # find Rx
        rx = RX_RE.search(text)
        # find scores Rx only
        score = SCORE_RE.search(text)
        if score and gender and rx:
            if std_uom == STD_UOM_TIME:
                score = score.group(1).split(":")
                score = int(score[0]) + int(score[1]) / 60
            elif std_uom == STD_UOM_REPS:
                score = int(score.group(1))
            benchmarks[gender]['total_score'] += score
            benchmarks[gender]['total_rxd'] += 1
            if score > benchmarks[gender]['max_score']:
                benchmarks[gender]['max_score'] = score
            if not benchmarks[gender]['min_score'] or score < benchmarks[gender]['min_score']:
                benchmarks[gender]['min_score'] = score

        # elif score_re == 'WT_SCORE_RE' and gender:
        #     score = WT_SCORE_RE.search(text)

    for gender in benchmarks:
        if benchmarks[gender]["total_rxd"] > 0:
            benchmarks[gender]["avg_score"] = benchmarks[gender]["total_score"] / benchmarks[gender]["total_rxd"]
        # find age

    return benchmarks

def get_page(date=datetime.now()):
    """Returns a browser with crossfit.com page open"""

    # initialize a web browser
    browser = webdriver.PhantomJS(service_log_path=os.path.devnull)
    # ensure we wait for DOM to populate
    browser.implicitly_wait(10)
    # The url for workouts of the days are formatted as
    # https://www.crossfit.com/workouts/2016/01/15
    # where the last three parameters are year, month, day.
    url = crawler_settings.CROSSFIT_WOD_URL + "/{:02d}/{:02d}/{:02d}".format(date.year, date.month, date.day)

    # open the page
    browser.get(url)
    
    return browser

def save_old_wod(date):
    """
    Get the workout of the day for the given date and
    save it as a Workout Model in the Database.
    """
    # get the date and compare it to database
    # if date in db, increment by one as long as new date <= today
    existing_wod = None
    while Crawled.objects.filter(date=date.date()).exists() and date.date() < datetime.now().date():
        date += timedelta(1)
        existing_wod = True

    # scrape the page
    page = get_page(date)
    title, description, uom = get_workout_info(page)
    url = page.current_url
    comments = get_comments(page)
    benchmarks = get_benchmarks(comments, uom)
    page.quit()

    # if WOD already exists, overwrite benchmarks vs creating new
    w = Workout.objects.filter(link=url)
    if w.exists() and benchmarks:
        w = w.get()
        for i in benchmarks:
            b = w.benchmark_set.filter(gender=benchmarks[i]["gender"]).get()
            b.min_score = benchmarks[i]["min_score"]
            b.avg_score = benchmarks[i]["avg_score"]
            b.max_score = benchmarks[i]["max_score"]
            b.total_rxd = benchmarks[i]["total_rxd"]
            b.total_attempts = benchmarks[i]["total_attempts"]
    else:
        workout = Workout(
            title=title,
            description=description,
            uom=uom,
            link=url
        )
        workout.save()
        
        if benchmarks:
            for i in benchmarks:
                benchmark = Benchmark(
                    workout=workout,
                    gender=benchmarks[i]["gender"],
                    min_age=0,
                    avg_age=0,
                    max_age=0,
                    min_score=benchmarks[i]["min_score"] or benchmarks[i]["max_score"],
                    avg_score=benchmarks[i]["avg_score"],
                    max_score=benchmarks[i]["max_score"],
                    total_rxd=benchmarks[i]["total_rxd"],
                    total_attempts=benchmarks[i]["total_attempts"],
                    uom="",
                )
                benchmark.save()

        crawled = Crawled(
            link=url,
            date=date.date(),
            success="True"
        )
        crawled.save()
