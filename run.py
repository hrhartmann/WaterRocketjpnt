import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from vars import *
from rocket import *

class Table:

    def __init__(self, rocket):
        self.values = {}
        self.rocket = rocket

    def run(self):
        self.rocket.get_initial_values()
        escaping = True
        in_air = True
        while in_air:
            self.get_value(self.rocket.t)
            if self.values[self.rocket.t]['height'] < 0:
                in_air = False
            #############################################################################
            #print(self.values[self.rocket.t])
            #print('Time: ', self.rocket.t * delta_t)
            self.rocket.step()


    def get_value(self, t):
        if t == 0:
            self.values[0] = {'air_vol':self.rocket.i_air_volume,
                                'vel':self.rocket.velocity(
                                    self.rocket.i_air_volume, 0
                                    ),
                                'a':self.rocket.acceleration(
                                0, self.rocket.i_air_volume
                                ),
                                'height':0,
                                'time':0}
        else:
            self.values[t] = {'air_vol':self.rocket.t_air_vol(
                                self.values[t - 1]['air_vol']),
                            'vel':self.rocket.velocity(
                                self.values[t - 1]['air_vol'],
                                self.values[t - 1]['vel']),
                            'a':self.rocket.acceleration(
                                self.values[t - 1]['vel'],
                                self.values[t - 1]['air_vol']),
                            'height':self.rocket.height(
                                self.values[t - 1]['height'],
                                self.values[t - 1]['vel']
                            ),
                            'time':self.rocket.t * delta_t
                            }

def generate_csv_rocket_data(rocket_data):
    with open('rocket_data.csv', 'w') as rdata_file:
        text = 'time,velocity,acceleration,height,air volume\n'
        for value in rocket_data.values():
            t = value['time']
            v = value['vel']
            a = value['a']
            h = value['height']
            av = value['air_vol']
            line = f'{t},{v},{a},{h},{av}\n'
            text += line
        rdata_file.writelines(text)






if __name__ == '__main__':
    wmissile = Rocket(bottle_radius,
                        bottle_height,
                        water_lvl,
                        air_pressure,
                        r_coefficient,
                        bottle_neck_radius,
                        bottle_mass,
                        planet_g)

    CtrlCenter = Table(wmissile)
    CtrlCenter.run()

    generate_csv_rocket_data(CtrlCenter.values)

    rocket_data = {'time':[value['time'] for value in CtrlCenter.values.values()],
                    'vel':[value['vel'] for value in CtrlCenter.values.values()],
                    'height':[value['height'] for value in CtrlCenter.values.values()]}



    #print(rocket_data)
    dataframe = pd.DataFrame(rocket_data)
    dataframe.plot(x='time', y='vel')














































    #nothing
    #By AbyssalBit
