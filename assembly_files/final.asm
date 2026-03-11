.data 
str_nl: 
	.asciz "\n" 
.text
L0:
	j Lmain
L1:
	sw ra, 0(sp)
L2:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-28(sp)
L3:
	lw t1,-28(sp)
	sw t1,-12(gp)
L4:
	lw t1,-12(sp)
	lw t2,-16(sp)
	bgt t1, t2, L6
L5:
	j L10
L6:
	lw t1,-12(sp)
	lw t2,-20(sp)
	bgt t1, t2, L8
L7:
	j L10
L8:
	lw t1,-12(sp)
	sw t1,-24(sp)
L9:
	j L17
L10:
	lw t1,-16(sp)
	lw t2,-12(sp)
	bgt t1, t2, L12
L11:
	j L16
L12:
	lw t1,-16(sp)
	lw t2,-20(sp)
	bgt t1, t2, L14
L13:
	j L16
L14:
	lw t1,-16(sp)
	sw t1,-24(sp)
L15:
	j L17
L16:
	lw t1,-20(sp)
	sw t1,-24(sp)
L17:
	lw t1,-24(sp)
	lw t0, -8(sp)
	sw t1,0(t0)
L18:
	lw ra, 0(sp)
	jr ra

L19:
	sw ra, 0(sp)
L20:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-16(sp)
L21:
	lw t1,-16(sp)
	sw t1,-12(gp)
L22:
	lw t1,-12(sp)
	li t2,0
	blt t1, t2, L24
L23:
	j L27
L24:
	li t1,0
	li t2,1
	sub t1,t1,t2
	sw t1,-20(sp)
L25:
	lw t1,-20(sp)
	lw t0, -8(sp)
	sw t1,0(t0)
	lw ra, 0(sp)
	jr ra
L26:
	j L43
L27:
	lw t1,-12(sp)
	li t2,0
	beq t1, t2, L31
L28:
	j L29
L29:
	lw t1,-12(sp)
	li t2,1
	beq t1, t2, L31
L30:
	j L33
L31:
	li t1,1
	lw t0, -8(sp)
	sw t1,0(t0)
	lw ra, 0(sp)
	jr ra
L32:
	j L43
L33:
	lw t1,-12(sp)
	li t2,1
	sub t1,t1,t2
	sw t1,-24(sp)
L34:
	addi fp, sp, 44
	lw t1,-24(sp)
	sw t1,-12 (fp)
L35:
	addi t0, sp, -28
	sw t0,-8(fp)
L36:
	sw sp, -4(fp)
	addi sp, sp, 44
	jal L19
	addi sp, sp, -44
L37:
	lw t1,-12(sp)
	li t2,2
	sub t1,t1,t2
	sw t1,-32(sp)
L38:
	addi fp, sp, 44
	lw t1,-32(sp)
	sw t1,-12 (fp)
L39:
	addi t0, sp, -36
	sw t0,-8(fp)
L40:
	sw sp, -4(fp)
	addi sp, sp, 44
	jal L19
	addi sp, sp, -44
L41:
	lw t1,-28(sp)
	lw t2,-36(sp)
	add t1,t1,t2
	sw t1,-40(sp)
L42:
	lw t1,-40(sp)
	lw t0, -8(sp)
	sw t1,0(t0)
L43:
	lw ra, 0(sp)
	jr ra

L44:
	sw ra, 0(sp)
L45:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-20(sp)
L46:
	lw t1,-20(sp)
	sw t1,-12(gp)
L47:
	lw t1,-16(sp)
	lw t2,-12(sp)
	div t1,t1,t2
	sw t1,-24(sp)
L48:
	lw t1,-24(sp)
	lw t2,-12(sp)
	mul t1,t1,t2
	sw t1,-28(sp)
L49:
	lw t1,-16(sp)
	lw t2,-28(sp)
	beq t1, t2, L51
L50:
	j L53
L51:
	li t1,1
	lw t0, -8(sp)
	sw t1,0(t0)
	lw ra, 0(sp)
	jr ra
L52:
	j L54
L53:
	li t1,0
	lw t0, -8(sp)
	sw t1,0(t0)
L54:
	lw ra, 0(sp)
	jr ra

L55:
	sw ra, 0(sp)
L56:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-20(sp)
L57:
	lw t1,-20(sp)
	sw t1,-12(gp)
L58:
	li t1,2
	sw t1,-16(sp)
L59:
	lw t1,-16(sp)
	lw t2,-12(sp)
	blt t1, t2, L61
L60:
	j L72
L61:
	addi fp, sp, 32
	lw t1,-16(sp)
	sw t1,-12 (fp)
L62:
	lw t1,-12(sp)
	sw t1,-16 (fp)
L63:
	addi t0, sp, -24
	sw t0,-8(fp)
L64:
	sw sp, -4(fp)
	addi sp, sp, 32
	jal L44
	addi sp, sp, -32
L65:
	lw t1,-24(sp)
	li t2,1
	beq t1, t2, L67
L66:
	j L69
L67:
	li t1,0
	lw t0, -8(sp)
	sw t1,0(t0)
	lw ra, 0(sp)
	jr ra
L68:
	j L69
L69:
	lw t1,-16(sp)
	li t2,1
	add t1,t1,t2
	sw t1,-28(sp)
L70:
	lw t1,-28(sp)
	sw t1,-16(sp)
L71:
	j L59
L72:
	li t1,1
	lw t0, -8(sp)
	sw t1,0(t0)
L73:
	lw ra, 0(sp)
	jr ra

L74:
	sw ra, 0(sp)
L75:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-16(sp)
L76:
	lw t1,-16(sp)
	sw t1,-12(gp)
L77:
	lw t1,-12(sp)
	lw t2,-12(sp)
	mul t1,t1,t2
	sw t1,-20(sp)
L78:
	lw t1,-20(sp)
	lw t0, -8(sp)
	sw t1,0(t0)
L79:
	lw ra, 0(sp)
	jr ra

L80:
	sw ra, 0(sp)
L81:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-20(sp)
L82:
	lw t1,-20(sp)
	sw t1,-12(gp)
L83:
	addi fp, sp, 24
	lw t1,-12(sp)
	sw t1,-12 (fp)
L84:
	addi t0, sp, -24
	sw t0,-8(fp)
L85:
	sw sp, -4(fp)
	addi sp, sp, 24
	jal L74
	addi sp, sp, -24
L86:
	addi fp, sp, 24
	lw t1,-12(sp)
	sw t1,-12 (fp)
L87:
	addi t0, sp, -28
	sw t0,-8(fp)
L88:
	sw sp, -4(fp)
	addi sp, sp, 24
	jal L74
	addi sp, sp, -24
L89:
	lw t1,-24(sp)
	lw t2,-28(sp)
	mul t1,t1,t2
	sw t1,-32(sp)
L90:
	lw t1,-32(sp)
	sw t1,-16(sp)
L91:
	lw t1,-16(sp)
	lw t0, -8(sp)
	sw t1,0(t0)
L92:
	lw ra, 0(sp)
	jr ra

L93:
	sw ra, 0(sp)
L94:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-16(sp)
L95:
	lw t1,-16(sp)
	sw t1,-12(gp)
L96:
	lw t1,-12(sp)
	li t2,4
	rem t1,t1,t2
	sw t1,-20(sp)
L97:
	lw t1,-20(sp)
	li t2,0
	beq t1, t2, L99
L98:
	j L102
L99:
	lw t1,-12(sp)
	li t2,100
	rem t1,t1,t2
	sw t1,-24(sp)
L100:
	lw t1,-24(sp)
	li t2,0
	bne t1, t2, L105
L101:
	j L102
L102:
	lw t1,-12(sp)
	li t2,400
	rem t1,t1,t2
	sw t1,-28(sp)
L103:
	lw t1,-28(sp)
	li t2,0
	beq t1, t2, L105
L104:
	j L107
L105:
	li t1,1
	lw t0, -8(sp)
	sw t1,0(t0)
	lw ra, 0(sp)
	jr ra
L106:
	j L108
L107:
	li t1,0
	lw t0, -8(sp)
	sw t1,0(t0)
L108:
	lw ra, 0(sp)
	jr ra

L109:
Lmain:
	addi sp,sp,56
	mv gp,sp
L110:
	li t1,0
	sw t1,-12(gp)
L111:
	li a7, 5
	ecall
	sw a0,-20(sp)
L112:
	lw t1,-20(sp)
	sw t1,-16(sp)
L113:
	lw a0,-16(sp)
	li a7, 1
	ecall
	la a0,str_nl
	li a7, 4
	ecall
L114:
	li t1,1600
	sw t1,-16(sp)
L115:
	lw t1,-16(sp)
	li t2,2000
	ble t1, t2, L117
L116:
	j L124
L117:
	addi fp, sp, 32
	lw t1,-16(sp)
	sw t1,-12 (fp)
L118:
	addi t0, sp, -24
	sw t0,-8(fp)
L119:
	sw sp, -4(fp)
	addi sp, sp, 32
	jal L93
	addi sp, sp, -32
L120:
	lw a0,-24(sp)
	li a7, 1
	ecall
	la a0,str_nl
	li a7, 4
	ecall
L121:
	lw t1,-16(sp)
	li t2,400
	add t1,t1,t2
	sw t1,-28(sp)
L122:
	lw t1,-28(sp)
	sw t1,-16(sp)
L123:
	j L115
L124:
	addi fp, sp, 32
	li t1,2023
	sw t1,-12 (fp)
L125:
	addi t0, sp, -32
	sw t0,-8(fp)
L126:
	sw sp, -4(fp)
	addi sp, sp, 32
	jal L93
	addi sp, sp, -32
L127:
	lw a0,-32(sp)
	li a7, 1
	ecall
	la a0,str_nl
	li a7, 4
	ecall
L128:
	addi fp, sp, 32
	li t1,2024
	sw t1,-12 (fp)
L129:
	addi t0, sp, -36
	sw t0,-8(fp)
L130:
	sw sp, -4(fp)
	addi sp, sp, 32
	jal L93
	addi sp, sp, -32
L131:
	lw a0,-36(sp)
	li a7, 1
	ecall
	la a0,str_nl
	li a7, 4
	ecall
L132:
	addi fp, sp, 36
	li t1,3
	sw t1,-12 (fp)
L133:
	addi t0, sp, -40
	sw t0,-8(fp)
L134:
	sw sp, -4(fp)
	addi sp, sp, 36
	jal L80
	addi sp, sp, -36
L135:
	lw a0,-40(sp)
	li a7, 1
	ecall
	la a0,str_nl
	li a7, 4
	ecall
L136:
	addi fp, sp, 44
	li t1,5
	sw t1,-12 (fp)
L137:
	addi t0, sp, -44
	sw t0,-8(fp)
L138:
	sw sp, -4(fp)
	addi sp, sp, 44
	jal L19
	addi sp, sp, -44
L139:
	lw a0,-44(sp)
	li a7, 1
	ecall
	la a0,str_nl
	li a7, 4
	ecall
L140:
	li t1,1
	sw t1,-16(sp)
L141:
	lw t1,-16(sp)
	li t2,12
	ble t1, t2, L143
L142:
	j L150
L143:
	addi fp, sp, 32
	lw t1,-16(sp)
	sw t1,-12 (fp)
L144:
	addi t0, sp, -48
	sw t0,-8(fp)
L145:
	sw sp, -4(fp)
	addi sp, sp, 32
	jal L55
	addi sp, sp, -32
L146:
	lw a0,-48(sp)
	li a7, 1
	ecall
	la a0,str_nl
	li a7, 4
	ecall
L147:
	lw t1,-16(sp)
	li t2,1
	add t1,t1,t2
	sw t1,-52(sp)
L148:
	lw t1,-52(sp)
	sw t1,-16(sp)
L149:
	j L141
L150:
	lw a0,-12(gp)
	li a7, 1
	ecall
	la a0,str_nl
	li a7, 4
	ecall
L151:
	li a0,0
	li a7,93
	ecall
L152:
