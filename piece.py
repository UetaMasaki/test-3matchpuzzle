import random
import copy

import pygame

def create_init_piece(row=16, col=8):
    piece_list = []
    
    for _ in range(row):
        col_piece =[]
        for _ in range(col):
            col_piece.append(create_piece())
        piece_list.append(col_piece)
    
    return piece_list

# 3つ並んでいるか判定
def match_3piece(piece_list, mode="judge"):
    update_piece_list = piece_list
    delete_piece_set = set()
     
    # 横に3つ揃っていいるか判定
    for row_i, col_pieces in enumerate(piece_list):
        for col_i in range(len(col_pieces)-2):
            if col_pieces[col_i] == col_pieces[col_i+1] == col_pieces[col_i+2]:
                if mode == "judge":
                    return True
                # 縦に3つ揃っていいる部分を消す
                elif mode == "delete":
                    delete_piece_set.add((row_i, col_i))
                    delete_piece_set.add((row_i, col_i+1))
                    delete_piece_set.add((row_i, col_i+2))
    
    # 縦に3つ揃っていいるか判定
    for row_i in range(len(piece_list)-2):
        for col_i in range(len(piece_list[row_i])):
            if piece_list[row_i][col_i] == piece_list[row_i+1][col_i] == piece_list[row_i+2][col_i]:
                if mode == "judge":
                    return True
                # 横に3つ揃っていいる部分を消す
                elif mode == "delete":
                    delete_piece_set.add((row_i, col_i))
                    delete_piece_set.add((row_i+1, col_i))
                    delete_piece_set.add((row_i+2, col_i))
                    
    if mode == "judge":
        return False
    
    elif mode == "delete":
        # ピースを消す
        for row, col in delete_piece_set:
            update_piece_list[row][col] = (0, 0, 0)
        
        return update_piece_list

# ピースを落下させる
def piece_down(piece_list):
    update_piece_list = piece_list
    
    for row_i in range(len(piece_list)):
        for coi_i in range(len(piece_list[row_i])):
            # 空白になっているマスを探索
            if piece_list[row_i][coi_i] == (0, 0, 0):
                for i in range(row_i+1):
                    down_row_i = row_i - i
                    # pieceを新たに生成
                    if down_row_i == 0:
                        update_piece_list[down_row_i][coi_i] = create_piece()
                    # 上のpieceを下のpieceにコピー
                    else:
                        update_piece_list[down_row_i][coi_i] = piece_list[down_row_i-1][coi_i]

                # 横で3つ消えている場合はまとめて落下させる
                if len(piece_list[row_i]) > coi_i+1:
                    if piece_list[row_i][coi_i+1] == (0, 0, 0):
                        continue
                
                return update_piece_list
    
    return piece_list
                
# 新たにpieceを生成
def create_piece():
    # 各ピースの色を設定（5色）
    color_list = [(255, 0, 0), # 赤
                  (0, 128, 0), # 緑
                  (0, 0, 255), # 青
                  (255, 255 ,0), # 黄
                  (255, 165, 0)] # 橙
    
    return color_list[random.randrange(5)]

# pieceの入れ替え
def swap_piece(piece_list, s_row, s_col, c_row, c_col):
    update_piece_list = copy.copy(piece_list)
    cursor_piece = piece_list[c_row][c_col]
    select_piece = piece_list[s_row][s_col]
    
    update_piece_list[s_row][s_col] = cursor_piece
    update_piece_list[c_row][c_col] = select_piece
    
    return update_piece_list

# 入れ替え可能なピースかどうか判定
def swap_judge(piece_list, s_row, s_col, c_row, c_col):
    judge = False
    if match_3piece(piece_list):
        if s_col == c_col-1 and s_row == c_row: # 上
            judge = True
        elif s_col == c_col+1 and s_row == c_row: # 下
            judge = True
        elif s_row == c_row-1 and s_col == c_col: # 左
            judge = True
        elif s_row == c_row+1 and s_col == c_col: # 右
            judge = True
    return judge