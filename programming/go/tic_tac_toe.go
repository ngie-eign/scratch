package main

import (
    "os"
)

const (
    BLANK = "", // 0 (map form)
    O = "O",    // 1 (...)
    X = "X",    // 2 (...)
)

func three_in_a_row(board [3][3]string, player string) {
    // build map of spaces to avoid having to pass over the board multiple
    // times
    var board_int[3] int

    for i, _ := range(board) {
        for j, value := range (board[i]) {
            switch {
            case value == BLANK:
                value_int = 0
            case value == O:
                value_int = 1
            case value == X:
                value_int = 2
            }
            board_int[i] = value_int
        }
    }
}

func main() {

    while true {
        var board [3][3] string{
            {BLANK, BLANK, BLANK},
            {BLANK, BLANK, BLANK},
            {BLANK, BLANK, BLANK},
        }

        var has_move_left bool = true
        var play_again string
        var player_is_x bool
        var won_game bool

        // an optimization to avoid having to call three_in_a_row(..)
        // unnecessarily
        var num_moves int = 0

        while has_move_left {

            draw_board(board)

            player_is_x = !player_is_x

            if player_is_x {
                player = X
            } else {
                player = O
            }

            // pick spot on board

            if len( <= num_moves and three_in_a_row(board, player) {
                fmt.Printf("Player %s WINS!\n", player)
            }
            num_moves++
        }

        // play again?
    }
}
