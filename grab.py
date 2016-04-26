#coding=utf-8

from flask import Flask,render_template
from selenium import webdriver
from PIL import Image
import time
import os
import StringIO
import base64

app=Flask(__name__)

@app.route('/getweather')
def getweather():
    url='http://www.jma.go.jp/jp/week/347.html'
    driver=webdriver.PhantomJS()
    driver.set_window_size(1280,800)
    driver.get(url)

    #----------------------execute js---------------------
    jscode='''
    document.getElementById("infotablefont").caption.innerHTML='週間天気予報：佐賀県';
    '''
    driver.execute_script(jscode)
    # time.sleep(1)

    #----------------------find element-------------------
    imgelement=driver.find_element_by_id('infotablefont')
    location=imgelement.location
    size=imgelement.size

    imgelement2=driver.find_element_by_class_name('forecast-bottom')
    donesize=imgelement2.size

    data=driver.get_screenshot_as_png()
    im = Image.open(StringIO.StringIO(data))
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = location['y'] + size['height']+donesize['height']
    im = im.crop((left,top,right,bottom))
    output=StringIO.StringIO()
    im.save(output,'PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    open("templates/weather.html","w+").write('<img src="data:image/png;base64,{0}"/>'.format(b64))
    return render_template('weather.html')

if __name__=='__main__':
    # app.run(host='0.0.0.0',debug=True)
    app.run()