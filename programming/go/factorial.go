package main

import (
    "fmt"
    "os"
)
//import "log"

func main() {
    // Also:
    //var factorial_result int
    //var n int
    var factorial_result, n int

    if len(os.Args) == 2 {
        fmt.Sscanf(os.Args[1], "%d", &n)
	if n < 0 {
	    // log.Fatal adds on a timestamp.. probably have to modify the
	    // default format string first.
            //log.Fatal("n!, where n < 0, is undefined")
            fmt.Fprintf(os.Stderr, "n!, where n < 0, is undefined\n")
            os.Exit(1)
	}
    } else {
        n = 0
    }

    if n <= 0 {
        factorial_result = 1
    } else {
        factorial_result = (n - 1) * n
    }

    fmt.Printf("%d! = %d\n", n, factorial_result)
}
