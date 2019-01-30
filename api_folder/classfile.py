# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 18:35:49 2018

@author: Dell
"""

from flask import Flask
app= Flask(__name__)

@app.route('/')
def index():
    return 'flask'

class User:

    def __init__(self, UserID, UserName, UserEmail, UserPassword,UserImage,UserPhoneNumber):
        self.UserID = UserID
        self.UserName = UserName
        self.UserEmail = UserEmail
        self.UserPassword = UserPassword
        self.UserImage = UserImage
        self.UserPhoneNumber = UserPhoneNumber
        
    def getUserID(self):
		return self.UserID
    
    def setUserID(self, UserID):
		self.UserID = UserID
        
    def getUserName(self):
		return self.UserName
    
    def setUserName(self, UserName):
		self.UserName = UserName
        
    def getUserEmail(self):
		return self.UserEmail
    
    def setUserEmail(self, UserEmail):
		self.UserEmail = UserEmail
        
        
    def getUserPassword(self):
		return self.UserPassword
    
    def setUserPassword(self, UserPassword):
		self.UserPassword = UserPassword
        
    def getUserImage(self):
		return self.UserImage
    
    def setUserImage(self, UserImage):
		self.UserImage = UserImage
        
    def getUserPhoneNumber(self):
		return self.UserPhoneNumber
    
    def setUserPhoneNumber(self, UserPhoneNumber):
		self.UserPhoneNumber = UserPhoneNumber
        
    def Display(self):
       print(self.UserID, self.UserName, self.UserEmail,  self.UserPassword, self.UserImage, self.UserPhoneNumber)
        
        
        
        
class Reminder:

    def __init__(self, ReminderID, ReminderNote, ReminderTime , ReminderDate):
        self.ReminderID = ReminderID
        self.ReminderNote = ReminderNote
        self.ReminderTime = ReminderTime
        self.ReminderDate = ReminderDate
        
    def getReminderID(self):
		return self.ReminderID
    
    def setReminderID(self, ReminderID):
		self.ReminderID = ReminderID
        
    def getReminderNote(self):
		return self.ReminderNote
    
    def setReminderNote(self, ReminderNote):
		self.ReminderNote = ReminderNote
        
    def getReminderTime(self):
		return self.ReminderTime
    
    def setReminderTime(self, ReminderTime):
		self.ReminderTime = ReminderTime
        
    def getReminderDate(self):
		return self.ReminderDate
    
    def setReminderDate(self, ReminderDate):
		self.ReminderDate = ReminderDate
        
    def Display(self):
        print(self.ReminderID, self.ReminderNote, self.ReminderTime , self.ReminderDate)
             
             
class Schedule:

    def __init__(self, ScheduleID, Day, Time):
        self.ScheduleID = ScheduleID
        self.Day = Day
        self.Time = Time
        
    def getScheduleID(self):
		return self.ScheduleID
    
    def setScheduleID(self, ScheduleID):
		self.ScheduleID = ScheduleID
        
    def getDay (self):
		return self.Day 
    
    def setDay (self, Day ):
		self.Day  = Day 
        
    def getTime(self):
		return self.Time
    
    def setTime(self, Time):
		self.Time = Time
        
    def Display(self):
       print(self.ScheduleID, self.Day, self.Time)
                     
        
class Doctor:

    def __init__(self, DID, DName, DEdu, DImage, DCategory):
        self.DID = DID
        self.DEdu = DEdu
        self.DImage = DImage
        self.DCategory= DCategory
        
    def getDID(self):
		return self.DID
    
    def setDID(self, ScheduleID):
		self.DID = DID

    def getDName(self):
		return self.DName
    
    def setDID(self, DName):
		self.DName = DName
    
    def getDEdu (self):
		return self.DEdu 
    
    def setDay (self, DEdu ):
		self.DEdu  = DEdu 
        
    def getDImage(self):
		return self.DImage
    
    def setTime(self, DImage):
		self.DImage = DImage
        
    def getCategory(self):
		return self.DCategory
    
    def setTime(self, DCategory):
		self.DCategory = DCategory
        
    def Display(self):
             print(self.DID, self.DName, self.DEdu, self.DImage, self.DCategory)
        
class Hospital:
    
    
    def __init__(self, HID, HName, HAdress, HPhoneNumber , HImage, HLocation):
        self.HID = HID
        self.HName = HName
        self.HAdress = HAdress
        self.HPhoneNumber= HPhoneNumber
        self.HImage = HImage
        self.HLocation = HLocation
        
    def getHID(self):
		return self.HID
    
    def setHID(self, HID):
		self.HID = HID

    def getHName(self):
		return self.HName
    
    def setHName(self, HName):
		self.HName = HName
       
    def getHAdress (self):
		return self.HAdress 
    
    def setHAdress (self, HAdress):
		self.HAdress  = HAdress 
        
    def getHPhoneNumber(self):
		return self.HPhoneNumber
    
    def setHPhoneNumber(self, HPhoneNumber):
		self.HPhoneNumber = HPhoneNumber
        
    def getHImage(self):
		return self.HImage
    
    def setHImage(self, HImage):
		self.HImage = HImage
        
    def Display(self):
             print(self.HID, self.HName, self.HAdress, self.HPhoneNumber , self.HImage, self.HLocation)
        
class HealthTip:
    
    
    def __init__(self, HTID, HTTittle, HTDetails, HTImage , HTUploadDT):
        self.HTID = HTID
        self.HTTittle = HTTittle
        self.HTDetails = HTDetails
        self.HTImage= HTImage
        self.HTUploadDT = HTUploadDT
        
    def getHTID(self):
		return self.HTID
    
    def setHTID(self, HTID):
		self.HTID =HTID

    def getHTTittle(self):
		return self.HTTittle
    
    def setHTTittle(self,HTTittle):
		self.HTTittle =HTTittle
       
    def getHTDetails (self):
		return self. HTDetails
    
    def setHTDetails (self,  HTDetails):
		self. HTDetails  =  HTDetails 
        
    def getHTImage(self):
		return self.HTImage
    
    def setHTImage(self, HTImage):
		self.HTImage = HTImage
        
    def getHTUploadDT(self):
		return self.HTUploadDT
    
    def setHTUploadDT(self, HTUploadDT):
		self.HTUploadDT =HTUploadDT
        
    def Display(self):
             print(self.HTID, self.HTTittle, self.HTDetails, self.HTImage , self.HTUploadDT)
        
        
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    