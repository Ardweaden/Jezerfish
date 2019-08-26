# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 21:31:23 2017

@author: Jan Jezersek
"""

import chess
import chess.pgn
import random

def play():
    board = chess.Board()
    
    for _ in range(1000):
        game = chess.pgn.Game.from_board(board)
        lm =  list(board.legal_moves)
        i = int(len(lm)*random.random())
        move = lm[i]
        board.push(move)
    
    return game
