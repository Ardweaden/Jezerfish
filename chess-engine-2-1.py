# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 15:53:34 2017

@author: Jan Jezersek
"""

import chess
import chess.pgn
import copy
from numba import jit 

values = {'p':1,'P':1,'r':5,'R':5,'n':3,'N':3,'b':3,'B':3,'q':9,'Q':9}

engine_color = True
calc_depth = 4
node_depth = 0

class MoveNode(object):
    def __init__(self,board,move,children,parent,depth):
        self.board = board
        self.move = move
        self.children = children
        self.parent = parent
        self.depth = depth
        w,b = material_count(board)
        self.score = w - b
        if depth == 0:
            if board.is_checkmate():
                if board.turn:
                    self.score = -999 + depth
                else:
                    self.score = 999 - depth
            else:
                w,b = material_count(board)
                self.score = w - b
        else:
            if board.is_checkmate():
                if board.turn:
                    self.score = -999 + depth
                else:
                    self.score = 999 - depth
            elif board.is_fivefold_repetition():
                self.score = 0
            else:
                board_test = board.copy()
                board_test.push(move)
                if board_test.is_checkmate():
                    if board.turn:
                        self.score = 999 - depth
                    else:
                        self.score = -999 + depth
                else:
                    w,b = material_count(board_test)
                    self.score = w - b

def TreeGenerator(board):
    tree = MoveNode(board,chess.Move.null(),[],None,0)
    tree_nodes = [tree]
    for i in range(1,calc_depth):
#        print(i)
        children_nodes = []
        for node in tree_nodes:
            if i == 1:
                board2 = board.copy()
            else:
                board2 = node.board.copy()
                board2.push(node.move)
            children_moves = list(board2.legal_moves)
            children = []
            for move in children_moves:
                children.append(MoveNode(board2,move,[],node,i))
            node.children = children
            children_nodes.append(children)
        tree_nodes = [item for sublist in children_nodes for item in sublist]
    return tree
    
def material_count(board):
    w = 0
    b = 0
    pieces = board.piece_map()
    for i in pieces:
        if pieces[i].symbol() == 'k' or pieces[i].symbol() == 'K':
            continue
        
        if pieces[i].color == True:
            w = w + values.get(pieces[i].symbol())
        else:
            b = b + values.get(pieces[i].symbol())
    return w,b

#@jit
def minimax(node,player,depth):
    global calc_depth # MoveTree

    if depth == calc_depth - 1:
        return node.score,node.move
        
    if node.children == [] and depth != calc_depth - 1:
#        print('Issue 1')
#        print(node.move)
#        print(node.score)
        return node.score,node.move
        
    if player:
        BestValue = -999
        BestMove = node.children[0].move
                
        for child in node.children:
            v,_ = minimax(child,not player,depth+1)
            BestValue = max(BestValue,v)
            if BestValue == v:
                BestMove = child.move
        return BestValue, BestMove
    else:
        BestValue = 999
        BestMove = node.children[0].move
                
        for child in node.children:
            v,_ = minimax(child,not player,depth+1)
            BestValue = min(BestValue,v)
            if BestValue == v:
                BestMove = child.move
        return BestValue, BestMove
  
def eliminate(tree,move):
    descendants = len(tree.children)
    for i in range(descendants):
        if tree.children[i].move == move:
            del tree.children[i]
            break
   
def best_move(board,player,cycles,eliminations=2):
    global calc_depth
        
    tree = TreeGenerator(board)
    
    if len(tree.children) == 1 or len(tree.children) < eliminations:
#        print('Move: ',tree.children[0].move)
#        print('Score: ',tree.children[0].score)
#        print('Only one legal move')
        evalu,bestm = minimax(tree,player,0)
#        print(evalu,bestm)
        return evalu,bestm
#        return tree.children[0].score,tree.children[0].move
        
#    if len(tree.children) < eliminations:
#        return best_move(board,player,cycles,eliminations=(len(tree.children)-1))
    
    if cycles == 0:
        evalu,bestm = minimax(tree,player,0)
        return evalu,bestm
    
    if eliminations >= len(tree.children):
        eliminations = len(tree.children) - 1
    
    candidates = []
    
    tree2 = copy.deepcopy(tree)
    
    for i in range(eliminations):
        _ , candidate = minimax(tree2,player,0)
        candidates.append(candidate)
        eliminate(tree2,candidate)
    
#    print(candidates)
        
    if player:
        BestScore = -999
        BestMove = None
    else:
        BestScore = 999
        BestMove = None
        
    for candidate in candidates:
        board_aux = board.copy()
        board_aux.push(candidate)
        evalu,bestm = best_move(board_aux,not player,cycles-1,eliminations=2)
        if player:
            if evalu > BestScore:
                BestScore = evalu
                BestMove = candidate
                print('Evaluation: ',BestScore, 'Candidate: ',BestMove)
        else:
            if evalu < BestScore:
                BestScore = evalu
                BestMove = candidate
                print('Evaluation: ',BestScore, 'Candidate: ',BestMove)
    
    return BestScore,BestMove
    
def engine_game(board=chess.Board(),player=True):
    while(1):
        game = chess.pgn.Game.from_board(board)
        if board.is_checkmate() or board.is_stalemate() or board.is_fivefold_repetition():
            break
        print(game)
        best_value,chosen_move = best_move(board,player,2,4)
        board.push(chosen_move)
#        print(chosen_move)
        player = not player

def tactic_solver(fen,cycles=2,eliminations=4):
    board = chess.Board(fen=fen)
    print(board)
    best_value,chosen_move = best_move(board,board.turn,cycles,eliminations)
    return board,chosen_move

def gamemode(engine_color,board=chess.Board(),cycles=2,eliminations=4):
    if not engine_color:
        print('Your move: ')
        a = input()
        move = chess.Move.from_uci(a)
        board.push(move)
    while(1):
        print(board)
        print(board.fen)
        best_value,chosen_move = best_move(board,engine_color,cycles,eliminations)
        print('Chosen move: ',chosen_move)
        board.push(chosen_move)
        print(board)
        print(board.fen)
        print('Your move: ')
        a = input()
        if a == '0000':
            break
        move = chess.Move.from_uci(a)
        board.push(move)