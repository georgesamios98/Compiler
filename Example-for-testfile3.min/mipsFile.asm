L100:	sw $ra,-0($sp)
L101:	li $t1,1
	sw $t1,-12($s0)
L102:	lw $t1,-12($s0)
	li $t2,4
	bne $t1,$t2,L104
L103:	j L107
L104:	lw $t1,-12($s0)
	li $t2,1
	add $t1,$t1,$t2
L105:	sw $t1,-12($s0)
L106:	j L102
L107:	lw $t1,-12($s0)
	li $t2,3
	sub $t1,$t1,$t2
L108:	sw $t1,-12($s0)
L109:	li $v0,1
	lw $t0,-12($s0)
	add $a0,$zero,$t0
	syscall
L110:	lw $ra,-0($sp) 
 	jr $ra
L111:	lw $ra,-0($sp) 
 	jr $ra
