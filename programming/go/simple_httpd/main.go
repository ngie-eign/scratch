// Based on the example from the
//   "Go: The Big Picture" course, "Demo: A Simple Web Service" section, from
//   PluralSight.

package main

import (
  "fmt"
  "net/http"
)

func main() {
  http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Welcome to a simple Go web server.")
  })

  // XXX: providing a route with the same name as a file to serve doesn't seem
  // to work. Makes sense, but for a Golang newbie, it's kind of confusing not
  // seeing any console-based response or application crash or error when
  // provided invalid input or error-prone programmer logic.
  //
  // I suspect it's because `http.ListenAndServe` is running with the standard
  // library default http response handler (nil).
  http.HandleFunc("/index", func(w http.ResponseWriter, r *http.Request) {
    http.ServeFile(w, r, "./index.html")
  })

  http.ListenAndServe(":8080", nil)
}
