# setup/imports
from operator import add
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import datetime
import time
from selenium.webdriver.firefox.service import Service
from schoologyLogin import login

# Globals
s=Service('C:/Users/zechaaron/Downloads/geckodriver.exe')
browser =  webdriver.Firefox(service=s)
userList = [] # list of students to check if their parents have the right schools attached
updatedParentList =[] # store list of parents that were change
parentFile = open("ParentChange.txt", "a")
parentEmail_Global = ''
parentEmail_Global_2 = ''
continueProgram = True
sleep_Adjustment = 0
fastmode = False
parentSchoologyProfileURL =''
parentSchoologyProfileURL_2 = ''
secondParentID = ''
thirdParentID = ''

# Functions

# Saves changes on the edit users page
def saveChanges():
    
    saveButton = browser.find_element(By.ID,'edit-submit')
    saveButton.submit()
    time.sleep(1.25+sleep_Adjustment) # delay for more reliablity
    #browser.get('https://osseo.schoology.com/users/manage/edit/moreinfo')

# Adds in the new school to match the student
def changePrimarySchool(SchoolName,childCount): 

    # Schoology not accepting Osseo ALC Sr High need to remove high
    if SchoolName == 'Osseo ALC Sr High':
        SchoolName = 'Osseo ALC Sr' 
    
    # Parent Only Has One Child Override the current school.
    if childCount == 1:
        schoolbox = browser.find_element(By.ID,'select2-chosen-4')
        schoolbox.click()
        schoolbox1 = browser.find_element(By.ID,'s2id_autogen4_search')  #
        schoolbox1.click()
        schoolbox1.send_keys(SchoolName)
        schoolbox1.send_keys(Keys.RETURN)
        return
    elif childCount ==2:
        #school count = 1
        input("Press Enter if you see just one school listed, else enter number of schools") 
        try:
            add_school_box = browser.find_element(By.CSS_SELECTOR,'.add-building-link')
            add_school_box.click()
            select_a_school_box = browser.find_element(By.CSS_SELECTOR,'#select2-chosen-8').click()
            inputBox = browser.find_element(By.CSS_SELECTOR,"#s2id_autogen8_search")
            inputBox.send_keys(SchoolName)
            inputBox.send_keys(Keys.RETURN)
        
        #school count = 2+
        except:
            # Single Search Result
            if childCount == 1:
                schoolbox = browser.find_element(By.ID,'select2-chosen-4')
                schoolbox.click()
                schoolbox1 = browser.find_element(By.ID,'s2id_autogen4_search')  #
                schoolbox1.click()
                schoolbox1.send_keys(SchoolName)
                schoolbox1.send_keys(Keys.RETURN)

            if childCount == 2:
                try:
                    schoolbox = browser.find_element(By.ID,'select2-chosen-5')
                    schoolbox.click()
                    schoolbox1 = browser.find_element(By.ID,'s2id_autogen5_search')  #
                    schoolbox1.click()
                    schoolbox1.send_keys(SchoolName)
                    schoolbox1.send_keys(Keys.RETURN)
                except:
                    print('break')
    elif childCount == 3:
        print('3 kids')
        
        # Method 1
        # Works on a Parent with 2 aleady configured school sites
        try:
            add_school_box = browser.find_element(By.CSS_SELECTOR,'.add-building-link')
            add_school_box.click()
            select_a_school_box = browser.find_element(By.XPATH,'//*[@id="select2-chosen-12"]').click()
            inputBox = browser.find_element(By.XPATH,'//*[@id="s2id_autogen12_search"]') 
            inputBox.send_keys(SchoolName)
            inputBox.send_keys(Keys.RETURN)
            return

        except:
             print('Error on Method 1')

        # Method 2
        # 1 School Already Configured
        try:
            select_a_school_box = browser.find_element(By.CSS_SELECTOR,'#select2-chosen-8').click()
            inputBox = browser.find_element(By.CSS_SELECTOR,"#s2id_autogen8_search")
            inputBox.send_keys(SchoolName)
            inputBox.send_keys(Keys.RETURN)
            return
        except:
            print("error on method 2")
        try:
            addSchool_Button = browser.find_element(By.XPATH,'//*[@id="edit-users-'+userID+'-building-nid-wrapper"]/div/div/div/a')
            addSchool_Button.click()  # works
            selectSchool = browser.find_element(By.XPATH,'//*[@id="select2-chosen-8"]')
            selectSchool.click()
            addSchool_SearchBox = browser.find_element(By.XPATH,'//*[@id="s2id_autogen8_search"]') #was 8
            addSchool_SearchBox.send_keys(student_school)
            addSchool_SearchBox.send_keys(Keys.RETURN)
            time.sleep(.8 + sleep_Adjustment)
        except:
            try:
                selectSchool = browser.find_element(By.XPATH,'//*[@id="select2-chosen-16"]')
                selectSchool.click()
                addSchool_SearchBox = browser.find_element(By.XPATH,'//*[@id="s2id_autogen16_search"]') #was 8
                addSchool_SearchBox.send_keys(student_school)
                addSchool_SearchBox.send_keys(Keys.RETURN)
            except:
                print('Error on 3 child parent try block:' + str(userList[i]))
                browser.quit()


# Populates the userList variable from the CSV file data
def populateUserList(MAX_SIZE):
    with open('users.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        for row in csv_reader:
            print(row)
            userList.append(row)
            if count > MAX_SIZE:  # break loop after 25 rows
                break
            count += 1

# Searches the student Schoology profile and reads the school data, and looks for parent
def studentProfile(username):
    username = userList[i]
    print("Username:",username)
    searchBox = browser.find_element(By.ID,'edit-filter-search')

    searchBox.send_keys(username)  # enter username to search for

    time.sleep(0.75+sleep_Adjustment) # delay for more reliablity

    searchButton = browser.find_element(By.CLASS_NAME,'sExtlink-processed').click()

    time.sleep(0.5+sleep_Adjustment) # delay for more reliablity

    submitForm = browser.find_element(By.CLASS_NAME,'sUserFilterForm-processed')
    submitForm.submit()

    time.sleep(4.5 + sleep_Adjustment) # delay for more reliablity

    # Search results page
    # open user profile
    try: 
        profileLink = browser.find_element(By.CSS_SELECTOR,"[title^='View user profile.']")
        profileLink.click()

        # Loaded Students profile page, scrape school info
        SchoolName = browser.find_element(By.CLASS_NAME,'school-name').text
        SchoolName = SchoolName.split(',', 1)[0]
        print('Student School: ' + SchoolName)
        print('\n')

        return SchoolName
    except:
        print("Error")
        global continueProgram
        continueProgram = False
        return

def checkForSecondParent():
    try:
        if(browser.find_element(By.XPATH,'//*[@id="main-inner"]/table/tbody/tr[3]/td/a[2]')):
            print("2nd parent found")
            # Not saving to global variable
            global secondParentID
            secondParentID = browser.find_element(By.XPATH,'//*[@id="main-inner"]/table/tbody/tr[3]/td/a[2]').get_attribute('href') #grab URL of 2nd parent           
            return True
    except: 
        print("No 2nd Parent")
    
def checkForThirdParent():
    try:
        if(browser.find_element(By.XPATH,'//*[@id="main-inner"]/table/tbody/tr[3]/td/a[3]')):
            print("3rd parent found")
            thirdParentID = browser.find_element(By.XPATH,'//*[@id="main-inner"]/table/tbody/tr[3]/td/a[3]').get_attribute('href')
            return True
    except:
        print("No 3rd Parent")

# Opens Parent Schoology account profile and reads data
# Returns the parent school
def readParentSchool():

    # check for more then one school
    try:
        showAllButton = browser.find_element(By.XPATH,'//*[@id="center-top"]/div/div/div/span/span[2]') #failed on 4 buildings
        showAllButton.click()
        parentSchool1 = browser.find_element(By.CLASS_NAME,'school-name').text
        print("parentSchool1:",parentSchool1)
        return parentSchool1
    except:
        #print('No Show All Button')
        parentSchool1 = browser.find_element(By.CLASS_NAME,'school-name').text
        print("Parent School: ",parentSchool1)
        return parentSchool1

# Grabs the Parent Schoology User ID & formats it into a string
def getParentUserID():
    userID = browser.current_url
    userID = userID.split('user/', 1)[1]
    #print(userID)
    userID = userID.split('/', 1)[0]
    #print(userID)
    return userID

# Reads how manys students are connected to the parent account
def getChildCount():
    child1 = browser.find_element(By.XPATH,'//*[@id="main-inner"]/table/tbody/tr/td/a').text  # No email parent
    #print("Child 1: " + child1)
    if child1 != '':
        childCount = 1

    # Then check for multiple children
    # check for multiple kids

    try:
        child2 = browser.find_element(By.XPATH,'//*[@id="main-inner"]/table/tbody/tr/td/a[2]').text

        #print('Child2: ' + child2)

        if child2 != '':
            childCount = 2
    except:
        print('no second child')

    if childCount == 2:
         try:
            child3 = browser.find_element(By.XPATH,'//*[@id="main-inner"]/table/tbody/tr[3]/td/a[3]').text
            if child3 !='':
                childCount = 3
         except:
             print('no third child')

    return childCount

# Click on parent profile on the student's profile page
def clickOnParentProfile():
    #Process the first parent
    try:
        profileLink = browser.find_element(By.CSS_SELECTOR,"[title^='View user profile.']") #on the student page currently
        profileLink.click() # on the student page curently
    except:
        print("\n----no parent found---\n--------------------------------\n")
        global continueProgram
        continueProgram = False
        return

def findParentEmail():
    
    try:
        parentEmail = browser.find_element(By.CSS_SELECTOR,"a.mailto").text
        return parentEmail
    except: 
        
        # Try again to find the email
        try:
            parentEmail = browser.find_element(By.XPATH,'#/html/body/div[3]/div[3]/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr[4]/td/span/a').text
            return parentEmail
        except:
            print("No Email Found")
            parentEmail = "~"
            return parentEmail

# Print out Changes to the log file
def parentLogFile(childCount):
    currentDT = datetime.datetime.now()
    print ()
    print('\n----------------\nParent:' + str(i) + ' ' + parentEmail_Global + ' of ' + str(userList[i]) + ' updated\n')
    print('School Added: ' + student_school + '\n------------------')
    updatedParentList.__add__((userList[i]))
    # Iterate Loop
    parentFile.write(
        '\n----------------\nParent:' + str(i) + ' ' + parentEmail_Global + ' of ' + str(userList[i]) + ' updated\n' + 'School Added: '
        + student_school + '\n' + parentSchool +  '\nold School:' + str(currentDT) + " Child Counts:" + str(childCount) 
        + '\nParent Schoology Profile URL: ' + parentSchoologyProfileURL +
        '\n------------------')

# Log students who have the same school as their parent to this file 
def sameSchoolAsChildLogFile(count):
    print('\nSAME SCHOOL AS CHILD: ' + str(userList[count]) +  '\n-----------------\n')
    browser.get('https://osseo.schoology.com/users/manage/edit/moreinfo')
    f = open("SameAsChildList.txt", "a")
    f.write(str(userList[count]) + "\n")
    f.close()

def processSecondParent(student_school):
    browser.get(secondParentID); # Opens the tab of the second parents profile
    # Need to read in the school
    parentSchool = readParentSchool()
    print("Second Parent School - ",parentSchool)
    # Store the second parents email
    parentEmail_Global_2 = findParentEmail()
    #add a child count read?
    childCount = getChildCount()
    print("Second Parent Child Count = ",childCount)
                
    # Check if 2nd parent school matches studetn
    if student_school in parentSchool:
        print("Second Parent: Same as student School")
        return
    else:
        print("Second Parent has a different school")
        browser.get("https://osseo.schoology.com/users/manage/edit/moreinfo?role=266607&search="+parentEmail_Global_2)
        changePrimarySchool(student_school,childCount)
        print(parentEmail_Global_2)
        saveChanges()
#-------------------------------------------
# Main Program Start
#-------------------------------------------
# Load up browser and login to Schoology

# Adjust the sleep delays throughout the program
if(fastmode == True):
    sleep_Adjustment = -0.25

#Log in to Schoology 
login(browser) 

# Populate userlist from CS
populateUserList(500) #enter max size of list #-works 8/22

#Loop thorugh the student list
length = len(userList)
i=1
while i < length:

    continueProgram = True
    # Load Schoology user management page
    browser.get("https://osseo.schoology.com/users/manage/edit/moreinfo")
    # read in the students school
    student_school = studentProfile(userList[i])

    if continueProgram == False:
        i += 1
        continue

    # read in parents schools
    #Check for more then one parent
    if(checkForSecondParent()):
        checkForThirdParent()

    # Open the Parent #1's profile page
    clickOnParentProfile()

    # Read Parent #1's schools
    parentSchool = readParentSchool()

    # Exit the current Loop iteration if no parent was found from above
    if continueProgram == False:
        i += 1
        continue

    # Grab parent #1's Schoology user ID
    userID = getParentUserID()

    parentEmailFound = False
    noChildFoundErro = False
    parentUserID = 0

    # If the child matches the parent school
    if student_school in parentSchool:
        
        # Log Result
        sameSchoolAsChildLogFile(i)

        #Process the second parent if there is one
        if(secondParentID!=''):
            processSecondParent(student_school) 

        browser.implicitly_wait(1.5)

        i += 1

    #Parent Account needs updating
    else:
        print ("Different School as child")
        # check for children schools
        childCount = 0

        #Find a Parent Email
        while True:
            try:
                # email field on parent profile page
                parentEmail = browser.find_element(By.XPATH,'//*[@id="main-inner"]/table/tbody/tr[2]/td/span/a').text
                print('parent email: '+parentEmail)
                parentEmailFound = True
                parentEmail_Global = parentEmail
                break
            except:
                parentEmail = findParentEmail()
                if parentEmail != '~':
                    print('parent email: '+parentEmail)
                    parentEmailFound = True
                    parentEmail_Global = parentEmail
                    break
                else:
                    parentEmailFound = False
                    break
            
        if parentEmailFound == False:
                print("------No email was found-------")
                i += 1
                continue

        try:  
            #Run a function for email parent stuff
            # Grab Parent Email or username
            # Then check for multiple children
            # check for multiple kids
            # Check children count
            childCount = getChildCount()
            # change to Manage Users page
            browser.get('https://osseo.schoology.com/users/manage/edit/moreinfo?role=266607&search=' + parentEmail)
            parentSchoologyProfileURL = 'https://osseo.schoology.com/users/manage/edit/moreinfo?role=266607&search=' + parentEmail
        except:
            if parentEmailFound == False:

                #Try and find again
                parentEmail = browser.find_element(By.CLASS,'sExtlink-processed mailto').text
                #Run a function for non-email parent stuff then return
                print("------No email was found-------")
                i += 1
                continue
                #browser.quit()
                #parentFile.close()

        #if one child
        if childCount == 1:
            changePrimarySchool(student_school,1)  # Changes the primary school location - ONLY DO THIS FOR SINGLE PARENT, STUDENTS?

        elif childCount == 2:
            print('two child')
            changePrimarySchool(student_school,2)

            # # Schoology not accepting Osseo ALC Sr High need to remove high
            # if student_school == 'Osseo ALC Sr High':
            #     student_school = 'Osseo ALC Sr'

            # addSchool_Button = browser.find_element(By.XPATH,'//*[@id="edit-users-'+userID+'-building-nid-wrapper"]/div/div/div/a')
            # try:
            #     addSchool_Button.click()  # works

            #     try:
            #         selectSchool = browser.find_element(By.XPATH,'//*[@id="select2-chosen-12"]') #was 8
            #         selectSchool.click()
            #         addSchool_SearchBox = browser.find_element(By.XPATH,'//*[@id="s2id_autogen12_search"]') #was 8
            #         addSchool_SearchBox.send_keys(student_school)
            #         addSchool_SearchBox.send_keys(Keys.RETURN)
            #     except:
            #         selectSchool = browser.find_element(By.XPATH,'//*[@id="select2-chosen-8"]')

            #         selectSchool.click()
            #         addSchool_SearchBox = browser.find_element(By.XPATH,'//*[@id="s2id_autogen8_search"]')
            #         addSchool_SearchBox.send_keys(student_school)
            #         addSchool_SearchBox.send_keys(Keys.RETURN)

        # Try this if there are three childen
        elif childCount==3:
            changePrimarySchool(student_school,3)
            
        # Save Changes to Parent Account Profile
        saveChanges()

        # Mark changes in log file
        parentLogFile(childCount)

        #Process the second parent
        if(secondParentID!=''):
            browser.get(secondParentID); # Opens the tab of the second parents profile
            # Need to read in the school
            school = readParentSchool()
            print("Second Parent School - ",school)

            secondParentID =''
            i += 1
            continue
            

        browser.implicitly_wait(1)
        secondParentID =''
        i += 1

# Close browser and log file
print('\n--------------------Quiting END OF LIST--------------------------')
browser.quit()
parentFile.close()