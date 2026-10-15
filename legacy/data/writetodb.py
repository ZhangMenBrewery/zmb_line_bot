import csv
from models import hmi_event, TMP

        # Create your views here.

def Writetodb(): #
    try:       
        ## Open file
        with open(r'C:\Users\Administrator\Documents\Data\Alarm_log_record0.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    if hmi_event.objects.filter(time=row[13]).count()!= 0:
                        hmi_event.objects.Create(time=row[13],event=row[14])
                    #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                    line_count += 1
            print(f'Processed {line_count} lines.')    
    except:
        print(text='錯誤。')

