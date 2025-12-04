import time
import RPi.GPIO as GPIO
import adc_plot
import numpy as np
from mcp3021_driver import MCP3021

def round_to_step(value, step=0.05, max_value=0.6):
    rounded = round(value / step) * step
    return min(max(rounded, 0), max_value) 
if __name__ == "__main__":
    mcp = MCP3021(3.8, True)
    voltage_values = []
    time_values = []
    sampling_periods = []

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(15, GPIO.IN)
    #duration = 60.0
    #start_time = time.time()
    
    try:
        devst = 1
        while True:
            start_time = time.time()
            while not GPIO.input(15):
                devst = 0
                voltage = mcp.get_voltage()
                voltage_values.append(voltage)
                time_values.append(time.time()-start_time)
                max_voltage = max(voltage_values)

                exp_time = time.time() - start_time
                print("Эксперимент идет! Время: ", exp_time, voltage)
            time.sleep(1)
            if devst == 0:
                break


        #sampling_periods = [round_to_step(time_values[i] - time_values[i-1]) for i in range(1, len(time_values))]

        data = np.column_stack((time_values, voltage_values))
        np.savetxt('\\home\\b03-405\\Desktop\\igor bogdan erdeny\\data_Erdeny.csv',
                    data,
                    delimiter = ',',
                    fmt='%.4f',
                    header = 'Время[с],Напряжение[В]',
                    comments = '',
                    encoding = 'utf-8')
        adc_plot.plot_voltage_vs_time(time_values, voltage_values, max_voltage)
        #adc_plot.plot_sampling_period_hist(sampling_periods)

    except ValueError:
        print()

    finally:
        mcp.deinit()