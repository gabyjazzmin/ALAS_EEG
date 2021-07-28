import argparse
import time
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, LogLevels
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, WindowFunctions, DetrendOperations
import csv

# Observaciones
# Alpha si funciona y se grafica
# Psd guarda en el csv solo una vez en la frecuencia de 125, guarda siempre 128 datos

ch1 = []
ch2 = []
ch3 = []
ch4 = []
ch5 = []
ch6 = []
ch7 = []
ch8 = []

psd_ch1 = []
psd_ch2 = []
psd_ch3 = []
psd_ch4 = []
psd_ch5 = []
psd_ch6 = []
psd_ch7 = []
psd_ch8 = []

alpha_data1 = []
alpha_data2 = []
alpha_data3 = []
alpha_data4 = []
alpha_data5 = []
alpha_data6 = []
alpha_data7 = []
alpha_data8 = []

beta_data1 = []
beta_data2 = []
beta_data3 = []
beta_data4 = []
beta_data5 = []
beta_data6 = []
beta_data7 = []
beta_data8 = []

alpha_beta_data1 = []
alpha_beta_data2 = []
alpha_beta_data3 = []
alpha_beta_data4 = []
alpha_beta_data5 = []
alpha_beta_data6 = []
alpha_beta_data7 = []
alpha_beta_data8 = []

#dictionary_psd = {}


################## Figuras de señal pura ################33
fig = plt.figure(1, constrained_layout=True)
gs = fig.add_gridspec(4, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_title("Channel 1")
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_title("Channel 2")
ax3 = fig.add_subplot(gs[2, 0])
ax3.set_title("Channel 3")
ax4 = fig.add_subplot(gs[3, 0])
ax4.set_title("Channel 4")
ax5 = fig.add_subplot(gs[0, 1])
ax5.set_title("Channel 5")
ax6 = fig.add_subplot(gs[1, 1])
ax6.set_title("Channel 6")
ax7 = fig.add_subplot(gs[2, 1])
ax7.set_title("Channel 7")
ax8 = fig.add_subplot(gs[3, 1])
ax8.set_title("Channel 8")

'''
###############Figura de señales alpha###############
fig2 = plt.figure(2, constrained_layout=True)
gs2 = fig2.add_gridspec(4, 2)#(Rows, Columns)
ax9 = fig2.add_subplot(gs2[0, 0])
ax9.set_title("Alpha Channel 1")
ax10 = fig2.add_subplot(gs2[1, 0])
ax10.set_title("Alpha Channel 2")
ax11 = fig2.add_subplot(gs2[2, 0])
ax11.set_title("Alpha Channel 3")
ax12 = fig2.add_subplot(gs2[3, 0])
ax12.set_title("Alpha Channel 4")
ax13 = fig2.add_subplot(gs2[0, 1])
ax13.set_title("Alpha Channel 5")
ax14 = fig2.add_subplot(gs2[1, 1])
ax14.set_title("Alpha Channel 6")
ax15 = fig2.add_subplot(gs2[2, 1])
ax15.set_title("Alpha Channel 7")
ax16 = fig2.add_subplot(gs2[3, 1])
ax16.set_title("Alpha Channel 8")
'''
'''

###############Figura de señales alpha/beta###############
fig3 = plt.figure(3, constrained_layout=True)
gs3 = fig3.add_gridspec(4, 2)  # (Rows, Columns)
ax17 = fig3.add_subplot(gs3[0, 0])
ax17.set_title("Alpha / Beta Channel 1")
ax18 = fig3.add_subplot(gs3[1, 0])
ax18.set_title("Alpha / Beta Channel 2")
ax19 = fig3.add_subplot(gs3[2, 0])
ax19.set_title("Alpha / Beta Channel 3")
ax20 = fig3.add_subplot(gs3[3, 0])
ax20.set_title("Alpha / Beta Channel 4")
ax21 = fig3.add_subplot(gs3[0, 1])
ax21.set_title("Alpha / Beta Channel 5")
ax22 = fig3.add_subplot(gs3[1, 1])
ax22.set_title("AAlpha / Beta Channel 6")
ax23 = fig3.add_subplot(gs3[2, 1])
ax23.set_title("Alpha / Beta Channel 7")
ax24 = fig3.add_subplot(gs3[3, 1])
ax24.set_title("Alpha / Beta Channel 8")
'''
BoardShim.enable_dev_board_logger()
params = BrainFlowInputParams()
# Modificar serial port de donde esté conectado el dongle
params.serial_port = 'COM3'
# Declarando id de lectura CYTON
board_id = BoardIds.SYNTHETIC_BOARD.value
sampling_rate = BoardShim.get_sampling_rate(board_id)
# sampling_rate = BoardShim.get_sampling_rate(board_id)
board = BoardShim(board_id, params)
####################################################################

############# Inicializamos sesión #######################

board.prepare_session()
# board.start_stream () # use this for default options
board.start_stream(45000, "file://testOpenBCI.csv:w")
BoardShim.log_message(LogLevels.LEVEL_INFO.value, ' ---- Starting the streaming with Cyton ---')

try:
    while (True):
        time.sleep(2)
        nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
        points_per_update = 4 * 255
        ####Checar variable dentro de get_current_data
        data = board.get_board_data()  # get latest 256 packages or less, doesnt remove them from internal buffer
        ############ Terminamos inicio de sesión ####################

        ############## Datos para transformadas #################
        eeg_channels = BoardShim.get_eeg_channels(board_id)
        eeg_channel1 = eeg_channels[0]
        # print(data[1]) #Para ver la info del canal 1
        DataFilter.detrend(data[eeg_channel1], DetrendOperations.LINEAR.value)
        psd_ch1 = DataFilter.get_psd_welch(data[eeg_channel1], nfft, nfft // 2, sampling_rate,
                                           WindowFunctions.BLACKMAN_HARRIS.value)  # agg
        psd_ch1_array = np.array(psd_ch1)  # Convertimos la psd a array para poder guardarlo en el csv
        #print(psd_ch1)  # Para verificar si se está calculado la psd contantemente
        # print(type(psd_ch1)) #PSD_CH1 es de tipo tuple
        alpha_ch1 = DataFilter.get_band_power(psd_ch1, 7.0, 13.0)  # Alpha
        beta_ch1 = DataFilter.get_band_power(psd_ch1, 14.0, 30.0)  # Beta
        alpha_beta_ch1 = alpha_ch1 / beta_ch1
        # print("Data Alpha 1", alpha_ch1)

        eeg_channel2 = eeg_channels[1]
        DataFilter.detrend(data[eeg_channel2], DetrendOperations.LINEAR.value)
        psd_ch2 = DataFilter.get_psd_welch(data[eeg_channel2], nfft, nfft // 2, sampling_rate,
                                           WindowFunctions.BLACKMAN_HARRIS.value)  # agg
        # print(psd_ch2)
        psd_ch2_array = np.array(psd_ch2)
        alpha_ch2 = DataFilter.get_band_power(psd_ch2, 7.0, 13.0)  # Alpha
        beta_ch2 = DataFilter.get_band_power(psd_ch2, 14.0, 30.0)  # Beta
        alpha_beta_ch2 = alpha_ch2 / beta_ch2
        # print("Data Alpha 2", alpha_ch2)

        eeg_channel3 = eeg_channels[2]
        DataFilter.detrend(data[eeg_channel3], DetrendOperations.LINEAR.value)
        psd_ch3 = DataFilter.get_psd_welch(data[eeg_channel3], nfft, nfft // 2, sampling_rate,
                                           WindowFunctions.BLACKMAN_HARRIS.value)  # agg
        # print(psd_ch3)
        psd_ch3_array = np.array(psd_ch3)
        alpha_ch3 = DataFilter.get_band_power(psd_ch3, 7.0, 13.0)  # Alpha
        beta_ch3 = DataFilter.get_band_power(psd_ch3, 14.0, 30.0)  # Beta
        # print("Data Alpha 3", alpha_ch3)
        alpha_beta_ch3 = alpha_ch2 / beta_ch3

        eeg_channel4 = eeg_channels[3]
        DataFilter.detrend(data[eeg_channel4], DetrendOperations.LINEAR.value)
        psd_ch4 = DataFilter.get_psd_welch(data[eeg_channel4], nfft, nfft // 2, sampling_rate,
                                           WindowFunctions.BLACKMAN_HARRIS.value)  # agg
        # print(psd_ch4)
        psd_ch4_array = np.array(psd_ch4)
        alpha_ch4 = DataFilter.get_band_power(psd_ch4, 7.0, 13.0)  # Alpha
        beta_ch4 = DataFilter.get_band_power(psd_ch4, 14.0, 30.0)  # Beta
        # print("Data Alpha 4", alpha_ch4)
        alpha_beta_ch4 = alpha_ch4 / beta_ch4

        eeg_channel5 = eeg_channels[4]
        DataFilter.detrend(data[eeg_channel5], DetrendOperations.LINEAR.value)
        psd_ch5 = DataFilter.get_psd_welch(data[eeg_channel5], nfft, nfft // 2, sampling_rate,
                                           WindowFunctions.BLACKMAN_HARRIS.value)  # agg
        # print(psd_ch5)
        psd_ch5_array = np.array(psd_ch5)
        alpha_ch5 = DataFilter.get_band_power(psd_ch5, 7.0, 13.0)  # Alpha
        beta_ch5 = DataFilter.get_band_power(psd_ch5, 14.0, 30.0)  # Beta
        # print("Data Alpha 5", alpha_ch5)
        alpha_beta_ch5 = alpha_ch5 / beta_ch5

        eeg_channel6 = eeg_channels[5]
        DataFilter.detrend(data[eeg_channel6], DetrendOperations.LINEAR.value)
        psd_ch6 = DataFilter.get_psd_welch(data[eeg_channel6], nfft, nfft // 2, sampling_rate,
                                           WindowFunctions.BLACKMAN_HARRIS.value)  # agg
        # print(psd_ch6)
        psd_ch6_array = np.array(psd_ch6)
        alpha_ch6 = DataFilter.get_band_power(psd_ch6, 7.0, 13.0)  # Alpha
        beta_ch6 = DataFilter.get_band_power(psd_ch6, 14.0, 30.0)  # Beta
        # print("Data Alpha 6", alpha_ch6)
        alpha_beta_ch6 = alpha_ch6 / beta_ch6

        eeg_channel7 = eeg_channels[6]
        DataFilter.detrend(data[eeg_channel7], DetrendOperations.LINEAR.value)
        psd_ch7 = DataFilter.get_psd_welch(data[eeg_channel7], nfft, nfft // 2, sampling_rate,
                                           WindowFunctions.BLACKMAN_HARRIS.value)  # agg
        # print(psd_ch7)
        psd_ch7_array = np.array(psd_ch7)
        alpha_ch7 = DataFilter.get_band_power(psd_ch7, 7.0, 13.0)  # Alpha
        beta_ch7 = DataFilter.get_band_power(psd_ch7, 14.0, 30.0)  # Beta
        # print("Data Alpha 7", alpha_ch7)
        alpha_beta_ch7 = alpha_ch7 / beta_ch7

        eeg_channel8 = eeg_channels[7]
        DataFilter.detrend(data[eeg_channel8], DetrendOperations.LINEAR.value)
        psd_ch8 = DataFilter.get_psd_welch(data[eeg_channel8], nfft, nfft // 2, sampling_rate,
                                           WindowFunctions.BLACKMAN_HARRIS.value)  # agg
        # print(psd_ch8)
        psd_ch8_array = np.array(psd_ch8)
        alpha_ch8 = DataFilter.get_band_power(psd_ch8, 7.0, 13.0)  # Alpha
        beta_ch8 = DataFilter.get_band_power(psd_ch8, 14.0, 30.0)  # Beta
        # print("Data Alpha 8", alpha_ch8)
        alpha_beta_ch8 = alpha_ch8 / beta_ch8

        # Creamos diccionario de listas de psd para guardar en csv
        # Lo hago con array porque la info de psd está dentro de arrays
        
        dictionary_psd = {'PSD 1': psd_ch1_array[0], 'PSD 2': psd_ch2_array[0], 'PSD 3': psd_ch3_array[0],
                          'PSD 4': psd_ch4_array[0], 'PSD 5': psd_ch5_array[0], 'PSD 6': psd_ch6_array[0],
                          'PSD 7': psd_ch7_array[0], 'PSD 8': psd_ch8_array[0]}
        
        '''
        dictionary_psd = {psd_ch1_array[0], psd_ch2_array[0], psd_ch3_array[0],
                           psd_ch4_array[0], psd_ch5_array[0], psd_ch6_array[0],
                           psd_ch7_array[0], psd_ch8_array[0], }
        '''
        #print(dictionary_psd)
        ###Guardado de datos en csv
        df = pd.DataFrame(dictionary_psd)
        #df2 = pd.DataFrame()
        #df2.append(df)
        df.to_csv('PSD.csv', mode='a')

        '''
        with open('urfile.csv', 'w') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['Psd'])
            for row in psd_ch1:
                csv_out.writerow(row)
        '''

        # Funciona esta generación de gráfica
        '''
        #Gráfica de datos crudos
        ch1.extend(data[1])
        ax1.clear()
        ax1.plot(ch1)
        plt.pause(0.01)

        ch2.extend(data[2])
        ax2.clear()
        ax2.plot(ch2)
        plt.pause(0.01)

        ch3.extend(data[3])
        ax3.clear()
        ax3.plot(ch3)
        plt.pause(0.01)

        ch4.extend(data[4])
        ax4.clear()
        ax4.plot(ch4)
        plt.pause(0.01)

        ch5.extend(data[5])
        ax5.clear()
        ax5.plot(ch5)
        plt.pause(0.01)

        ch6.extend(data[6])
        ax6.clear()
        ax6.plot(ch6)
        plt.pause(0.01)

        ch7.extend(data[7])
        ax7.clear()
        ax7.plot(ch7)
        plt.pause(0.01)

        ch8.extend(data[8])
        ax8.clear()
        ax8.plot(ch8)
        plt.pause(0.01)
        # Funciona esta generación de gráfica
        '''
        '''
        #Gráfica de datos con psd
        psd_ch1.extend(psd)
        bx1.clear()
        bx1.plot(psd_ch1)
        plt.pause(0.01)
        '''
        '''
        #Gráfica de datos crudos
        ch1.append(eeg_channel1)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax1.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax1.plot(ch1)
        plt.pause(0.001)

        ch2.append(eeg_channel2)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax2.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax2.plot(ch2)
        plt.pause(0.001)

        ch3.append(eeg_channel3)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax3.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax3.plot(ch3)
        plt.pause(0.001)

        ch4.append(eeg_channel4)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax4.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax4.plot(ch4)
        plt.pause(0.001)

        ch5.append(eeg_channel5)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax5.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax5.plot(ch5)
        plt.pause(0.001)

        ch6.append(eeg_channel6)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax6.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax6.plot(ch6)
        plt.pause(0.001)

        ch7.append(eeg_channel7)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax7.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax7.plot(ch7)
        plt.pause(0.001)

        ch8.append(eeg_channel8)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax8.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax8.plot(ch8)
        plt.pause(0.001)
        '''

        #### del 9 a 16
        # Gráfica de datos con alpha

        '''

        alpha_data1.append(alpha_ch1)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax9.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax9.plot(alpha_data1)
        plt.pause(0.001)

        alpha_data2.append(alpha_ch2)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax10.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax10.plot(alpha_data2)
        plt.pause(0.001)

        alpha_data3.append(alpha_ch3)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax11.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax11.plot(alpha_data3)
        plt.pause(0.001)

        alpha_data4.append(alpha_ch4)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax12.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax12.plot(alpha_data4)
        plt.pause(0.001)

        alpha_data5.append(alpha_ch5)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax13.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax13.plot(alpha_data5)
        plt.pause(0.001)

        alpha_data6.append(alpha_ch6)#Se usa append ya que no son valores de un array a diferencia de extend
        ax14.clear()#Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax14.plot(alpha_data6)
        plt.pause(0.001)

        alpha_data7.append(alpha_ch7)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax15.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax15.plot(alpha_data7)
        plt.pause(0.001)

        alpha_data8.append(alpha_ch8)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax16.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax16.plot(alpha_data8)
        plt.pause(0.001)
        '''
        '''
        #############################################################################################################
        ##############################################################################################################
        #### del 17 a 24
        # Gráfica de datos con alpha / beta

        alpha_beta_data1.append(alpha_beta_ch1)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax17.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax17.plot(alpha_beta_data1)
        plt.pause(0.001)

        alpha_beta_data2.append(alpha_beta_ch2)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax18.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax18.plot(alpha_beta_data2)
        plt.pause(0.001)

        alpha_beta_data3.append(alpha_beta_ch3)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax19.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax19.plot(alpha_beta_data3)
        plt.pause(0.001)

        alpha_beta_data4.append(alpha_beta_ch4)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax20.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax20.plot(alpha_beta_data4)
        plt.pause(0.001)

        alpha_beta_data5.append(alpha_beta_ch5)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax21.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax21.plot(alpha_beta_data5)
        plt.pause(0.001)

        alpha_beta_data6.append(alpha_beta_ch6)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax22.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax22.plot(alpha_beta_data6)
        plt.pause(0.001)

        alpha_beta_data7.append(alpha_beta_ch7)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax23.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax23.plot(alpha_beta_data7)
        plt.pause(0.001)

        alpha_beta_data8.append(alpha_beta_ch8)  # Se usa append ya que no son valores de un array a diferencia de extend
        ax24.clear()  # Sirve para borrar la gráfica anterior y escribir la nueva gráfica.
        ax24.plot(alpha_beta_data8)
        plt.pause(0.001)

        # df = pd.DataFrame(np.transpose(data))
        # plt.figure()
        # df[eeg_channels].plot(subplots=True)
        # plt.savefig('after_processing.png')
        '''
except KeyboardInterrupt:
    #DataFilter.write_file(psd_ch8_array, 'PSD.csv', 'w')
    board.stop_stream()
    board.release_session()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, ' ---- End the session with Cyton ---')

##############Links que pueden ayudar al entendimiento del código ##############
# https://www.geeksforgeeks.org/python-save-list-to-csv/

