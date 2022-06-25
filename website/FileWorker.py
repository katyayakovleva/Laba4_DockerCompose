import os

from flask import flash


def readFile(file):
    if isFileExist(file):
        f = open(os.path.join("files", file), "r")
        flash("Вміст файлу: " + file, category="result")
        flash(f.read(), category="result")
        f.close()


def getFileProperties(file):
    if isFileExist(file):
        flash("Ім\'я файлу: " + file, category="result")
        size = os.path.getsize(os.path.join("files", file))
        flash("Розмфр файлу: " + str(size) + ' bytes', category="result")
        path = os.path.abspath(os.path.join("files", file))
        flash('Повний шлях до файлу: ' + path, category="result")


def checkIfWordExistInFile(file, word):
    if isFileExist(file):
        f = open(os.path.join("files", file), "r")
        if word in f.read():
            flash("Cлово " + word + "є у файлі " + file, category="result")
        else:
            flash("Cлова " + word + " у файлі нема " + file, category="result")
        f.close()


def renameFile(file, name):
    if isFileExist(file):
        old_name = os.path.join("files", file)
        new_name = os.path.join("files", name)
        os.rename(old_name, new_name)
        flash("Ім\'я файлу змінено з" + old_name + " на " + new_name, category="result")


def writeToFile(file, text):
    if isFileExist(file):
        f = open(os.path.join("files", file), "a+")
        f.write('\n' + text)
        flash("Переглянемо змінений файл " + file + ": ", category='result')

        f = open(os.path.join("files", file), "r")
        flash(f.read(), category='result')
        f.close()


def createFile(file):
    if isFileExist(file):
        flash("Файл " + file + " вже існує", category='result')
    else:
        f = open(os.path.join("files", file), 'x')
        f.close()
        flash("Файл " + file + " створено", category='result')


def deleteFile(file):
    if isFileExist(file):
        os.remove(os.path.join("files", file))
        flash("Файл " + file + " видалено", category='result')





def combineTwoFiles(file1, file2):
    # file1 = files[0]
    # file2 = files[1]
    # files = file1 + file2
    if isFileExist(file1) and isFileExist(file2):
        new_file = os.path.splitext(os.path.basename(file1))[0] + '_' + file2
        f = open(os.path.join("files", new_file), 'w')
        f1 = open(os.path.join("files", file1), 'r')
        f2 = open(os.path.join("files", file2), 'r')
        f.write(f1.read())
        f.write(f2.read())

        flash("Створено файл" + new_file, category='result')



def isFileExist(file):
    if os.path.exists(os.path.join("files", file)):
        return True
    else:
        # flash("The file does not exist", category='error')
        return False
