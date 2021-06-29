#PASSIVE

from itertools import permutations
import math

###################################################################################


def introduction():
    function_type = 'Tool Path Optimiser'
    dependant_functions = []
    active_passive = 'passive'
    performative_types = ['request_tool_path_optimization']
    return {'function_type': function_type, 'Dependant Function': dependant_functions, "active_passive": active_passive,
            "performative_types": performative_types}


###################################################################################

def ToolPathOptimser(file_name, tool_R=2.5, base_plane='xz', spindle_speed=1000, feed_rate=50):
    file = open(file_name, "r")
    #initialisation
    data=[]
    cartesian_point_data=[]
    cartesian_point_data_x=[]
    cartesian_point_data_y=[]
    cartesian_point_data_z=[]
    hole_centre_coord_data=[]

    for line in file:
        if(line[0]=='#'):
            data.append(line[0:-2])
            if 'CYLINDRICAL_SURFACE' in line:
                data_array=data[-1].split(',')
                R_array=(data_array[2][:-1]).split('E')
                R=float(R_array[0])*10**(float(R_array[1]))
                if R==tool_R:
                    coord_array=data[-5].split(',')
                    x_array=(coord_array[1][1:]).split('E')
                    y_array=(coord_array[2]).split('E')
                    z_array=(coord_array[3][:-2]).split('E')
                    x=float(x_array[0])*10**(float(x_array[1]))
                    y=float(y_array[0])*10**(float(y_array[1]))
                    z=float(z_array[0])*10**(float(z_array[1]))
                    hole_centre_coord_data.append([x,y,z])
                
            elif 'CARTESIAN_POINT' in line:
                coord_array=data[-1].split(',')
                x_array=(coord_array[1][1:]).split('E')
                y_array=(coord_array[2]).split('E')
                z_array=(coord_array[3][:-2]).split('E')
                x=float(x_array[0])*10**(float(x_array[1]))
                y=float(y_array[0])*10**(float(y_array[1]))
                z=float(z_array[0])*10**(float(z_array[1]))
                cartesian_point_data.append([x,y,z])
                cartesian_point_data_x.append(x)
                cartesian_point_data_y.append(y)
                cartesian_point_data_z.append(z)


    hole_centre_coord_data=list(set(tuple(row) for row in hole_centre_coord_data))
    for i in range (len(hole_centre_coord_data)): hole_centre_coord_data[i]=list(hole_centre_coord_data[i])

    job_max_x=max(cartesian_point_data_x)
    job_max_y=max(cartesian_point_data_y)
    job_max_z=max(cartesian_point_data_z)
    job_min_x=min(cartesian_point_data_x)
    job_min_y=min(cartesian_point_data_y)
    job_min_z=min(cartesian_point_data_z)

    machine_home_position=[job_min_x,job_min_y,job_min_z]

    for i in range (len(hole_centre_coord_data)):
        hole_centre_coord_data[i][0]=hole_centre_coord_data[i][0]-machine_home_position[0]
        hole_centre_coord_data[i][1]=hole_centre_coord_data[i][1]-machine_home_position[1]
        hole_centre_coord_data[i][2]=hole_centre_coord_data[i][2]-machine_home_position[2]

    home_positin=(0,0,0)

    if base_plane=='xy':
        dim1=1
        dim2=1
        dim3=0
        thickness=job_max_z-job_min_z
        index1=0
        index2=1
        
    elif base_plane=='xz':
        dim1=1
        dim2=0
        dim3=1
        thickness=job_max_y-job_min_y
        index1=0
        index2=2
        
    else:
        dim1=0
        dim2=1
        dim3=1
        thickness=job_max_x-job_min_x
        index1=1
        index2=2

    cur_pos=[0.0, 0.0, 0.0]
    Seq_hole_centre_coord=[]
    for i in range(len(hole_centre_coord_data)):
        min_dist=float('inf')
        for xj, yj, zj in hole_centre_coord_data:
            x2 = ((xj-cur_pos[0])**2)*dim1
            y2 = ((yj-cur_pos[1])**2)*dim2
            z2 = ((zj-cur_pos[2])**2)*dim3
            cur_dist = math.sqrt(x2+y2+z2)
            if cur_dist < min_dist:
                min_dist = cur_dist
                temp_cur_pos = [xj, yj, zj]

        cur_pos = temp_cur_pos
        next_hole_index = hole_centre_coord_data.index(cur_pos)
        del hole_centre_coord_data[next_hole_index]
        Seq_hole_centre_coord.append(cur_pos)

    CNC_code='N10 G21 G90 G40 G80 G49 G54 G94 F50\n'
    CNC_code+='N20 M06 T1'
    CNC_code+='N30 M03 S'+str(spindle_speed)+'\n'
    CNC_code+='N40 G00 X0 Y0 Z'+str(10+thickness)+'\n'
    CNC_code+='N50 G99 G81 X'+str(Seq_hole_centre_coord[0][index1])+' Y'+str(Seq_hole_centre_coord[0][index2])+' F'+str(feed_rate)+' Z0 R'+str(5+thickness)+'\n'
    n=50
    for hole_coord in (Seq_hole_centre_coord[1:]):
        n+=10
        CNC_code+='N'+str(n)+' X'+str(hole_coord[index1])+' Y'+str(hole_coord[index2])+'\n'
    n+=10
    CNC_code+='N'+str(n)+' G00 X0 Y0 Z'+str(10+thickness)+'\n'
    n+=10
    CNC_code+='N'+str(n)+' M30\n'
   
    file1 = open("CNC_code.txt","w")  
    file1.write(CNC_code) 
    file1.close()

    return CNC_code

###################################################################################

##file_name = "D:\\Academics\\MTP\\Agent\\data\\30x30-5holes.stp"
##print(ToolPathOptimser(file_name, tool_R=2.5, base_plane='xz', spindle_speed=1000, feed_rate=50))
