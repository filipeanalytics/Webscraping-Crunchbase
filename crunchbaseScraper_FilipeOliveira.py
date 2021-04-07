import time  # to use sleep function to allow website to load
from selenium import webdriver  # to connect to a browser and access an URL
from bs4 import BeautifulSoup  # to remove HTML tags from HTML content
from selenium.webdriver.common.keys import Keys  # so I can press the Enter Key in the search fields
import pandas as pd # make use of Dataframes and read from and write to csv/excel files.

# This script extracts multiple businesses information from crunchdatabase for a given list of companies' URLs.

# High level ALGORITHM
# 0 - Read list of URLs from csv file
# 1 - FOR loop with the size of number of URLS.
# 2 - For each URL, read all the required fields for that business
# 3 - Store business details into a Business object and into a Dataframe
# 4 - Save Dataframe with all business details into a csv file

class Business:

    # Constructor to initialize Business object with given parameters
    def __init__(self, name,website,logo,pitch_line,hq_location,size,industries,founded_date,legal_name,email,phone,
                 description,facebook,linkedin,twitter,total_funding,transaction_name,last_announced_date,cb_url
                ):
        self.name = name
        self.website = website
        self.logo = logo
        self.pitch_line = pitch_line
        self.hq_location = hq_location
        self.size = size
        self.industries = industries
        self.founded_date = founded_date
        self.legal_name = legal_name
        self.email = email
        self.phone = phone
        self.description = description
        self.facebook = facebook
        self.linkedin = linkedin
        self.twitter = twitter
        self.total_funding = total_funding
        self.transaction_name = transaction_name
        self.last_announced_date = last_announced_date
        self.cb_url = cb_url

# method created to convert HTML to String format
def HTMLtoText(HTMLelement):
    htmlContent = HTMLelement.get_attribute('innerHTML')
    # Beautiful soup removes HTML tags from content, if it exists.
    rawString = BeautifulSoup(htmlContent, features="lxml")
    textContent = rawString.get_text().strip()  # Leading and trailing whitespaces are removed
    return textContent

#  Connect to Browser
DRIVER_PATH = "C:/Users/filip/Documents/PythonFiles/chromedriver"
browser = webdriver.Chrome(DRIVER_PATH)

businessList = [] # will store all business collected into a list of objects

# Create dataframe that willstore all business info to be saved into a csv file
df = pd.DataFrame(columns=['name',	'website',	'logo',	'pitch_line',	'hq_location',	'size',	'industries',
                           'founded_date',	'legal_name',	'email',	'phone',	'descrption',	'facebook',
                           'linkedin',	'twitter',	'total_funding',	'transaction_name',	'last_announced_date',
                           'cb_url'
                          ])

# Reads URL list from csv file
PATH = "C:/Users/filip/Documents/PythonFiles/"
CSV_FILE = "Cruncbase URL Inputs.xlsx"
dfURLs = pd.read_excel(PATH+CSV_FILE)
numberOfBusiness = len(dfURLs)

# 1 - FOR loop with the size of number of URLS.
for i in range(numberOfBusiness):

    #  Access website
    currentURL = dfURLs['CB URL'][i]
    browser.get(currentURL)

    # saving URL into cb_url field
    cb_url = currentURL

    # Give the browser time to load all content.
    time.sleep(3)

# 2 - For each URL, read all the required fields for that company.

    # 1st field: Logo URL
    try:
        logoSelector = browser.find_element_by_css_selector(".organization img")
        logo = logoSelector.get_attribute("src")
    except:
        logo = ""

    # 2nd field: Name
    try:
        nameSelector = browser.find_element_by_css_selector(".profile-name")
        name = HTMLtoText(nameSelector)
    except:
        name = ""

    # 3rd field: Pitch line
    try:
        pitchSelector = browser.find_element_by_css_selector(".description")
        pitch_line = HTMLtoText(pitchSelector)
    except:
        pitch_line = ""

    # In this section, the whole About section is stored in one list, which is treated dynamically per item.
    # It checks if the item is the one we need by checking the tooltip message associated with each item.
    # 4-6th fields: Location, Size and Website
    try:
        # ul_AboutItems returns a list of all 6 items in the About section (location, size...website...)
        ul_AboutItems = browser.find_elements_by_css_selector(
            ".icon_and_value .ng-star-inserted .ng-star-inserted .ng-star-inserted .component--field-formatter")
        # ul_TooltipItems returns a list of the 6 tooltip messages associated with each item in the About section.
        ul_TooltipItems = browser.find_elements_by_css_selector(
            ".icon_and_value .ng-star-inserted .ng-star-inserted .mat-tooltip-trigger ")
        # navigates through all items in the list of About items
        for i in range(len(ul_TooltipItems)):
            attr = ul_TooltipItems[i].get_attribute("aria-describedby")  # ex: cdk-describedby-message-0
            tooltipMessageSelector = browser.find_element_by_id(attr)  # get specific tooltip message head
            tooltip = HTMLtoText(tooltipMessageSelector)  # get specific tooltip message. ex: 'Headquarters Location'
            if tooltip == 'Headquarters Location':
                hqLocSelector = ul_AboutItems[i]
                hq_location = HTMLtoText(hqLocSelector)
            elif tooltip == 'Number of Employees':
                sizeSelector = ul_AboutItems[i]
                size = HTMLtoText(sizeSelector)
            elif tooltip == 'Website':
                websiteSelector = ul_AboutItems[i]
                website = HTMLtoText(websiteSelector)
    except:
        hq_location = ""
        size = ""
        website = ""

    # 7th field: Industries
    try:
        industriesSelector = browser.find_elements_by_css_selector(".cb-overflow-ellipsis")
        industriesList = []  # declared a list that will store all industries
        for i in range(len(industriesSelector)):
            industriesText = HTMLtoText(industriesSelector[i])
            industriesList.append(industriesText)  # appends each new industry to end of list
        industries = ", ".join(industriesList)  # joins the list with commas separating each value
    except:
        industries = ""

    # 8th field: Founded date
    try:
        foundedDateSelector = browser.find_element_by_css_selector(".field-type-date_precision")
        founded_date = HTMLtoText(foundedDateSelector)
    except:
        founded_date = ""

    # 9th field: Legal name
    try:
        legalNameSelector = browser.find_element_by_css_selector\
            (".text_and_value .ng-star-inserted~ .ng-star-inserted+ "
            ".ng-star-inserted .ng-star-inserted .ng-star-inserted span.ng-star-inserted")
        legal_name = HTMLtoText(legalNameSelector) # has title "Legal Name " before the actual value
    except:
        legal_name = ""

    # 10th field: Phone number
    try:
        email_phoneNumber_Selector = browser.find_element_by_css_selector(".ng-star-inserted~ .ng-star-inserted+ "
                                                                          ".ng-star-inserted .text_and_value")
        email_phoneNumberText = HTMLtoText(email_phoneNumber_Selector)
        # Divide email_phoneNumberText in 3 strings by "Phone Number"
        email_phoneNumber = email_phoneNumberText.partition("Phone Number")
        phone = email_phoneNumber[2].strip()
    except:
        phone = ""

    # 11th field: Email
    try:
        if phone == "":  # means there is no phone number
            email = email_phoneNumberText.partition("Contact Email")[2].strip()
        else:
            email = email_phoneNumber[0].partition("Contact Email")[2].strip()
    except:
        email = ""

    # 12th field: Description
    # The excel file given as a sample has a typo (descrption), so I'm using the proper spelling descrIption.
    try:  # clicking on Read More button
        readMoreButton = browser.find_element_by_css_selector(".mat-accent")
        readMoreButton.send_keys(Keys.RETURN)
        time.sleep(1)
    except:
        description = ""
    try: # getting description content
        descriptionSelector = browser.find_element_by_css_selector(".main-content description-card")
        description = HTMLtoText(descriptionSelector)

        if description.rpartition("Read Less")[0] != "":  # if there is a "Read Less" in the end, remove it
            description = description.rpartition("Read Less")[0]
    except:
        description = ""

    # 13-15th fields: Social Media (Facebook, Linkedin, Twitter)
    try:
        socialMediaSelector = browser.find_elements_by_css_selector(".link-primary.ng-star-inserted")
        # initializing fields with empty strings
        facebook = ""
        linkedin = ""
        twitter = ""
        for i in range(len(socialMediaSelector)):
            socialMedia = socialMediaSelector[i].get_attribute("href")
            if socialMedia.find("facebook") != -1:  # if find() returns -1, means haven't found "facebook"
                facebook = socialMedia
            elif socialMedia.find("linkedin") != -1:
                linkedin = socialMedia
            elif socialMedia.find("twitter") != -1:
                twitter = socialMedia
    except:
        facebook = ""
        linkedin = ""
        twitter = ""

    # 16th field: Total funding
    try:
        totalFundingSelector = browser.find_element_by_css_selector(".info .field-type-money")
        total_funding = HTMLtoText(totalFundingSelector)
    except:
        total_funding = ""


    # 17,18th field: Transaction name & Last Announced Date
    try:  # open Financials tab
        financialsTab = browser.find_element_by_css_selector(".mat-tab-label-active+ .ng-star-inserted")
        financialsTab.send_keys(Keys.RETURN)
        time.sleep(2)
        # collect info
        mainContentSelector = browser.find_element_by_css_selector("#funding_rounds+ .ng-star-inserted .mat-elevation-z3")
        mainContentText = HTMLtoText(mainContentSelector)
        # if Announced Data and Transaction Name columns exist in the Financials Summary, collect data
        if mainContentText.find("Announced Date") != -1 and mainContentText.find("Transaction Name") != -1:
            # identifies how many rows of transactions need to be read
            numberOfTransactions = mainContentText.partition("Total")[0] # Funding RoundsNumber of Funding Rounds 2Total...
            numberOfTransactions = numberOfTransactions.rpartition("Number of Funding Rounds")[2]
            numberOfTransactions = int(numberOfTransactions)

            # part of the string where transactions rows start
            transaction_details = mainContentText.rpartition("Lead Investors")[2]

            # LAST_ANNOUNCED_DATE
            # only reads first record, which is the most recent announced date
            dateEndIndex = transaction_details.find(",") + 6  # distance from the comma to end of date
            last_announced_date = transaction_details[0:dateEndIndex].strip()
            last_announced_date = pd.Timestamp(last_announced_date) # convert to Timestamp

            # TRANSACTION_NAME
            # splits the results based on the comma from the date (Apr 1, 2018)
            # if numberOfTransactions > 1:
            transaction_detailsList = transaction_details.split(",") # Apr 1, 2018 Venture Round - 4M Carbon Fiber —$1.7M —
            transaction_nameList = []  # declared a list that will store all transaction names
            for i in range(numberOfTransactions):
                transaction_details = transaction_detailsList[i + 1]
                startIndex = 6 # starts after the year and space
                endIndex = transaction_details.find("-")-1 # separates transaction name from company name
                transaction_name = transaction_details[startIndex:endIndex]
                transaction_nameList.append(transaction_name)  # appends each new transaction_name to end of list
            transaction_name = ", ".join(transaction_nameList)  # joins the list with commas separating each value
        else:
            transaction_name = ""
            last_announced_date = ""
    except:
        transaction_name = ""
        last_announced_date = ""

    # STORING BUSINESS DETAILS INTO AN OBJECT'S LIST
    # Creating BUSINESS object
    businessObj = Business(name,website,logo,pitch_line,hq_location,size,industries,founded_date,legal_name,email,phone,
                 description,facebook,linkedin,twitter,total_funding,transaction_name,last_announced_date,cb_url
                )
    # appending business by business into an Objects List.
    businessList.append(businessObj)

    # STORING BUSINESS DETAILS INTO A DATAFRAME
    # adding current business info into a dictionary
    businessDict = {'name': name, 	'website': website, 	'logo': logo, 	'pitch_line': pitch_line,
                 'hq_location': hq_location, 	'size': size, 	'industries': industries, 	'founded_date': founded_date,
                 'legal_name': legal_name, 	'email': email, 	'phone': phone, 	'descrption': description,
                 'facebook': facebook, 	'linkedin': linkedin, 	'twitter': twitter, 	'total_funding': total_funding,
                 'transaction_name': transaction_name, 	'last_announced_date': last_announced_date, 	'cb_url': cb_url
                }
    # appending property by property into a DataFrame
    df = df.append(businessDict, ignore_index=True)

# Save DataFrame into a CSV File
PATH = "C:/Users/filip/Documents/PythonFiles/"
CSV_FILE = "BusinessInfo5.csv"
df.to_csv(PATH+CSV_FILE, sep=',')
