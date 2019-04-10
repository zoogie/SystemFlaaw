;colorfill code courtesy of CTURT
;https://cturt.github.io/DS-exploit-finding.html#injecting-a-payload

.nds
.create "payload.bin", 0x02167C6C
.arm
.align 4

.definelabel MODE_FB0, 0x00020000
.definelabel VRAM_ENABLE, 0x80
.definelabel VRAM_A_LCD, 0
.definelabel VRAM_A, 0x06800000


mov r0, #0x04000000                     ; I/O space offset
mov r1, #0x3                            ; Both screens on

mov r2, #MODE_FB0                       ; Use VRAM_A as framebuffer
mov r3, #(VRAM_ENABLE | VRAM_A_LCD)     ; VRAM bank A enabled in LCD mode
mov r4, #0                              ; Full brightness (FIFA Street 2 fades out before our code)

str r1, [r0, #0x304]                    ; Set POWERCNT
str r2, [r0]                            ;        DISPCNT
str r3, [r0, #0x240]                    ;        VRAMCNT_A
str r4, [r0, #0x6C]                     ;        MASTER BRIGHT


reset:
add r1, #31                             ; Next colour
mov r0, #VRAM_A                         ; VRAM A offset, framebuffer
mov r2, #(256 * 192)                    ; Pixel count

writePixel:
strh r1, [r0], #2                       ; Write a pixel
subs r2, r2, #1                         ; Move along one
bne writePixel                          ; Fill whole screen

b reset

.pool
.Close