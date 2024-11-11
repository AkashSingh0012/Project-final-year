import time
import calendar

def update_time(label, root):
    """
    Function to update the time in the provided label.
    This function will update every second.
    """
   
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    

    label.config(text=f"Current Date/Time:\n{current_time}")
    
    
    root.after(1000, update_time, label, root)

def update_calendar(label):
    """
    Function to display the current month's calendar.
    """
   
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    
    
    cal = calendar.month(year, month)
    
   
    label.config(text=f"Calendar:\n{cal}")
