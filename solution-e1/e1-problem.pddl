(define (problem scheduling-problem)
  (:domain scheduling-domain)
  (:objects t8am t9am t10am t11am t12pm t1pm t2pm - time
    room1 room2 room3 room4 room5 - room
    inhabitant1 inhabitant2 inhabitant3 inhabitant4 inhabitant5 - inhabitant
  )
  (:init 
    (currentTime t8am) 
    (next t8am t9am) (next t9am t10am) (next t10am t11am) (next t11am t12pm) (next t12pm t1pm) (next t1pm t2pm) 
    (locked room1) (locked room2) (locked room3) (locked room4) (locked room5)
    (canArrive inhabitant1 t8am room1)
    (canArrive inhabitant1 t9am room1)
    (canArrive inhabitant1 t12pm room1)
    (canArrive inhabitant2 t8am room2)
    (canArrive inhabitant2 t9am room2)
    (canArrive inhabitant3 t10am room3)
    (canArrive inhabitant4 t12pm room4)
    (canArrive inhabitant4 t1pm room4)
    (canArrive inhabitant5 t9am room5)
  )
  
  (:goal (and 
    (setup inhabitant1)
    (setup inhabitant2)
    (setup inhabitant3)
    (setup inhabitant4)
    (setup inhabitant5)
  ))
)