import pygame

# パズルのフィールドとなる格子を描画
def draw_grid(screen, row=16, col=8):
    grid_color = (0, 0, 0) # 黒
    cell_size = 41 # piece_size+1のサイズ
    shift_px = 20 # 描画の初期位置
    
    # 横の線を描画
    for i in range(0, row+1):
        pygame.draw.line(screen, grid_color, 
                         (shift_px, cell_size*i+shift_px), 
                         (col*cell_size+shift_px, cell_size*i+shift_px))
        
    # 縦の線を描画
    for i in range(0, col+1):
        pygame.draw.line(screen, grid_color, 
                         (cell_size*i+shift_px, shift_px), 
                         (cell_size*i+shift_px, row*cell_size+shift_px))


# ピースを描画 
def draw_piece(screen, piece_list):
    piece_size = 40
    shift_px = 21
    
    for row_i, col_piece in enumerate(piece_list):
        
        # 描画するy座標
        draw_y = piece_size*row_i+shift_px+row_i
        
        for col_i in range(len(col_piece)):
            
            # 描画するx座標
            draw_x = piece_size*col_i+shift_px+col_i
            
            pygame.draw.rect(screen, col_piece[col_i],
                             (draw_x, draw_y, piece_size, piece_size))


# 選択カーソルの描画
def draw_select_cursor(screen, row=0, col=0, color=(128, 128, 128)):
    shift_px = 19
    cursor_size = 42
    cursor_color = color
    
    field_size = (16, 8)
    row, col = cursor_outside(row, col, field_size)
    
    draw_x = col*cursor_size+shift_px-col # 描画するx座標
    draw_y = row*cursor_size+shift_px-row # 描画するy座標
    
    # カーソルを描画
    pygame.draw.rect(screen, cursor_color,
                     (draw_x, draw_y, cursor_size, cursor_size), 5)
    
    return row, col

# カーソルが領域外に出ないように調整    
def cursor_outside(row, col, field_size):
    if row < 0:
        row += 1
    elif row > field_size[0]-1:
        row -= 1
    
    if col < 0:
        col += 1
    elif col > field_size[1]-1:
        col -= 1
        
    return row, col

    
    
            