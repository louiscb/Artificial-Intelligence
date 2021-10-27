;; Problem definition
(define (problem problem-1)

  ;; Specifying the domain for the problem
  (:domain student-life-domain)

  ;; Objects definition
  (:objects
    ; Buildings
    B1
    B2
    B3
    B4
    B5
    B6
    ; People (Students and teachers)
    S1
    S2
    S3
    S4
    T1
    T2
    T3
    ; Lectures
    L1
    L2
    L3
    L4
    L5
    L6
  )

  ;; Intial state of problem 1
  (:init
    ;; Declaration of the objects
    ; Buildings
    (BUILDING B1)
    (BUILDING B2)
    (BUILDING B3)
    (BUILDING B4)
    (BUILDING B5)
    (BUILDING B6)
    ; People (Students and teachers)
    (PERSON S1)
    (PERSON S2)
    (PERSON S3)
    (PERSON S4)
    (PERSON T1)
    (PERSON T2)
    (PERSON T3)
    ; Lectures
    (LECTURE L1)
    (LECTURE L2)
    (LECTURE L3)
    (LECTURE L4)
    (LECTURE L5)
    (LECTURE L6)
        
    ;; Declaration of the predicates of the objects
    ; We set people locations
    (is-person-at S1 B4)
    (is-person-at T1 B2)
    (is-person-at T2 B3)
   
    ; We set the buildings where lectures take place
    ; B1
    (IS-LECTURE-AT L1 B1)
    (IS-LECTURE-AT L2 B1)
    ; B2
    (IS-LECTURE-AT L3 B2)
    ; B3
    (IS-LECTURE-AT L4 B3)
    (IS-LECTURE-AT L2 B3)
    ; B4
    (IS-LECTURE-AT L1 B4)
    (IS-LECTURE-AT L6 B4)
    ; B6
    ; -- NONE --
    ; B6
    (IS-LECTURE-AT L4 B6)
    (IS-LECTURE-AT L5 B6)
    
    ; We set whether the lecture is a morning or afternoon lecture (or both)
    ; L1
    (IS-MORNING L1)
    ; L2
    (IS-AFTERNOON L2)
    ; L3
    (IS-MORNING L3)
    ; L4
    (IS-MORNING L4)
    ; L5
    (IS-AFTERNOON L5)
    ; L6
    (IS-AFTERNOON L6)

    ; We set whether the building has a restuarant
    (HAS-RESTURANT B5)

    ; We set whether the person is a teacher or a student
    ; Teacher
    (IS-TEACHER T1)
    (IS-TEACHER T2)
    (IS-TEACHER T3)
    ; Student
    (IS-STUDENT S1)
    (IS-STUDENT S2)
    (IS-STUDENT S3)
    (IS-STUDENT S4)

    ; We set which teacher teaches which lecture
    ; T1
    (teaches-lecture T1 L1)
    (teaches-lecture T1 L3)
    ; T2
    (teaches-lecture T2 L2)
    (teaches-lecture T2 L4)
    ; T3
    (teaches-lecture T3 L5)
    (teaches-lecture T3 L6)
    
    ; We set the connections between the buildings
    (IS-CONNECTED B1 B2) (IS-CONNECTED B2 B1) 
    (IS-CONNECTED B2 B5) (IS-CONNECTED B5 B2) 
    (IS-CONNECTED B2 B3) (IS-CONNECTED B3 B2) 
    (IS-CONNECTED B3 B4) (IS-CONNECTED B4 B3) 
    (IS-CONNECTED B3 B6) (IS-CONNECTED B6 B3)  
  )

  ;; Goal specification
  (:goal
    (and
    ; S1
      (attended-lecture S1 L1)
      (attended-lecture S1 L6)

      (had-lunch S1)
    
    ;  S2
      (attended-lecture S2 L2)
      (attended-lecture S2 L3)

      (had-lunch S2)

    ;   S3
      (attended-lecture S3 L4)
      (attended-lecture S3 L5)

      (had-lunch S3)
    ;   S4
      (attended-lecture S4 L5)
      (attended-lecture S4 L1)

      (had-lunch S4)
    ;   T1
      (teaches-lecture T1 L1)
      (teaches-lecture T1 L3)
    ;   T2
      (teaches-lecture T2 L2)
      (teaches-lecture T2 L4)

      (had-lunch T2)
    ;   T3
      (teaches-lecture T3 L5)
      (teaches-lecture T3 L6)

      (had-lunch T3)  
    )
  )
)
