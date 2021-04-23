
from datetime import datetime
from datetime import date
import time
import plyer
#from win10toast import ToastNotifier
#toaster = ToastNotifier()
  
import threading
import sys

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.picker import MDDatePicker
from kivy.factory import Factory
import pandas as pd
import numpy as np
from kivymd.uix.card import MDCardSwipe
from kivy.properties import StringProperty
from kivymd.toast import toast

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import random
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
from kivy.properties import ObjectProperty
encoder = LabelEncoder()
import json 

data1 = pd.read_csv(r'E:\Final_yr_project\Code\diabetes_data_preprocessed.csv',error_bad_lines=False)
df = pd.read_csv(r'E:\Final_yr_project\Code\Final_Meal.csv').fillna('NA')
df_meal = df.filter(['Category','Dish_name','Type','Serving','Calories (cal)','Carbohydrates (g)','Protein (g)','Fat (g)','Fiber (g)'], axis=1)


model_knn = NearestNeighbors(metric = 'euclidean', algorithm = 'brute')

class WelcomeScreen(Screen):
    pass
class LoginScreen(Screen):
    pass
class NavigationScreen(Screen):
    pass
class MainScreen(Screen):
    pass
class CreateAccountScreen(Screen):
    pass
class Content(MDBoxLayout):
    pass
class Tab(MDFloatLayout, MDTabsBase):
    pass
class xyz(MDCardSwipe):
    '''Card with `swipe-to-delete` behavior.'''

    text = StringProperty()

def background(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def backgrnd_func(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return backgrnd_func

    
@background   
def back1(self):
    print("background 1")
    with open('userProfile.json','r') as json_file: 
        data = json.load(json_file) 
    
    for i in range(len(data)):
        if data[i]['email']==self.file.get_screen('navi').ids._email.text:
            for j in range(len(data[i])):
                if ((data[i]['medicines'][j]['med_name']!="Add medicine")):
                    temp_list=[]
                    if ((data[i]['medicines'][j]['med_name']) in self.medicine_names):
                        index1=self.medicine_names.index(data[i]['medicines'][j]['med_name'])
                        self.st_date=data[i]['medicines'][j]['med_start_date']
                        self.end_date=data[i]['medicines'][j]['med_end_date']
                        self.medicine_names[index1]=data[i]['medicines'][j]['med_name'] 
                        self.medicine_desc[index1]=data[i]['medicines'][j]['med_description'] 
                        
                        if ((str(data[i]['medicines'][j]['med_time'][0]['time1'])!="00:00:00")):
                            temp_list.append(data[i]['medicines'][j]['med_time'][0]['time1'])
                    
                            
                            
                        if ((str(data[i]['medicines'][j]['med_time'][0]['time2'])!="00:00:00")):
                            temp_list.append(data[i]['medicines'][j]['med_time'][0]['time2'])
                       
                            
                        if ((str(data[i]['medicines'][j]['med_time'][0]['time3'])!="00:00:00")):
                            temp_list.append(data[i]['medicines'][j]['med_time'][0]['time3'])
                       
                            
                        self.medicine_times[index1].clear()
                        self.medicine_times[index1].extend(temp_list)
                    else:
                        self.medicine_names.append(data[i]['medicines'][j]['med_name'])
                        self.medicine_desc.append(data[i]['medicines'][j]['med_description'])
                        if str(data[i]['medicines'][j]['med_time'][0]['time1'])!="00:00:00":
                            temp_list.append(data[i]['medicines'][j]['med_time'][0]['time1'])
                        if str(data[i]['medicines'][j]['med_time'][0]['time2'])!="00:00:00":
                            temp_list.append(data[i]['medicines'][j]['med_time'][0]['time2'])
                        if str(data[i]['medicines'][j]['med_time'][0]['time3'])!="00:00:00":
                            temp_list.append(data[i]['medicines'][j]['med_time'][0]['time3'])
                        self.medicine_times.append(temp_list)

    print("Back 1 list: ",self.medicine_names)
    print("Back 1 list: ",self.medicine_times)
  #  toaster.show_toast("Example","Notifcation Text",icon_path=None,duration=5,threaded=True)
    
    while (True):
        self.now = datetime.now()

        
        self.current_time = self.now.strftime("%H:%M:%S")
        self.current_date = self.now.strftime("%d.%m.%Y")
        
       # print(self.current_time)
        if self.daily==0:
            if (datetime.strptime(self.st_date, "%d.%m.%Y") <= datetime.strptime(self.current_date, "%d.%m.%Y") <= datetime.strptime(self.end_date, "%d.%m.%Y")):
        # Check if the current time is the same as the alarm
                for i in range(len(self.medicine_times)):
                    for j in range(len(self.medicine_times[i])):
                        if self.current_time == self.medicine_times[i][j]:
                            plyer.notification.notify(title='It is Time to take your medicine', message="Notification using plyer")
                            #toaster.show_toast("It's Time to take your medicine",self.medicine_names[i]+"-"+self.medicine_desc[i],icon_path=None,duration=5,threaded=True)
                if self.med_submit==1:
                    back2(self)
                    sys.exit()
                        
        else:
            for i in range(len(self.medicine_times)):
                    for j in range(len(self.medicine_times[i])):
                        if self.current_time == self.medicine_times[i][j]:
                            plyer.notification.notify(title='It is Time to take your medicine', message="Notification using plyer")
                            #toaster.show_toast("It's Time to take your medicine",self.medicine_names[i]+"-"+self.medicine_desc[i],icon_path=None,duration=5,threaded=True)
            if self.med_submit==1:
                back2(self)
                sys.exit()
@background
def back2(self):
    print("background 2")
    self.med_submit=2
    with open('userProfile.json','r') as json_file: 
        data = json.load(json_file) 
    for i in range(len(data)):
        if data[i]['email']==self.file.get_screen('navi').ids._email.text:
                if ((data[i]['medicines'][self.id-1]['med_name']!="Add medicine")):
                    temp_list=[]
                    if ((data[i]['medicines'][self.id-1]['med_name'])  in self.medicine_names):
                        index1=self.medicine_names.index(data[i]['medicines'][self.id-1]['med_name'])
                        self.st_date=data[i]['medicines'][self.id-1]['med_start_date']
                        self.end_date=data[i]['medicines'][self.id-1]['med_end_date']
                        print("Back 2", index1)                        
                        self.medicine_names[index1]=data[i]['medicines'][self.id-1]['med_name'] 
                        self.medicine_desc[index1]=data[i]['medicines'][self.id-1]['med_description'] 
                        
                        if ((str(data[i]['medicines'][self.id-1]['med_time'][0]['time1'])!="00:00:00")):
                            temp_list.append(data[i]['medicines'][self.id-1]['med_time'][0]['time1'])
                        
                            
                            
                        if ((str(data[i]['medicines'][self.id-1]['med_time'][0]['time2'])!="00:00:00")):
                            temp_list.append(data[i]['medicines'][self.id-1]['med_time'][0]['time2'])
                        
                            
                            
                        if ((str(data[i]['medicines'][self.id-1]['med_time'][0]['time3'])!="00:00:00")):
                            temp_list.append(data[i]['medicines'][self.id-1]['med_time'][0]['time3'])
                        
                            
                        self.medicine_times[index1].clear()
                        self.medicine_times[index1].extend(temp_list)
                        break
                    else:
                        self.medicine_names.append(data[i]['medicines'][self.id-1]['med_name'])
                        self.medicine_desc.append(data[i]['medicines'][self.id-1]['med_description'])
                        if str(data[i]['medicines'][self.id-1]['med_time'][0]['time1'])!="00:00:00":
                            temp_list.append(data[i]['medicines'][self.id-1]['med_time'][0]['time1'])
                        if str(data[i]['medicines'][self.id-1]['med_time'][0]['time2'])!="00:00:00":
                            temp_list.append(data[i]['medicines'][self.id-1]['med_time'][0]['time2'])
                        if str(data[i]['medicines'][self.id-1]['med_time'][0]['time3'])!="00:00:00":
                            temp_list.append(data[i]['medicines'][self.id-1]['med_time'][0]['time3'])
                        self.medicine_times.append(temp_list) 
                        break
        
    print("temp list is", temp_list)
  #  toaster.show_toast("Example","Notifcation Text",icon_path=None,duration=5,threaded=True)
    print("Back 2 list: ",self.medicine_names) 
    print("Back 2 list: ",self.medicine_times)
    while (True):
        self.now = datetime.now()
 
        self.current_time = self.now.strftime("%H:%M:%S")
        self.current_date = self.now.strftime("%d.%m.%Y")
        
       # print(self.current_time)
        if self.daily==0:
            if (datetime.strptime(self.st_date, "%d.%m.%Y") <= datetime.strptime(self.current_date, "%d.%m.%Y") <= datetime.strptime(self.end_date, "%d.%m.%Y")):
                
       # print(self.current_time)
     
        # Check if the current time is the same as the alarm
                for i in range(len(self.medicine_times)):
                    for j in range(len(self.medicine_times[i])):
                        if self.current_time == self.medicine_times[i][j]:
                            plyer.notification.notify(title='It is Time to take your medicine', message="Notification using plyer")
                            #toaster.show_toast("It's Time to take your medicine",self.medicine_names[i]+"-"+self.medicine_desc[i],icon_path=None,duration=5,threaded=True)
                if self.med_submit==1:
                    back1(self)
                    sys.exit()
                    
        else:
            for i in range(len(self.medicine_times)):
                    for j in range(len(self.medicine_times[i])):
                        if self.current_time == self.medicine_times[i][j]:
                            plyer.notification.notify(title='It is Time to take your medicine', message="Notification using plyer")
                            #toaster.show_toast("It's Time to take your medicine",self.medicine_names[i]+"-"+self.medicine_desc[i],icon_path=None,duration=5,threaded=True)
            if self.med_submit==1:
                back2(self)
                sys.exit()

    
sm = ScreenManager()
sm.add_widget(WelcomeScreen(name = 'welcomescreen'))
sm.add_widget(LoginScreen(name = 'loginscreen'))
sm.add_widget(NavigationScreen(name = 'navi'))
sm.add_widget(MainScreen(name = 'mainscreen'))
sm.add_widget(CreateAccountScreen(name='create'))



            
def write_json(data, filename='userProfile.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4)
            
class NewApp(MDApp):
    tf_date_1 = ObjectProperty(None)
    date_1 = None
    date_2 = None
    dialog=None
    low=high=medium=normal=0
    low_bp=high_bp=moderate_bp=normal_bp=0
    bp=0
    low_insulin=high_insulin=normal_insulin=0
    insulin=0
    mf=0
    flag0=flag1=False
   
    
    cal_female = cal_male = 0.0
    recommendation_bf = ""
    serving_bf = ""
    cal_bf = 0.0
    recommendation_l = ""
    serving_l = ""
    cal_l = 0.0
    recommendation_s = ""
    serving_s = ""
    cal_s = 0.0
    recommendation_d = ""
    serving_d = ""
    cal_d = 0.0
    daily=0
    total=0
    
    swap_bf = swap_l = swap_s = swap_d = 0
    list_bf = []
    list_l = []
    list_s = []
    list_d = []
    
    medicine_names=[]
    medicine_desc=[]
    medicine_times=[]
    current_time = ""
    current_date = ""
    st_date = "01.01.2021"
    end_date = "31.12.2021"
    med_submit=0
    remove_medi= ""
    
    id=0
    gender = ""
    food_type = ""
    beverage = ""
    
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        self.file = Builder.load_file("original.kv")
        self.date_1 = None
        self.date_2 = None
        self.root = Factory.Pickers()
        return self.file
               
    def create_account(self):
        self.name_text = self.file.get_screen('create').ids.name_text_field.text
        self.email_text = self.file.get_screen('create').ids.email_text_field.text
        self.password_text = self.file.get_screen('create').ids.password_text_field.text
        
        with open('userProfile.json') as json_file: 
            data1 = json.load(json_file) 
            temp = data1  
            y = {"name": self.name_text,
                 "email": self.email_text,
                 "password": self.password_text,
                  "medicines": [
            {
                "med_name": "Add medicine",
                "med_description": "Add description",
                "med_start_date": "dd-mm-yyyy",
                "med_end_date": "dd-mm-yyyy",
                "med_time": [
                        {
                              "time1": "00:00:00",
                              "time2": "00:00:00",
                              "time3": "00:00:00"
                        }
                        
                        ],
                "med_daily": 0
            },
            {
                "med_name": "Add medicine",
                "med_description": "Add description",
                "med_start_date": "dd-mm-yyyy",
                "med_end_date": "dd-mm-yyyy",
                "med_time": [
                        {
                              "time1": "00:00:00",
                              "time2": "00:00:00",
                              "time3": "00:00:00"
                        }
                        
                        ],
                "med_daily": 0
            },
            {
                "med_name": "Add medicine",
                "med_description": "Add description",
                "med_start_date": "dd-mm-yyyy",
                "med_end_date": "dd-mm-yyyy",
                "med_time": [
                        {
                              "time1": "00:00:00",
                              "time2": "00:00:00",
                              "time3": "00:00:00"
                        }
                        
                        ],
                "med_daily": 0
            },
            {
                "med_name": "Add medicine",
                "med_description": "Add description",
                "med_start_date": "dd-mm-yyyy",
                "med_end_date": "dd-mm-yyyy",
                "med_time": [
                        {
                              "time1": "00:00:00",
                              "time2": "00:00:00",
                              "time3": "00:00:00"
                        }
                        
                        ],
                "med_daily": 0
            },
            {
                "med_name": "Add medicine",
                "med_description": "Add description",
                "med_start_date": "dd-mm-yyyy",
                "med_end_date": "dd-mm-yyyy",
                "med_time": [
                        {
                              "time1": "00:00:00",
                              "time2": "00:00:00",
                              "time3": "00:00:00"
                        }
                        
                        ],
                "med_daily": 0
            },
            {
                "med_name": "Add medicine",
                "med_description": "Add description",
                "med_start_date": "dd-mm-yyyy",
                "med_end_date": "dd-mm-yyyy",
                "med_time": [
                        {
                              "time1": "00:00:00",
                              "time2": "00:00:00",
                              "time3": "00:00:00"
                        }
                        
                        ],
                "med_daily": 0
            },
            {
                "med_name": "Add medicine",
                "med_description": "Add description",
                "med_start_date": "dd-mm-yyyy",
                "med_end_date": "dd-mm-yyyy",
                "med_time": [
                        {
                              "time1": "00:00:00",
                              "time2": "00:00:00",
                              "time3": "00:00:00"
                        }
                        
                        ],
                "med_daily": 0
            },
            {
                "med_name": "Add medicine",
                "med_description": "Add description",
                "med_start_date": "dd-mm-yyyy",
                "med_end_date": "dd-mm-yyyy",
                "med_time": [
                        {
                              "time1": "00:00:00",
                              "time2": "00:00:00",
                              "time3": "00:00:00"
                        }
                        
                        ],
                "med_daily": 0
            }
        ]
                } 
          
            temp.append(y) 
     
        write_json(data1)
         
   # Check email and password
    def verify(self):              
        self.email_text = self.file.get_screen('loginscreen').ids.email_text_field.text
        self.password_text = self.file.get_screen('loginscreen').ids.password_text_field.text
        name=""
        if (self.email_text=="" or self.password_text==""):
            cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
            self.dialog = MDDialog(title = 'Error!',text = "Please fill in required fields!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
            self.dialog.open()
            
        else:
            with open('userProfile.json') as json_file: 
                data = json.load(json_file) 
                
                self.email_text = self.file.get_screen('loginscreen').ids.email_text_field.text
                self.password_text = self.file.get_screen('loginscreen').ids.password_text_field.text
                
                flag1=True
                flag2=True
                for i in range(len(data)):
                    if data[i]['email']==self.email_text:
                        flag1=False
                        if data[i]['password']==self.password_text:
                            flag2=False
                            name = data[i]['name']
                            break
                        
                            
                if flag1:
                    self.dialog = MDDialog(title = 'Account does not exist!',text = "Please create a new account!")
                    self.dialog.open()
                    
                elif (not flag1) and flag2:
                    cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
                    self.dialog = MDDialog(title = 'Invalid password',text = "Please enter a valid password!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
                    self.dialog.open()
                    
                else:
                    self.dialog = MDDialog(title = 'Login Successful!',text = "Please click anywhere on the page to continue.")
                    self.dialog.open()
                    self.file.get_screen('loginscreen').manager.current = 'navi'
                    self.file.get_screen('navi').ids.screen_manager.current = 'scr1'
                  #  self.file.get_screen('navi').ids.screen_manager.current = 'activityscreen'
                    self.file.get_screen('navi').ids._name.text = name
                    self.file.get_screen('navi').ids._email.text = self.email_text
                    self.now = datetime.now()
                  #  print((self.now))
                    # Format the current time
                    self.current_time = self.now.strftime("%H:%M:%S")
                    print(self.current_time)
                    back1(self)
                    
                
                   
                    '''
                 
                    for i in range(len(data)):
                
                        if data[i]['email']==self.file.get_screen('navi').ids._email.text:
                            for j in range(len(data[i])):
                                if data[i]['medicines'][j]['med_name']!="Add medicine":
                                    self.medicine_names.append(data[i]['medicines'][j]['med_name'])
                                    self.medicine_times.append(data[i]['medicines'][j]['med_time'])
        
                  #  toaster.show_toast("Example","Notifcation Text",icon_path=None,duration=5,threaded=True)
                    
                    while (True):
                        self.now = datetime.now()
                 
                        self.current_time = self.now.strftime("%H:%M:%S")
                       # print(self.current_time)
                     
                        # Check if the current time is the same as the alarm
                        if self.current_time in self.medicine_times:
            
                            toaster.show_toast("Example","Notifcation Text",icon_path=None,duration=5,threaded=True)
                    '''     
  
        
        
        
                  
                  
     # Validate name and email       
    def check_email(self):

        self.name_text = self.file.get_screen('create').ids.name_text_field.text
        self.email_text = self.file.get_screen('create').ids.email_text_field.text
        self.password_text = self.file.get_screen('create').ids.password_text_field.text
        
        if self.name_text=="" or self.email_text=="" or self.password_text=="":
            cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
            self.dialog = MDDialog(title = 'Error!',text = "Please fill in required fields!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
            self.dialog.open()
            
        else:
            
            name_check_false = True
            try:
                int(self.name_text)
            except:
                name_check_false = False
            if name_check_false:
                    cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
                    self.dialog = MDDialog(title = 'Invalid Name',text = "Please input a valid name",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
                    self.dialog.open()
        
            else:        
                with open('userProfile.json') as json_file: 
                    data = json.load(json_file) 
                    flag=False
                    for i in range(len(data)):
                        if data[i]['email']==self.email_text:
                            flag=True
                            break
                        
                    if flag:
                        self.dialog = MDDialog(title = 'Email id exists!',text = "Please enter new email id!")
                        self.dialog.open()
                        
                    else:
                    
                        NewApp.create_account(self)
                        self.dialog = MDDialog(title = 'Account created successfully!',text = "Please click on the left arrow button.")
                        self.dialog.open()
                        self.file.get_screen('create').manager.current = 'loginscreen'
     
    #check if gender selected is male/female
    def male(self):
        self.mf=1
    def female(self):
        self.mf=2  
        
    def check(self):
        self.a_dpf_text=self.file.get_screen('navi').ids.a_text_field.text
        self.b_dpf_text=self.file.get_screen('navi').ids.b_text_field.text
        self.c_dpf_text=self.file.get_screen('navi').ids.c_text_field.text
       
        if (self.a_dpf_text=="" or self.b_dpf_text=="" or self.c_dpf_text==""):
            cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
            self.dialog = MDDialog(title = 'Error!',text = "Please fill in required fields!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
            self.dialog.open()
            
        elif(self.mf==1):
            NewApp.prediction_male(self)
        else:
            NewApp.prediction_female(self)
    
    #check if all required fields are filled for getcheckedmale
    def getcheckedmale(self):
        self.height_text = self.file.get_screen('navi').ids.height_text_field_male.text
        self.weight_text = self.file.get_screen('navi').ids.weight_text_field_male.text
       
        if (self.height_text=="" or self.weight_text==""):
            cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
            self.dialog = MDDialog(title = 'Error!',text = "Please fill in required fields!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
            self.dialog.open()
            
        else:
            self.file.get_screen('navi').ids.screen_manager.current = 'glucosescreen'
            self.file.get_screen('navi').ids.screen_manager.transition.direction = 'left'
    
    #check if all required fields are filled for getcheckedfemale           
    def getcheckedfemale(self):
        self.preg_text = self.file.get_screen('navi').ids.preg_text_field_female.text
        self.height_text = self.file.get_screen('navi').ids.height_text_field_female.text
        self.weight_text = self.file.get_screen('navi').ids.weight_text_field_female.text
       
        if (self.height_text=="" or self.weight_text=="" or self.preg_text==""):
            cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
            self.dialog = MDDialog(title = 'Error!',text = "Please fill in required fields!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
            self.dialog.open()
            
        else:
            self.file.get_screen('navi').ids.screen_manager.current = 'glucosescreen'
            self.file.get_screen('navi').ids.screen_manager.transition.direction = 'left'
    
    
     #prediction function for male
    def prediction_male(self):
        self.preg_text = 0
        print("Prediction male is called")
        self.bmi_text = float(self.weight_text)/(((float(self.height_text))/100)*((float(self.height_text))/100))
        self.no=float(((int(self.a_dpf_text))*0.5)+((int(self.b_dpf_text))*0.25)+((int(self.c_dpf_text))*0.125))
        print(self.no)
        self.age_text= int(self.file.get_screen('navi').ids.slider1.value)
        print(self.age_text)
        NewApp.prediction(self,self.preg_text,self.glucose,self.bp,self.insulin,self.bmi_text,self.no,self.age_text)
    
    #prediction function for female
    def prediction_female(self):
        print("Prediction female is called")
        self.bmi_text = float(self.weight_text)/(((float(self.height_text))/100)*((float(self.height_text))/100))
        self.preg  = int(self.preg_text)
        self.no=float(((int(self.a_dpf_text))*0.5)+((int(self.b_dpf_text))*0.25)+((int(self.c_dpf_text))*0.125))
        print(self.no)
        self.age_text= int(self.file.get_screen('navi').ids.slider1_female.value)
        print(self.age_text)
        NewApp.prediction(self,self.preg,self.glucose,self.bp,self.insulin,self.bmi_text,self.no,self.age_text)
        
        
    #LOW GLUCOSE SYMPTOMS
    def on_checkbox_active_dizziness(self, checkbox, value):
        if value:
            self.low+=1
        elif self.low>0:
            self.low-=1
    def on_checkbox_active_palpitation(self, checkbox, value):
        if value:
            self.low+=1
        elif self.low>0:
            self.low-=1
    def on_checkbox_active_weakness(self, checkbox, value):
        if value:
            self.low+=1
        elif self.low>0:
            self.low-=1
    def on_checkbox_active_slurred(self, checkbox, value):
        if value:
            self.low+=1
        elif self.low>0:
            self.low-=1      
    def on_checkbox_active_seizure(self, checkbox, value):
        if value:
            self.low+=1
        elif self.low>0:
            self.low-=1
            
    #HIGH GLUCOSE SYMPTOMS
    def on_checkbox_active_blurred(self, checkbox, value):
        if value:
            self.high+=1
        elif self.high>0:
            self.high-=1
    def on_checkbox_active_urine(self, checkbox, value):
        if value:
            self.high+=1
        elif self.high>0:
            self.high-=1
    def on_checkbox_active_gum(self, checkbox, value):
        if value:
            self.high+=1
        elif self.high>0:
            self.high-=1
    def on_checkbox_active_sunburn(self, checkbox, value):
        if value:
            self.high+=1
        elif self.high>0:
            self.high-=1
    def on_checkbox_active_fruity_smell(self, checkbox, value):
        if value:
            self.high+=1
        elif self.high>0:
            self.high-=1
            
    #MEDIUM GLUCOSE SYMTOMS
    def on_checkbox_active_hunger(self, checkbox, value):
        if value:
            self.medium+=1
        elif self.medium>0:
            self.medium-=1
    def on_checkbox_active_pale(self, checkbox, value):
        if value:
            self.medium+=1
        elif self.medium>0:
            self.medium-=1
    def on_checkbox_active_bloating(self, checkbox, value):
        if value:
            self.medium+=1
        elif self.medium>0:
            self.medium-=1
    def on_checkbox_active_bodyache(self, checkbox, value):
        if value:
            self.medium+=1
        elif self.medium>0:
            self.medium-=1
    def on_checkbox_active_wounds(self, checkbox, value):
        if value:
            self.medium+=1
        elif self.medium>0:
            self.medium-=1
            
    #NO SYMPTOMS
    def on_checkbox_active_no_sym(self, checkbox, value):
        if value:
    
            self.normal=1
            self.low=0
            self.high=0
            self.medium=0
            self.file.get_screen('navi').ids.fruity_smell.disabled=True
            self.file.get_screen('navi').ids.gum.disabled=True
            self.file.get_screen('navi').ids.sunburn.disabled=True
            self.file.get_screen('navi').ids.frequent_urine.disabled=True
            self.file.get_screen('navi').ids.blurred.disabled=True
            self.file.get_screen('navi').ids.wounds.disabled=True
            self.file.get_screen('navi').ids.bodyache.disabled=True
            self.file.get_screen('navi').ids.bloating.disabled=True
            self.file.get_screen('navi').ids.hunger_ext_thirst.disabled=True
            self.file.get_screen('navi').ids.turning_pale.disabled=True
            self.file.get_screen('navi').ids.seizure.disabled=True
            self.file.get_screen('navi').ids.slurred_speech.disabled=True
            self.file.get_screen('navi').ids.Dizziness.disabled=True
            self.file.get_screen('navi').ids.palpitation.disabled=True
            self.file.get_screen('navi').ids.weakness.disabled=True
            print(self.normal)
            print(self.low)
            print(self.high)
            print(self.medium)
            
            
        else:
            self.file.get_screen('navi').ids.fruity_smell.disabled=False
            self.file.get_screen('navi').ids.gum.disabled=False
            self.file.get_screen('navi').ids.sunburn.disabled=False
            self.file.get_screen('navi').ids.frequent_urine.disabled=False
            self.file.get_screen('navi').ids.blurred.disabled=False
            self.file.get_screen('navi').ids.wounds.disabled=False
            self.file.get_screen('navi').ids.bodyache.disabled=False
            self.file.get_screen('navi').ids.bloating.disabled=False
            self.file.get_screen('navi').ids.hunger_ext_thirst.disabled=False
            self.file.get_screen('navi').ids.turning_pale.disabled=False
            self.file.get_screen('navi').ids.seizure.disabled=False
            self.file.get_screen('navi').ids.slurred_speech.disabled=False
            self.file.get_screen('navi').ids.Dizziness.disabled=False
            self.file.get_screen('navi').ids.palpitation.disabled=False
            self.file.get_screen('navi').ids.weakness.disabled=False
            
            self.file.get_screen('navi').ids.fruity_smell.active =False
            self.file.get_screen('navi').ids.gum.active =False
            self.file.get_screen('navi').ids.sunburn.active =False
            self.file.get_screen('navi').ids.frequent_urine.active=False 
            self.file.get_screen('navi').ids.blurred.active =False
            self.file.get_screen('navi').ids.wounds.active =False
            self.file.get_screen('navi').ids.bodyache.active =False
            self.file.get_screen('navi').ids.bloating.active =False
            self.file.get_screen('navi').ids.hunger_ext_thirst.active=False 
            self.file.get_screen('navi').ids.turning_pale.active =False
            self.file.get_screen('navi').ids.seizure.active =False
            self.file.get_screen('navi').ids.slurred_speech.active=False 
            self.file.get_screen('navi').ids.palpitation.active =False
            self.file.get_screen('navi').ids.weakness.active=False
            self.file.get_screen('navi').ids.Dizziness.active=False
            self.normal=0
            print(self.normal)
            print(self.low)
            print(self.high)
            print(self.medium)
    
    #Check if user is male/female & accordingly divert back to getcheckedmale/getcheckedfemale screen
    def glucose_check(self):
        if(self.mf==1):
            self.file.get_screen('navi').ids.screen_manager.current = 'getcheckedmalescreen'
            self.file.get_screen('navi').ids.screen_manager.transition.direction = 'right'  
        else:
            self.file.get_screen('navi').ids.screen_manager.current = 'getcheckedfemalescreen'
            self.file.get_screen('navi').ids.screen_manager.transition.direction = 'right'      
    
    #verify if user has chosen atleast 1 symptom
    def glucose_verify(self):
        if(self.high==0 and self.medium==0 and self.low==0 and self.normal==0):
            cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
            self.dialog = MDDialog(title = 'Error!',text = "Please choose atleast one symptom!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
            self.dialog.open()
            
        else:
            self.file.get_screen('navi').ids.screen_manager.current = 'bloodpressurescreen'
            self.file.get_screen('navi').ids.screen_manager.transition.direction = 'left'
            
    #Calculating glucose levels
    def glucose_cnt(self):
        self.glucose=0
        if self.normal==1:
            self.glucose=random.randint(70,140)
            print(self.glucose)
        else:
            glucose_freq = {"low":self.low,"medium":self.medium,"high":self.high}
            low_glucose1=  random.randint(45,70)
            medium_glucose1=random.randint(141,160)
            high_glucose1=random.randint(161,180)
            glucose_vals = {"low":60,"medium":150,"high":180}
           
            freq=list(glucose_freq.values())
            print(freq)
            sorted_f=freq
            sorted_f.sort(reverse=True)

            #(4,1,1) (5,2,1) (5,1,1) (3,1,1) (4,2,1) (2,1,1)
            if ((sorted_f[0]-sorted_f[1])>1) and ((sorted_f[1]-sorted_f[2])<=1):
                for key, value in glucose_freq.items():
                    if value == sorted_f[0]:
                        self.glucose=glucose_vals[key]
                        break
            #(4,3,2) (4,3,1) (5,4,1) (5,4,2) (4,4,1) (4,4,2) (5,5,1) (5,5,2) (5,5,3) (3,2,1) (3,3,1) (2,2,1)        
            elif ((sorted_f[0]-sorted_f[1])<=1):
               for key, value in glucose_freq.items():
                   if value == sorted_f[0]:
                       self.glucose+=glucose_vals[key]
                   elif value == sorted_f[1]:
                       self.glucose+=glucose_vals[key]
            
               self.glucose=self.glucose/2
                
            else: 
                self.glucose=((freq[0]*low_glucose1)+(freq[1]*medium_glucose1)+(freq[2]*high_glucose1))/sum(freq)
         
            self.glucose=round(self.glucose,2)    
            print(self.glucose)
     #LOW BP SYMPTOMS
    def on_checkbox_active_fainting(self, checkbox, value):
        if value:
            self.low_bp+=1
        elif self.low_bp>0:
            self.low_bp-=1
    def on_checkbox_active_sick(self, checkbox, value):
        if value:
            self.low_bp+=1
        elif self.low_bp>0:
            self.low_bp-=1
    def on_checkbox_active_confusion(self, checkbox, value):
        if value:
            self.low_bp+=1
        elif self.low_bp>0:
            self.low_bp-=1
    def on_checkbox_active_nausea(self, checkbox, value):
        if value:
            self.low_bp+=1
        elif self.low_bp>0:
            self.low_bp-=1
    
            
    #HIGH BP SYMPTOMS
    def on_checkbox_active_bloodurine(self, checkbox, value):
        if value:
            self.high_bp+=1
        elif self.high_bp>0:
            self.high_bp-=1
    def on_checkbox_active_chestpain(self, checkbox, value):
        if value:
            self.high_bp+=1
        elif self.high_bp>0:
            self.high_bp-=1
    def on_checkbox_active_heartbeat(self, checkbox, value):
        if value:
            self.high_bp+=1
        elif self.high_bp>0:
            self.high_bp-=1
    def on_checkbox_active_migraine(self, checkbox, value):
        if value:
            self.high_bp+=1
        elif self.high_bp>0:
            self.high_bp-=1
    
            
    #MODERATE BP SYMTOMS
    def on_checkbox_active_vision(self, checkbox, value):
        if value:
            self.moderate_bp+=1
        elif self.moderate_bp>0:
            self.moderate_bp-=1
    def on_checkbox_active_pounding(self, checkbox, value):
        if value:
            self.moderate_bp+=1
        elif self.moderate_bp>0:
            self.moderate_bp-=1
    def on_checkbox_active_fatigue_bp(self, checkbox, value):
        if value:
            self.moderate_bp+=1
        elif self.moderate_bp>0:
            self.moderate_bp-=1
    def on_checkbox_active_nose(self, checkbox, value):
        if value:
            self.moderate_bp+=1
        elif self.moderate_bp>0:
            self.moderate_bp-=1
    
            
    #NO SYMPTOMS
    def on_checkbox_active_no_symptoms(self, checkbox, value):
        if value:
            self.normal_bp=1
            self.low_bp=0
            self.high_bp=0
            self.moderate_bp=0
            self.file.get_screen('navi').ids.fainting.disabled=True
            self.file.get_screen('navi').ids.sick.disabled=True
            self.file.get_screen('navi').ids.confusion.disabled=True
            self.file.get_screen('navi').ids.nausea.disabled=True
            self.file.get_screen('navi').ids.vision.disabled=True
            self.file.get_screen('navi').ids.pounding.disabled=True
            self.file.get_screen('navi').ids.fatigue_bp.disabled=True
            self.file.get_screen('navi').ids.nosebleeed.disabled=True
            self.file.get_screen('navi').ids.migraine.disabled=True
            self.file.get_screen('navi').ids.heartbeat.disabled=True
            self.file.get_screen('navi').ids.chestpain.disabled=True
            self.file.get_screen('navi').ids.bloodurine.disabled=True
           
            print(self.normal_bp)
            print(self.low_bp)
            print(self.high_bp)
            print(self.moderate_bp)
            

            
            
        else:
            self.file.get_screen('navi').ids.fainting.disabled=False
            self.file.get_screen('navi').ids.sick.disabled=False
            self.file.get_screen('navi').ids.confusion.disabled=False
            self.file.get_screen('navi').ids.nausea.disabled=False
            self.file.get_screen('navi').ids.vision.disabled=False
            self.file.get_screen('navi').ids.pounding.disabled=False
            self.file.get_screen('navi').ids.fatigue_bp.disabled=False
            self.file.get_screen('navi').ids.nosebleeed.disabled=False
            self.file.get_screen('navi').ids.migraine.disabled=False
            self.file.get_screen('navi').ids.heartbeat.disabled=False
            self.file.get_screen('navi').ids.chestpain.disabled=False
            self.file.get_screen('navi').ids.bloodurine.disabled=False
         
            self.file.get_screen('navi').ids.fainting.active=False
            self.file.get_screen('navi').ids.sick.active=False
            self.file.get_screen('navi').ids.confusion.active=False
            self.file.get_screen('navi').ids.nausea.active=False
            self.file.get_screen('navi').ids.vision.active=False
            self.file.get_screen('navi').ids.pounding.active=False
            self.file.get_screen('navi').ids.fatigue_bp.active=False
            self.file.get_screen('navi').ids.nosebleeed.active=False
            self.file.get_screen('navi').ids.migraine.active=False
            self.file.get_screen('navi').ids.heartbeat.active=False
            self.file.get_screen('navi').ids.chestpain.active=False
            self.file.get_screen('navi').ids.bloodurine.active=False
          
         
            self.normal_bp=0
            print(self.normal_bp)
            print(self.low_bp)
            print(self.high_bp)
            print(self.moderate_bp)
            
        
            
    #verify if user has chosen atleast 1 symptom      
    def bp_verify(self):
        if(self.high_bp==0 and self.moderate_bp==0 and self.low_bp==0 and self.normal_bp==0):
            cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
            self.dialog = MDDialog(title = 'Error!',text = "Please choose atleast one symptom!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
            self.dialog.open()
        else:
            self.file.get_screen('navi').ids.screen_manager.current = 'insulinscreen'
            self.file.get_screen('navi').ids.screen_manager.transition.direction = 'left'        
    
    def bp_cnt(self):
        if self.normal_bp==1:
            self.bp= random.randint(60,80)
            print(self.bp)
        else:
            bp_freq = {"low":self.low_bp,"medium":self.moderate_bp,"high":self.high_bp}
            low_bp1=random.randint(45,60)
            moderate_bp1= random.randint(81,120)
            high_bp1=random.randint(121,140)
            bp_vals = {"low":low_bp1,"medium":moderate_bp1,"high":high_bp1}
            freq=list(bp_freq.values())
            print(freq)
            sorted_f=freq
            sorted_f.sort(reverse=True)

            #(4,1,1) (5,2,1) (5,1,1) (3,1,1) (4,2,1) (2,1,1)
            if ((sorted_f[0]-sorted_f[1])>1) and ((sorted_f[1]-sorted_f[2])<=1):
                for key, value in bp_freq.items():
                    if value == sorted_f[0]:
                        self.bp=bp_vals[key]
                        break
            #(4,3,2) (4,3,1) (5,4,1) (5,4,2) (4,4,1) (4,4,2) (5,5,1) (5,5,2) (5,5,3) (3,2,1) (3,3,1) (2,2,1)        
            elif ((sorted_f[0]-sorted_f[1])<=1):
               for key, value in bp_freq.items():
                   if value == sorted_f[0]:
                       self.bp+=bp_vals[key]
                   elif value == sorted_f[1]:
                       self.bp+=bp_vals[key]
            
               self.bp=self.bp/2
                
            else: 
                self.bp=((freq[0]*low_bp1)+(freq[1]*moderate_bp1)+(freq[2]*high_bp1))/sum(freq)
         
            self.bp=round(self.bp,2)    
            print(self.bp)  
            
      #LOW INSULIN SYMPTOMS
    def on_checkbox_active_loss(self, checkbox, value):
        if value:
            self.low_insulin+=1
        elif self.low_insulin>0:
            self.low_insulin-=1
    def on_checkbox_active_sores(self, checkbox, value):
        if value:
            self.low_insulin+=1
        elif self.low_insulin>0:
            self.low_insulin-=1
    def on_checkbox_active_fatigue_insulin(self, checkbox, value):
        if value:
            self.low_insulin+=1
        elif self.low_insulin>0:
            self.low_insulin-=1
    def on_checkbox_active_excess_thirst(self, checkbox, value):
        if value:
            self.low_insulin+=1
        elif self.low_insulin>0:
            self.low_insulin-=1
    def on_checkbox_active_freq_urine(self, checkbox, value):
        if value:
            self.low_insulin+=1
        elif self.low_insulin>0:
            self.low_insulin-=1
            
    #HIGH INSULIN SYMPTOMS
    def on_checkbox_active_intense_hunger(self, checkbox, value):
        if value:
            self.high_insulin+=1
        elif self.high_insulin>0:
            self.high_insulin-=1
    def on_checkbox_active_sugar(self, checkbox, value):
        if value:
            self.high_insulin+=1
        elif self.high_insulin>0:
            self.high_insulin-=1
    def on_checkbox_active_gain(self, checkbox, value):
        if value:
            self.high_insulin+=1
        elif self.high_insulin>0:
            self.high_insulin-=1
    def on_checkbox_active_motivation(self, checkbox, value):
        if value:
            self.high_insulin+=1
        elif self.high_insulin>0:
            self.high_insulin-=1
    def on_checkbox_active_panic(self, checkbox, value):
        if value:
            self.high_insulin+=1
        elif self.high_insulin>0:
            self.high_insulin-=1
    
            
    #NO SYMPTOMS
    def on_checkbox_active_no_symptoms_insulin(self, checkbox, value):
        if value:
            self.normal_insulin=1
            self.low_insulin=0
            self.high_insulin=0
            self.file.get_screen('navi').ids.weightloss.disabled=True
            self.file.get_screen('navi').ids.sores.disabled=True
            self.file.get_screen('navi').ids.fatigue_insulin.disabled=True
            self.file.get_screen('navi').ids.excess_thirst.disabled=True
            self.file.get_screen('navi').ids.freq_urine.disabled=True
            self.file.get_screen('navi').ids.sugar.disabled=True
            self.file.get_screen('navi').ids.intense_hunger.disabled=True
            self.file.get_screen('navi').ids.gain.disabled=True
            self.file.get_screen('navi').ids.motivation.disabled=True
            self.file.get_screen('navi').ids.panic.disabled=True
       
           
            print(self.normal_insulin)
            print(self.low_insulin)
            print(self.high_insulin)
            
            

            
            
        else:
            self.file.get_screen('navi').ids.weightloss.disabled=False
            self.file.get_screen('navi').ids.sores.disabled=False
            self.file.get_screen('navi').ids.fatigue_insulin.disabled=False
            self.file.get_screen('navi').ids.excess_thirst.disabled=False
            self.file.get_screen('navi').ids.freq_urine.disabled=False
            self.file.get_screen('navi').ids.intense_hunger.disabled=False
            self.file.get_screen('navi').ids.sugar.disabled=False
            self.file.get_screen('navi').ids.gain.disabled=False
            self.file.get_screen('navi').ids.motivation.disabled=False
            self.file.get_screen('navi').ids.panic.disabled=False
        
         
            self.file.get_screen('navi').ids.weightloss.active=False
            self.file.get_screen('navi').ids.sores.active=False
            self.file.get_screen('navi').ids.fatigue_insulin.active=False
            self.file.get_screen('navi').ids.excess_thirst.active=False
            self.file.get_screen('navi').ids.freq_urine.active=False
            self.file.get_screen('navi').ids.intense_hunger.active=False
            self.file.get_screen('navi').ids.sugar.active=False
            self.file.get_screen('navi').ids.gain.active=False
            self.file.get_screen('navi').ids.motivation.active=False
            self.file.get_screen('navi').ids.panic.active=False
         
          
         
            self.normal_insulin=0
            print(self.normal_insulin)
            print(self.low_insulin)
            print(self.high_insulin)
           
    
    #verify if user has chosen atleast 1 symptom
    def insulin_verify(self):
        if(self.high_insulin==0 and self.low_insulin==0 and self.normal_insulin==0):
            cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
            self.dialog = MDDialog(title = 'Error!',text = "Please choose atleast one symptom!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
            self.dialog.open()
            
        else:
            self.file.get_screen('navi').ids.screen_manager.current = 'dpfscreen'
            self.file.get_screen('navi').ids.screen_manager.transition.direction = 'left'          
   
    def insulin_cnt(self):
        if self.normal_insulin==1:
            self.insulin= random.randint(16,166)
            print(self.insulin)
        else:
            insulin_freq = {"low":self.low_insulin,"high":self.high_insulin}
            low_insulin1= random.randint(5,15)
            high_insulin1= random.randint(166,180)
            insulin_vals = {"low":low_insulin1,"high":high_insulin1}
           
            freq=list(insulin_freq.values())
            print(freq)
            sorted_f=freq
            sorted_f.sort(reverse=True)

        #(4,1) (5,2) (5,1) (3,1) 
            if (((sorted_f[0]-sorted_f[1])>2) or (((sorted_f[0]-sorted_f[1])==2) and (sorted_f[0]==3))):
                for key, value in insulin_freq.items():
                    if value == sorted_f[0]:
                        self.insulin=insulin_vals[key]
                        break

            else: 
                self.insulin=(low_insulin1+high_insulin1)/2

            self.insulin=round(self.insulin,2)    
            print(self.insulin)
    
    #reset all values from the get checked tab
    def resetformmale(self):
      
        self.file.get_screen('navi').ids.height_text_field_male.text=""
        self.file.get_screen('navi').ids.weight_text_field_male.text=""
        self.file.get_screen('navi').ids.a_text_field.text=""
        self.file.get_screen('navi').ids.b_text_field.text=""
        self.file.get_screen('navi').ids.c_text_field.text=""
        self.file.get_screen('navi').ids.slider1.value=30
        self.file.get_screen('navi').ids.preg_text_field_female.text=""
        self.file.get_screen('navi').ids.height_text_field_female.text=""
        self.file.get_screen('navi').ids.weight_text_field_female.text=""
        self.file.get_screen('navi').ids.slider1_female.value=30
        self.file.get_screen('navi').ids.weightloss.active=False
        self.file.get_screen('navi').ids.sores.active=False
        self.file.get_screen('navi').ids.fatigue_insulin.active=False
        self.file.get_screen('navi').ids.excess_thirst.active=False
        self.file.get_screen('navi').ids.freq_urine.active=False
        self.file.get_screen('navi').ids.intense_hunger.active=False
        self.file.get_screen('navi').ids.sugar.active=False
        self.file.get_screen('navi').ids.gain.active=False
        self.file.get_screen('navi').ids.motivation.active=False
        self.file.get_screen('navi').ids.panic.active=False
        self.file.get_screen('navi').ids.fainting.active=False
        self.file.get_screen('navi').ids.sick.active=False
        self.file.get_screen('navi').ids.confusion.active=False
        self.file.get_screen('navi').ids.nausea.active=False
        self.file.get_screen('navi').ids.vision.active=False
        self.file.get_screen('navi').ids.pounding.active=False
        self.file.get_screen('navi').ids.fatigue_bp.active=False
        self.file.get_screen('navi').ids.nosebleeed.active=False
        self.file.get_screen('navi').ids.migraine.active=False
        self.file.get_screen('navi').ids.heartbeat.active=False
        self.file.get_screen('navi').ids.chestpain.active=False
        self.file.get_screen('navi').ids.bloodurine.active=False
        self.file.get_screen('navi').ids.fruity_smell.active =False
        self.file.get_screen('navi').ids.gum.active =False
        self.file.get_screen('navi').ids.sunburn.active =False
        self.file.get_screen('navi').ids.frequent_urine.active=False 
        self.file.get_screen('navi').ids.blurred.active =False
        self.file.get_screen('navi').ids.wounds.active =False
        self.file.get_screen('navi').ids.bodyache.active =False
        self.file.get_screen('navi').ids.bloating.active =False
        self.file.get_screen('navi').ids.hunger_ext_thirst.active=False 
        self.file.get_screen('navi').ids.turning_pale.active =False
        self.file.get_screen('navi').ids.seizure.active =False
        self.file.get_screen('navi').ids.slurred_speech.active=False 
        self.file.get_screen('navi').ids.palpitation.active =False
        self.file.get_screen('navi').ids.weakness.active=False
        self.file.get_screen('navi').ids.Dizziness.active=False
        self.file.get_screen('navi').ids.no_sym.active=False
        self.file.get_screen('navi').ids.no_symptoms.active=False
        self.file.get_screen('navi').ids.no_symptoms_insulin.active=False
        self.normal_insulin=0
        self.low_insulin=0
        self.high_insulin=0
        self.normal_bp=0
        self.low_bp=0
        self.high_bp=0
        self.moderate_bp=0
        self.normal=0
        self.low=0
        self.high=0
        self.medium=0
     
        #main prediction function
    def prediction(self,preg_text,glucose,bp,insulin_text,bmi_text,no,age_text):
        X1 = data1.drop(columns='Outcome')
        y1 = data1['Outcome']
        X1_train,X1_test,y1_train,y1_test = train_test_split(X1,y1,random_state=0)
        randomforest1 = RandomForestClassifier(n_estimators=500,random_state=100)
        randomforest1.fit(X1_train,y1_train)
        input1 = randomforest1.predict([[preg_text,glucose,bp,insulin_text,bmi_text,no,age_text]])
        output = input1.tostring()
        int_val = int.from_bytes(output,"big")
        if int_val == 0:
            self.dialog = MDDialog(title="         YOU SEEM TO NOT HAVE DIABETES.")
        else:
           self.dialog = MDDialog(title="         YOU MAY HAVE DIABETES. PLEASE GET CHECKED")
     
        self.dialog.open()
        NewApp.resetformmale(self)


    #   MEAL RECOMMENDATION           
     
    def male_checkbox_active(self):
        self.gender = "Male"
        
    def female_checkbox_active(self):
        self.gender = "Female"
        
    def veg_checkbox_active(self):
        self.food_type = "Veg"
        
    def nonveg_checkbox_active(self):
        self.food_type = "Nonveg"
        
    def tea_checkbox_active(self):
        self.beverage = "Tea without sugar"
        
    def coffee_checkbox_active(self):
        self.beverage = "Coffee without sugar"
     
    def bev_verify(self):
        if (self.file.get_screen("navi").ids.tea_check.active == False and self.file.get_screen("navi").ids.coffee_check.active == False):
            cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
            self.dialog = MDDialog(title = 'Error!',text = "Please choose any one beverage!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
            self.dialog.open()
            
        else:
            self.dialog = MDDialog(title = 'Good to go!',text = "Please click on any one tab",size_hint = (0.7,0.2))
            self.dialog.open()
     
    def verify_fields(self):
        self.height_text = self.file.get_screen('navi').ids.height_text_field.text
        self.weight_text = self.file.get_screen('navi').ids.weight_text_field.text
        self.age_text= self.file.get_screen('navi').ids.slidermeal.value
        print(self.age_text)
        if (self.height_text=="" or self.weight_text=="" or (self.file.get_screen("navi").ids.male_check.active == False and self.file.get_screen("navi").ids.female_check.active == False) or (self.file.get_screen("navi").ids.veg_check.active == False and self.file.get_screen("navi").ids.nonveg_check.active == False)):
            cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
            self.dialog = MDDialog(title = 'Error!',text = "Please fill in required fields!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
            self.dialog.open()
            
        else:
            NewApp.expansion(self)
            self.file.get_screen('navi').ids.screen_manager.current = 'activityscreen'
            
    def expansion(self):
        
        for i in range(1):
            self.file.get_screen('navi').ids.activity.add_widget(
                MDExpansionPanel(
                    content=Content(),
                    panel_cls=MDExpansionPanelOneLine(
                        text=""           
                    )
                    
                )
            )
                    

    def activity1(self):
        act1 = self.file.get_screen('navi').ids.one.secondary_text
        NewApp.calorie_counter(self,float(act1))
        
    def activity2(self):
        act2 = self.file.get_screen('navi').ids.two.secondary_text
        NewApp.calorie_counter(self,float(act2))
        
    def activity3(self):
        act3 = self.file.get_screen('navi').ids.three.secondary_text
        NewApp.calorie_counter(self,float(act3))
        
    def activity4(self):
        act4 = self.file.get_screen('navi').ids.four.secondary_text
        NewApp.calorie_counter(self,float(act4))
        
    def activity5(self):
        act5 = self.file.get_screen('navi').ids.five.secondary_text
        NewApp.calorie_counter(self,float(act5))
        
    def activity6(self):
        act6 = self.file.get_screen('navi').ids.six.secondary_text
        NewApp.calorie_counter(self,float(act6))
        
    def activity7(self):
        act7 = self.file.get_screen('navi').ids.seven.secondary_text
        NewApp.calorie_counter(self,float(act7))
        
    def activity8(self):
        act8 = self.file.get_screen('navi').ids.eight.secondary_text
        NewApp.calorie_counter(self,float(act8))
        
    def cuisine1(self):
        c1 = self.file.get_screen('navi').ids.c_one.text
        print(c1)
        
    def cuisine2(self):
        c2 = self.file.get_screen('navi').ids.c_two.text
        print(c2)
        
    def cuisine3(self):
        c3 = self.file.get_screen('navi').ids.c_three.text
        print(c3)
        
    def cuisine4(self):
        c4 = self.file.get_screen('navi').ids.c_four.text
        print(c4)
        
    def cuisine5(self):
        c5 = self.file.get_screen('navi').ids.c_five.text
        print(c5)
        
    def cuisine6(self):
        c6 = self.file.get_screen('navi').ids.c_six.text
        print(c6)
        
    def cuisine7(self):
        c7 = self.file.get_screen('navi').ids.c_seven.text
        print(c7)
        
    def meal_recommendation(self,sample1,sample2):
        
        NewApp.breakfast(self,sample2)
        NewApp.lunch(self,sample1)
        NewApp.snacks(self,sample2)
        NewApp.dinner(self,sample1)
        
    def calorie_counter(self,activity_factor):
        self.height_text = float(self.file.get_screen('navi').ids.height_text_field.text)
        self.weight_text = float(self.file.get_screen('navi').ids.weight_text_field.text)
        self.age_text = int(self.file.get_screen('navi').ids.slidermeal.value)
        
        if (self.height_text=="" or self.weight_text=="" or self.age_text==""):
            cancel_btn_name_dialogue = MDFlatButton(text='Retry',on_release = self.close_dialogue)
            self.dialog = MDDialog(title = 'Error!',text = "Please fill in required fields!",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
            self.dialog.open()
        
        if self.gender=='Female':
            cal_female = ((10*self.weight_text)+(6.25*self.height_text)-(5*self.age_text)-161)*activity_factor
            cal_female=round(cal_female,2)
            self.file.get_screen('navi').ids.daily_calories.text = str(cal_female)
            cal_ld=cal_female/3 #FOR LUNCH AND DINNER
            cal_bs=cal_ld/2 #FOR BREAKFAST AND SNACKS 
            sample1 = np.arange(start=cal_ld,stop=cal_ld+1,step=1).reshape(1,-1)
            sample2 = np.arange(start=cal_bs,stop=cal_bs+1,step=1).reshape(1,-1)
            NewApp.meal_recommendation(self,sample1,sample2)
                

        else:
            cal_male = ((10*self.weight_text)+(6.25*self.height_text)-(5*self.age_text)+5)*activity_factor
            cal_male=round(cal_male,2)
            self.file.get_screen("navi").ids.daily_calories.text = str(cal_male)
            cal_ld=cal_male/3 #FOR LUNCH AND DINNER
            cal_bs=cal_ld/2 #FOR BREAKFAST AND SNACKS 
            sample1 = np.arange(start=cal_ld,stop=cal_ld+1,step=1).reshape(1,-1)
            sample2 = np.arange(start=cal_bs,stop=cal_bs+1,step=1).reshape(1,-1)
            NewApp.meal_recommendation(self,sample1,sample2)
    
    def breakfast(self,sample2):
        if self.food_type=="Veg":
            df_breakfast = df_meal[(df_meal['Category'] == 'Breakfast') & (df_meal['Type'] == 'Veg')]
 
        else:
            df_breakfast = df_meal[(df_meal['Category'] == 'Breakfast')]
            
        df_breakfast_pivot=df_breakfast.pivot_table(index='Dish_name',columns='Category',values='Calories (cal)').fillna(0)
        df_breakfast_pivot_matrix = csr_matrix(df_breakfast_pivot.values)
        
        model_knn.fit(df_breakfast_pivot_matrix)
        distances_bf, indices_bf = model_knn.kneighbors(sample2, n_neighbors = 4)
        for i in range(0, len(distances_bf.flatten())):
            self.recommendation_bf = df_breakfast_pivot.index[indices_bf.flatten()[i]]
            self.list_bf.append(self.recommendation_bf)
            
            
    def swap_breakfast(self):
        self.swap_bf+=1
        if self.swap_bf>=4:
            self.dialog = MDDialog(title = 'Oops!',text = "You are out of options!",size_hint = (0.7,0.2))
            self.dialog.open()
            
        else:
            NewApp.print_breakfast(self)
        
    def print_breakfast(self):
        self.file.get_screen("navi").ids.ok_bf.opacity = 4
        self.file.get_screen("navi").ids.ok_d.opacity = 0
        self.file.get_screen("navi").ids.ok_s.opacity = 0
        self.file.get_screen("navi").ids.ok_l.opacity = 0
        self.file.get_screen("navi").ids.bev_label.text = ""
        self.file.get_screen("navi").ids.tea_label.text = ""
        self.file.get_screen("navi").ids.coffee_label.text = ""
        self.file.get_screen("navi").ids.tea_check.opacity = 0
        self.file.get_screen("navi").ids.coffee_check.opacity = 0
        self.file.get_screen("navi").ids.proceed_button.opacity = 0
        self.file.get_screen("navi").ids.swap_l.opacity = 0
        self.file.get_screen("navi").ids.swap_s.opacity = 0
        self.file.get_screen("navi").ids.swap_d.opacity = 0
        self.file.get_screen("navi").ids.swap_bf.opacity = 4
        self.file.get_screen("navi").ids.swap_bf.disabled = False
        self.file.get_screen("navi").ids.swap_l.disabled = True
        self.file.get_screen("navi").ids.swap_s.disabled = True
        self.file.get_screen("navi").ids.swap_d.disabled = True
        self.file.get_screen("navi").ids.ok_bf.disabled = False
        self.file.get_screen("navi").ids.ok_l.disabled = True
        self.file.get_screen("navi").ids.ok_s.disabled = True
        self.file.get_screen("navi").ids.ok_d.disabled = True
        
        if self.swap_bf>=4:
            self.swap_bf=3
        
        df_breakfast = df_meal[(df_meal['Category'] == 'Breakfast')]
        self.file.get_screen("navi").ids.b_dishname.text = "Dishname: "+str(self.list_bf[self.swap_bf])
        self.serving_bf=df_breakfast['Serving'][df_breakfast[df_breakfast['Dish_name'] == self.list_bf[self.swap_bf]].index.values.astype(int)[0]]
        self.cal_bf=df_breakfast['Calories (cal)'][df_breakfast[df_breakfast['Dish_name'] == self.list_bf[self.swap_bf]].index.values.astype(int)[0]]
        self.file.get_screen("navi").ids.b_serving.text = "Serving: "+str(self.serving_bf)
        self.file.get_screen("navi").ids.b_calories.text = "Calories: "+str(self.cal_bf)
        self.file.get_screen("navi").ids.b_beverage.text = "Beverage: {}".format(self.beverage)
        
        self.file.get_screen("navi").ids.l_dishname.text = ""
        self.file.get_screen("navi").ids.l_serving.text = ""
        self.file.get_screen("navi").ids.l_calories.text = ""
        
        self.file.get_screen("navi").ids.s_dishname.text = ""
        self.file.get_screen("navi").ids.s_serving.text = ""
        self.file.get_screen("navi").ids.s_calories.text = ""
        self.file.get_screen("navi").ids.s_beverage.text = ""
        
        self.file.get_screen("navi").ids.d_dishname.text = ""
        self.file.get_screen("navi").ids.d_serving.text = ""
        self.file.get_screen("navi").ids.d_calories.text = ""
        
    def ok_breakfast(self):
        
        with open('userProfile.json', 'r') as json_file: 
            data1 = json.loads(json_file.read()) 
            
          
        for i in range(len(data1)):
            if data1[i]['email']==self.file.get_screen('navi').ids._email.text:
                
                data1[i]['bf_cal'] = self.cal_bf
                data1[i]['bf_serving'] = self.serving_bf
                data1[i]['bf_name'] = self.recommendation_bf
                data1[i]['bf_bev'] = self.beverage
                break
                    
        with open('userProfile.json', 'w') as json_file:
            json_file.write(json.dumps(data1, indent=4, separators=(',', ': ')))
            
        toast ("Saved!")
            
    def lunch(self,sample1):
          
        if self.food_type=="Veg":
            df_lunch = df_meal[(df_meal['Category'] == 'Lunch') & (df_meal['Type'] == 'Veg')]
 
        else:
            df_lunch = df_meal[(df_meal['Category'] == 'Lunch')]

        df_lunch_pivot=df_lunch.pivot_table(index='Dish_name',columns='Category',values='Calories (cal)').fillna(0)
        df_lunch_pivot_matrix = csr_matrix(df_lunch_pivot.values)
        
        model_knn.fit(df_lunch_pivot_matrix)
        
        distances_l, indices_l = model_knn.kneighbors(sample1, n_neighbors = 4)
        for i in range(0, len(distances_l.flatten())):
            self.recommendation_l = df_lunch_pivot.index[indices_l.flatten()[i]]
            self.list_l.append(self.recommendation_l)
            
    def swap_lunch(self):
        self.swap_l+=1
        if self.swap_l>=4:
            self.dialog = MDDialog(title = 'Oops!',text = "You are out of options!",size_hint = (0.7,0.2))
            self.dialog.open()
            
        else:
            NewApp.print_lunch(self)
            
    def print_lunch(self):
        self.file.get_screen("navi").ids.ok_l.opacity = 4
        self.file.get_screen("navi").ids.ok_bf.opacity = 0
        self.file.get_screen("navi").ids.ok_s.opacity = 0
        self.file.get_screen("navi").ids.ok_d.opacity = 0
        self.file.get_screen("navi").ids.tea_check.opacity = 0
        self.file.get_screen("navi").ids.coffee_check.opacity = 0
        self.file.get_screen("navi").ids.proceed_button.opacity = 0
        self.file.get_screen("navi").ids.swap_l.opacity = 4
        self.file.get_screen("navi").ids.swap_s.opacity = 0
        self.file.get_screen("navi").ids.swap_d.opacity = 0
        self.file.get_screen("navi").ids.swap_bf.opacity = 0
        self.file.get_screen("navi").ids.tea_label.text = ""
        self.file.get_screen("navi").ids.coffee_label.text = ""
        self.file.get_screen("navi").ids.bev_label.text = ""
        self.file.get_screen("navi").ids.swap_bf.disabled = True
        self.file.get_screen("navi").ids.swap_l.disabled = False
        self.file.get_screen("navi").ids.swap_s.disabled = True
        self.file.get_screen("navi").ids.swap_d.disabled = True
        self.file.get_screen("navi").ids.ok_l.disabled = False
        self.file.get_screen("navi").ids.ok_bf.disabled = True
        self.file.get_screen("navi").ids.ok_s.disabled = True
        self.file.get_screen("navi").ids.ok_d.disabled = True
        
        
        if self.swap_l>=4:
            self.swap_l=3
        
        df_lunch = df_meal[(df_meal['Category'] == 'Lunch')]
        self.file.get_screen("navi").ids.l_dishname.text = "Dishname: "+str(self.list_l[self.swap_l])
        self.serving_l=df_lunch['Serving'][df_lunch[df_lunch['Dish_name'] == self.list_l[self.swap_l]].index.values.astype(int)[0]]
        self.cal_l=df_lunch['Calories (cal)'][df_lunch[df_lunch['Dish_name'] == self.list_l[self.swap_l]].index.values.astype(int)[0]]
        self.file.get_screen("navi").ids.l_serving.text = "Serving: "+str(self.serving_l)
        self.file.get_screen("navi").ids.l_calories.text = "Calories: "+str(self.cal_l)
        
        self.file.get_screen("navi").ids.b_beverage.text = ""
        self.file.get_screen("navi").ids.b_dishname.text = ""
        self.file.get_screen("navi").ids.b_serving.text = ""
        self.file.get_screen("navi").ids.b_calories.text = ""
        
        self.file.get_screen("navi").ids.s_dishname.text = ""
        self.file.get_screen("navi").ids.s_serving.text = ""
        self.file.get_screen("navi").ids.s_calories.text = ""
        self.file.get_screen("navi").ids.s_beverage.text = ""
        
        self.file.get_screen("navi").ids.d_dishname.text = ""
        self.file.get_screen("navi").ids.d_serving.text = ""
        self.file.get_screen("navi").ids.d_calories.text = ""
        
        
    def ok_lunch(self):
       
        with open('userProfile.json', 'r') as json_file: 
            data1 = json.loads(json_file.read()) 
            
          
        for i in range(len(data1)):
            if data1[i]['email']==self.file.get_screen('navi').ids._email.text:
                
                data1[i]['l_cal'] = self.cal_l
                data1[i]['l_serving'] = self.serving_l
                data1[i]['l_name'] = self.recommendation_l
                break
                    
        with open('userProfile.json', 'w') as json_file:
            json_file.write(json.dumps(data1, indent=4, separators=(',', ': ')))
            
        toast ("Saved!")
        
        
    def snacks(self,sample2):
                
        if self.food_type=="Veg":
            df_snacks = df_meal[(df_meal['Category'] == 'Snacks') & (df_meal['Type'] == 'Veg')]
 
        else:
            df_snacks = df_meal[(df_meal['Category'] == 'Snacks')]
            
        df_snacks_pivot=df_snacks.pivot_table(index='Dish_name',columns='Category',values='Calories (cal)').fillna(0)
        df_snacks_pivot_matrix = csr_matrix(df_snacks_pivot.values)
        
        model_knn.fit(df_snacks_pivot_matrix)
        
        distances_s, indices_s = model_knn.kneighbors(sample2, n_neighbors = 4)
        for i in range(0, len(distances_s.flatten())):
            self.recommendation_s = df_snacks_pivot.index[indices_s.flatten()[i]]
            self.list_s.append(self.recommendation_s)
            
    def swap_snacks(self):
        self.swap_s+=1
        if self.swap_s>=4:
            self.dialog = MDDialog(title = 'Oops!',text = "You are out of options!",size_hint = (0.7,0.2))
            self.dialog.open()
            
        else:
            NewApp.print_snacks(self)
            
    def print_snacks(self):
        self.file.get_screen("navi").ids.ok_s.opacity = 4
        self.file.get_screen("navi").ids.ok_bf.opacity = 0
        self.file.get_screen("navi").ids.ok_d.opacity = 0
        self.file.get_screen("navi").ids.ok_l.opacity = 0
        self.file.get_screen("navi").ids.tea_check.opacity = 0
        self.file.get_screen("navi").ids.coffee_check.opacity = 0
        self.file.get_screen("navi").ids.proceed_button.opacity = 0
        self.file.get_screen("navi").ids.swap_l.opacity = 0
        self.file.get_screen("navi").ids.swap_s.opacity = 4
        self.file.get_screen("navi").ids.swap_bf.opacity = 0
        self.file.get_screen("navi").ids.swap_d.opacity = 0
        self.file.get_screen("navi").ids.tea_label.text = ""
        self.file.get_screen("navi").ids.coffee_label.text = ""
        self.file.get_screen("navi").ids.bev_label.text = ""
        self.file.get_screen("navi").ids.swap_bf.disabled = True
        self.file.get_screen("navi").ids.swap_l.disabled = True
        self.file.get_screen("navi").ids.swap_s.disabled = False
        self.file.get_screen("navi").ids.swap_d.disabled = True
        self.file.get_screen("navi").ids.ok_s.disabled = False
        self.file.get_screen("navi").ids.ok_l.disabled = True
        self.file.get_screen("navi").ids.ok_bf.disabled = True
        self.file.get_screen("navi").ids.ok_d.disabled = True
        
        
        if self.swap_s>=4:
            self.swap_s=3
        
        df_snacks = df_meal[(df_meal['Category'] == 'Snacks')]
        self.file.get_screen("navi").ids.s_dishname.text = "Dishname: "+str(self.list_s[self.swap_s])
        self.serving_s=df_snacks['Serving'][df_snacks[df_snacks['Dish_name'] == self.list_s[self.swap_s]].index.values.astype(int)[0]]
        self.cal_s=df_snacks['Calories (cal)'][df_snacks[df_snacks['Dish_name'] == self.list_s[self.swap_s]].index.values.astype(int)[0]]
        self.file.get_screen("navi").ids.s_serving.text = "Serving: "+str(self.serving_s)
        self.file.get_screen("navi").ids.s_calories.text = "Calories: "+str(self.cal_s)
        self.file.get_screen("navi").ids.s_beverage.text = "Beverage: {}".format(self.beverage)
        
        self.file.get_screen("navi").ids.l_dishname.text = ""
        self.file.get_screen("navi").ids.l_serving.text = ""
        self.file.get_screen("navi").ids.l_calories.text = ""
        
        self.file.get_screen("navi").ids.b_dishname.text = ""
        self.file.get_screen("navi").ids.b_serving.text = ""
        self.file.get_screen("navi").ids.b_calories.text = ""
        self.file.get_screen("navi").ids.b_beverage.text = ""
        
        self.file.get_screen("navi").ids.d_dishname.text = ""
        self.file.get_screen("navi").ids.d_serving.text = ""
        self.file.get_screen("navi").ids.d_calories.text = ""
        
        
    def ok_snacks(self):
       
        with open('userProfile.json', 'r') as json_file: 
            data1 = json.loads(json_file.read()) 
            
          
        for i in range(len(data1)):
            if data1[i]['email']==self.file.get_screen('navi').ids._email.text:
                
                data1[i]['s_cal'] = self.cal_s
                data1[i]['s_serving'] = self.serving_s
                data1[i]['s_name'] = self.recommendation_s
                data1[i]['s_bev'] = self.beverage
                break
                    
        with open('userProfile.json', 'w') as json_file:
            json_file.write(json.dumps(data1, indent=4, separators=(',', ': ')))
            
        toast ("Saved!")
        
    def dinner(self,sample1):
            
        if self.food_type=="Veg":
            df_dinner = df_meal[(df_meal['Category'] == 'Dinner') & (df_meal['Type'] == 'Veg')]
 
        else:
            df_dinner = df_meal[(df_meal['Category'] == 'Dinner')]
   
        df_dinner_pivot=df_dinner.pivot_table(index='Dish_name',columns='Category',values='Calories (cal)').fillna(0)
        df_dinner_pivot_matrix = csr_matrix(df_dinner_pivot.values)
        
        model_knn.fit(df_dinner_pivot_matrix)
        
        distances_d, indices_d = model_knn.kneighbors(sample1, n_neighbors = 4)
        for i in range(0, len(distances_d.flatten())):
            self.recommendation_d = df_dinner_pivot.index[indices_d.flatten()[i]]
            self.list_d.append(self.recommendation_d)  
            
            
    def swap_dinner(self):
        self.swap_d+=1
        if self.swap_d>=4:
            self.dialog = MDDialog(title = 'Oops!',text = "You are out of options!",size_hint = (0.7,0.2))
            self.dialog.open()
            
        else:
            NewApp.print_dinner(self)
            
    def print_dinner(self):
        self.file.get_screen("navi").ids.ok_d.opacity = 4
        self.file.get_screen("navi").ids.ok_bf.opacity = 0
        self.file.get_screen("navi").ids.ok_s.opacity = 0
        self.file.get_screen("navi").ids.ok_l.opacity = 0
        self.file.get_screen("navi").ids.tea_check.opacity = 0
        self.file.get_screen("navi").ids.coffee_check.opacity = 0
        self.file.get_screen("navi").ids.proceed_button.opacity = 0
        self.file.get_screen("navi").ids.swap_l.opacity = 0
        self.file.get_screen("navi").ids.swap_s.opacity = 0
        self.file.get_screen("navi").ids.swap_bf.opacity = 0
        self.file.get_screen("navi").ids.swap_d.opacity = 4
        self.file.get_screen("navi").ids.tea_label.text = ""
        self.file.get_screen("navi").ids.coffee_label.text = ""
        self.file.get_screen("navi").ids.bev_label.text = ""
        self.file.get_screen("navi").ids.swap_bf.disabled = True
        self.file.get_screen("navi").ids.swap_l.disabled = True
        self.file.get_screen("navi").ids.swap_s.disabled = True
        self.file.get_screen("navi").ids.swap_d.disabled = False
        self.file.get_screen("navi").ids.ok_d.disabled = False
        self.file.get_screen("navi").ids.ok_l.disabled = True
        self.file.get_screen("navi").ids.ok_s.disabled = True
        self.file.get_screen("navi").ids.ok_bf.disabled = True
        
        if self.swap_d>=4:
            self.swap_d=3
        
        df_dinner = df_meal[(df_meal['Category'] == 'Dinner')]
        self.file.get_screen("navi").ids.d_dishname.text = "Dishname: "+str(self.list_d[self.swap_d])
        self.serving_d=df_dinner['Serving'][df_dinner[df_dinner['Dish_name'] == self.list_d[self.swap_d]].index.values.astype(int)[0]]
        self.cal_d=df_dinner['Calories (cal)'][df_dinner[df_dinner['Dish_name'] == self.list_d[self.swap_d]].index.values.astype(int)[0]]
        self.file.get_screen("navi").ids.d_serving.text = "Serving: "+str(self.serving_d)
        self.file.get_screen("navi").ids.d_calories.text = "Calories: "+str(self.cal_d)
        
        self.file.get_screen("navi").ids.l_dishname.text = ""
        self.file.get_screen("navi").ids.l_serving.text = ""
        self.file.get_screen("navi").ids.l_calories.text = ""
        
        self.file.get_screen("navi").ids.s_dishname.text = ""
        self.file.get_screen("navi").ids.s_serving.text = ""
        self.file.get_screen("navi").ids.s_calories.text = ""
        self.file.get_screen("navi").ids.s_beverage.text = ""
        
        self.file.get_screen("navi").ids.b_dishname.text = ""
        self.file.get_screen("navi").ids.b_serving.text = ""
        self.file.get_screen("navi").ids.b_calories.text = ""
        self.file.get_screen("navi").ids.b_beverage.text = ""
        
    def ok_dinner(self):
       
        with open('userProfile.json', 'r') as json_file: 
            data1 = json.loads(json_file.read()) 
            
          
        for i in range(len(data1)):
            if data1[i]['email']==self.file.get_screen('navi').ids._email.text:
                
                data1[i]['d_cal'] = self.cal_d
                data1[i]['d_serving'] = self.serving_d
                data1[i]['d_name'] = self.recommendation_d
                break
                    
        with open('userProfile.json', 'w') as json_file:
            json_file.write(json.dumps(data1, indent=4, separators=(',', ': ')))
            
        toast ("Saved!")
        
    def prev_meals(self):
        
        with open('userProfile.json', 'r') as json_file: 
            data1 = json.loads(json_file.read()) 
            
          
        for i in range(len(data1)):
            if data1[i]['email']==self.file.get_screen('navi').ids._email.text:
                
                self.file.get_screen("navi").ids.prev_bf.text = str(data1[i]['bf_name']) + " & " +str(data1[i]['bf_bev'])
                self.file.get_screen("navi").ids.prev_bf.secondary_text = str(data1[i]['bf_serving'])
                self.file.get_screen("navi").ids.prev_bf.tertiary_text = str(data1[i]['bf_cal'])
                
                self.file.get_screen("navi").ids.prev_l.text = str(data1[i]['l_name'])
                self.file.get_screen("navi").ids.prev_l.secondary_text = str(data1[i]['l_serving'])
                self.file.get_screen("navi").ids.prev_l.tertiary_text = str(data1[i]['l_cal'])
                
                self.file.get_screen("navi").ids.prev_s.text = str(data1[i]['s_name']) + " & " + str(data1[i]['s_bev'])
                self.file.get_screen("navi").ids.prev_s.secondary_text = str(data1[i]['s_serving'])
                self.file.get_screen("navi").ids.prev_s.tertiary_text = str(data1[i]['s_cal'])
                
                self.file.get_screen("navi").ids.prev_d.text = str(data1[i]['d_name'])
                self.file.get_screen("navi").ids.prev_d.secondary_text = str(data1[i]['d_serving'])
                self.file.get_screen("navi").ids.prev_d.tertiary_text = str(data1[i]['d_cal'])
                
                break
        
        
    
    def chg_breakfast(self):
        self.file.get_screen('navi').ids.breakfast_field.md_bg_color=[0,0,0,1]
        self.file.get_screen('navi').ids.lunch_field.md_bg_color=self.theme_cls.primary_color 
        self.file.get_screen('navi').ids.snacks_field.md_bg_color=self.theme_cls.primary_color 
        self.file.get_screen('navi').ids.dinner_field.md_bg_color=self.theme_cls.primary_color 
        
        
    def chg_snacks(self):
        self.file.get_screen('navi').ids.breakfast_field.md_bg_color=self.theme_cls.primary_color
        self.file.get_screen('navi').ids.lunch_field.md_bg_color=self.theme_cls.primary_color 
        self.file.get_screen('navi').ids.snacks_field.md_bg_color=[0,0,0,1]
        self.file.get_screen('navi').ids.dinner_field.md_bg_color=self.theme_cls.primary_color 
        
    def chg_dinner(self):
        self.file.get_screen('navi').ids.breakfast_field.md_bg_color=self.theme_cls.primary_color   
        self.file.get_screen('navi').ids.lunch_field.md_bg_color=self.theme_cls.primary_color 
        self.file.get_screen('navi').ids.snacks_field.md_bg_color=self.theme_cls.primary_color 
        self.file.get_screen('navi').ids.dinner_field.md_bg_color=[0,0,0,1]
        
    def chg_lunch(self):
        self.file.get_screen('navi').ids.breakfast_field.md_bg_color=self.theme_cls.primary_color
        self.file.get_screen('navi').ids.lunch_field.md_bg_color=[0,0,0,1]
        self.file.get_screen('navi').ids.snacks_field.md_bg_color=self.theme_cls.primary_color 
        self.file.get_screen('navi').ids.dinner_field.md_bg_color=self.theme_cls.primary_color 
         
    def chg_all(self):
        self.file.get_screen('navi').ids.breakfast_field.md_bg_color=self.theme_cls.primary_color  
        self.file.get_screen('navi').ids.lunch_field.md_bg_color=self.theme_cls.primary_color
        self.file.get_screen('navi').ids.snacks_field.md_bg_color=self.theme_cls.primary_color 
        self.file.get_screen('navi').ids.dinner_field.md_bg_color=self.theme_cls.primary_color 
           
    
            
    def close_dialogue(self,obj):
        self.dialog.dismiss()
        
    def close_logout_dialog(self,obj):
        self.dialog.dismiss()
        NewApp.reset_logout(self)
        
    def logout_dialog(self):
        cancel_btn_name_dialogue = MDFlatButton(text='Yes',on_release = self.close_logout_dialog)
        self.dialog = MDDialog(title = 'Logout',text = "Are you sure?",size_hint = (0.7,0.2),buttons = [cancel_btn_name_dialogue])
        self.dialog.open()
        
    def reset_func(self):
        
        self.file.get_screen("navi").ids.ok_d.opacity = 0
        self.file.get_screen("navi").ids.ok_bf.opacity = 0
        self.file.get_screen("navi").ids.ok_s.opacity = 0
        self.file.get_screen("navi").ids.ok_l.opacity = 0
        
        self.file.get_screen("navi").ids.tea_check.opacity = 4
        self.file.get_screen("navi").ids.coffee_check.opacity = 4
        self.file.get_screen("navi").ids.proceed_button.opacity = 4
        
        self.file.get_screen("navi").ids.swap_bf.opacity = 0
        self.file.get_screen("navi").ids.swap_l.opacity = 0
        self.file.get_screen("navi").ids.swap_s.opacity = 0
        self.file.get_screen("navi").ids.swap_d.opacity = 0
        
        self.file.get_screen("navi").ids.tea_label.text = "Tea"
        self.file.get_screen("navi").ids.coffee_label.text = "Coffee"
        self.file.get_screen("navi").ids.bev_label.text = "What is your preference?"
                
        self.file.get_screen('navi').ids.height_text_field.text = ""
        self.file.get_screen('navi').ids.weight_text_field.text = ""
        
        self.file.get_screen("navi").ids.b_dishname.text = ""
        self.file.get_screen("navi").ids.b_serving.text = ""
        self.file.get_screen("navi").ids.b_calories.text = ""
        self.file.get_screen("navi").ids.b_beverage.text = ""
        
        
        self.file.get_screen("navi").ids.l_dishname.text = ""
        self.file.get_screen("navi").ids.l_serving.text = ""
        self.file.get_screen("navi").ids.l_calories.text = ""
        
        self.file.get_screen("navi").ids.s_dishname.text = ""
        self.file.get_screen("navi").ids.s_serving.text = ""
        self.file.get_screen("navi").ids.s_calories.text = ""
        self.file.get_screen("navi").ids.s_beverage.text = ""
        
        self.file.get_screen("navi").ids.d_dishname.text = ""
        self.file.get_screen("navi").ids.d_serving.text = ""
        self.file.get_screen("navi").ids.d_calories.text = ""
        self.file.get_screen('navi').ids.slidermeal.value=30
        
        self.file.get_screen("navi").ids.male_check.active = True
        self.file.get_screen("navi").ids.veg_check.active = True
        self.file.get_screen("navi").ids.female_check.active = False
        self.file.get_screen("navi").ids.nonveg_check.active = False
        self.file.get_screen("navi").ids.tea_check.active = False
        self.file.get_screen("navi").ids.coffee_check.active = False
        
        self.swap_bf = 0
        self.swap_l = 0
        self.swap_s = 0
        self.swap_d = 0
        
    def reset_logout(self):
        self.file.get_screen('create').ids.name_text_field.text = ""
        self.file.get_screen('create').ids.email_text_field.text = ""
        self.file.get_screen('create').ids.password_text_field.text = ""
        
        self.file.get_screen('loginscreen').ids.email_text_field.text = ""
        self.file.get_screen('loginscreen').ids.password_text_field.text = ""
        
        NewApp.reset_func(self)
        self.file.get_screen('welcomescreen').manager.current = 'welcomescreen'
        
    def on_start(self):
        
        self.file.get_screen('welcomescreen').manager.current = 'welcomescreen'
        
        
    
    
    

 

    def set_date_1(self, date_obj):
        """
        Sets the start date / display of the start date in the user interface.

        :type date_obj: <class 'datetime.date'>
        :return:
        """
        self.date_1 = date_obj
        self.file.get_screen('navi').ids.date_text.text = str(date_obj.strftime("%d.%m.%Y"))

    def show_date_picker(self):
        """
        Open date dialog.
        :return: void
        """

        MDDatePicker(self.set_date_1,).open()
        
    def set_date_2(self, date_obj):
        """
        Sets the start date / display of the start date in the user interface.

        :type date_obj: <class 'datetime.date'>
        :return:
        """
        self.date_2 = date_obj
        self.file.get_screen('navi').ids.date_text_2.text = str(date_obj.strftime("%d.%m.%Y"))

    def show_date_picker1(self):
        """
        Open date dialog.
        :return: void
        """

        MDDatePicker(self.set_date_2,).open()    
    
  
   
    def show_time_picker1(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time1)
        time_dialog.open()

    def get_time1(self, instance, time):
        self.file.get_screen('navi').ids.time_text1.text = str(time)
        
    def show_time_picker2(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time2)
        time_dialog.open()

    def get_time2(self, instance, time):
        self.file.get_screen('navi').ids.time_text2.text = str(time)
        
    def show_time_picker3(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time3)
        time_dialog.open()

    def get_time3(self, instance, time):
        self.file.get_screen('navi').ids.time_text3.text = str(time)
    
    
    def on_checkbox_active_daily(self, checkbox, value):
        if value:
            
           # self.file.get_screen('navi').ids.date_text.disabled=True
            self.file.get_screen('navi').ids.date_text.text="dd-mm-yyyy"
            #self.file.get_screen('navi').ids.date_text_2.disabled=True
            self.file.get_screen('navi').ids.date_text_2.text="dd-mm-yyyy"
            self.file.get_screen('navi').ids.date.disabled=True
            self.file.get_screen('navi').ids.date1.disabled=True
            self.daily=1
            print(self.daily)
        else:
            self.daily=0
            self.file.get_screen('navi').ids.date.disabled=False
            self.file.get_screen('navi').ids.date1.disabled=False     
            
   
            
   
    def on_swipe_complete(self, instance):
        self.file.get_screen('navi').ids.md_list.remove_widget(instance)
    def on_click_med(self):
     
        '''Creates a list of cards.
        self.file.get_screen('navi').ids.md_list.add_widget(
            
                xyz(text=f"One-line item {32}")
            )
        '''
        for i in range(10):
            self.file.get_screen('navi').ids.md_list.add_widget(
                xyz(text=f"One-line item {i}")
            )
            
    def add(self):
        self.file.get_screen('navi').ids.md_list.add_widget(xyz(text=f"One-line item {30}"))
        self.total=self.total+1
          
    def med_chg1(self):
        self.id=1
        NewApp.med_chg(self,self.id)
        
    def med_chg2(self):
        self.id=2
        NewApp.med_chg(self,self.id)
        
    def med_chg3(self):
        self.id=3
        NewApp.med_chg(self,self.id)
        
    def med_chg4(self):
        self.id=4  
        NewApp.med_chg(self,self.id)
        
    def med_chg5(self):
        self.id=5 
        NewApp.med_chg(self,self.id)
        
    def med_chg6(self):
        self.id=6 
        NewApp.med_chg(self,self.id)
    
    def med_chg7(self):
        self.id=7  
        NewApp.med_chg(self,self.id)
        
    def med_chg8(self):
        self.id=8  
        NewApp.med_chg(self,self.id)
    
    def med_chg(self,id):
        print(id)
        
        with open('userProfile.json', 'r') as json_file:
                 data1 = json.loads(json_file.read())
           
           
         
        for i in range(len(data1)):
    
            if data1[i]['email']==self.file.get_screen('navi').ids._email.text:
                
                self.file.get_screen('navi').ids.medication.text = data1[i]['medicines'][id-1]['med_name']
                self.file.get_screen('navi').ids.description.text = data1[i]['medicines'][id-1]['med_description']
                self.file.get_screen('navi').ids.date_text.text  = data1[i]['medicines'][id-1]['med_start_date']
                self.file.get_screen('navi').ids.date_text_2.text = data1[i]['medicines'][id-1]['med_end_date']
                self.file.get_screen('navi').ids.time_text1.text=data1[i]['medicines'][id-1]['med_time'][0]['time1']
                self.file.get_screen('navi').ids.time_text2.text=data1[i]['medicines'][id-1]['med_time'][0]['time2']
                self.file.get_screen('navi').ids.time_text3.text=data1[i]['medicines'][id-1]['med_time'][0]['time3']
                self.daily = data1[i]['medicines'][id-1]['med_daily']
                if(self.daily==1):
                    self.file.get_screen('navi').ids.daily.active=True
                    self.file.get_screen('navi').ids.date.disabled=True
                    self.file.get_screen('navi').ids.date1.disabled=True
                else:
                    self.file.get_screen('navi').ids.daily.active=False
                    self.file.get_screen('navi').ids.date.disabled=False
                    self.file.get_screen('navi').ids.date1.disabled=False
                    
                    
                break
        self.file.get_screen('navi').ids.screen_manager.current = 'reminder'
      
    
    def med_data_add(self):
       
        print(self.id)
        
        with open('userProfile.json', 'r') as json_file:
            data1 = json.loads(json_file.read())
           
    
        
         
        for i in range(len(data1)):
    
            if data1[i]['email']==self.file.get_screen('navi').ids._email.text:
            
                data1[i]['medicines'][self.id-1]['med_name'] = self.file.get_screen('navi').ids.medication.text
                
                data1[i]['medicines'][self.id-1]['med_description'] = self.file.get_screen('navi').ids.description.text
                data1[i]['medicines'][self.id-1]['med_start_date'] = self.file.get_screen('navi').ids.date_text.text
                data1[i]['medicines'][self.id-1]['med_end_date'] = self.file.get_screen('navi').ids.date_text_2.text
                data1[i]['medicines'][self.id-1]['med_time'][0]['time1'] = self.file.get_screen('navi').ids.time_text1.text
                data1[i]['medicines'][self.id-1]['med_time'][0]['time2'] = self.file.get_screen('navi').ids.time_text2.text
                data1[i]['medicines'][self.id-1]['med_time'][0]['time3'] = self.file.get_screen('navi').ids.time_text3.text
                data1[i]['medicines'][self.id-1]['med_daily'] = self.daily
                break
                   
        with open('userProfile.json', 'w') as json_file:
            json_file.write(json.dumps(data1, indent=4, separators=(',', ': ')))
            
        self.flag0=self.flag1=False
        t1=str(self.file.get_screen('navi').ids.time_text1.text)
        t2=str(self.file.get_screen('navi').ids.time_text2.text)
        t3=str(self.file.get_screen('navi').ids.time_text3.text)
        if(self.id==1):
            self.file.get_screen('navi').ids.content1.text = str( self.file.get_screen('navi').ids.medication.text + " - "+ self.file.get_screen('navi').ids.description.text)
            if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content1.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t2=="00:00:00":
                self.file.get_screen('navi').ids.content1.secondary_text=str(self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content1.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t2=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content1.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours")
            elif t1!="00:00:00" and t2!="00:00:00":
                self.file.get_screen('navi').ids.content1.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t1!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content1.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content1.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            else:
                self.file.get_screen('navi').ids.content1.secondary_text="00:00:00 hours"
                
        if(self.id==2):
            self.file.get_screen('navi').ids.content2.text = str( self.file.get_screen('navi').ids.medication.text + " - "+ self.file.get_screen('navi').ids.description.text)
            if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content2.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t2=="00:00:00":
                self.file.get_screen('navi').ids.content2.secondary_text=str(self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content2.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t2=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content2.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours")
            elif t1!="00:00:00" and t2!="00:00:00":
                self.file.get_screen('navi').ids.content2.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t1!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content2.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content2.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            else:
                self.file.get_screen('navi').ids.content2.secondary_text="00:00:00 hours"
                
        if(self.id==3):
            self.file.get_screen('navi').ids.content3.text = str( self.file.get_screen('navi').ids.medication.text + " - "+ self.file.get_screen('navi').ids.description.text)
            if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content3.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t2=="00:00:00":
                self.file.get_screen('navi').ids.content3.secondary_text=str(self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content3.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t2=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content3.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours")
            elif t1!="00:00:00" and t2!="00:00:00":
                self.file.get_screen('navi').ids.content3.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t1!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content3.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content3.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            else:
                self.file.get_screen('navi').ids.content3.secondary_text="00:00:00 hours"
                
        if(self.id==4):
            self.file.get_screen('navi').ids.content4.text = str( self.file.get_screen('navi').ids.medication.text + " - "+ self.file.get_screen('navi').ids.description.text)
            if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content4.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t2=="00:00:00":
                self.file.get_screen('navi').ids.content4.secondary_text=str(self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content4.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t2=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content4.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours")
            elif t1!="00:00:00" and t2!="00:00:00":
                self.file.get_screen('navi').ids.content4.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t1!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content4.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content4.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            else:
                self.file.get_screen('navi').ids.content4.secondary_text="00:00:00 hours"
                
        if(self.id==5):
            self.file.get_screen('navi').ids.content5.text = str( self.file.get_screen('navi').ids.medication.text + " - "+ self.file.get_screen('navi').ids.description.text)
            if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content5.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t2=="00:00:00":
                self.file.get_screen('navi').ids.content5.secondary_text=str(self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content5.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t2=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content5.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours")
            elif t1!="00:00:00" and t2!="00:00:00":
                self.file.get_screen('navi').ids.content5.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t1!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content5.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content5.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            else:
                self.file.get_screen('navi').ids.content5.secondary_text="00:00:00 hours"
        if(self.id==6):
            self.file.get_screen('navi').ids.content6.text = str( self.file.get_screen('navi').ids.medication.text + " - "+ self.file.get_screen('navi').ids.description.text)
            if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content6.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t2=="00:00:00":
                self.file.get_screen('navi').ids.content6.secondary_text=str(self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content6.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t2=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content6.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours")
            elif t1!="00:00:00" and t2!="00:00:00":
                self.file.get_screen('navi').ids.content6.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t1!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content6.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content6.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            else:
                self.file.get_screen('navi').ids.content6.secondary_text="00:00:00 hours"
        if(self.id==7):
            self.file.get_screen('navi').ids.content7.text = str( self.file.get_screen('navi').ids.medication.text + " - "+ self.file.get_screen('navi').ids.description.text)
            if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content7.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t2=="00:00:00":
                self.file.get_screen('navi').ids.content7.secondary_text=str(self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content7.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t2=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content7.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours")
            elif t1!="00:00:00" and t2!="00:00:00":
                self.file.get_screen('navi').ids.content7.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t1!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content7.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content7.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            else:
                self.file.get_screen('navi').ids.content7.secondary_text="00:00:00 hours"
        if(self.id==8):
            self.file.get_screen('navi').ids.content8.text = str( self.file.get_screen('navi').ids.medication.text + " - "+ self.file.get_screen('navi').ids.description.text)
            if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content8.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t2=="00:00:00":
                self.file.get_screen('navi').ids.content8.secondary_text=str(self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t1=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content8.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t2=="00:00:00" and t3=="00:00:00":
                self.file.get_screen('navi').ids.content8.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours")
            elif t1!="00:00:00" and t2!="00:00:00":
                self.file.get_screen('navi').ids.content8.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text2.text + " hours")
            elif t1!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content8.secondary_text=str(self.file.get_screen('navi').ids.time_text1.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            elif t2!="00:00:00" and t3!="00:00:00":
                self.file.get_screen('navi').ids.content8.secondary_text=str(self.file.get_screen('navi').ids.time_text2.text + " hours , "+self.file.get_screen('navi').ids.time_text3.text + " hours")
            else:
                self.file.get_screen('navi').ids.content8.secondary_text="00:00:00 hours"
        
        toast ("Saved!")
        self.med_submit=1
        #back2(self)
    def card(self):
        '''
        toaster = ToastNotifier()
     

        toaster.show_toast("Example two",
                   "This notification is in it's own thread!",
                   icon_path=None,
                   duration=2,
                   threaded=False)
        '''
# Wait for threaded notification to finish
    #    while toaster.notification_active():
     #       time.sleep(0.1)
            
        with open('userProfile.json', 'r') as json_file:
            data1 = json.loads(json_file.read())
        
        for i in range(len(data1)):
            if data1[i]['email']==self.file.get_screen('navi').ids._email.text:
                self.file.get_screen('navi').ids.content1.text = str( data1[i]['medicines'][0]['med_name']+" - "+data1[i]['medicines'][0]['med_description'])
                t1=str(data1[i]['medicines'][0]['med_time'][0]['time1'])
                t2=str(data1[i]['medicines'][0]['med_time'][0]['time2'])
                t3=str(data1[i]['medicines'][0]['med_time'][0]['time3'])
                if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content1.secondary_text=str(t1+ " hours , "+t2+" hours , "+t3 + " hours")
                elif t1=="00:00:00" and t2=="00:00:00":
                    self.file.get_screen('navi').ids.content1.secondary_text=str(t3 + " hours")
                elif t1=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content1.secondary_text=str(t2 + " hours")
                elif t2=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content1.secondary_text=str(t1 + " hours")
                elif t1!="00:00:00" and t2!="00:00:00":
                    self.file.get_screen('navi').ids.content1.secondary_text=str(t1 + " hours , "+t2 + " hours")
                elif t1!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content1.secondary_text=str(t1 + " hours , "+t3 + " hours")
                elif t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content1.secondary_text=str(t2 + " hours , "+t3 + " hours")
                else:
                    self.file.get_screen('navi').ids.content1.secondary_text="00:00:00 hours"
                    
            
                self.file.get_screen('navi').ids.content2.text = str( data1[i]['medicines'][1]['med_name']+" - "+data1[i]['medicines'][1]['med_description'])
                t1=str(data1[i]['medicines'][1]['med_time'][0]['time1'])
                t2=str(data1[i]['medicines'][1]['med_time'][0]['time2'])
                t3=str(data1[i]['medicines'][1]['med_time'][0]['time3'])
                if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content2.secondary_text=str(t1+ " hours , "+t2+" hours , "+t3 + " hours")
                elif t1=="00:00:00" and t2=="00:00:00":
                    self.file.get_screen('navi').ids.content2.secondary_text=str(t3 + " hours")
                elif t1=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content2.secondary_text=str(t2 + " hours")
                elif t2=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content2.secondary_text=str(t1 + " hours")
                elif t1!="00:00:00" and t2!="00:00:00":
                    self.file.get_screen('navi').ids.content2.secondary_text=str(t1 + " hours , "+t2 + " hours")
                elif t1!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content2.secondary_text=str(t1 + " hours , "+t3 + " hours")
                elif t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content2.secondary_text=str(t2 + " hours , "+t3 + " hours")
                else:
                    self.file.get_screen('navi').ids.content2.secondary_text="00:00:00 hours"
                
                
                self.file.get_screen('navi').ids.content3.text = str( data1[i]['medicines'][2]['med_name']+" - "+data1[i]['medicines'][2]['med_description'])
                t1=str(data1[i]['medicines'][2]['med_time'][0]['time1'])
                t2=str(data1[i]['medicines'][2]['med_time'][0]['time2'])
                t3=str(data1[i]['medicines'][2]['med_time'][0]['time3'])
                if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content3.secondary_text=str(t1+ " hours , "+t2+" hours , "+t3 + " hours")
                elif t1=="00:00:00" and t2=="00:00:00":
                    self.file.get_screen('navi').ids.content3.secondary_text=str(t3 + " hours")
                elif t1=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content3.secondary_text=str(t2 + " hours")
                elif t2=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content3.secondary_text=str(t1 + " hours")
                elif t1!="00:00:00" and t2!="00:00:00":
                    self.file.get_screen('navi').ids.content3.secondary_text=str(t1 + " hours , "+t2 + " hours")
                elif t1!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content3.secondary_text=str(t1 + " hours , "+t3 + " hours")
                elif t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content3.secondary_text=str(t2 + " hours , "+t3 + " hours")
                else:
                    self.file.get_screen('navi').ids.content3.secondary_text="00:00:00 hours"

                                                                                                  
                self.file.get_screen('navi').ids.content4.text = str( data1[i]['medicines'][3]['med_name']+" - "+data1[i]['medicines'][3]['med_description'])
                t1=str(data1[i]['medicines'][3]['med_time'][0]['time1'])
                t2=str(data1[i]['medicines'][3]['med_time'][0]['time2'])
                t3=str(data1[i]['medicines'][3]['med_time'][0]['time3'])
                if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content4.secondary_text=str(t1+ " hours , "+t2+" hours , "+t3 + " hours")
                elif t1=="00:00:00" and t2=="00:00:00":
                    self.file.get_screen('navi').ids.content4.secondary_text=str(t3 + " hours")
                elif t1=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content4.secondary_text=str(t2 + " hours")
                elif t2=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content4.secondary_text=str(t1 + " hours")
                elif t1!="00:00:00" and t2!="00:00:00":
                    self.file.get_screen('navi').ids.content4.secondary_text=str(t1 + " hours , "+t2 + " hours")
                elif t1!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content4.secondary_text=str(t1 + " hours , "+t3 + " hours")
                elif t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content4.secondary_text=str(t2 + " hours , "+t3 + " hours")
                else:
                    self.file.get_screen('navi').ids.content4.secondary_text="00:00:00 hours"

                
                self.file.get_screen('navi').ids.content5.text = str( data1[i]['medicines'][4]['med_name']+" - "+data1[i]['medicines'][4]['med_description'])
                t1=str(data1[i]['medicines'][4]['med_time'][0]['time1'])
                t2=str(data1[i]['medicines'][4]['med_time'][0]['time2'])
                t3=str(data1[i]['medicines'][4]['med_time'][0]['time3'])
                if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content5.secondary_text=str(t1+ " hours , "+t2+" hours , "+t3 + " hours")
                elif t1=="00:00:00" and t2=="00:00:00":
                    self.file.get_screen('navi').ids.content5.secondary_text=str(t3 + " hours")
                elif t1=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content5.secondary_text=str(t2 + " hours")
                elif t2=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content5.secondary_text=str(t1 + " hours")
                elif t1!="00:00:00" and t2!="00:00:00":
                    self.file.get_screen('navi').ids.content5.secondary_text=str(t1 + " hours , "+t2 + " hours")
                elif t1!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content5.secondary_text=str(t1 + " hours , "+t3 + " hours")
                elif t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content5.secondary_text=str(t2 + " hours , "+t3 + " hours")
                else:
                    self.file.get_screen('navi').ids.content5.secondary_text="00:00:00 hours"



                self.file.get_screen('navi').ids.content6.text = str( data1[i]['medicines'][5]['med_name']+" - "+data1[i]['medicines'][5]['med_description'])
                t1=str(data1[i]['medicines'][5]['med_time'][0]['time1'])
                t2=str(data1[i]['medicines'][5]['med_time'][0]['time2'])
                t3=str(data1[i]['medicines'][5]['med_time'][0]['time3'])
                if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content6.secondary_text=str(t1+ " hours , "+t2+" hours , "+t3 + " hours")
                elif t1=="00:00:00" and t2=="00:00:00":
                    self.file.get_screen('navi').ids.content6.secondary_text=str(t3 + " hours")
                elif t1=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content6.secondary_text=str(t2 + " hours")
                elif t2=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content6.secondary_text=str(t1 + " hours")
                elif t1!="00:00:00" and t2!="00:00:00":
                    self.file.get_screen('navi').ids.content6.secondary_text=str(t1 + " hours , "+t2 + " hours")
                elif t1!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content6.secondary_text=str(t1 + " hours , "+t3 + " hours")
                elif t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content6.secondary_text=str(t2 + " hours , "+t3 + " hours")
                else:
                    self.file.get_screen('navi').ids.content6.secondary_text="00:00:00 hours"


                self.file.get_screen('navi').ids.content7.text = str( data1[i]['medicines'][6]['med_name']+" - "+data1[i]['medicines'][6]['med_description'])
                t1=str(data1[i]['medicines'][6]['med_time'][0]['time1'])
                t2=str(data1[i]['medicines'][6]['med_time'][0]['time2'])
                t3=str(data1[i]['medicines'][6]['med_time'][0]['time3'])
                if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content7.secondary_text=str(t1+ " hours , "+t2+" hours , "+t3 + " hours")
                elif t1=="00:00:00" and t2=="00:00:00":
                    self.file.get_screen('navi').ids.content7.secondary_text=str(t3 + " hours")
                elif t1=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content7.secondary_text=str(t2 + " hours")
                elif t2=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content7.secondary_text=str(t1 + " hours")
                elif t1!="00:00:00" and t2!="00:00:00":
                    self.file.get_screen('navi').ids.content7.secondary_text=str(t1 + " hours , "+t2 + " hours")
                elif t1!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content7.secondary_text=str(t1 + " hours , "+t3 + " hours")
                elif t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content7.secondary_text=str(t2 + " hours , "+t3 + " hours")
                else:
                    self.file.get_screen('navi').ids.content7.secondary_text="00:00:00 hours"
                
                
                self.file.get_screen('navi').ids.content8.text = str( data1[i]['medicines'][7]['med_name']+" - "+data1[i]['medicines'][7]['med_description'])
                t1=str(data1[i]['medicines'][7]['med_time'][0]['time1'])
                t2=str(data1[i]['medicines'][7]['med_time'][0]['time2'])
                t3=str(data1[i]['medicines'][7]['med_time'][0]['time3'])
                if t1!="00:00:00" and t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content8.secondary_text=str(t1+ " hours , "+t2+" hours , "+t3 + " hours")
                elif t1=="00:00:00" and t2=="00:00:00":
                    self.file.get_screen('navi').ids.content8.secondary_text=str(t3 + " hours")
                elif t1=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content8.secondary_text=str(t2 + " hours")
                elif t2=="00:00:00" and t3=="00:00:00":
                    self.file.get_screen('navi').ids.content8.secondary_text=str(t1 + " hours")
                elif t1!="00:00:00" and t2!="00:00:00":
                    self.file.get_screen('navi').ids.content8.secondary_text=str(t1 + " hours , "+t2 + " hours")
                elif t1!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content8.secondary_text=str(t1 + " hours , "+t3 + " hours")
                elif t2!="00:00:00" and t3!="00:00:00":
                    self.file.get_screen('navi').ids.content8.secondary_text=str(t2 + " hours , "+t3 + " hours")
                else:
                    self.file.get_screen('navi').ids.content8.secondary_text="00:00:00 hours"

    
    def remove_med(self):
        self.remove_medi=self.file.get_screen('navi').ids.medication.text
        
   
        #index_medname=index_medtime=0
        #index_medname=self.medicine_names.index(self.remove_medi)
        #index_medtime=self.medicine_times.index(self.remove_time)
        for i in range(len(self.medicine_names)):
            if ((self.medicine_names[i]==self.remove_medi)):
                self.medicine_names.remove(self.medicine_names[i])
                self.medicine_times.remove(self.medicine_times[i])
                self.medicine_desc.remove(self.medicine_desc[i])
                break
        
        
        
        print("after removal",self.medicine_names)
        self.med_submit=2 
        NewApp.resetmed(self)                                                                                             
                
    def resetmed(self):
        with open('userProfile.json', 'r') as json_file:
            data1 = json.loads(json_file.read())
        
        
        for i in range(len(data1)):
    
            if data1[i]['email']==self.file.get_screen('navi').ids._email.text:
                
                data1[i]['medicines'][self.id-1]['med_name'] = "Add medicine"
                data1[i]['medicines'][self.id-1]['med_description'] = "Add description"
                data1[i]['medicines'][self.id-1]['med_start_date'] = "dd-mm-yyyy"
                data1[i]['medicines'][self.id-1]['med_end_date'] = "dd-mm-yyyy"
                data1[i]['medicines'][self.id-1]['med_time'][0]['time1']= "00:00:00"
                data1[i]['medicines'][self.id-1]['med_time'][0]['time2']= "00:00:00"
                data1[i]['medicines'][self.id-1]['med_time'][0]['time3']= "00:00:00"
                data1[i]['medicines'][self.id-1]['med_daily'] = 0
                
                self.file.get_screen('navi').ids.date_text.text  = data1[i]['medicines'][self.id-1]['med_start_date']
                self.file.get_screen('navi').ids.date_text_2.text = data1[i]['medicines'][self.id-1]['med_end_date']
                self.file.get_screen('navi').ids.time_text1.text=data1[i]['medicines'][self.id-1]['med_time'][0]['time1']
                self.file.get_screen('navi').ids.time_text2.text=data1[i]['medicines'][self.id-1]['med_time'][0]['time2']
                self.file.get_screen('navi').ids.time_text3.text=data1[i]['medicines'][self.id-1]['med_time'][0]['time3']
                self.daily = data1[i]['medicines'][self.id-1]['med_daily']
                    
                break
        
        with open('userProfile.json', 'w') as json_file:
                 json_file.write(json.dumps(data1, indent=4, separators=(',', ': ')))  
             
        self.file.get_screen('navi').ids.screen_manager.current = 'reminder'
     
        self.file.get_screen('navi').ids.daily.active=False
        
        if(self.id==1):
            self.file.get_screen('navi').ids.content1.text = str("Add medicine - Add description")
            self.file.get_screen('navi').ids.content1.secondary_text=str("00:00:00 hours")
        elif(self.id==2):     
            self.file.get_screen('navi').ids.content2.text = str("Add medicine - Add description")
            self.file.get_screen('navi').ids.content2.secondary_text=str("00:00:00 hours")
        elif(self.id==3):       
            self.file.get_screen('navi').ids.content3.text = str("Add medicine - Add description")
            self.file.get_screen('navi').ids.content3.secondary_text=str("00:00:00 hours")
        elif(self.id==4):                                                                                              
            self.file.get_screen('navi').ids.content4.text = str("Add medicine - Add description")
            self.file.get_screen('navi').ids.content4.secondary_text=str("00:00:00 hours")
        elif(self.id==5):          
            self.file.get_screen('navi').ids.content5.text = str("Add medicine - Add description")
            self.file.get_screen('navi').ids.content5.secondary_text=str("00:00:00 hours") 
        elif(self.id==6):
            self.file.get_screen('navi').ids.content6.text = str("Add medicine - Add description")
            self.file.get_screen('navi').ids.content6.secondary_text=str("00:00:00 hours")    
        elif(self.id==7):
            self.file.get_screen('navi').ids.content7.text = str("Add medicine - Add description")
            self.file.get_screen('navi').ids.content7.secondary_text=str("00:00:00 hours")          
        elif(self.id==8):
            self.file.get_screen('navi').ids.content8.text = str("Add medicine - Add description")
            self.file.get_screen('navi').ids.content8.secondary_text=str("00:00:00 hours")  
    
          
        

    def __init__(self, **kwargs):
        
        self.title = "Diabetes Care"
        super().__init__(**kwargs)
        self.date_1 = None
        self.date_2 = None
        self.time_1 = None
        
        

if __name__ == "__main__":
    NewApp().run()
    
