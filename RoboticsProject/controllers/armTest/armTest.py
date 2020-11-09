
#fwd kin with PoE method
def fwdkin(angles):
    x=np.array([1,0,0])
    y=np.array([0,1,0])
    z=np.array([0,0,1])
    l0=.156
    l1=.147
    l2=.033
    l3=.155
    l4=.135
    l5=.2175
    h1=y
    h2=z
    h3=z
    h4=z
    h5=y
    p01=l0*x
    p12=l2*x+l1*y
    p23=l3*y
    p34=l4*y
    p45=y*0
    p5T=y*l5
    
    R01=rotAA(h1,angles[0])
    R12=rotAA(h2,angles[1])
    R23=rotAA(h3,angles[2])
    R34=rotAA(h4,angles[3])
    R45=rotAA(h5,angles[4])
    
    p01_0=p01
    p12_0=np.dot(R01,p12)
    p23_0=np.dot(R01*R12,p23)
    p34_0=np.dot(R01*R12*R23,p34)
    p45_0=p45
    p5T_0=np.dot(R01*R12*R23*R34*R45,p5T)
    pT=p01_0+p12_0+p23_0+p34_0+p45_0+p5T_0
    R0T= R01*R12*R23*R34*R45
    return R0T,pT
def rotAA(ax,ang):
    skewMat=skew(ax)
    return np.identity(3)+skewMat*np.sin(ang)+skewMat*skewMat*(1-np.cos(ang))
def skew(vec):
    return np.matrix([[0,-vec[2],vec[1]],[vec[2],0,-vec[0]],[-vec[1],vec[0],0]])
    
from controller import Robot
import numpy as np
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
gps=robot.getGPS("gps")
gps.enable(timestep)
finger1=robot.getMotor("finger1")
finger2=robot.getMotor("finger2")
finger1.setPosition(0.025)
finger2.setPosition(0.025)
joint1=robot.getMotor("arm1")
joint2=robot.getMotor("arm2")
joint3=robot.getMotor("arm3")
joint4=robot.getMotor("arm4")
joint5=robot.getMotor("arm5")
q=[0,0,0,0,0]
joint1.setPosition(q[0])
joint2.setPosition(q[1])
joint3.setPosition(q[2])
joint4.setPosition(q[3])
joint5.setPosition(q[4])
joints=[joint1,joint2,joint3,joint4,joint5]

robot.step(timestep)
robot.step(timestep)
robot.step(timestep)
robot.step(timestep)
robot.step(timestep)
robot.step(timestep)
robot.step(timestep)

Rot,pot=fwdkin(q)
#Rot=rotAA(np.array([1,0,0]),-np.pi/2)*Rot
print(Rot)
pos=gps.getValues()
print("robot position: ",pos)
print("from robot position to end effector",pot)
print("end effect pos in world space",pot+pos)

