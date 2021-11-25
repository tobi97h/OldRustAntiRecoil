import numpy as np
from matplotlib import pyplot as plt
import math
from scipy.interpolate import make_interp_spline, BSpline

ms_adjust = 4

def calc(weapon):
   
    weapon_x = [0]
    weapon_y = [0]
    shot_ms = [0]
    last_value= [0,0]

    animation_extra = 0
   
    first = True
    ms_passed = 0
    for val in weapon.values:

        delta_x = val[0] - last_value[0]
        delta_y = val[1] - last_value[1]
        animation_time = math.sqrt((delta_x * delta_x) + (delta_y * delta_y)) / 0.02
   
        # only happens late on some bullets
        if animation_time > weapon.ms_per_shot: 
            print(f'animation time larger than ms_per_shot {weapon.name} on shot {len(weapon_x)}')

            weapon_x.append(val[0])
            weapon_y.append(val[1])

            if first:
                # to catch up to the game we have to speed up the recoil compensation by a few seconds
                ms_passed+=weapon.ms_per_shot - ms_adjust
            else:
                # only do it on first shot so we offset the graph
                ms_passed+=weapon.ms_per_shot

            shot_ms.append(ms_passed)
        else:
            # move all during animation time
            weapon_x.append(val[0])
            weapon_y.append(val[1])

            if first:
                # to catch up to the game we have to speed up the recoil compensation by a few seconds
                ms_passed+=animation_time - ms_adjust
            else:
                # only do it on first shot so we offset the graph
                ms_passed+=animation_time

            shot_ms.append(ms_passed)

            ms_passed_next = 0
            if first:
                ms_passed_next = weapon.ms_per_shot - animation_time - ms_adjust
            else:
                ms_passed_next = weapon.ms_per_shot - animation_time

            if ms_passed_next < 0:
                 print(f'ms_passed_next for weapon {weapon.name}  on shot {len(weapon_x)} cannot be smaller than zero, choose a lower ms_adjust time ')
                 return

            # only change time on next datapoint
            weapon_x.append(val[0])
            weapon_y.append(val[1])
            ms_passed+=ms_passed_next
            shot_ms.append(ms_passed)

        # we completed the first iteration
        if first:
            first = False
        
   
        last_value = val


    total_ms = math.floor(ms_passed)
    full_range = np.array(range(0, total_ms))

    fun_y = make_interp_spline(shot_ms, weapon_y, k=1)
    fun_x = make_interp_spline(shot_ms, weapon_x, k=1)

    plt.plot(shot_ms, weapon_y, 'ro')
    plt.plot(full_range, fun_y(full_range))
    #plt.show()

    plt.plot(shot_ms, weapon_x, 'ro')
    plt.plot(full_range, fun_x(full_range))
    #plt.show()

    full_vector = []

    for i in range(0, int(weapon.shots * weapon.ms_per_shot)):
        full_vector.append([fun_x(i), fun_y(i)])

    string_vector_parts = []

    for vector_part in full_vector:
        string_vector_parts.append("{" + str(vector_part[0]) + ", " + str(vector_part[1]) + "}")


    values = "{" + ", ".join(string_vector_parts) + "}"


    return weapon.name + " = " + values

class Weapon:

    def __init__(self, name, rpm, shots, deg, values):
        self.deg = deg
        self.name = name
        self.rpm = rpm
        self.shots = shots
        self.values = values
        self.ms_per_shot = 1000 / (self.rpm/60)

weapons = []
weapons.append(Weapon("ak", 450, 30, 25, [[1.390706, -2.003941], [1.176434, -3.844176], [3.387171, -5.516686], [5.087049, -7.017456], [5.094189, -8.342467], [4.426013, -9.487704], [3.250455, -10.44915], [1.73545, -11.22279], [0.04893398, -11.8046], [-1.641158, -12.19056], [-3.166891, -12.58713], [-4.360331, -13.32077], [-5.053545, -14.32128], [-5.090651, -15.51103], [-4.489915, -16.81242], [-3.382552, -18.14783], [-1.899585, -19.43966], [-0.1720295, -20.61031], [1.669086, -21.58213], [3.492748, -22.27755], [5.16793, -22.61893], [6.563614, -22.81778], [7.548776, -23.37389], [7.992399, -24.21139], [7.512226, -25.23734], [6.063792, -26.35886], [4.117367, -27.48302], [2.143932, -28.51692], [0.6144824, -29.36766]]))
weapons.append(Weapon("smg", 600, 24, 15, [[0.6512542, -1.305408], [0.9681615, -2.599905], [0.9872047, -3.859258], [0.6951124, -5.05923], [0.2062594, -6.175588], [-0.3338249, -7.184096], [-0.7796098, -8.060521], [-0.9855663, -8.812342], [-0.8372459, -9.496586], [-0.4148501, -10.11968], [0.1267298, -10.68622], [0.6324611, -11.20081], [0.9473124, -11.66807], [0.9353167, -12.09258], [0.6385964, -12.47896], [0.1786009, -12.83181], [-0.3247314, -13.15574], [-0.7514643, -13.45534], [-0.9816588, -13.73522], [-0.9354943, -13.99999], [-0.714118, -14.25425], [-0.4193012, -14.5026], [-0.1487077, -14.74965]]))
weapons.append(Weapon("lr", 500, 30, 15, [[0.09836517, -1.004928], [0.3469534, -2.248523], [0.7512205, -3.575346], [1.326888, -4.829963], [1.958069, -5.858609], [2.527623, -6.687347], [2.918412, -7.399671], [3.007762, -8.005643], [2.641919, -8.515327], [1.950645, -8.938788], [1.144313, -9.286088], [0.4332969, -9.567291], [0.02797037, -9.793953], [0.04550591, -9.992137], [0.2685102, -10.17017], [0.6408804, -10.33037], [1.127565, -10.47505], [1.693516, -10.60654], [2.303682, -10.72716], [2.923013, -10.83923], [3.516459, -10.94506], [4.04897, -11.04699], [4.485496, -11.14732], [4.790986, -11.24838], [4.92656, -11.35249], [4.387823, -11.46197], [3.16274, -11.57914], [1.714368, -11.70632], [0.5057687, -11.84584]]))
weapons.append(Weapon("m2", 500, 100, 15, [[0.0, -2.75], [0.0, -5.5], [0.0, -8.25], [0.0, -11.0], [0.0, -13.75], [0.0, -16.5], [0.0, -19.25], [0.0, -22.0], [0.0, -24.75], [0.0, -27.5], [0.0, -30.25], [0.0, -33.0], [0.0, -35.75], [0.0, -38.5], [0.0, -41.25], [0.0, -44.0], [0.0, -46.75], [0.0, -49.5], [0.0, -52.25], [0.0, -55.0], [0.0, -57.75], [0.0, -60.5], [0.0, -63.25], [0.0, -66.0], [0.0, -68.75], [0.0, -71.5], [0.0, -74.25], [0.0, -77.0], [0.0, -79.75], [0.0, -82.5], [0.0, -85.25], [0.0, -88.0], [0.0, -90.75], [0.0, -93.5], [0.0, -96.25], [0.0, -99.0], [0.0, -101.75], [0.0, -104.5], [0.0, -107.25], [0.0, -110.0], [0.0, -112.75], [0.0, -115.5], [0.0, -118.25], [0.0, -121.0], [0.0, -123.75], [0.0, -126.5], [0.0, -129.25], [0.0, -132.0], [0.0, -134.75], [0.0, -137.5], [0.0, -140.25], [0.0, -143.0], [0.0, -145.75], [0.0, -148.5], [0.0, -151.25], [0.0, -154.0], [0.0, -156.75], [0.0, -159.5], [0.0, -162.25], [0.0, -165.0], [0.0, -167.75], [0.0, -170.5], [0.0, -173.25], [0.0, -176.0], [0.0, -178.75], [0.0, -181.5], [0.0, -184.25], [0.0, -187.0], [0.0, -189.75], [0.0, -192.5], [0.0, -195.25], [0.0, -198.0], [0.0, -200.75], [0.0, -203.5], [0.0, -206.25], [0.0, -209.0], [0.0, -211.75], [0.0, -214.5], [0.0, -217.25], [0.0, -220.0], [0.0, -222.75], [0.0, -225.5], [0.0, -228.25], [0.0, -231.0], [0.0, -233.75], [0.0, -236.5], [0.0, -239.25], [0.0, -242.0], [0.0, -244.75], [0.0, -247.5], [0.0, -250.25], [0.0, -253.0], [0.0, -255.75], [0.0, -258.5], [0.0, -261.25], [0.0, -264.0], [0.0, -266.75], [0.0, -269.5], [0.0, -272.25], [0.0, -275.0], [0.0, -277.75]]))
weapons.append(Weapon("mp5", 600, 30, 15, [[0, -0.8688382], [0, -2.042219], [-2.992364e-14, -3.370441], [-0.5103882, -4.703804], [-1.687297, -5.892606], [-2.999344, -6.787148], [-3.915147, -7.311441], [-3.948318, -7.742482], [-3.224567, -8.127406], [-2.228431, -8.468721], [-1.438722, -8.768936], [-1.288914, -9.03056], [-1.598686, -9.2561], [-2.154637, -9.448063], [-2.826861, -9.60896], [-3.485454, -9.741299], [-4.000507, -9.847586], [-4.242117, -9.930332], [-4.184897, -9.992043], [-3.969568, -10.03523], [-3.629241, -10.0624], [-3.194572, -10.07606], [-2.696223, -10.07872], [-2.16485, -10.07288], [-1.631112, -10.06106], [-1.125667, -10.04577], [-0.6791761, -10.02951], [-0.3222946, -10.01479], [-0.08568263, -10.00412]]))
weapons.append(Weapon("thompson", 462, 20 , 15, [[0.7399524, -1.565956], [1.011324, -3.109221], [0.8437103, -4.587918], [0.3127854, -5.960169], [-0.3338249, -7.184096], [-0.8446444, -8.217823], [-0.9689822, -9.093672], [-0.6067921, -9.877484], [0.01632042, -10.57721], [0.6324611, -11.20081], [0.9737339, -11.75624], [0.8438975, -12.25145], [0.3745165, -12.6944], [-0.2263549, -13.09305], [-0.7514643, -13.45534], [-0.9935587, -13.78924], [-0.862007, -14.1027], [-0.5397906, -14.40368], [-0.1962007, -14.70013]] ))

#res = calc(weapons[5])

vectors = []
ms_per_shots = []

for weapon in weapons:
    vectors.append(calc(weapon))
    ms_per_shots.append(weapon.name + " = " + str(int(weapon.ms_per_shot)))


full_weapon_data = "{\n"+"\n,".join(vectors) + "\n}"
ms_per_shots = "{\n"+"\n,".join(ms_per_shots) + "\n}"
wait = 1