import sys
import time

from pygame.locals import *
import pygame

from drawing import *
from piece import *

# パズル画面を初期化
def screen_init(screen, row, col, piece_list):
    # 背景色の設定
    screen.fill((255, 255, 224))
    # 格子を描画
    draw_grid(screen, row, col)
    # 初期のピースを描画
    draw_piece(screen, piece_list)
    
# 空白のマスがあるか判定
def judge_blank(piece_list):
    for pieces in piece_list:
        if (0, 0, 0) in pieces:
            return True
        
    return False

def timer(time_num=3):
    pygame.display.update() #描画処理を実行
    time.sleep(time_num)

def main():
    pygame.init()

    # ウインドウのサイズを指定
    size = (370, 700)
    screen = pygame.display.set_mode(size)
    # ウインドウの名前を設定
    pygame.display.set_caption("3Match_Pazzle")
    
    row, col = 16, 8
    # ピースの情報を保存したリスト生成
    piece_list = create_init_piece(row, col)
    # 初期状態の3matchを除去しておく
    while match_3piece(piece_list) or judge_blank(piece_list):
        piece_list = match_3piece(piece_list, mode="delete")
        piece_list = piece_down(piece_list)
    
    # 選択カーソルの位置（初期：(0,0)）
    cursor_row, cursor_col = 0, 0
    
    # パズル画面の初期化
    screen_init(screen, row, col, piece_list)
    
    running = True
    select_flag = False
    step = 0
    
    #メインループ
    while running:
        
        pygame.display.update() #描画処理を実行

        # ピースを消去するステップ
        if step == 0:
            # ピースが3つ並んでいる場合に消す
            piece_list = match_3piece(piece_list, mode="delete")
            # 処理後のピースを描画
            draw_piece(screen, piece_list)
        
            timer(1)
            step = 1
        
        # 空白にピースを落下させるステップ
        if step == 1:
            if judge_blank(piece_list):
                # ピースを落下させる
                piece_list = piece_down(piece_list)
                # 処理後のピースを描画
                draw_piece(screen, piece_list)
                timer(0.5)
            else:
                step = 2
        
        # プレイヤーが操作するステップ（カーソル移動、ピース選択、ピース入れ替え）
        if step == 2:
            # カーソルの描画
            cursor_row, cursor_col = draw_select_cursor(screen, cursor_row, cursor_col)
            
            if select_flag:
                draw_select_cursor(screen, select_row, select_col, color=(47,79,79))
                
            if match_3piece(piece_list):
                step = 0
            
            for event in pygame.event.get():

                if event.type == QUIT:  # 終了イベント
                    running = False
                    pygame.quit()  #pygameのウィンドウを閉じる
                    sys.exit() #システム終了
                    
                if event.type == KEYDOWN:
                    
                    # カーソルの上下左右移動
                    if event.key == K_DOWN:
                        cursor_row += 1
                        screen_init(screen, row, col, piece_list)
                    if event.key == K_UP:
                        cursor_row -= 1
                        screen_init(screen, row, col, piece_list)
                    if event.key == K_RIGHT:
                        cursor_col += 1
                        screen_init(screen, row, col, piece_list)
                    if event.key == K_LEFT:
                        cursor_col -= 1
                        screen_init(screen, row, col, piece_list)
                        
                    if event.key == K_SPACE:
                        if select_flag:
                            update_piece_list = swap_piece(piece_list, select_row, select_col, cursor_row, cursor_col)
                            if swap_judge(piece_list, select_row, select_col, cursor_row, cursor_col):
                                piece_list = update_piece_list
                                step = 0
                            else:
                                piece_list = swap_piece(piece_list, select_row, select_col, cursor_row, cursor_col)
                            select_flag = False
                            screen_init(screen, row, col, piece_list)
                        else:
                            select_row, select_col = cursor_row, cursor_col
                            select_flag = True
                            
                if event.type == MOUSEBUTTONDOWN:
                    mouse_col, mouse_row = event.pos
                    cursor_row, cursor_col = (mouse_row-21)//40, (mouse_col-21)//40
                    screen_init(screen, row, col, piece_list)
                    
                    if select_flag:
                        update_piece_list = swap_piece(piece_list, select_row, select_col, cursor_row, cursor_col)
                        if swap_judge(piece_list, select_row, select_col, cursor_row, cursor_col):
                            piece_list = update_piece_list
                            step = 0
                        else:
                            piece_list = swap_piece(piece_list, select_row, select_col, cursor_row, cursor_col)
                        select_flag = False
                        screen_init(screen, row, col, piece_list)
                    else:
                        select_row, select_col = cursor_row, cursor_col
                        select_flag = True
                        
                    

if __name__ == "__main__":
    main()