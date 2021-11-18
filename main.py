# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

sys.path.append('/home/yuxin/.local/lib/python2.7/site-packages')

import os
import exrex
import subprocess
from sympy import *


def copyFile():
    subprocess.run(
        "cp ~/IdeaProjects/VirtualMachineForIR/out/artifacts/VirtualMachineForIR_jar/VirtualMachineForIR.jar ~/PycharmProjects/ATM4Compiler/vm.jar",
        shell=True)
    subprocess.run("cp ~/CLionProjects/Compiler/cmake-build-debug/Compiler ~/PycharmProjects/ATM4Compiler/Compiler",
                   shell=True)


def runCompiler():
    p = subprocess.run(
        "./Compiler",
        stdout=subprocess.PIPE,
        text=True,
        shell=True
    )


def runVM(input_file):
    p = subprocess.run(
        "cat " + input_file + " | java -jar vm.jar",
        stdout=subprocess.PIPE,
        text=True,
        shell=True
    )

def runMars(input_file):
    p = subprocess.run(
        "cat " + input_file + " | java -jar Mars-Compile-2021.jar mips.txt > MarsRes.txt",
        stdout=subprocess.PIPE,
        text=True,
        shell=True
    )

def compare(standard_file):
    res = open("console.txt", "r")
    standard = open(standard_file, "r")
    mars = open("MarsRes.txt", "r")
    mars.readline()
    mars.readline()
    IRwrong = False
    MIPSwrong = False
    while True:
        resLine = res.readline().split("\n", 1)[0]
        if resLine == '':
            break
        standardLine = standard.readline().split("\n", 1)[0]
        if standardLine == '':
            break
        marsLine = mars.readline().split("\n", 1)[0]
        if marsLine == '':
            break
        if resLine != standardLine:
            IRwrong = True
            break
        if marsLine != standardLine:
            MIPSwrong = True
            break
    res.close()
    standard.close()
    if not IRwrong and not MIPSwrong:
        print("ALL\t-- AC")
        return
    if IRwrong:
        p = subprocess.run(
            "diff " + standard_file + " ./console.txt",
            shell=True
        )
        print("IR\t-- WA ")
    else:
        print("IR\t-- AC")
    if MIPSwrong:
        p = subprocess.run(
            "diff " + standard_file + " ./MarsRes.txt",
            shell=True
        )
        print("MIPS\t-- WA ")
    else:
        print("MIPS\t-- AC")
def moveTestCode2buf(file):
    p = subprocess.run(
        "cat " + file + "> ./testfile.txt",
        shell=True
    )

def Communicate(stdinLine, order):
    # communicate to .jar file
    p = subprocess.run(
        order,
        # input=stdinLine,
        # stdout=subprocess.PIPE,
        # text=True,
        shell=True
    )
    # buffer = p.stdout
    # answer = buffer.split("\n", 1)[0]

    # return answer

directory = "A"
fileNum = 1

Communicate("", "echo hello")
copyFile()
for dir in range(3):
    files = 0
    if dir == 0:
        directory = "A"
        files = 26
        print("Dir A")
    elif dir == 1:
        directory = "B"
        files = 27
        print("Dir B")
    else:
        directory = "C"
        files = 29
        print("Dir C")
    for i in range(1, files+1):
        print(" File " + str(i))
        fileNum = i
        moveTestCode2buf("./IRTest/testfiles/" + directory + "/testfile" + str(fileNum) + ".txt")
        runCompiler()
        runVM("./IRTest/testfiles/" + directory + "/input" + str(fileNum) + ".txt")
        runMars("./IRTest/testfiles/" + directory + "/input" + str(fileNum) + ".txt")
        compare("./IRTest/testfiles/" + directory + "/output" + str(fileNum) + ".txt")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
