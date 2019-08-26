# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 15:14:41 2017

@author: Jan Jezersek
"""

import chess
import chess.pgn

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
#        w,b = material_count(board)
#        self.score = w - b
        if depth == 0:
            if board.is_checkmate():
                if board.turn:
                    self.score = -999
                else:
                    self.score = 999
            else:
                w,b = material_count(board)
                self.score = w - b
        else:
            if board.is_checkmate():
                if board.turn:
                    self.score = -999
                else:
                    self.score = 999
            else:
                board_test = board.copy()
                board_test.push(move)
                if board_test.is_checkmate():
                    if board.turn:
                        self.score = 999
                    else:
                        self.score = -999
                else:
                    w,b = material_count(board_test)
                    self.score = w - b

def TreeGenerator(board):
    tree = MoveNode(board,chess.Move.null(),[],None,0)
    tree_nodes = [tree]
    for i in range(1,calc_depth):
        print(i)
        children_nodes = []
        for node in tree_nodes:
            if i == 1:
                board2 = board
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

def minimax(node,player,depth):
    global calc_depth # MoveTree
    try:
        if depth == calc_depth - 1:
            return node.score,node.move
        
        if node.move == 0000:
            return node.score,node.move
        
        if node.board.is_checkmate():
            if player:
                return -999
            else:
                return 999
        
        if node.children == [] and depth != calc_depth - 1:
            print('Issue 1')
            print(node.move)
            return node.score,node.move
        
        board_test = node.board.copy()
        board_test.push(node.move)
        if board_test.is_checkmate():
            if player:
                return -999
            else:
                return 999
    #    print(depth)
        
        if player:
            BestValue = -999
            try:
                BestMove = node.children[0].move
            except:
                print('Issue 2')
                
            for child in node.children:
#                print(child.board)
#                print(child.move)
                v,_ = minimax(child,not player,depth+1)
                BestValue = max(BestValue,v)
                if BestValue == v:
                    BestMove = child.move
            return BestValue, BestMove
        else:
            BestValue = 999
            try:
                BestMove = node.children[0].move
            except:
                print('Issue 3') 
                
            for child in node.children:
#                print(child.board)
#                print(child.move)
    #            print(depth)
                v,_ = minimax(child,not player,depth+1)
                BestValue = min(BestValue,v)
                if BestValue == v:
                    BestMove = child.move
            return BestValue, BestMove
    except:
        print(node.board)
        print(node.move)
        print(depth)
        print(node.score)
        print(node.children[0].move)
        
def engine_game(board=chess.Board()):
#    game = chess.pgn.Game()
#    game.headers["Event"] = "Example"
    i = True
#    board = chess.Board()
    while(1):
        game = chess.pgn.Game.from_board(board)
        print(game)
        MoveTree = TreeGenerator(board)
        best_value,chosen_move = minimax(MoveTree,i,0)
        board.push(chosen_move)
        print(chosen_move)
        i = not i
    
    
#board = chess.Board()
#        
#board.push(chess.Move(chess.F2,chess.F4))
#board.push(chess.Move(chess.E7,chess.E6))
#board.push(chess.Move(chess.G2,chess.G4))
#
#
#w,b = material_count(board)
#
#MoveTree = TreeGenerator(board)
#
#best_value,chosen_move = minimax(MoveTree,True,0)
#
#print(chosen_move)
#print(w,b)