
from math import pi
import matplotlib.pyplot as plt
from vars import *





class Rocket:

    def __init__(self,
                bottle_radius,
                bottle_height,
                water_lvl,
                air_pressure,
                r_coefficient,
                bottle_neck_radius,
                bottle_mass,
                planet_g):

        self.volume = pi*(bottle_radius**2)*bottle_height
        self.water_lvl = water_lvl
        self.air_i_pressure = air_pressure
        self.r_coefficient = r_coefficient
        self.bottle_neck_A = 2*pi*bottle_radius
        self.bottle_horizontal_A = pi*(bottle_radius**2)
        self.bottle_mass = bottle_mass
        self.planet_g = planet_g
        self.final_vel = None
        self.t = 0

    def step(self):
        self.t += 1

    def get_initial_values(self):
        self.i_water_vol = self.volume*self.water_lvl
        self.i_water_mass = self.i_water_vol * Water_rho
        self.i_air_volume = (1 - water_lvl) * self.volume
        self.i_air_mass = self.i_air_volume*Air_rho

        self.i_tot_mass = (self.bottle_mass +
                        self.i_air_mass +
                        self.i_water_mass)


    def t_air_p(self, air_vol):
        if air_vol >= self.volume:
            return atm_pressure
        p = self.air_i_pressure * (self.i_air_volume / air_vol)**gamma
        #print('P: ', p)
        return p

    def t_air_vol(self, air_vol):
        if air_vol >= self.volume:
            return self.volume
        p = self.t_air_p(air_vol)
        if p > atm_pressure:
            term = delta_t*self.bottle_neck_A*((
                self.t_air_p(air_vol) - atm_pressure)/Water_rho
                )**0.5
            return air_vol + term
        else:
            return self.volume

    def wex(self, air_vol):
        if air_vol >= self.volume:
            return 0
        sqwex = (2*self.t_air_p(air_vol) - atm_pressure) / Water_rho
        return sqwex ** 0.5

    def t_mass(self, air_vol):
        airmass = air_vol*Air_rho
        watermass = (self.volume - air_vol)*Water_rho
        return self.bottle_mass + airmass + watermass

    def velocity(self, air_vol, w):
        wex_term = Water_rho*(self.wex(air_vol)**2)*(
                self.bottle_neck_A/self.t_mass(air_vol))
        w_term = Air_rho*self.bottle_horizontal_A*(
                self.r_coefficient*(w**2))/2
        #print('wex: ', wex_term)
        #print('w term: ', w_term)
        aterm = wex_term - w_term - planet_g
        vel = aterm*delta_t + w
        '''if air_vol >= self.volume:
            if self.final_vel == None:
                self.final_vel = vel
            return self.free_velocity(self.final_vel)'''
        return vel

    def free_velocity(self, final_v):
        return final_v - (self.planet_g*self.t)

    def acceleration(self, w, air_vol):
        if air_vol >= self.volume:
            return -planet_g
        return (self.velocity(air_vol, w) - w)/delta_t

    def height(self, h, vel):
        return h + (vel*delta_t)







if __name__ == '__main__':
    pass









































#nothing
