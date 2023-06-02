from email.mime import image
import os
from PyQt5.QtWidgets import QApplication,QLabel, QWidget, QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import shutil
import string

class DLSSUpdater(QWidget):
    def __init__(self):
        super().__init__()

        Image_label = QLabel(self)
        pixmap = QPixmap('bg.png')
        Image_label.setPixmap(pixmap)
        Image_label.resize(650,370)
        Image_label.setScaledContents(True)

        #info_button
        self.info_button = QPushButton("  Help  ", self)
        self.info_button.setFont(QFont('Bahnschrift Light', 10))
        self.info_button.move(590, 10)
        self.info_button.clicked.connect(self.open_info_window)
        self.info_button.setStyleSheet('QPushButton {background-color: #FFF28B; border:  none}')

        #list
        self.file_list = QListWidget(self)
        self.file_list.move(20, 90)
        self.file_list.resize(420, 220)

        #search_button
        self.search_button = QPushButton(' Search for DLSS files ', self)
        self.search_button.move(20, 30)
        self.search_button.setFont(QFont('Bahnschrift Light', 14))
        self.search_button.clicked.connect(self.search_files)
        self.search_button.setStyleSheet('QPushButton {background-color: #46B228; border:  none}')

        #update_button
        self.update_button = QPushButton(' UPDATE ', self)
        self.update_button.move(270, 325)
        self.update_button.setFont(QFont('Bahnschrift Light', 19))
        self.update_button.clicked.connect(self.update_files)
        self.update_button.setStyleSheet('QPushButton {background-color: #00AD4E; border:  none}')

        self.setGeometry(300, 300, 650, 370)
        self.setFixedSize(650, 370)
        self.setWindowTitle('DLSSer v1.0.22')
        self.show()

    def open_info_window(self):
        # Create a new dialog window
        dialog = QDialog(self)
        dialog.setWindowTitle("DLSS'er Information & Use")
        dialog.setGeometry(100, 200, 1500, 600)
        
        # Add label with information
        self.label = QLabel("1. Download and extract DLSS file from TechPowerUp.com first.", dialog)
        self.label.setFont(QFont('Bahnschrift Light', 20)) 
        self.label.move(20, 0)

        self.lable1 = QLabel('2. Click the Search Button to auto-search your PC for a DLSS file. WAIT a few seconds for it to respond. ',dialog)
        self.lable1.setFont(QFont('Bahnschrift Light', 14)) 
        self.lable1.move(20, 60)

        self.lable2 = QLabel('3. Click a game path available to you for Update.',dialog)
        self.lable2.setFont(QFont('Bahnschrift Light', 14))
        self.lable2.move(20, 100)
        
        self.lable3 = QLabel('4. Click the Update button and choose a new nvngx_dlss.dll file. If successful a backup folder is created with old DLSS file.',dialog)
        self.lable3.setFont(QFont('Bahnschrift Light', 14))
        self.lable3.move(20, 140)

        self.lable4 = QLabel('5. To restore/change versions click Update and go to the DLSS Backup folder or choose other DLSS files.',dialog)
        self.lable4.setFont(QFont('Bahnschrift Light', 14))
        self.lable4.move(20, 180)

        self.lable5 = QLabel('(Each time you update, the unused DLSS file goes to the Backup folder located where you originally chose the new DLSS file.)',dialog)
        self.lable5.setFont(QFont('Bahnschrift Light', 14))
        self.lable5.move(20, 210)

        self.lable6 = QLabel('*NOTE - for DLSS 2 ONLY. NOT for DLSSG (Frame Generation). ',dialog)
        self.lable6.setFont(QFont('Bahnschrift Light', 14))
        self.lable6.move(20, 285)
        
        self.lable7 = QLabel('Version 1.0.22 - DEAD FISH FLIP-FLOP - Created by Marco Trollbender Wagner and Ziv_Bns',dialog)
        self.lable7.setFont(QFont('Bahnschrift Light', 14))
        self.lable7.move(20, 335)

        dialog.exec_()

        #search button click
    def search_files(self):
        self.refresh_list()           

        #get the fill list
    def get_file_list(self):
        file_list = []
        drives = ['%s:\\' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        for drive in drives:
            for root, dirs, files in os.walk(drive):
                for file in files:
                    if file == 'nvngx_dlss.dll':
                        file_list.append(os.path.join(root, file))
        return file_list

    #Update button click
    def update_files(self):
        selected_file, _ = QFileDialog.getOpenFileName(self, 'Select a nvngx_dlss.dll File for Replacement', '', 'DLL files (*.dll)')
        if selected_file:
            backup_folder = os.path.join(os.path.dirname(selected_file), 'DLSS Backup')
            os.makedirs(backup_folder, exist_ok=True)

            for file_path in self.file_list.selectedItems():
                backup_path = os.path.join(backup_folder, os.path.basename(file_path.text()))
                try:
                    if os.path.samefile(os.path.dirname(file_path.text()), os.path.dirname(selected_file)):
                        shutil.move(file_path.text(), backup_path)
                        shutil.move(selected_file, file_path.text())
                    else:
                        shutil.copy2(file_path.text(), backup_path)
                        shutil.copy2(selected_file, os.path.join(os.path.dirname(file_path.text()), os.path.basename(selected_file)))
                        os.remove(selected_file)
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'Failed to Update {file_path.text()}: {e}')

            QMessageBox.information(self, 'Success', 'DLSS File Replaced Successfully. Backup Created.')

    #refresh_list in the white box
    def refresh_list(self):
        self.file_list.clear()
        for file_path in self.get_file_list():
            item = QListWidgetItem(file_path)
            self.file_list.addItem(item)



if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Breeze')
    nvngx_updater = DLSSUpdater()
    #nvngx_updater.refresh_list()
    app.exec_()
