import matplotlib.pyplot as plt
from io import BytesIO
import pylab
import time
from datetime import date
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def get_Current_date():
    curr_time = str("Fuzzed session finished at ")
    today = date.today()
    curr_time = curr_time + " at time: " + str(today)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    curr_time += "  "
    curr_time += current_time
    return curr_time

def write_to_pdf(plot_x, plot_y, plot_payload, plot_mutator,plot_depth, plot_all,total_attempts, total_faults,site_name,
                 req_vectors, req_statuses, rfi_bool_check,url_lsit):
    get_Current_date()
    fig = plt.figure(figsize=(3, 3))
    plot_x = plot_x
    plot_y = plot_y
    plt.plot(plot_x, plot_y)
    plt.xlabel("Attempts")
    plt.ylabel("Faults ")
    plt.title("Faults caught in time")

    plt.grid(True)

    # plt.show()
    imgdata = BytesIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Payloads', 'Mutators', 'Depth_Search'

    sizes = [plot_payload, plot_mutator, plot_depth]
    explode = (0, 0.1, 0.1)

    fig1, ax1 = plt.subplots(figsize=(3, 3))
    ax1.pie(sizes, explode=explode, labels=labels,
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    fig2, ax2 = plt.subplots(figsize=(3, 3))
    req_vector_sliced = req_vectors[:len(req_statuses)]
    ax2.pie(req_vector_sliced, autopct='%1.1f%%', labels=req_statuses,
            shadow=True, startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    circle_imgdata = BytesIO()
    fig1.savefig(circle_imgdata, format='svg')
    circle_imgdata.seek(0)  # rewind the data

    circle_imgdata_req = BytesIO()
    fig2.savefig(circle_imgdata_req, format='svg')
    circle_imgdata_req.seek(0)  # rewind the data

    drawing = svg2rlg(imgdata)
    drawing_circle = svg2rlg(circle_imgdata)
    drawing_circle_req = svg2rlg(circle_imgdata_req)

    c = canvas.Canvas('results.pdf', pagesize=letter)
    c.setFont("Helvetica-Bold", 10)  # choose your font type and font size
    renderPDF.draw(drawing, c, 10, 300)
    if plot_payload > 0 and plot_mutator > 0:
        renderPDF.draw(drawing_circle, c, 300, 300)
    c.drawString(10, 280, "Status code of responses")
    renderPDF.draw(drawing_circle_req, c, 10, 0)
    c.setTitle("Graphs in time, TITLE HERE")

    c.drawString(30, 750, ("Url fuzzed: " + site_name))
    c.setFont("Helvetica", 15)  # choose your font type and font size
    c.drawString(10, 700, get_Current_date())
    c.drawString(10, 670, ("Total attempts during the session: " + str(total_attempts)))
    c.drawString(10, 640, ("Total faults during the session: " + str(total_faults)))
    c.drawString(10, 600, ("Remote file inclusion vulnerability: " + str(rfi_bool_check)))
    c.showPage()

    textobject = c.beginText(x=10,y=740)
    url_list = url_lsit.split('\n')
    for line in url_list:
        print("Line: " +  line)
        textobject.textLine(line)
    c.drawText(textobject)
    c.showPage()

    print("pdf created!")
    c.save()


