from PyQt6.QtWidgets import *
from votingballot import *
import csv

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        '''
        Sets up UI and opens up CSV file to store voting data
        '''
        super().__init__()
        self.setupUi(self)
        self.submitButton.clicked.connect(lambda: self.submit()) #ensures that the ID is submitted
        self.idInput.setEnabled(True) #allows voter to input ID
        self.janeButton.setEnabled(False) #prevents the voter from voting without their ID being checked
        self.johnButton.setEnabled(False) #prevents the voter from voting without their ID being checked
        #creates CSV file for the first time
        with open("voting.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Voter ID", "Candidate"])

    def submit(self) -> None:
        '''
        allows for the submission of voter ID if it meets the criteria (numerical and five digits)
        '''
        voterID = self.idInput.text().strip()
        #checks if voter ID is valid or not
        if not voterID.isdigit() or len(voterID) != 5:
            self.message.setText("Invalid. ID must be a 5 digit number.")
            self.message.setStyleSheet("color: red;")
            return
        #checks if the voter ID is already in the CSV file
        if self.exists(voterID):
            self.message.setText("Already Voted")
            self.message.setStyleSheet("color: red;")
            return
        #if voter is voting for the first time, voting is allowed
        self.message.setText("Please cast your vote")
        self.message.setStyleSheet("color: green;")
        self.janeButton.setEnabled(True) #allows voter to select Jane or John
        self.johnButton.setEnabled(True) #allows voter to select John or Jane
        self.idInput.setEnabled(False) #prevents voter from changing their voter ID
        self.submitButton.setText("SUBMIT VOTE")
        self.submitButton.clicked.disconnect() #disconnects button from checking to ID to voting
        self.submitButton.clicked.connect(lambda: self.castVote(voterID))
    
    def castVote(self, voterID) -> None:
        '''
        assigns the voter ID with their vote and records the vote in the CSV file
        '''
        if self.janeButton.isChecked():
            candidate = "Jane"
        elif self.johnButton.isChecked():
            candidate = "John"
        else:
            candidate = ""

        self.record(voterID, candidate) #records the vote in the CSV file
        self.message.setText("Thank you for voting.")
        self.message.setStyleSheet("color: green;")
        self.submitButton.setText("SUBMIT ID")
        self.reset() #resets the voting ballot
    
    def reset(self) -> None:
        '''
        Resets the form so that the next voter can vote
        '''
        self.idInput.clear() 
        self.idInput.setEnabled(True)
        self.janeButton.setEnabled(False)
        self.johnButton.setEnabled(False)
        self.submitButton.setText("SUBMIT ID")
        self.submitButton.clicked.disconnect()
        self.submitButton.clicked.connect(lambda: self.submit())
        

    def exists(self, voterID) -> None:
        '''
        checks to see if the voter has already voted
        '''
        with open("voting.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if voterID == row[0]:
                    return True
        return False
    
    def record(self, voterID, candidate) -> None:
        '''
        records the voter's ID and candidate in the CSV file
        '''
        with open("voting.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([voterID, candidate])
