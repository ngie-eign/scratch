package main
// an alternative method that doesn't use the syscall import, necessarily:
// http://stackoverflow.com/questions/28370646/how-do-i-fork-a-go-process

import (
    "fmt"
    "syscall"
)

func do_fork_exec(command string) {
    pid, error := syscall.ForkExec(command, nil, nil)
    // this doesn't work -- needs commas
    //fmt.Println("command=" command ", pid=" pid ", error=" error)
    // looks ugly. use Printf.
    //fmt.Println("command=", command, ", pid=", pid, ", error=", error)
    fmt.Printf("command='%s', pid=%d, error='%s'\n", command, pid, error)
}

func main() {
    do_fork_exec("true")
    do_fork_exec("false")
    do_fork_exec("/usr/bin/true")
    do_fork_exec("/usr/bin/false")
    do_fork_exec("i-do-not-exist")
    do_fork_exec("/")
}
