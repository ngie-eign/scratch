// Inspired by "Demo: CLI Application" from "Go: The Big Picture".
//
// Key differences are:
// - Some variables are purposely named with slightly more self-documenting names.
// - Imports are sorted :D.
// - I replaced log level parsing with a "more fun" default application: looking for
//     words in Electric Six's song, High Voltage.
//
// Example:
// >>> go run simple_parser.go -input song.txt "Danger, danger"

package main

import (
  "bufio"
  "flag"
  "fmt"
  "log"
  "os"
  "strings"
)

func main() {
  input := flag.String("input", "./haystack.txt", "Text file to search (haystack).")
  // NB: an alternate solution to using flag.Args(), if one wanted to specify a default value.
  //needle := flag.String("needle", "Danger, danger", "Needle to search haystack for..")
  flag.Parse()
  if len(flag.Args()) != 1 {
    log.Fatal("usage: ", os.Args[0], " [-input haystack.txt] needle")
  }
  needle := &flag.Args()[0]

  fobj, err := os.Open(*input)
  if err != nil {
    log.Fatal(err)
  }
  defer fobj.Close()

  bufReader := bufio.NewReader(fobj)

  // Note that `:=` declares `line` and `err` in the fot-loop's pre clause,
  // whereas `=` merely changes the value.
  for line, err := bufReader.ReadString('\n'); err == nil; line, err = bufReader.ReadString('\n') {
    if strings.Contains(line, *needle) {
      fmt.Print(line)
    }
  }
}
