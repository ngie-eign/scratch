package main

import "fmt"

func add_100(val *int) {
    *val += 100
}

func main() {
    var a int

    a = 0

    fmt.Printf("a (before) = %d\n", a)

    add_100(&a)

    fmt.Printf("a (after)  = %d\n", a)
}
