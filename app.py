# app.py
from flask import Flask, render_template, request, redirect, Markup , url_for
import pymysql
import datetime
import time

conn = pymysql.connect(
    host='myadbdatabase.cexehdx2znq4.us-east-1.rds.amazonaws.com',
    port=int(3306),
    user="admin",
    passwd="password123",
    db="database_container",
    charset='utf8mb4')

cursor=conn.cursor()

application = Flask(__name__, template_folder="templates")


@application.route("/")
def index():


   return render_template('/index.html')


@application.route("/", methods = ['POST', 'GET'])
def handle_data():
  minMag = float(request.form['minMag'])
  maxMag = float(request.form['maxMag'])
  netValue = str(request.form['netValue'])

  intervals = float(request.form['interval_of_mags'])

  print('You have reached here from the submit button')
  print('minMag is :'+str(minMag))
  print('maxMag is :'+str(maxMag))
  print('Intervals of : '+str(intervals))
  #data = minMag + " " + maxMag 
  #return render_template('data.html', data = data )

  arr = []
  latRange= []
  internal_limit =0

  while (float(minMag)<float(maxMag)):
    #arr.append(int(minMag))
    #minMag+=int(intervals)
    if internal_limit < float(maxMag):
      #internal_limit = int(minMag) + int(intervals)
      #arr.append(internal_limit)
      #minMag+=int(intervals)
      print("MinMag:"+str(minMag))
      internal_limit = float(minMag) + float(intervals) 
      print("Internal_limit: "+str(internal_limit))
      latRange.append(str(minMag)+" to "+str(internal_limit))
      tsql = "select count(*) from database_container.quake where mag BETWEEN "+str(minMag)+" AND "+str(internal_limit)+" and net='"+netValue+"'"
      cursor.execute(tsql)
      for row in cursor:
        arr.append(row[0])
      #data = cursor.fetchall()
      minMag=internal_limit
      #arr.append(format(data))

    #  p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
     #      tools="hover", tooltips="@country: @value", x_range=(3, 8))

    
      #p.wedge(x=0, y=1, radius=0.4,
       # start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        #line_color="white", fill_color='color', legend_field='country', source=data)

      #p.axis.axis_label=None
      #p.axis.visible=False
      #p.grid.grid_line_color = None

      #show(p)

  

  #tsql = "select * from [dbo].[quake] where mag BETWEEN "+minMag+" AND "+maxMag
  #cursor.execute(tsql)
  #data = cursor.fetchall()
  return render_template('data.html', zipped_values=zip(latRange,arr))



@application.route("/data",methods = ['POST', 'GET'])
def data():
    return render_template('data.html', title='Contact')




@application.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')

if __name__ == '__main__':
    application.run(debug=True)
