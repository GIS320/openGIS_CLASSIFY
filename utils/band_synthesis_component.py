import os
from osgeo import gdal
from utils.band_synthesis_dialog import Band_Synthesis_Dialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog,QFileDialog,QMessageBox

class Band_Synthesis_Component(QDialog,Band_Synthesis_Dialog):
    add_layer_signal = pyqtSignal(str)
    input_path_list=[]
    def __init__(self):
        super(Band_Synthesis_Component, self).__init__()
        self.setupUi(self)
        self.slot_connect()

    def slot_connect(self):
        self.input_file_browser.clicked.connect(self.action_input_file_browser_clicked)
        self.output_file_browser.clicked.connect(self.action_output_file_browser_clicked)
        self.add_img_button.clicked.connect(self.action_add_img_button_clicked)
        self.execute_button.clicked.connect(self.action_execute_button_clicked)

    def action_input_file_browser_clicked(self):
        self.input_path_list, type = QFileDialog.getOpenFileNames(self, "导入待合成影像", os.getcwd(), "*.tif;;*.jpg;;*.jpeg;;*.bmp;;*.png")
        file_path=""
        for item in self.input_path_list:
            file_path=file_path+item+";"
        self.input_file_path.setText(file_path)

    def action_add_img_button_clicked(self):
        raw_img_list=list(map(lambda x:os.path.splitext(os.path.basename(x))[0],self.input_path_list))
        print(raw_img_list)
        self.raw_img_list.addItems(raw_img_list)

    def action_output_file_browser_clicked(self):
        output_path,type=QFileDialog.getSaveFileName(self,"导出合成影像",os.getcwd(), "*.tif;;*.jpg;;*.bmp")
        self.output_file_path.setText(output_path)

    def action_execute_button_clicked(self):
        try:
            file_path=os.path.dirname(self.input_path_list[0])
            file_extension_name=os.path.splitext(self.input_path_list[0])[1]
            band_count=self.raw_img_list.count()
            current_band_order=list(map(lambda x:file_path+'/'+self.raw_img_list.item(x).text()+file_extension_name,range(band_count)))
            print(current_band_order)
        except Exception as e:
            print(e)
        raw_img=list(map(lambda x:gdal.Open(x),current_band_order))
        img_rows = raw_img[0].RasterYSize
        img_cols = raw_img[0].RasterXSize
        img_datasets=list(map(lambda x:x.GetRasterBand(1).ReadAsArray(0, 0, img_cols, img_rows),raw_img))
        driver = gdal.GetDriverByName("GTiff")
        output_img = driver.Create(self.output_file_path.text(), img_cols, img_rows, band_count, gdal.GDT_Byte)
        for i in range(1,band_count+1):
            output_img.GetRasterBand(i).WriteArray(img_datasets[i-1])
        del output_img
        if (QMessageBox.question(self,"消息框","合成完成，是否将结果添加到图层？",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)==QMessageBox.Yes):
            self.add_layer_signal.emit(self.output_file_path.text())