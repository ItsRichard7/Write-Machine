	.text
	.file	"<string>"
	.globl	linea1
	.p2align	4, 0x90
	.type	linea1,@function
linea1:
	.cfi_startproc
	subq	$40, %rsp
	.cfi_def_cfa_offset 48
	movl	$1, 36(%rsp)
	movabsq	$formato_posy, %rcx
	movabsq	$printf, %rax
	movl	$1, %edx
	callq	*%rax
	movabsq	$fflush, %rax
	xorl	%ecx, %ecx
	callq	*%rax
	addq	$40, %rsp
	retq
.Lfunc_end0:
	.size	linea1, .Lfunc_end0-linea1
	.cfi_endproc

	.globl	posiciona
	.p2align	4, 0x90
	.type	posiciona,@function
posiciona:
	.cfi_startproc
	pushq	%rsi
	.cfi_def_cfa_offset 16
	pushq	%rdi
	.cfi_def_cfa_offset 24
	subq	$40, %rsp
	.cfi_def_cfa_offset 64
	.cfi_offset %rdi, -24
	.cfi_offset %rsi, -16
	movl	%ecx, %eax
	movl	%ecx, 36(%rsp)
	movl	%edx, 32(%rsp)
	movabsq	$formato_posx, %rcx
	movabsq	$printf, %rsi
	movl	%eax, %edx
	callq	*%rsi
	movabsq	$fflush, %rdi
	xorl	%ecx, %ecx
	callq	*%rdi
	movl	32(%rsp), %edx
	movabsq	$formato_posy, %rcx
	callq	*%rsi
	xorl	%ecx, %ecx
	callq	*%rdi
	addq	$40, %rsp
	popq	%rdi
	popq	%rsi
	retq
.Lfunc_end1:
	.size	posiciona, .Lfunc_end1-posiciona
	.cfi_endproc

	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:
	.cfi_startproc
	subq	$40, %rsp
	.cfi_def_cfa_offset 48
	movl	$1, 36(%rsp)
	movabsq	$linea1, %rax
	callq	*%rax
	movabsq	$posiciona, %rax
	movl	$5, %ecx
	movl	$3, %edx
	callq	*%rax
	addq	$40, %rsp
	retq
.Lfunc_end2:
	.size	main, .Lfunc_end2-main
	.cfi_endproc

	.type	formato_posy,@object
	.section	.rodata,"a",@progbits
	.globl	formato_posy
	.p2align	4
formato_posy:
	.asciz	"Posicion en Y: %d\n"
	.size	formato_posy, 19

	.type	formato_posx,@object
	.globl	formato_posx
	.p2align	4
formato_posx:
	.asciz	"Posicion en X: %d\n"
	.size	formato_posx, 19

	.section	".note.GNU-stack","",@progbits
