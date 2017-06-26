from crawl.models import Workout, Benchmark
from crawl.regexutils import TITLE_RE, UOM_RE, GENDER_RE, RX_RE
from crawl.regexutils import get_score_re, TIME_SCORE_RE, REPS_SCORE_RE
from crawl.regexutils import STD_UOM_TIME, STD_UOM_REPS

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import os
from datetime import datetime, timedelta
from decimal import *

def get_page(base_url, date=datetime.now()):
    """Returns a browser with crossfit.com page open"""
    # initialize a web browser
    browser = webdriver.PhantomJS(service_log_path=os.path.devnull)
    # ensure we wait for DOM to populate
    browser.implicitly_wait(10)
    # The url for workouts of the days are formatted as
    # https://www.crossfit.com/workouts/2016/01/15
    # where the last three parameters are year, month, day.
    url = "{}/{:02d}/{:02d}/{:02d}".format(base_url, date.year, date.month, date.day)
    # open and return the page
    browser.get(url)
    return browser

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
    # Get url again
    info['url'] = browser.current_url
    # Return a better title if available, description and uom
    return info['better_title'] or info['og:title'], info['og:description'], info['uom'], info['url']

def get_comments(browser):
    # comments are displayed under class name and class text,
    # under the ids comments/commentsContainer/.../comment-partial,
    # so just grab all of the class names and class text.
    # names = browser.find_elements_by_class_name('name')
    comments = browser.find_elements_by_class_name('text')
    # and zip them into a dictionary. Later use a generator.
    return comments

def get_benchmarks(comments, uom):
    """
    Comments show individual results.
    Scrape each comment for gender, age, height, weight, results
    Then produce benchmarks.
    """
    # Use UOM to determine what kind of words to look
    # for in the comment results. If no UOM e.g. rest day,
    # exit the crawl.
    SCORE_RE, std_uom = get_score_re(uom)
    if not SCORE_RE: return None
    # Set up 6 benchmarks: Male, Female, Either, and
    # then Rx and non-Rx versions of both.
    benchmarks = {g : {r : None for r in ["RX", "Maybe"]} for g in ["M", "F", "E"]}
    for gender in benchmarks:
        for rx in benchmarks[gender]:
            benchmarks[gender][rx] = Benchmark(workout=None, gender=gender,
                min_age=0, avg_age=0, max_age=0,
                min_score=None, avg_score=None, max_score=0, total_score=0,
                rx=rx, count=0, uom=uom,)
    # Extract gender, Rx yes/no, score from each comment
    for c in comments:
        # Unwrap comment text
        text = c.text
        # find gender by looking at first character from regex
        gender = GENDER_RE.search(text)
        gender = gender.group(1).upper()[0] if gender else "E"
        # find Rx
        rx = RX_RE.search(text)
        rx = "RX" if rx else "Maybe"
        # Catalogue the scores
        score = SCORE_RE.search(text)
        if score:
            if std_uom == STD_UOM_TIME:
                score = score.group(1).split(":")
                score = int(score[0]) + int(score[1]) / 60
            elif std_uom == STD_UOM_REPS:
                score = int(score.group(1))
            benchmarks[gender][rx].total_score += score
            benchmarks[gender][rx].count += 1
            if score > benchmarks[gender][rx].max_score:
                benchmarks[gender][rx].max_score = score
            if not benchmarks[gender][rx].min_score:
                benchmarks[gender][rx].min_score = benchmarks[gender][rx].max_score
            elif score < benchmarks[gender][rx].min_score:
                benchmarks[gender][rx].min_score = score
    # Calculate averages for each gender and rx
    for gender in benchmarks:
        for rx in benchmarks[gender]:
            if benchmarks[gender][rx].count > 0:
                benchmarks[gender][rx].avg_score = benchmarks[gender][rx].total_score / benchmarks[gender][rx].count
            else:
                benchmarks[gender][rx].avg_score = 0
                benchmarks[gender][rx].min_score = 0
    print (benchmarks)
    return benchmarks

def save_wod(base_url, date):
    """
    Get the workout of the day for the given date and
    save it as a Workout Model in the Database.
    """
    # get the date and compare it to database
    # if date in db, increment by one as long as new date <= today
    while Workout.objects.filter(date=date.date()).exists() and date.date() < datetime.now().date():
        date += timedelta(1)
    # scrape the page
    page = get_page(base_url, date)
    title, description, uom, url = get_workout_info(page)
    comments = get_comments(page)
    benchmarks = get_benchmarks(comments, uom)
    page.quit()
    # if WOD already exists, overwrite benchmarks vs creating new
    w = Workout.objects.filter(link=url)
    if w.exists():
        w = w.get()
    else:
        w = Workout(title=title, description=description,
            uom=uom, link=url, date=date)
        w.save()
    if benchmarks:
        for gender in benchmarks:
            for rx in benchmarks[gender]:
                benchmarks[gender][rx].workout = w
                benchmarks[gender][rx].save()
