	.text
	.file	"<string>"
	.globl	linea1
	.p2align	4, 0x90
	.type	linea1,@function
linea1:
	.cfi_startproc
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$1, 4(%rsp)
	movabsq	$formato_posy, %rdi
	movabsq	$printf, %rcx
	movl	$1, %esi
	xorl	%eax, %eax
	callq	*%rcx
	movabsq	$fflush, %rax
	xorl	%edi, %edi
	callq	*%rax
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	linea1, .Lfunc_end0-linea1
	.cfi_endproc

	.globl	posiciona
	.p2align	4, 0x90
	.type	posiciona,@function
posiciona:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%rbx
	.cfi_def_cfa_offset 40
	subq	$24, %rsp
	.cfi_def_cfa_offset 64
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movl	%edi, 16(%rsp)
	movl	%esi, 20(%rsp)
	movl	$1, 12(%rsp)
	movabsq	$formato_posy, %r14
	movabsq	$printf, %r15
	movabsq	$fflush, %rbx
	.p2align	4, 0x90
.LBB1_1:
	movl	12(%rsp), %ebp
	cmpl	$3, %ebp
	jg	.LBB1_3
	movl	16(%rsp), %esi
	incl	%esi
	movl	%esi, 16(%rsp)
	movq	%r14, %rdi
	xorl	%eax, %eax
	callq	*%r15
	xorl	%edi, %edi
	callq	*%rbx
	incl	%ebp
	movl	%ebp, 12(%rsp)
	jmp	.LBB1_1
.LBB1_3:
	addq	$24, %rsp
	.cfi_def_cfa_offset 40
	popq	%rbx
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	posiciona, .Lfunc_end1-posiciona
	.cfi_endproc

	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:
	.cfi_startproc
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$1, 4(%rsp)
	movabsq	$linea1, %rax
	callq	*%rax
	movabsq	$posiciona, %rax
	movl	$1, %edi
	movl	$1, %esi
	callq	*%rax
	popq	%rax
	.cfi_def_cfa_offset 8
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

	.section	".note.GNU-stack","",@progbits
