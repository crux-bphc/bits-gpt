import os
import socket
import threading
import time
import shutil
import keyboard

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ChatGPTAutomation:

    def __init__(self, chrome_path, chrome_driver_path):
        """
        This constructor automates the following steps:
        1. Open a Chrome browser with remote debugging enabled at a specified URL.
        2. Prompt the user to complete the log-in/registration/human verification, if required.
        3. Connect a Selenium WebDriver to the browser instance after human verification is completed.

        :param chrome_path: file path to chrome.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        :param chrome_driver_path: file path to chrome.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        """

        self.chrome_path = chrome_path
        self.chrome_driver_path = chrome_driver_path

        url = r"https://chat.openai.com"
        free_port = self.find_available_port()
        self.launch_chrome_with_remote_debugging(free_port, url)
        self.wait_for_human_verification()
        self.driver = self.setup_webdriver(free_port)

    @staticmethod
    def find_available_port():
        """ This function finds and returns an available port number on the local machine by creating a temporary
            socket, binding it to an ephemeral port, and then closing the socket. """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def launch_chrome_with_remote_debugging(self, port, url):
        """ Launches a new Chrome instance with remote debugging enabled on the specified port and navigates to the
            provided url """

        def open_chrome():
            chrome_cmd = f"{self.chrome_path} --remote-debugging-port={port} --user-data-dir=remote-profile {url}"
            os.system(chrome_cmd)

        chrome_thread = threading.Thread(target=open_chrome)
        chrome_thread.start()

    def setup_webdriver(self, port):
        """  Initializes a Selenium WebDriver instance, connected to an existing Chrome browser
             with remote debugging enabled on the specified port"""

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = self.chrome_driver_path
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def send_prompt_to_chatgpt(self, prompt):
        """ Sends a message to ChatGPT and waits for 20 seconds for the response """

        input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@id, "prompt-textarea")]')
        self.driver.execute_script(f"arguments[0].value = '{prompt}';", input_box)
        input_box.send_keys(Keys.RETURN)
        input_box.submit()
        keyboard.wait("alt")


    def return_last_response(self):
        """ :return: the text of the last chatgpt response """

        response_elements = self.driver.find_elements(by=By.XPATH, value='//div[@class="markdown prose w-full break-words dark:prose-invert dark"]')
        return response_elements[-1].text

    @staticmethod
    def wait_for_human_verification():
        print("You need to manually complete the log-in or the human verification if required.")

        while True:
            user_input = input(
                "Enter 'y' if you have completed the log-in or the human verification, or 'n' to check again: ").lower()

            if user_input == 'y':
                print("Continuing with the automation process...")
                break
            elif user_input == 'n':
                print("Waiting for you to complete the human verification...")
                time.sleep(5)  # You can adjust the waiting time as needed
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def quit(self):
        """ Closes the browser and terminates the WebDriver session."""
        print("Closing the browser...")
        self.driver.close()
        self.driver.quit()


chrome_driver_path = r"D:\Documents\GitHub\Studily\chromedriver.exe" #just put the path to where you installed chromedriver
chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"' #this should be same for all systems but just double check it if errors pop up

chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)

table_summaries = []
text_summaries = []


in_path = "data\\Handouts\\rawdata"
out_path = "data\\Handouts\\Summary"
processed_path = "data\\Handouts\\tt_processed" #raw files after summarising are sent here so that program can continue from where it left off
raw_data_filelist = os.listdir(in_path)
errors=[]

#How to use:
#1. Setup the paths
#2. Run the script, it will open a chrome window and ask you to login to chatgpt
#3. After logging in type "y" in the terminal, this will attach selenium to the browser and start the automation
#4. Due to chatgpt being slow and buggy at times, i have made it such that the program waits for you to press alt to save the response
#   after the summary is generated. Ill automate this portion later.


def summarise_text(in_path, out_path, processed_path, input_prompt = None):
    raw_data_filelist = os.listdir(in_path)
    for raw_file in raw_data_filelist:
        print("Summarising", raw_file)
        basename = os.path.splitext(raw_file)[0]
        with open(os.path.join(in_path, raw_file), "r", encoding="utf-8") as handle:
            raw_data = handle.read()
            raw_data = raw_data.replace("\n","(newline)") #this and the next line is to not fuck up the javascript syntax
            raw_data = raw_data.replace("'","\\")
            if "rawtext" in raw_file:
                prompt =f"You are an assistant tasked with summarizing text. It also contains (newline) which signifies a new line. If any detail is NOT present in the chunk DO NOT explicitly mention that in the summary \ Give a concise summary of the text. The chunk is for the course - {basename}, mention the course in the summary. Text chunk: {raw_data}"
                
            if "rawtable" in raw_file:
                #prompt = f"You are an assistant tasked with creating a summary based on this CSV data. generate a summary of the this data, clearly stating any numbers related to lecture number, textbook chapter, evaluation components, duration. Also give a breif description in the beginning in about 30 words before continuing to describe the entire table.\ (newline) means the presence of a new line\ The chunk is for the course - {basename}, mention the course in the summary. Table chunk: {raw_data}"
                prompt = input_prompt + f"|| use ONLY the following CSV data : {raw_data} ||"
            try: 
                chatgpt.send_prompt_to_chatgpt(prompt)
            except:
                errors.append(raw_file)

        cooked_file = raw_file.replace("rawtable", "cookedtable")
        cooked_file = cooked_file.replace("rawtext", "cookedtext")
        cooked_file = cooked_file.replace("csv", "txt") #change the extension to txt

        with open(os.path.join(out_path, cooked_file), "w", encoding="utf-8") as handle:
            try:
                handle.write(chatgpt.return_last_response().replace("ChatGPT", ""))
            except:
                errors.append(cooked_file)
        
        shutil.move(os.path.join(os.getcwd(),in_path, raw_file), os.path.join(os.getcwd(),processed_path))


tt_prompt = """Generate a summary of this CSV data. list the summary of each course in the form of a paragraph along with its details, making sure the course name is present in the paragraph. DO NOT mention the class timings. Take note of the following abbreviations: COM CODE - Computer code for the course; COURSE NO - Course number; COURSE TITLE - Course title; CREDIT L - Lecture hours per week; CREDIT P - pratical hours per week; CREDIT U - total units of the course; SEC- Section Number; INSTRUCTOR-IN-CHARGE/instructor - Name in CAPITAL LETTERS indicate INSTRUCTOR-IN-CHARGE small letters are other instructors; ROOM - First letter indicates block. Eg: F indicates that the room is in F block First digit of number indicates floor, 1 for ground floor and 2 for first floor; DAYS - M - Monday, T - Tuesday, W - Wednesday, TH - Thursday, F - Friday, S - Saturday; HOURS - 1 stands for 1st hour 2 stands for 2nd hour and so on; COMPRE EXAM (session) - FN: 9.30 AM to 12.30 PM || AN: 2.00 PM to 5.00 PM ;"""
books_prompt = "Generate a summary of this CSV data. list the course name along with its corresponding books"

summarise_text(in_path, out_path, processed_path, tt_prompt)
print("Completed with errors: ", errors)
chatgpt.quit()