""" Manager module to helper building this app """

from datetime import datetime, timedelta, timezone


class Manager(object):
    """ Manager Object """

    def setup_datetime(self):
        """ Setup date time to Sao Paulo time timezone """
        
        current_date_time = datetime.now()
        timezone_diference = timedelta(hours=-3)
        return timezone(timezone_diference), current_date_time
    
    
    def numeric_date_recover(self):
        """ Return a numeric current date  in the 
            format 00-00-0000 """
       
        sp_time_zone, current_datetime = self.setup_datetime()   
        converter2sptimezone = current_datetime.astimezone(sp_time_zone)
        
        return converter2sptimezone.strftime('%d-%m-%Y')
    
    