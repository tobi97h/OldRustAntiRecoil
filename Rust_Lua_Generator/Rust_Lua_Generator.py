import numpy as np
from matplotlib import pyplot as plt
import math
import pickle
from scipy.interpolate import make_interp_spline, BSpline
from getkey import getkey, keys
from datetime import datetime
import glob

manager = plt.get_current_fig_manager()
manager.window.state('zoomed')

def calc(weapon):
  
    full_graph = build_graph(weapon.x, weapon.y, weapon.ms_per_shot, weapon.shots, weapon.name)
    values = get_string_graph(full_graph)

    return weapon.name + " = " + values

def get_string_graph(full_vector):
    string_vector_parts = []

    for vector_part in full_vector:
        string_vector_parts.append("{" + str(vector_part[0]) + ", " + str(vector_part[1]) + "}")


    values = "{" + ", ".join(string_vector_parts) + "}"

    return values


def build_graph(x, y, ms_per_shot, shots, name):
    weapon_x = [0]
    weapon_y = [0]
    shot_ms = [0]

    last_x = 0
    last_y = 0
   
    ms_passed = 0
    for i in range(0, shots - 1):

        x_val = x[i]
        y_val = y[i]

        delta_x = x_val - last_x
        delta_y = y_val - last_y
        animation_time = math.sqrt((delta_x * delta_x) + (delta_y * delta_y)) / 0.02
   
        # only happens late on some bullets, animation time is hard capped by ms_per_shot
        if animation_time > ms_per_shot: 
            print(f'animation time larger than ms_per_shot {name} on shot {len(weapon_x)}')

            weapon_x.append(x_val)
            weapon_y.append(y_val)

            ms_passed+=ms_per_shot

            shot_ms.append(ms_passed)
        else:
            # move all during animation time
            weapon_x.append(x_val)
            weapon_y.append(y_val)

            ms_passed+=animation_time

            shot_ms.append(ms_passed)

            ms_passed_next = 0

            ms_passed_next = ms_per_shot - animation_time

            # only change time on next datapoint
            weapon_x.append(x_val)
            weapon_y.append(y_val)
            ms_passed+=ms_passed_next
            shot_ms.append(ms_passed)
       
   
        last_x = x_val
        last_y = y_val

    total_ms = math.floor(ms_passed)
    full_range = np.array(range(0, total_ms))

    fun_y = make_interp_spline(shot_ms, weapon_y, k=1)
    fun_x = make_interp_spline(shot_ms, weapon_x, k=1)

    plt.plot(fun_x(full_range), fun_y(full_range))
    #plt.show()

    full_vector = []

    for i in range(0, int(shots * ms_per_shot)):
        full_vector.append([fun_x(i), fun_y(i)])

    return full_vector

class Weapon:

    def __init__(self, name, repeat_delay, shots, x, y):
        self.name = name
        self.shots = shots
        self.x = x
        self.y = y
        self.ms_per_shot = repeat_delay


weapons = []
weapons.append(Weapon("ak", 133.30000638961792, 30, 
                      [1.3907062632285214,1.1764334502408484,3.3871707461173646,5.0870491851652755,5.094189086829459,4.426012801154849,3.2504552119818904,1.7354512031510199,0.04893565850270232,-1.6411565381226527,-3.166890502884598,-4.360331351942659,-5.053544201456452,-5.090650616437088,-4.489915538556545,-3.382553537114461,-1.8995856377872116,-0.17203286625115766,1.6690837518171975,3.4927431907415496,5.1679244248454665,6.56360642845253,7.548768175886437,7.992388641470555,7.5122256391478,6.06379234579299,4.11736515892494,2.1439320548176966,0.6144810097516711],
                      [-2.0039412840665776,-3.8441756774048494,-5.516686177315278,-7.017455781098323,-8.342467486054444,-9.487704289484107,-10.449149188687768,-11.222785180965893,-11.804595263618937,-12.190562433947365,-12.587131622128602,-13.320773253380537,-14.321275417643292,-15.511026930930969,-16.81241660925766,-18.147833268637438,-19.439665725084474,-20.61030279461278,-21.582133293236506,-22.27754603696978,-22.618929841826656,-22.817776859076133,-23.373894638142545,-24.211385718746534,-25.237342069507864,-26.358855659045446,-27.483018455978456,-28.51692242892666,-29.36765954650875]))


weapons.append(Weapon("smg", 100.00000149011612, 24,
                      [0.651254165073501,0.9681616160214163,0.9872046834883221,0.695112524764647,0.2062594494706041,-0.3338245942279136,-0.7796096581650126,-0.9855657941747964,-0.8372459636693952,-0.4148498504128195,0.12672997539772357,0.6324615667530731,0.9473129766440191,0.9353167033025045,0.6385964463887284,0.17860115195416526,-0.32473155964416023,-0.7514640680490192,-0.9816587529033072,-0.9354942149046508,-0.7141180735168717,-0.41930136757237335,-0.148707531567851],
                      [-1.3054078694024145,-2.5999053142889004,-3.859257580673728,-5.059229914571167,-6.1755875619954885,-7.1840957689609635,-8.06051978148186,-8.812341524253384,-9.496585579241554,-10.119676075782417,-10.686216907821706,-11.20081196930516,-11.668065154178516,-12.092580356387515,-12.478961469877888,-12.831812388595383,-13.155737006485728,-13.45533921749466,-13.735222915567926,-13.999991994651257,-14.254250348690393,-14.502601871631068,-14.749650457419026]))

weapons.append(Weapon("lr", 119.99999731779099, 30, 
                      [0.09836514635608265,0.3469533789917512,0.7512205038624928,1.3268879949694437,1.958068809785123,2.5276233222645432,2.9184119063627105,3.007762319876548,2.641919134416759,1.9506449686124094,1.144313210242629,0.4332972470865659,0.02797046692339933,0.04550590779400121,0.26851015669925093,0.6408799500842433,1.127565185131858,1.6935157590249261,2.303681568946354,2.923012512079022,3.516458485605769,4.0489693867094845,4.485495112573048,4.790985560379264,4.926560492954195,4.387823457638831,3.1627396123795393,1.7143682354833345,0.5057686052555255],
                      [-1.0049278982371976,-2.248522231216003,-3.5753458305742956,-4.829961527949953,-5.858608882698031,-6.687347209318497,-7.399670622719284,-8.00564277160374,-8.515327304675212,-8.93878787063705,-9.286088118192598,-9.567291696045205,-9.793952470720207,-9.992136744761961,-10.170167360168087,-10.33036462935772,-10.475048864750004,-10.60654037876408,-10.72715948381909,-10.839226492334173,-10.945061716728468,-11.04698546942112,-11.147318062831266,-11.24837980937805,-11.352491021480612,-11.461972011558085,-11.579143092029623,-11.706324575314362,-11.845836773831438]))

weapons.append(Weapon("m2", 119.99999731779099, 100, 
                      [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                      [-2.75, -5.5, -8.25, -11.0, -13.75, -16.5, -19.25, -22.0, -24.75, -27.5, -30.25, -33.0, -35.75, -38.5, -41.25, -44.0, -46.75, -49.5, -52.25, -55.0, -57.75, -60.5, -63.25, -66.0, -68.75, -71.5, -74.25, -77.0, -79.75, -82.5, -85.25, -88.0, -90.75, -93.5, -96.25, -99.0, -101.75, -104.5, -107.25, -110.0, -112.75, -115.5, -118.25, -121.0, -123.75, -126.5, -129.25, -132.0, -134.75, -137.5, -140.25, -143.0, -145.75, -148.5, -151.25, -154.0, -156.75, -159.5, -162.25, -165.0, -167.75, -170.5, -173.25, -176.0, -178.75, -181.5, -184.25, -187.0, -189.75, -192.5, -195.25, -198.0, -200.75, -203.5, -206.25, -209.0, -211.75, -214.5, -217.25, -220.0, -222.75, -225.5, -228.25, -231.0, -233.75, -236.5, -239.25, -242.0, -244.75, -247.5, -250.25, -253.0, -255.75, -258.5, -261.25, -264.0, -266.75, -269.5, -272.25, -275.0, -277.75]))

weapons.append(Weapon("mp5", 100.00000149011612, 30, 
                      [0.0,0.0,-1.9984014443252818e-14,-0.5103880100538412,-1.6872967973036639,-2.9993441399873153,-3.9151478163425866,-3.9483186188134525,-3.224567446351184,-2.2284308986912293,-1.4387222429643565,-1.2889144179521281,-1.598685737232632,-2.1546366967936876,-2.826861274774007,-3.485453449312388,-4.000507198547659,-4.242116500618501,-4.184897313209387,-3.969568622066628,-3.629240982872229,-3.1945729437001233,-2.6962230526243083,-2.164849857718675,-1.6311119070571785,-1.125667748713763,-0.6791759307624048,-0.3222950012770376,-0.0856835083315417],
                      [-0.8688381835178702,-2.0422188027642503,-3.3704409607782955,-4.7038037605991585,-5.8926063052659945,-6.787147697817959,-7.311441429815275,-7.74248210853942,-8.127405961242223,-8.468721276993662,-8.768936344863713,-9.030559453922352,-9.256098893239557,-9.448062951885303,-9.60895991892957,-9.74129808344233,-9.847585734493565,-9.930331161153248,-9.992042652491357,-10.035228497577869,-10.062396985482758,-10.076056405276008,-10.078715046027584,-10.072881196807476,-10.06106314668565,-10.045769184732087,-10.02950760001677,-10.014786681609662,-10.004114718580745]))

weapons.append(Weapon("thompson", 129.99999523162842, 20,
                      [0.7399524345182151,1.0113242215698288,0.8437103753398514,0.31278550034307934,-0.3338245942279136,-0.8446441579424624,-0.968982159641607,-0.6067921302544388,0.01632084668775846,0.6324615667530731,0.9737348255096734,0.8438976127423636,0.3745162665276691,-0.22635502972853772,-0.7514640680490192,-0.9935586404566443,-0.8620070859040752,-0.539790457889282,-0.19620062431773277],
                      [-1.5659557044685295,-3.109220788486232,-4.587917597165765,-5.96016847561979,-7.1840957689609635,-8.217821822301945,-9.093672222474856,-9.877483654967222,-10.577211727664578,-11.20081196930516,-11.756239908627201,-12.251451074368939,-12.694400995268605,-13.093045200064433,-13.45533921749466,-13.789238576297523,-14.10269880521125,-14.403675432974085,-14.700123988324258]))

def save(weapon_name, x_values, y_values):
    # remove the first added shot for saving
    x_values.pop(0)
    y_values.pop(0)
    save_obj = {"weapon_name": weapon_name, "x_values": x_values, "y_values" : y_values}
    ts = datetime.now().strftime("%d-%H-%M-%S")
    file_name = f'{weapon_name}_{ts}.obj'
    with open(file_name, "wb") as obj:
        pickle.dump(save_obj, obj, protocol=pickle.HIGHEST_PROTOCOL)
        print(f'saved {file_name}')

def load_save_objects():
    obj_store = []
    for obj in glob.glob("*.obj"):
        with open(obj, "rb") as handle:
            loaded = pickle.load(handle)
            obj_store.append(loaded)
    return obj_store

def graph_generation():
    saved_graphs = load_save_objects()

    weapons_str = ', '.join(w.name for w in weapons) 
    desired_action = input(f'select weapon: {weapons_str}')

    selected_weapon = None
    for weapon in weapons:
        if weapon.name == desired_action:
            selected_weapon = weapon
    
    if selected_weapon is None:
        print(f"no weapon with name{desired_action} was found")
        return

    print(f'Selected Weapon: {selected_weapon.name}')

    # add first shot for better visualisation
    selected_weapon.x.insert(0, 0)
    selected_weapon.y.insert(0, 0)

    #plot original
    plt.scatter(selected_weapon.x, selected_weapon.y, c="blue", s=3)

    #plot loaded
    fitting_graphs = []
    for graph in saved_graphs:
        if graph["weapon_name"] == selected_weapon.name:
            fitting_graphs.append(graph)

    for graph in fitting_graphs:
        plt.scatter(graph["x_values"], graph["y_values"], s=3)

  
    # new loop
    step = 0.01
    y_values = selected_weapon.y.copy()
    x_values = selected_weapon.x.copy()
    edit = plt.scatter(x_values, y_values)
    plt.show(block=False)
    plt.pause(0.001)
        
    current_shot = 1
    action = None
    while action != 'q':
        
        action = getkey()
        if action == keys.UP:
            if (y_values[current_shot] + step) < y_values[current_shot-1]:
                y_values[current_shot] = y_values[current_shot]+step
                print(f'y_values[{current_shot}] = {y_values[current_shot]}, x_values[{current_shot}] = {x_values[current_shot]}', end="\r")
            else:
                print("cant move up cuz y recoil vector always has to be negative")
        elif action == keys.DOWN: 
            if current_shot +1 >= len(y_values):
                y_values[current_shot] = y_values[current_shot]-step
            elif (y_values[current_shot]-step) > y_values[current_shot+1]:
                y_values[current_shot] = y_values[current_shot]-step
                print(f'y_values[{current_shot}] = {y_values[current_shot]}, x_values[{current_shot}] = {x_values[current_shot]}', end="\r")
            else:
                print("cant move down cuz y recoil vector always has to be negative")
        elif action == keys.LEFT:
            x_values[current_shot] = x_values[current_shot]-step
            print(f'y_values[{current_shot}] = {y_values[current_shot]}, x_values[{current_shot}] = {x_values[current_shot]}', end="\r")
        elif action == keys.RIGHT:
            x_values[current_shot] = x_values[current_shot]+step
            print(f'y_values[{current_shot}] = {y_values[current_shot]}, x_values[{current_shot}] = {x_values[current_shot]}', end="\r")
        elif action == '-':#next shot
            current_shot = current_shot+1
            print(f'current_shot: {current_shot}', end="\r")
        elif action  == '.':# previous shot
            current_shot = current_shot-1
            print(f'current_shot: {current_shot}', end="\r")
        elif action == 'r':#reset current shot
            y_values[current_shot] = selected_weapon.y[current_shot]
            x_values[current_shot] = selected_weapon.x[current_shot]
        elif action == 's':#save current
            save(selected_weapon.name, x_values, y_values)
            print("saved")
        elif action == 'n':#new one + save current
            save(selected_weapon.name, x_values, y_values)
            # plot the current (we are gonna use red for the current to edit)
            plt.scatter(x_values, y_values, s=1)

            y_values = selected_weapon.y.copy()
            x_values = selected_weapon.x.copy()
            current_shot = 1
            print("added new + current shot = 1")

        edit.remove()
        edit = plt.scatter(x_values, y_values, c="red", s=3)
        plt.pause(0.001)
        

def initial_actions_prompt():
    desired_action = input("wdywtd? 1. generate graphs, 2. add legit pattern")

    if desired_action.startswith("1"):

        tryout_graphs = load_save_objects()

        tryout_res_dict = {}

        for tryout_graph in tryout_graphs:
            search_weapon = None
            for weapon in weapons:
                if weapon.name == tryout_graph["weapon_name"]:
                    search_weapon = weapon

            full_vector = build_graph(tryout_graph["x_values"], tryout_graph["y_values"], search_weapon.ms_per_shot, search_weapon.shots, search_weapon.name)
            if search_weapon.name in tryout_res_dict:
                tryout_res_dict[search_weapon.name].append(get_string_graph(full_vector))
            else:
                tryout_res_dict[search_weapon.name] = [get_string_graph(full_vector)]

        str_graphs = []
        # build the lua object
        for name, graphs in tryout_res_dict.items():
            str_graph = name + " = " + "{" + ", ".join(graphs) + "}"
            str_graphs.append(str_graph)

        tryout_weapon_data = "{\n" + "\n, ".join(str_graphs) + "\n}"


        vectors = []

        for weapon in weapons:
            vectors.append(calc(weapon))

        full_weapon_data = "{\n"+"\n,".join(vectors) + "\n}"
        print("\n\n" + full_weapon_data)#break here for easy copy

    elif desired_action.startswith("2"):
        graph_generation()

initial_actions_prompt()
