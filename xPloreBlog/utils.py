# utils.py

import matplotlib.pyplot as plt
from django.conf import settings
import os
import base64
import io
from matplotlib.dates import DateFormatter
import seaborn as sns
# as per article: https://stackoverflow.com/questions/27147300/matplotlib-tcl-asyncdelete-async-handler-deleted-by-the-wrong-thread
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')


def generate_chart(data, chart_type, chart_id):
    plt.figure(figsize=(10, 6))

    if chart_type == 'bar':
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c',
                  '#d62728', '#9467bd']  # Customize colors here
        bars = plt.bar(data['labels'], data['values'],
                       color=colors[:len(data['values'])])
        plt.xticks([])  # Remove x-axis labels
        plt.legend(bars, data['labels'])
        plt.title('Top Rated Posts')

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval,
                     f'{yval:.2f}', va='bottom')  # Add values

    elif chart_type == 'line':
        lines = plt.plot(data['labels'], data['values'], marker='o')
        plt.xticks([])  # Remove x-axis labels
        plt.legend(lines, data['labels'])
        plt.title('Recent Posts')

        for i, value in enumerate(data['values']):
            plt.text(i, value, f'{value:.2f}', va='bottom')  # Add values

    elif chart_type == 'pie':
        plt.pie(data['values'], labels=data['labels'], autopct='%1.1f%%')
        plt.title('Category Wise Posts')

    elif chart_type == 'doughnut':
        wedges, texts, autotexts = plt.pie(
            data['values'], labels=data['labels'], autopct='%1.1f%%', startangle=140)
        for w in wedges:
            w.set_edgecolor('white')
        plt.gca().add_artist(plt.Circle((0, 0), 0.70, fc='white'))
        plt.title('Tag Wise Posts')

    elif chart_type == 'recent_posts':
        dates = data['labels']
        values = data['values']
        plt.plot_date(dates, values, '-')
        date_format = DateFormatter('%Y-%m-%d')
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.gca().invert_yaxis()  # Invert y-axis to show recent dates on top
        plt.xticks(rotation=45)
        plt.title('Recent Posts')

        for i, (date, value) in enumerate(zip(dates, values)):
            plt.text(date, value, f'{value}', va='bottom')  # Add values

    # Save chart to a PNG in memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + string.decode('utf-8')

    buf.close()
    plt.close()

    return uri


# def generate_chart(data, chart_type, chart_name):
#     plt.figure(figsize=(10, 6))

#     if chart_type == 'bar':
#         sns.barplot(x=data['labels'], y=data['values'])
#         plt.legend(data['labels'], loc='upper right')
#     elif chart_type == 'pie':
#         wedges, texts, autotexts = plt.pie(data['values'], autopct='%1.1f%%')
#         plt.legend(wedges, data['labels'], title="Categories",
#                    loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
#     elif chart_type == 'line':
#         sns.lineplot(x=data['labels'], y=data['values'])
#         plt.legend(data['labels'], loc='upper right')
#     elif chart_type == 'doughnut':
#         wedges, texts, autotexts = plt.pie(
#             data['values'], autopct='%1.1f%%', wedgeprops=dict(width=0.3))
#         plt.legend(wedges, data['labels'], title="Categories",
#                    loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

#     chart_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
#     if not os.path.exists(chart_dir):
#         os.makedirs(chart_dir)

#     chart_path = os.path.join(chart_dir, f"{chart_name}.png")
#     plt.savefig(chart_path, bbox_inches='tight')
#     plt.close()

#     return os.path.join(settings.MEDIA_URL, 'charts', f"{chart_name}.png")
