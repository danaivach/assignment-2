(define (problem BLOCKS-4-1)
(:domain BLOCKS)
(:objects A B C - block)
(:INIT (CLEAR B) (ONTABLE A) (ONTABLE B) (ON C A) (CLEAR C) (HANDEMPTY))
(:goal (AND (ON B C) (ON A B) (ONTABLE C) ))
)