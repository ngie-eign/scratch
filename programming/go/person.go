package main

import "fmt"

type Person struct {
    Name string
    Age int
    Occupation string
}

func (person Person) description() string {
    var descr string

    descr = fmt.Sprintf("%s is %d years old and is a %s",
        person.Name, person.Age, person.Occupation)

    return descr
}

func main() {
    jane := Person{
        Name: "Jane Doe",
	Age: 42,
	Occupation: "programmer",
    }

    john := Person{
        Name: "John Doe",
	Age: 24,
	Occupation: "barista",
    }

    fmt.Printf("%s\n", jane.description())
    fmt.Printf("%s\n", john.description())
}
