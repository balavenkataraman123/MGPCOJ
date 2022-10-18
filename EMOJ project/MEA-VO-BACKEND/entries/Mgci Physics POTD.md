    
# Format
- #### A new problem is revealed every wednesday.
- #### You must provide a solution to it within a week on the MGPCOJ website
- #### problems will be taken up in the physics club meeting on wednesday, the new problem will be proposed.
- #### Anyone who solves every problem in a 2 month interval will get bubble tea.

# Problem 1 - Elevator Sunset

> Proposed by Bala Venkataraman (instagram: bariumlanthanum)

You are riding an elevator with glass walls up the tallest building in Singapore (which is almost exactly on the equator). As you get on the elevator, the center of the sun is exactly at the level of the horizon. Assume you are exactly on the equator on surface level, and the radius of the earth is 6371km, and ignore the tilt of the earth along its axis and atmospheric refraction effects.

a) If the center of the setting sun is to stay level with the horizon, write an equation for the instantaneous speed of the elevator with respect to time (you may use a scientific calculator)

b) If the elevator can travel at a maximum of 100km/h, how long (to the nearest second) can you see the center of the sun on the horizon? 

## Solution 
### a)
![[/image/1]]
let A be the point in space and time where you are initially at ground level, and assume B is the point where the elevator has travelled for a certain amount of time.

yesthat 

We can express the distance as a function of time t in hours.

Since AOB is a right triangle, 
## $r+h$ = $\frac{r}{cos \frac{\pi t}{12}}$ 
$cos \frac{\pi t}{12}$ is because the earth covers $2\pi$ radians in 24 hours

## $h = \frac{6371}{cos \frac{\pi t}{12}} - 6371$


## $\frac{d}{dt}$ $\frac{6371}{cos \frac{\pi t}{12}}$

This can be differentiated using the trig identiy 1/ cos (x) = sec x, and the chain rule

## $\frac{d}{dt}$ $\frac{6371}{cos \frac{\pi t}{12}}  = \frac{6371\pi }{12}\sec \left(\frac{\pi x}{12}\right)\tan \left(\frac{\pi x}{12}\right)$

### b)

### $\frac{6371\pi }{12}\sec \left(\frac{\pi t}{12}\right)\tan \left(\frac{\pi t}{12}\right)$ < 100 is satisfied for t < 0.228

#### which is approximately 821 seconds

## You can see the sunset in that position for approximately 821 seconds	


# Problem 2 - Drunk Driving

> Proposed by Bala Venkataraman (instagram: bariumlanthanum)


A drunk driver in 1600kg Honda Accord has a half full shot glass of vodka in the cup holder. When driving 50km/h, he crashes into a stationery 2000kg Dodge Challdnger. The bumpers of each car are 0.5m long, and behave like ideal springs with a coefficient of 5000000 n/m. Assuming no energy is lost, will the vodka in the shot glass spill?

(dimensions of a shot glass are: **Diameter: 4cm**, **Height: 6cm)



# Problem 3 - pendulum in a car
> Proposed by Bala Venkataraman (instagram: bariumlanthanum)

![[Pasted image 20220922190139.png]]
BariumLanthanum's car has an air freshener thingy hanging from the inside rear view mirror.  Assume it is a 20g point mass, connected to the mirror with a massless 10cm string. 

immediately after giving it an initial swing along the direction of motion of the car, so its 45 degrees from the horizontal towards the front of the car, He starts a quarter mile drag race with Trentium's Honda Civic, and slams the pedal to the floor. His 2022 Toyota Corolla runs the quarter mile in 16.35 seconds, finishing head to head with Trentium, as even though the Civic has more power than the Corolla, it is weighed down by Trentium's huge MSI laptop in the trunk.

a) Assuming the cars accelerate constantly, What distance does the pendulum travel throughout the duration of the race?

b) If Trentium swings his air freshener 45 degrees perpendicular to the direction of motion of his car, how far does his pendulum travel throughout the duration of the race?



