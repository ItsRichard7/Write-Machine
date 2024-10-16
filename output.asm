	.text
	.file	"<string>"
	.globl	linea1
	.p2align	4, 0x90
	.type	linea1,@function
linea1:
	.cfi_startproc
	movl	$1, -4(%rsp)
	retq
.Lfunc_end0:
	.size	linea1, .Lfunc_end0-linea1
	.cfi_endproc

	.globl	posiciona
	.p2align	4, 0x90
	.type	posiciona,@function
posiciona:
	.cfi_startproc
	movl	%edi, -4(%rsp)
	movl	%esi, -8(%rsp)
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

	.section	".note.GNU-stack","",@progbits
