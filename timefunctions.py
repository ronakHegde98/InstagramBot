def time_difference(start, end):
  """
  Calculate number of minutes elapsed between two standard time strings

  Args:
    start: int: start time of task 
    end: int: end time of task
  
  Returns:
    minutes: number of minutes elapsed 
  """

  #convert standard times into military 
  start = military_time(start.upper().strip())
  end = military_time(end.upper().strip())

  start = [int(x) for x in start.split(":")]
  end = [int(x) for x in end.split(":")]

  difference = []
  if(len(start) == len(end)):
    if(start[0]>=12 and end[0]<=12):
      difference.append(24-start[0]+(end[0]))
      [difference.append(abs(end[i]-start[i])) for i in range(1,len(end))]
    else:
      difference = [abs(end[i]-start[i]) for i in range(len(end))]
    
    for i in range(1,len(end)):
      if(start[i] > end[i]):
        difference[i] = (60-start[i])+end[i]
        difference[i-1]-=1

    seconds=0
    for i in range(len(difference)):
      if(i==0):
        seconds+=difference[i]*60*60
      elif(i==1):
        seconds+=difference[i]*60
      else:
        seconds+=difference[i]
    
  minutes = int(seconds/60.0)
  return minutes

def military_time(time):
  """ 
  Convert standard time into military time representation
  
  Example:
    input -> 05:30:40 PM
    output -> 17:30:40 
  """
  meridian = time[-2:] 
  time = time.replace(meridian,"").strip()

  hour = int(time.split(':')[0])

  #recalculate hour component (account for 12 AM/12 PM)
  if(meridian=="AM"):
    if(hour==12):
      new_hour=00
    elif(hour<10):
      new_hour="0"+ str(hour)
  else:
    if(hour==12):
      new_hour = hour
    else:
      new_hour = hour+12
  
  new_time = time.replace(time.split(':')[0], str(new_hour), 1)

  return new_time