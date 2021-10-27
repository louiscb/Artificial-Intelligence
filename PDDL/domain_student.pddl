  ;; Domain definition
(define (domain student-life-domain)
    (:requirements :negative-preconditions)
  

(:predicates
	(BUILDING ?x) ; true if x is a building
	(PERSON ?x) ; true if x is a person
	(LECTURE ?x) ; true if x is a lecture
	(IS-MORNING ?x) ; true if lecture x is a morning lecture
	(IS-AFTERNOON ?x) ; true if lecture y is an afternoon lecture
    (IS-CONNECTED ?x ?y) ; true if building x is connected to building y
    (IS-STUDENT ?x) ; true if person x is a student
    (IS-TEACHER ?x) ; true if person x is a teacher
	(HAS-RESTURANT ?x) ; true if building x has a restaurant inside
    (IS-LECTURE-AT ?x ?y) ; true if lecture x is in the building y
	(is-person-at ?x ?y) ; true if person x is in building y
	(attended-lecture ?x ?y) ; true if person x has attended lecture y
	(had-lunch ?x) ; ; true if person x has had lunch
    (teaches-lecture ?x ?y) ; true if teacher x teaches lecture y
)

; The person x moves from building y to building z if they are connected
; As a result, person x in no longer at y but they are at z
; Parameters:
; - x: the person
; - y: a building
; - z: another building
(:action move
    :parameters ( ?x ?y ?z )
    :precondition (and (PERSON ?x) (BUILDING ?y) (BUILDING ?z) (is-person-at ?x ?y) (IS-CONNECTED ?y ?z) )
    :effect (and (is-person-at ?x ?z) (not (is-person-at ?x ?y)))
    
)

; The student or the teacher x have lunch at the building y that has a restaurant.
; (If they haven't had lunch already)
; As a result they have lunch
; Parameters:
; - x: the person (student or teacher)
; - y: a building that has a resturant
(:action have-lunch 
	; WRITE HERE THE CODE FOR THIS ACTION
    :parameters ( ?x ?y )
    :precondition (and (PERSON ?x) (BUILDING ?y) (not (had-lunch ?x)) (HAS-RESTURANT ?y) )
    :effect (had-lunch ?x)
)

; The student x attends the MORNING lecture w thaught by teacher y inside the building z
; (The student must NOT have had lunch before attending a morning lecture)
; As a result the student x has attended the lecture w
; Parameters:
; - x: a student
; - y: a teacher
; - z: a building
; - w: a lecture
(:action attend-morning-lecture
	; WRITE HERE THE CODE FOR THIS ACTION
    :parameters ( ?x ?y ?z ?w)
    :precondition (and 
        (IS-STUDENT ?x)
        (IS-TEACHER ?y)
        (BUILDING ?z)
        (LECTURE ?w)
        (IS-MORNING ?w)
        (IS-LECTURE-AT ?w ?z)
        (is-person-at ?y ?z)
        (not (had-lunch ?x))
    )
    :effect (and 
        (attended-lecture ?x ?w)
        (teaches-lecture ?y ?w)
    )
)

; The student x attends the AFTERNOON lecture w thaught by teacher y inside the building z
; (The student must have had lunch before being able to attend an afternoon lecture)
; As a result the student x has attended the lecture w
; Parameters:
; - x: a student
; - y: a teacher
; - z: a building
; - w: a lecture
(:action attend-afternoon-lecture
	; WRITE HERE THE CODE FOR THIS ACTION
    :parameters ( ?x ?y ?z ?w)
    :precondition (and 
        (IS-STUDENT ?x)
        (IS-TEACHER ?y)
        (BUILDING ?z)
        (LECTURE ?w)
        (IS-AFTERNOON ?w)
        (IS-LECTURE-AT ?w ?z)
        (is-person-at ?y ?z)
        (had-lunch ?x)
    )
    :effect (and 
        (attended-lecture ?x ?w)
        (teaches-lecture ?y ?w)
    )
)

)
