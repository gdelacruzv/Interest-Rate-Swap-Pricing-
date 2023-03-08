# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 22:13:27 2023

@author: Gilberto
"""

import pandas as pd
from dateutil.relativedelta import relativedelta
from dateutil import parser
from pandas.tseries.offsets import Day


class CashflowGenerator:
    
    def __init__(self, start_date, end_date, frequency, day_count, effective_date=None):
        
        self.start_date = parser.parse(start_date).date()
        self.end_date = parser.parse(end_date).date()
        self.frequency = frequency
        self.day_count = day_count
        self.effective_date = parser.parse(effective_date).date() if effective_date is not None else self.start_date

    def _get_day_count(self, start_date, end_date):
        
        if self.day_count == '30/360':
            
            start_day = start_date.day
            start_month = start_date.month
            start_year = start_date.year
            end_day = end_date.day
            end_month = end_date.month
            end_year = end_date.year
            
            if start_day == 31:
                start_day = 30
                
            if end_day == 31 and start_day == 30:
                end_day = 30
                
            days = ((end_year - start_year) * 360 + (end_month - start_month) * 30 + (end_day - start_day)) / 360
        
        elif self.day_count == 'act/360':
            
            days = (end_date - start_date).days / 360
            
        else:
            
            if self.effective_date >= start_date:
                start_date = self.effective_date
            if self.effective_date >= end_date:
                end_date = self.effective_date
            
            days = (end_date - start_date).days / 365
            
        return days
    
    def generate_cashflows(self):
        
        # Generate a list of cashflow dates based on the frequency
        cashflow_dates = []
        date = self.start_date
        while date < self.end_date:
            cashflow_dates.append(date)
            date += relativedelta(months=self.frequency)
        cashflow_dates.append(self.end_date)
        
        # Calculate the number of days between each cashflow date based on the day count convention
        cashflow_days = []
        for i in range(1, len(cashflow_dates)):
            days = self._get_day_count(cashflow_dates[i-1], cashflow_dates[i])
            cashflow_days.append(days)
        
        # Create a pandas DataFrame to store the cashflow dates and amounts
        cashflows_df = pd.DataFrame({'date': cashflow_dates[:-1], 'days': cashflow_days})
        
        return cashflows_df
    
    
cf_generator = CashflowGenerator('2022-04-15', '2043-06-01', 3, 'act/360' , effective_date='2022-03-15')
cashflows_df = cf_generator.generate_cashflows()
print(cashflows_df)