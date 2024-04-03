import re
import subprocess
import getpass

#function to validate ip
def checkip(input):
    ippattern = r'^((([01]?[0-9]{1,2}|25[0-5]|[2][0-4][0-9])\.){3}([01]?[0-9]{1,2}|25[0-5]|[2][0-4][0-9]))((\/[0-2]?[0-9]|\/3[0-2])?)?$'
    match = re.match(ippattern,input)
    if match:
        print(ipinput + " is valid.")
        return True
    else:
        print(ipinput + " is invalid. ")
        return False


        
print("Hi! Welcome to Domain Mapper v1!")
ipinput = input("Please enter the target network range or ip adress: ")  
print("You have entered "  + ipinput)
print("Checking if you have entered a valid range or ip address .......")
if not checkip(ipinput):
    ipinput = False

while True: 
    if ipinput==False:
        ipinput = input("Your ip input is invalid please key in another entry: ")
    else:
        domaininput = input("If you have a domain name , please enter it. If not just press ENTER: ")
    break

usernameinput =  input("Please enter a username if you possess one. If not please hit ENTER.: ")
passwordinput =  input("Please enter a password if you have one. If not please hit ENTER.: ")

passwordlist = 'rockyou.txt'
pinput = input("Do you have a preferred pass wordlist, if you do key the full path here. If not we will use rockyou.txt as your passwordlist : ")
if pinput is None :
    passwordlist=pinput

print("Information Added:")
print("IP: " + ipinput)
print("Domain: " + domaininput)
print("Username: " + usernameinput)
print("Password: " + passwordinput)
print("Password List: "+ passwordlist)

#==============================SCANNING=====================================================
print("We shall now begin the scanning phase. Please select a desired operational level by entering the corresponding numbers: ")

scanningmode = input("[1-Basic], [2-Intermediate], [3-Advance]: ")
scanoutput=""
def run_scan_basic(ip):
    command =["nmap","-Pn", ip]
    result = subprocess.run(command,capture_output=True,text=True,check=True)
    scanresult=(result.stdout)
    return scanresult
   
def run_scan_intermediate(ip):
    command=["nmap","-Pn", ip, "-p-"]
    result=subprocess.run(command,capture_output=True,check=True,text=True)
    scanresult=(result.stdout)
    return scanresult    
 
def run_scan_advanced(ip):
    command=["nmap","-Pn", ip ,"-p-"]
    #command2=["sudo","nmap","-Pn", "-sU", ip]
    command2=["nmap","-Pn", ip ,"-p-"]
    result=subprocess.run(command,capture_output=True,check=True,text=True)
    scanresult=(result.stdout)
    result2=subprocess.run(command2,capture_output=True,check=True,text=True)
    scanresult2=(result2.stdout)
    return scanresult + scanresult2

def extractopenport(scanoutput):
    openport=[]
    for line in scanoutput.split('\n'):
        segments=line.split()
        if len(segments) == 3 and segments[1]=="open":
            portnumber=segments[0].split('/')[0]
            openport.append(portnumber)
    return openport


if scanningmode =="1":
    scanoutput=run_scan_basic(ipinput)
elif scanningmode =="2":
    scanoutput=run_scan_intermediate(ipinput)
else:
    scanoutput=run_scan_advanced(ipinput)

print(scanoutput)


openports=', '.join(list(set(extractopenport(scanoutput))))
print(openports)
#===============Enumeration====================
def run_enumeration_basic(ipinput, openports):
    command=["sudo", "nmap", "-sV", "-Pn", ipinput , "-p", openports]
    result=subprocess.run(command,capture_output=True,check=True, text=True )
    ebasicresult= (result.stdout)
    return ebasicresult

print("Welcome to the Enumeration Phase. Please select a desired operational level by entering the corresponding numbers: ")
enumerationlevel = input("[1-Basic], [2-Intermediate], [3-Advance]: ")

if enumerationlevel =="1":
    eoutput=run_enumeration_basic(ipinput, openports)
    print(eoutput)

