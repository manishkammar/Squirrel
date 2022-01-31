

def weekly_report():
    import matplotlib.pyplot as plt
    plt.rcdefaults()
    import numpy as np

    objects = ('ID001', 'ID002', 'ID003', 'ID004', 'ID005', 'ID006')
    y_pos = np.arange(len(objects))
    performance = [6, 6.5, 5, 6, 5, 6]

    plt.bar(y_pos, performance, align='center', alpha=0.5,color='blue')
    plt.xticks(y_pos, objects)
    plt.ylabel('Days')
    plt.title('Weekely Report')

    plt.show()


def monthly_report():
    import matplotlib.pyplot as plt
    labels = 'No. of days present','No of days absent'
    sizes = [20,4]
    colors = ['red','yellow']
    explode = (0.1, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title("Monthly Report",color="blue")
    plt.show()
weekly_report()